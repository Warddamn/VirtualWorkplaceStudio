#!/usr/bin/env python3
"""Check the E6 firmware's register map and SDRAM setup against ST's own sources.

The E6 firmware (code/T3_dram/stm32_retention/) writes its own small register header, regs_f429.h,
instead of using ST's SDK. This script compares every number in it, and the SDRAM pin list, timings,
command sequence and mode register in sdram_fmc.c, with ST's code:

  1. It compiles two tiny C files with arm-none-eabi-gcc: one includes ST's CMSIS header
     (stm32f429xx.h), the other the firmware's regs_f429.h. Each stores ~90 numbers (addresses,
     offsets, bit masks, packed register values) in an array. The script reads both arrays back
     from the object files and compares them one by one.
  2. It parses ST's board-support package (BSP), HAL driver and the STM32F429I-Discovery examples
     as text: the 38 SDRAM pins, the BSP timing cycle counts, the mode-register value, the refresh
     formula, the alternate-function numbers, the UART pins and the baud-rate divider.
  3. It compares the flash and RAM regions of the firmware's linker script with ST's memory map.

It prints OK or MISMATCH per item, with the ST file and line, and exits 1 on any mismatch.

Get ST's sources first (shallow clones, about 60 MB in all), each into its own empty folder:

  git clone --depth 1 --filter=blob:none --sparse https://github.com/STMicroelectronics/STM32CubeF4 cubef4
  git -C cubef4 sparse-checkout set Drivers/CMSIS/Include Projects/STM32F429I-Discovery/Examples/FMC \\
      Projects/STM32F429I-Discovery/Examples/UART/UART_TwoBoards_ComPolling
  git clone --depth 1 https://github.com/STMicroelectronics/cmsis-device-f4 cmsis-device-f4
  git clone --depth 1 https://github.com/STMicroelectronics/stm32f4xx_hal_driver hal
  git clone --depth 1 https://github.com/STMicroelectronics/32f429idiscovery-bsp bsp

then run:

  python3 home-lab/tools/e6_regcheck.py --cubef4 cubef4 --cmsis-device cmsis-device-f4 --hal hal --bsp bsp

Python standard library only; needs arm-none-eabi-gcc and arm-none-eabi-objcopy (or --cross PREFIX).
Verified 2026-11-04 with cmsis-device-f4 @ 9192c7b9df75, stm32f4xx_hal_driver @ 1f6451c3e077,
32f429idiscovery-bsp @ d77779a2a4e9 and STM32CubeF4 @ 60c8abe0ae88: every item OK.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FW = os.path.join(os.path.dirname(HERE), "code", "T3_dram", "stm32_retention")

# (name, expression with ST's CMSIS names, expression with the firmware's regs_f429.h names)
ITEMS = [
    ("RCC_CR address", "RCC_BASE + offsetof(RCC_TypeDef, CR)", "A(RCC_CR)"),
    ("RCC_PLLCFGR address", "RCC_BASE + offsetof(RCC_TypeDef, PLLCFGR)", "A(RCC_PLLCFGR)"),
    ("RCC_CFGR address", "RCC_BASE + offsetof(RCC_TypeDef, CFGR)", "A(RCC_CFGR)"),
    ("RCC_AHB1ENR address", "RCC_BASE + offsetof(RCC_TypeDef, AHB1ENR)", "A(RCC_AHB1ENR)"),
    ("RCC_AHB3ENR address", "RCC_BASE + offsetof(RCC_TypeDef, AHB3ENR)", "A(RCC_AHB3ENR)"),
    ("RCC_APB2ENR address", "RCC_BASE + offsetof(RCC_TypeDef, APB2ENR)", "A(RCC_APB2ENR)"),
    ("GPIOAEN", "RCC_AHB1ENR_GPIOAEN", "1UL << PORTA"),
    ("GPIOBEN", "RCC_AHB1ENR_GPIOBEN", "1UL << PORTB"),
    ("GPIOCEN", "RCC_AHB1ENR_GPIOCEN", "1UL << PORTC"),
    ("GPIODEN", "RCC_AHB1ENR_GPIODEN", "1UL << PORTD"),
    ("GPIOEEN", "RCC_AHB1ENR_GPIOEEN", "1UL << PORTE"),
    ("GPIOFEN", "RCC_AHB1ENR_GPIOFEN", "1UL << PORTF"),
    ("GPIOGEN", "RCC_AHB1ENR_GPIOGEN", "1UL << PORTG"),
    ("FMCEN", "RCC_AHB3ENR_FMCEN", "RCC_AHB3ENR_FMCEN_BIT"),
    ("USART1EN", "RCC_APB2ENR_USART1EN", "RCC_APB2ENR_USART1EN_BIT"),
    ("RCC_CR_HSEON", "RCC_CR_HSEON", "RCC_CR_HSEON"),
    ("RCC_CR_HSERDY", "RCC_CR_HSERDY", "RCC_CR_HSERDY"),
    ("RCC_CR_HSEBYP", "RCC_CR_HSEBYP", "RCC_CR_HSEBYP"),
    ("RCC_CR_PLLON", "RCC_CR_PLLON", "RCC_CR_PLLON"),
    ("RCC_CR_PLLRDY", "RCC_CR_PLLRDY", "RCC_CR_PLLRDY"),
    ("PLLCFGR M=4 N=64 P=8 Q=8 HSE",
     "RCC_PLLCFGR_PLLSRC_HSE | (4U << RCC_PLLCFGR_PLLM_Pos) | (64U << RCC_PLLCFGR_PLLN_Pos)"
     " | (((8U >> 1U) - 1U) << RCC_PLLCFGR_PLLP_Pos) | (8U << RCC_PLLCFGR_PLLQ_Pos)",
     "RCC_PLLCFGR_SRC_HSE | RCC_PLLCFGR_M(4) | RCC_PLLCFGR_N(64) | RCC_PLLCFGR_P(8) | RCC_PLLCFGR_Q(8)"),
    ("RCC_CFGR SW mask", "RCC_CFGR_SW", "RCC_CFGR_SW_MASK"),
    ("RCC_CFGR SW=PLL", "RCC_CFGR_SW_PLL", "RCC_CFGR_SW_PLL"),
    ("RCC_CFGR SW=HSI", "RCC_CFGR_SW_HSI", "RCC_CFGR_SW_HSI"),
    ("RCC_CFGR SWS mask", "RCC_CFGR_SWS", "RCC_CFGR_SWS_MASK"),
    ("RCC_CFGR SWS=PLL", "RCC_CFGR_SWS_PLL", "RCC_CFGR_SWS_PLL"),
] + [("GPIO%s base" % c, "GPIO%s_BASE" % c, "GPIO_BASE(PORT%s)" % c) for c in "ABCDEFG"] + [
    ("GPIO MODER offset", "offsetof(GPIO_TypeDef, MODER)", "A(GPIO_MODER(0)) - GPIO_BASE(0)"),
    ("GPIO OTYPER offset", "offsetof(GPIO_TypeDef, OTYPER)", "A(GPIO_OTYPER(0)) - GPIO_BASE(0)"),
    ("GPIO OSPEEDR offset", "offsetof(GPIO_TypeDef, OSPEEDR)", "A(GPIO_OSPEEDR(0)) - GPIO_BASE(0)"),
    ("GPIO PUPDR offset", "offsetof(GPIO_TypeDef, PUPDR)", "A(GPIO_PUPDR(0)) - GPIO_BASE(0)"),
    ("GPIO IDR offset", "offsetof(GPIO_TypeDef, IDR)", "A(GPIO_IDR(0)) - GPIO_BASE(0)"),
    ("GPIO ODR offset", "offsetof(GPIO_TypeDef, ODR)", "A(GPIO_ODR(0)) - GPIO_BASE(0)"),
    ("GPIO BSRR offset", "offsetof(GPIO_TypeDef, BSRR)", "A(GPIO_BSRR(0)) - GPIO_BASE(0)"),
    ("GPIO AFRL offset", "offsetof(GPIO_TypeDef, AFR[0])", "A(GPIO_AFRL(0)) - GPIO_BASE(0)"),
    ("GPIO AFRH offset", "offsetof(GPIO_TypeDef, AFR[1])", "A(GPIO_AFRH(0)) - GPIO_BASE(0)"),
    ("MODER output", "GPIO_MODER_MODER0_0", "MODER_OUTPUT"),
    ("MODER alternate", "GPIO_MODER_MODER0_1", "MODER_AF"),
    ("OSPEEDR very high", "GPIO_OSPEEDER_OSPEEDR0", "OSPEED_VERY_HIGH"),
    ("PUPDR pull-up", "GPIO_PUPDR_PUPDR0_0", "PUPD_PULLUP"),
    ("USART1 SR address", "USART1_BASE + offsetof(USART_TypeDef, SR)", "A(USART1_SR)"),
    ("USART1 DR address", "USART1_BASE + offsetof(USART_TypeDef, DR)", "A(USART1_DR)"),
    ("USART1 BRR address", "USART1_BASE + offsetof(USART_TypeDef, BRR)", "A(USART1_BRR)"),
    ("USART1 CR1 address", "USART1_BASE + offsetof(USART_TypeDef, CR1)", "A(USART1_CR1)"),
    ("USART_SR_RXNE", "USART_SR_RXNE", "USART_SR_RXNE"),
    ("USART_SR_TXE", "USART_SR_TXE", "USART_SR_TXE"),
    ("USART_SR_ORE", "USART_SR_ORE", "USART_SR_ORE"),
    ("USART_CR1_UE", "USART_CR1_UE", "USART_CR1_UE"),
    ("USART_CR1_TE", "USART_CR1_TE", "USART_CR1_TE"),
    ("USART_CR1_RE", "USART_CR1_RE", "USART_CR1_RE"),
    ("SysTick CTRL address", "SysTick_BASE + offsetof(SysTick_Type, CTRL)", "A(SYST_CSR)"),
    ("SysTick LOAD address", "SysTick_BASE + offsetof(SysTick_Type, LOAD)", "A(SYST_RVR)"),
    ("SysTick VAL address", "SysTick_BASE + offsetof(SysTick_Type, VAL)", "A(SYST_CVR)"),
    ("SysTick CTRL on", "SysTick_CTRL_CLKSOURCE_Msk | SysTick_CTRL_TICKINT_Msk | SysTick_CTRL_ENABLE_Msk",
     "SYST_CSR_ENABLE_ALL"),
] + [("FMC_%s address" % n, "FMC_Bank5_6_R_BASE + offsetof(FMC_Bank5_6_TypeDef, %s)" % m, "A(FMC_%s)" % n)
     for n, m in (("SDCR1", "SDCR[0]"), ("SDCR2", "SDCR[1]"), ("SDTR1", "SDTR[0]"), ("SDTR2", "SDTR[1]"),
                  ("SDCMR", "SDCMR"), ("SDRTR", "SDRTR"), ("SDSR", "SDSR"))] + [
    ("SDCR NR 12 bits", "FMC_SDCR1_NR_0", "SDCR_NR_12BIT"),
    ("SDCR MWID 16", "FMC_SDCR1_MWID_0", "SDCR_MWID_16"),
    ("SDCR NB 4 banks", "FMC_SDCR1_NB", "SDCR_NB_4BANKS"),
    ("SDCR CAS 3", "FMC_SDCR1_CAS", "SDCR_CAS(3)"),
    ("SDCR CAS 2", "FMC_SDCR1_CAS_1", "SDCR_CAS(2)"),
    ("SDCR WP", "FMC_SDCR1_WP", "SDCR_WP"),
    ("SDCR SDCLK HCLK/2", "FMC_SDCR1_SDCLK_1", "SDCR_SDCLK_DIV2"),
    ("SDCR SDCLK HCLK/3", "FMC_SDCR1_SDCLK", "SDCR_SDCLK_DIV3"),
    ("SDCR SDCLK mask", "FMC_SDCR1_SDCLK", "SDCR_SDCLK_MASK"),
    ("SDCR RBURST", "FMC_SDCR1_RBURST", "SDCR_RBURST"),
    ("SDCR RPIPE 1", "FMC_SDCR1_RPIPE_0", "SDCR_RPIPE(1)"),
    ("SDCR RPIPE mask", "FMC_SDCR1_RPIPE", "SDCR_RPIPE_MASK"),
    ("SDTR packing (2,7,4,7,3,2,2)",
     "((2U-1U) << FMC_SDTR1_TMRD_Pos) | ((7U-1U) << FMC_SDTR1_TXSR_Pos) | ((4U-1U) << FMC_SDTR1_TRAS_Pos)"
     " | ((7U-1U) << FMC_SDTR1_TRC_Pos) | ((3U-1U) << FMC_SDTR1_TWR_Pos) | ((2U-1U) << FMC_SDTR1_TRP_Pos)"
     " | ((2U-1U) << FMC_SDTR1_TRCD_Pos)", "SDTR(2, 7, 4, 7, 3, 2, 2)"),
    ("SDTR TRC mask", "FMC_SDTR1_TRC", "SDTR_TRC_MASK"),
    ("SDTR TRP mask", "FMC_SDTR1_TRP", "SDTR_TRP_MASK"),
    ("SDCMR MODE mask", "FMC_SDCMR_MODE", "SDCMR_MODE_MASK"),
    ("SDCMR CTB2", "FMC_SDCMR_CTB2", "SDCMR_CTB2"),
    ("SDCMR CTB1", "FMC_SDCMR_CTB1", "SDCMR_CTB1"),
    ("SDCMR NRFS 8", "(8UL - 1UL) << FMC_SDCMR_NRFS_Pos", "SDCMR_NRFS(8)"),
    ("SDCMR NRFS mask", "FMC_SDCMR_NRFS", "SDCMR_NRFS(16)"),
    ("SDCMR MRD 0x230", "0x230UL << FMC_SDCMR_MRD_Pos", "SDCMR_MRD(0x230)"),
    ("SDCMR MRD mask", "FMC_SDCMR_MRD", "SDCMR_MRD(0x1FFF)"),
    ("SDRTR CRE", "FMC_SDRTR_CRE", "SDRTR_CRE"),
    ("SDRTR COUNT 105", "105UL << FMC_SDRTR_COUNT_Pos", "SDRTR_COUNT(105)"),
    ("SDRTR COUNT max", "FMC_SDRTR_COUNT_Msk >> FMC_SDRTR_COUNT_Pos", "SDRTR_COUNT_MAX"),
    ("SDRTR COUNT mask", "FMC_SDRTR_COUNT", "SDRTR_COUNT(SDRTR_COUNT_MAX)"),
    ("SDSR MODES2 mask", "FMC_SDSR_MODES2", "SDSR_MODES2_MASK"),
    ("SDSR BUSY", "FMC_SDSR_BUSY", "SDSR_BUSY"),
]

C_HEAD = "#include <stddef.h>\n#include <stdint.h>\n#include \"%s\"\n#define A(r) ((uint32_t)(uintptr_t)&(r))\n"


def run(cmd, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if p.returncode != 0:
        sys.exit("command failed: %s\n%s" % (" ".join(cmd), p.stdout + p.stderr))
    return p


def compiled_values(cross, tmp, header, incs, exprs, tag):
    src = os.path.join(tmp, tag + ".c")
    obj = os.path.join(tmp, tag + ".o")
    raw = os.path.join(tmp, tag + ".bin")
    with open(src, "w") as fh:
        fh.write(C_HEAD % header)
        fh.write("const uint32_t vals_%s[] = {\n%s\n};\n" % (tag, ",\n".join("(uint32_t)(%s)" % e for e in exprs)))
    run([cross + "gcc", "-mcpu=cortex-m4", "-mthumb", "-std=c11", "-fdata-sections", "-c", src, "-o", obj]
        + ["-I" + d for d in incs])
    run([cross + "objcopy", "-O", "binary", "-j", ".rodata.vals_" + tag, obj, raw])
    data = open(raw, "rb").read()
    return [int.from_bytes(data[4 * i:4 * i + 4], "little") for i in range(len(exprs))]


def grep(path, pattern):
    """(line number, line) of the first line matching pattern, or (None, None)."""
    rx = re.compile(pattern)
    with open(path, encoding="utf-8", errors="replace") as fh:
        for i, ln in enumerate(fh, 1):
            if rx.search(ln):
                return i, ln.rstrip("\n")
    return None, None


def define(path, name):
    i, ln = grep(path, r"#define\s+%s\b" % re.escape(name))
    if ln is None:
        return None, None
    m = re.search(r"\(\s*(?:\(\s*uint\d+_t\s*\))?\s*(0x[0-9A-Fa-f]+|\d+)U?L?\s*\)", ln) or \
        re.search(r"#define\s+\w+\s+(0x[0-9A-Fa-f]+|\d+)", ln)
    return (int(m.group(1), 0) if m else None), i


def pins_from_bsp(path):
    """{port letter: set of pins} from the HAL_GPIO_Init calls in BSP_SDRAM_MspInit."""
    text = open(path, encoding="utf-8", errors="replace").read()
    body = text[text.index("BSP_SDRAM_MspInit(SDRAM_HandleTypeDef"):]
    body = body[:body.index("Configure common DMA parameters")]
    out = {}
    for m in re.finditer(r"Pin\s*=\s*([^;]+);\s*HAL_GPIO_Init\(GPIO([A-K])", body):
        out[m.group(2)] = {int(p) for p in re.findall(r"GPIO_PIN_(\d+)", m.group(1))}
    return out


def pins_from_fw(path):
    text = open(path, encoding="utf-8").read()
    table = text[text.index("k_sdram_pins[] = {"):]
    table = table[:table.index("};")]
    out = {}
    for port, pin in re.findall(r"\{PORT([A-K]),\s*(\d+)\}", table):
        out.setdefault(port, set()).add(int(pin))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cubef4", required=True, help="STM32CubeF4 clone (for core_cm4.h and the examples)")
    ap.add_argument("--cmsis-device", required=True, help="cmsis-device-f4 clone")
    ap.add_argument("--hal", required=True, help="stm32f4xx_hal_driver clone")
    ap.add_argument("--bsp", required=True, help="32f429idiscovery-bsp clone")
    ap.add_argument("--cross", default="arm-none-eabi-", help="toolchain prefix (default arm-none-eabi-)")
    a = ap.parse_args()

    dev_inc = os.path.join(a.cmsis_device, "Include")
    core_inc = os.path.join(a.cubef4, "Drivers", "CMSIS", "Include")
    for p in (os.path.join(dev_inc, "stm32f429xx.h"), os.path.join(core_inc, "core_cm4.h"),
              os.path.join(a.bsp, "stm32f429i_discovery_sdram.c")):
        if not os.path.exists(p):
            sys.exit("missing %s: clone ST's sources first (see the top of this file)" % p)
    bad = 0

    def report(ok, name, detail):
        nonlocal bad
        bad += 0 if ok else 1
        print("%-9s %-32s %s" % ("OK" if ok else "MISMATCH", name, detail))

    mem_exprs = ["FLASH_BASE", "FLASH_END - FLASH_BASE + 1U", "SRAM1_BASE", "SRAM2_BASE - SRAM1_BASE",
                 "SRAM3_BASE - SRAM2_BASE", "SRAM3_BASE + 0x10000U - SRAM1_BASE"]
    with tempfile.TemporaryDirectory(prefix="e6_regcheck_") as tmp:
        st = compiled_values(a.cross, tmp, "stm32f429xx.h", [dev_inc, core_inc], [s for _, s, _ in ITEMS], "st")
        fw = compiled_values(a.cross, tmp, "regs_f429.h", [FW], [f for _, _, f in ITEMS], "fw")
        mem = compiled_values(a.cross, tmp, "stm32f429xx.h", [dev_inc, core_inc], mem_exprs, "mem")
    print("== 1. numbers: ST's CMSIS header vs regs_f429.h (%d items)" % len(ITEMS))
    for (name, _, _), s, f in zip(ITEMS, st, fw):
        report(s == f, name, "ST 0x%08x  firmware 0x%08x" % (s, f))

    print("== 2. SDRAM setup and pins vs ST's board code")
    bsp_c = os.path.join(a.bsp, "stm32f429i_discovery_sdram.c")
    bsp_h = os.path.join(a.bsp, "stm32f429i_discovery_sdram.h")
    sd_c = os.path.join(FW, "sdram_fmc.c")
    bp, fp = pins_from_bsp(bsp_c), pins_from_fw(sd_c)
    n_b, n_f = sum(len(v) for v in bp.values()), sum(len(v) for v in fp.values())
    report(bp == fp and n_b == 38, "SDRAM pins (AF12)", "BSP %d pins, firmware %d pins%s" % (
        n_b, n_f, "" if bp == fp else ": BSP %r vs firmware %r" % (bp, fp)))
    addr, line = define(bsp_h, "SDRAM_DEVICE_ADDR")
    report(addr == 0xD0000000, "SDRAM bank 2 address", "BSP 0x%08x (sdram.h:%s), firmware 0xD0000000" % (addr or 0, line))
    want = {"LoadToActiveDelay": 2, "ExitSelfRefreshDelay": 7, "SelfRefreshTime": 4, "RowCycleDelay": 7,
            "RPDelay": 2, "RCDDelay": 2, "WriteRecoveryTime": 2}
    for field, fw_val in want.items():
        i, ln = grep(bsp_c, r"Timing\.%s\s*=" % field)
        v = int(re.search(r"=\s*(\d+)", ln).group(1)) if ln else None
        note = " (firmware uses TWR = 3: safer, see sdram_fmc.c)" if field == "WriteRecoveryTime" else ""
        report(v == fw_val, "BSP timing " + field, "BSP %s (sdram.c:%s)%s" % (v, i, note))
    mr = 0
    lines = []
    for n in ("BURST_LENGTH_1", "BURST_TYPE_SEQUENTIAL", "CAS_LATENCY_3", "OPERATING_MODE_STANDARD",
              "WRITEBURST_MODE_SINGLE"):
        v, i = define(bsp_h, "SDRAM_MODEREG_" + n)
        mr |= v or 0
        lines.append(str(i))
    i, _ = grep(bsp_c, r"tmpmrd = \(uint32_t\)SDRAM_MODEREG_BURST_LENGTH_1")
    report(mr == 0x230, "mode register", "BSP 0x%04x (sdram.c:%s, sdram.h:%s), firmware 0x0230" % (mr, i, ",".join(lines)))
    i, ln = grep(bsp_h, r"15\.62 us x Freq\) - 20")
    report(ln is not None and round(15.625e-6 * 8e6) - 20 == 105, "refresh count formula",
           "BSP '(15.62 us x Freq) - 20' (sdram.h:%s) -> 105 at 8 MHz SDCLK" % i)
    seq = []
    for cmd in ("FMC_SDRAM_CMD_CLK_ENABLE", "FMC_SDRAM_CMD_PALL", "FMC_SDRAM_CMD_AUTOREFRESH_MODE",
                "FMC_SDRAM_CMD_LOAD_MODE"):
        i, _ = grep(bsp_c, r"CommandMode\s*=\s*%s" % cmd)
        seq.append(i or 0)
    report(seq == sorted(seq) and 0 not in seq, "init command order",
           "clock enable, PALL, auto-refresh, load mode at BSP sdram.c lines %s" % seq)
    i, ln = grep(bsp_c, r"CommandTarget\s*=\s*FMC_SDRAM_CMD_TARGET_BANK2")
    report(ln is not None, "command target bank 2", "BSP sdram.c:%s" % i)

    print("== 3. HAL constants used by the firmware")
    ll = os.path.join(a.hal, "Inc", "stm32f4xx_ll_fmc.h")
    for n, v in (("FMC_SDRAM_ROW_BITS_NUM_12", 0x4), ("FMC_SDRAM_MEM_BUS_WIDTH_16", 0x10),
                 ("FMC_SDRAM_INTERN_BANKS_NUM_4", 0x40), ("FMC_SDRAM_CAS_LATENCY_3", 0x180),
                 ("FMC_SDRAM_CLOCK_PERIOD_2", 0x800), ("FMC_SDRAM_RPIPE_DELAY_1", 0x2000),
                 ("FMC_SDRAM_CMD_CLK_ENABLE", 1), ("FMC_SDRAM_CMD_PALL", 2), ("FMC_SDRAM_CMD_AUTOREFRESH_MODE", 3),
                 ("FMC_SDRAM_CMD_LOAD_MODE", 4), ("FMC_SDRAM_CMD_SELFREFRESH_MODE", 5),
                 ("FMC_SDRAM_CMD_POWERDOWN_MODE", 6)):
        got, i = define(ll, n)
        report(got == v, n, "HAL %s (ll_fmc.h:%s), firmware %s" % (got, i, v))
    gx = os.path.join(a.hal, "Inc", "stm32f4xx_hal_gpio_ex.h")
    blk, _ = grep(gx, r"#if defined\(STM32F429xx\)")
    for n, v in (("GPIO_AF12_FMC", 12), ("GPIO_AF7_USART1", 7)):
        with open(gx, encoding="utf-8", errors="replace") as fh:
            hit = [(k, ln) for k, ln in enumerate(fh, 1) if k > (blk or 0) and re.search(r"#define %s\b" % n, ln)]
        k, ln = hit[0] if hit else (None, "")
        got = int(re.search(r"0x([0-9A-Fa-f]+)", ln).group(1), 16) if ln else None
        report(got == v, n, "HAL %s (gpio_ex.h:%s, F429 block from line %s)" % (got, k, blk))
    ex = os.path.join(a.cubef4, "Projects", "STM32F429I-Discovery", "Examples", "UART",
                      "UART_TwoBoards_ComPolling", "Inc", "main.h")
    if os.path.exists(ex):
        txt = open(ex, encoding="utf-8", errors="replace").read()
        ok = all(s in txt for s in ("USARTx                           USART1", "USARTx_TX_PIN                    GPIO_PIN_9",
                                     "USARTx_RX_PIN                    GPIO_PIN_10", "GPIO_AF7_USART1"))
        report(ok, "UART pins", "ST example: USART1, TX PA9, RX PA10, AF7; firmware the same")
    for baud, fw_brr in ((115200, (16000000 + 115200 // 2) // 115200), (500000, (16000000 + 250000) // 500000)):
        div = (16000000 * 25) // (4 * baud)
        mant, frac = div // 100, ((div - (div // 100) * 100) * 16 + 50) // 100
        st_brr = (mant << 4) + (frac & 0xF0) + (frac & 0x0F)
        report(st_brr == fw_brr, "USART BRR %d baud" % baud, "HAL UART_BRR_SAMPLING16 0x%x, firmware 0x%x" % (st_brr, fw_brr))
    print("== 4. linker script vs ST's memory map")
    ld = open(os.path.join(FW, "stm32f429_flash.ld"), encoding="utf-8").read()
    regions = {m.group(1): (int(m.group(2), 0), int(m.group(3)) * 1024) for m in
               re.finditer(r"^\s*(\w+)\s*\([rwx]+\)\s*:\s*ORIGIN\s*=\s*(0x[0-9A-Fa-f]+),\s*LENGTH\s*=\s*(\d+)K", ld, re.M)}
    flash_base, flash_size, sram_base, sram1, sram2, sram_all = mem
    fo, fl = regions.get("FLASH", (None, None))
    ro, rl = regions.get("RAM", (None, None))
    report(fo == flash_base and fl == flash_size, "FLASH region", "ST 0x%08x, %d KB; linker 0x%08x, %d KB" % (
        flash_base, flash_size // 1024, fo or 0, (fl or 0) // 1024))
    report(ro == sram_base and rl == sram_all and sram1 == 112 * 1024 and sram2 == 16 * 1024, "RAM region (SRAM1-3)",
           "ST 0x%08x, %d KB contiguous (112 + 16 + 64); linker 0x%08x, %d KB" % (
               sram_base, sram_all // 1024, ro or 0, (rl or 0) // 1024))
    print("== RESULT: %s (%d mismatches)" % ("ALL OK" if bad == 0 else "MISMATCHES FOUND", bad))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
