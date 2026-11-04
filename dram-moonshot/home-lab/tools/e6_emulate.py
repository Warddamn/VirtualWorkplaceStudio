#!/usr/bin/env python3
"""Run the E6 firmware binary (e6_retention.elf) on an emulated Cortex-M4, with no board.

This is a test bench for the firmware's logic, not a model of a real DRAM. It runs the exact ELF
that `make` builds, on the Unicorn CPU emulator, with small stand-ins for the parts of the
STM32F429 the firmware touches:
  - RCC: the 8 MHz crystal (HSE) and the PLL report "ready" (or never, with --no-hse);
  - GPIO ports A-G: plain registers, and PB6 reads back high when it is a GPIO output set high;
  - USART1: what the firmware sends is printed; the commands you give are typed in;
  - FMC: never busy; registers keep what is written; every write is logged;
  - SDRAM: 8 MB of perfect memory, optionally with one address line stuck low
    (--stuck-address-bit), or with four "leaky" words that flip a bit when read 1 s or more after
    they were written (--campaign);
  - SysTick: the 1 ms counter g_ms advances by 1 on every read, so waits cost no real time.
It does not model analog behaviour, timing, refresh, the real FMC state machine or temperature.

Needs the Unicorn emulator (pip install unicorn; tested with 2.1.4) and a built ELF:

  cd home-lab/code/T3_dram/stm32_retention && make && cd -
  python3 home-lab/tools/e6_emulate.py                       # boot, PING, INFO, TEMP, SELFTEST, RUN A/B/C
  python3 home-lab/tools/e6_emulate.py --no-hse               # crystal never starts: HELLO ends in HSI
  python3 home-lab/tools/e6_emulate.py --stuck-address-bit 9  # self-test must report word 0x100
  python3 home-lab/tools/e6_emulate.py --campaign --out emu.log   # the real capture_retention.py
                                                                  # campaign, with 4 leaky words
A full 8 MB write and read takes about 3 s of emulation per RUN.
"""
import argparse
import os
import struct
import sys

try:
    from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_MODE_MCLASS, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UcError
    from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_PC
except ImportError:
    sys.exit("needs the Unicorn emulator: python3 -m pip install unicorn")

HERE = os.path.dirname(os.path.abspath(__file__))
T3 = os.path.join(os.path.dirname(HERE), "code", "T3_dram")
DEFAULT_ELF = os.path.join(T3, "stm32_retention", "e6_retention.elf")
FLASH, SRAM, SDRAM, SDRAM_SIZE = 0x08000000, 0x20000000, 0xD0000000, 8 * 1024 * 1024
LEAKY_WORDS = (0x0ABCDE, 0x1F0001, 0x2A0102, 0x3FFFF0)
FMC_NAMES = {0x140: "SDCR1", 0x144: "SDCR2", 0x148: "SDTR1", 0x14C: "SDTR2", 0x150: "SDCMR",
             0x154: "SDRTR", 0x158: "SDSR"}


def read_elf(path):
    """(list of (paddr, bytes) for loadable data, {symbol: (address, size)}) from an ELF32 file."""
    d = open(path, "rb").read()
    if d[:4] != b"\x7fELF" or d[4] != 1:
        sys.exit("%s is not a 32-bit ELF file" % path)
    phoff, shoff = struct.unpack_from("<II", d, 28)
    phentsize, phnum, shentsize, shnum = struct.unpack_from("<HHHH", d, 42)
    segs = []
    for i in range(phnum):
        p_type, off, _, paddr, filesz = struct.unpack_from("<5I", d, phoff + i * phentsize)
        if p_type == 1 and filesz:
            segs.append((paddr, d[off:off + filesz]))
    secs = [struct.unpack_from("<10I", d, shoff + i * shentsize) for i in range(shnum)]
    syms = {}
    for sh in secs:
        if sh[1] != 2:                                   # SHT_SYMTAB
            continue
        strtab = secs[sh[6]]
        for k in range(sh[5] // 16):
            name_off, value, size = struct.unpack_from("<III", d, sh[4] + 16 * k)
            start = strtab[4] + name_off
            name = d[start:d.index(b"\0", start)].decode()
            if name:
                syms[name] = (value & ~1, size)
    return segs, syms


class Board:
    def __init__(self, elf, hse_ok=True, stuck_bit=None):
        segs, self.sym = read_elf(elf)
        for need in ("g_ms", "uart_getline"):
            if need not in self.sym:
                sys.exit("symbol %s not found: is this the E6 firmware ELF?" % need)
        self.uc = uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB | UC_MODE_MCLASS)
        uc.mem_map(FLASH, 2 * 1024 * 1024)
        uc.mem_map(SRAM, 192 * 1024)
        self.stuck_bit = stuck_bit
        if stuck_bit is None:
            uc.mem_map(SDRAM, SDRAM_SIZE)
        else:
            self.sdram = bytearray(SDRAM_SIZE)
            uc.mmio_map(SDRAM, SDRAM_SIZE, self.sd_read, None, self.sd_write, None)
        for paddr, blob in segs:
            uc.mem_write(paddr, blob)
        self.hse_ok, self.regs, self.gpio, self.fmc_log = hse_ok, {}, {}, []
        self.out, self.inp, self.started = bytearray(), bytearray(), False
        uc.mmio_map(0x40020000, 0x4000, self.ahb1_read, None, self.ahb1_write, None)   # GPIOA-K, RCC
        uc.mmio_map(0x40011000, 0x1000, self.usart_read, None, self.usart_write, None)  # USART1
        uc.mmio_map(0xA0000000, 0x1000, self.fmc_read, None, self.fmc_write, None)      # FMC
        uc.mmio_map(0xE000E000, 0x1000, lambda *a: 0, None, lambda *a: None, None)     # SysTick etc.
        g = self.sym["g_ms"][0]
        uc.hook_add(UC_HOOK_MEM_READ, self.tick, begin=g, end=g + 3)

    def now(self):
        return struct.unpack("<I", self.uc.mem_read(self.sym["g_ms"][0], 4))[0]

    def tick(self, uc, access, address, size, value, user):
        uc.mem_write(address, struct.pack("<I", (self.now() + 1) & 0xFFFFFFFF))

    def sd_read(self, uc, off, size, user):
        o = off & ~(1 << self.stuck_bit)
        return int.from_bytes(self.sdram[o:o + size], "little")

    def sd_write(self, uc, off, size, value, user):
        o = off & ~(1 << self.stuck_bit)
        self.sdram[o:o + size] = value.to_bytes(size, "little")

    def ahb1_read(self, uc, off, size, user):
        if off >= 0x3800:                                # RCC
            r = off - 0x3800
            v = self.regs.get(("RCC", r), 0)
            if r == 0x00:                                # CR: HSIRDY; HSERDY/PLLRDY follow HSEON/PLLON
                v |= 0x2
                if self.hse_ok and v & (1 << 16):
                    v |= 1 << 17
                if self.hse_ok and v & (1 << 24):
                    v |= 1 << 25
            elif r == 0x08:                              # CFGR: SWS follows SW
                v = (v & ~0xC) | ((v & 3) << 2)
            return v
        port, r = divmod(off, 0x400)
        if r == 0x10:                                    # IDR: output pins read back their ODR bit
            moder, odr = self.gpio.get((port, 0), 0), self.gpio.get((port, 0x14), 0)
            return sum(odr & (1 << p) for p in range(16) if (moder >> (2 * p)) & 3 == 1)
        return self.gpio.get((port, r), 0)

    def ahb1_write(self, uc, off, size, value, user):
        if off >= 0x3800:
            self.regs[("RCC", off - 0x3800)] = value
            return
        port, r = divmod(off, 0x400)
        if r == 0x18:                                    # BSRR: set low half, reset high half
            odr = (self.gpio.get((port, 0x14), 0) | (value & 0xFFFF)) & ~(value >> 16)
            self.gpio[(port, 0x14)] = odr
        else:
            self.gpio[(port, r)] = value

    def usart_read(self, uc, off, size, user):
        if off == 0x00:                                  # SR: TXE and TC always; RXNE if input waits
            if not self.inp:
                a, n = self.sym["uart_getline"]
                if a <= uc.reg_read(UC_ARM_REG_PC) < a + max(n, 2):
                    uc.emu_stop()                        # waiting for a command: hand back control
            return 0xC0 | (0x20 if self.inp else 0)
        if off == 0x04:
            if self.inp:
                c = self.inp[0]
                del self.inp[0]
                return c
            return 0
        return self.regs.get(("USART", off), 0)

    def usart_write(self, uc, off, size, value, user):
        if off == 0x04:
            self.out.append(value & 0xFF)
        else:
            self.regs[("USART", off)] = value

    def fmc_read(self, uc, off, size, user):
        if off == 0x158:
            return 0                                     # SDSR: never busy, both banks normal
        reset = 0x0FFFFFFF if off in (0x148, 0x14C) else (0x2D0 if off in (0x140, 0x144) else 0)
        return self.regs.get(("FMC", off), reset)

    def fmc_write(self, uc, off, size, value, user):
        self.regs[("FMC", off)] = value
        self.fmc_log.append((FMC_NAMES.get(off, hex(off)), value))

    def go(self, limit_s=600):
        uc = self.uc
        if not self.started:
            sp, pc = struct.unpack("<II", uc.mem_read(FLASH, 8))
            uc.reg_write(UC_ARM_REG_SP, sp)
            self.started = True
        else:
            pc = uc.reg_read(UC_ARM_REG_PC)
        try:
            uc.emu_start(pc | 1, 0xFFFFFFFF, timeout=int(limit_s * 1e6))
        except UcError as exc:
            self.out += ("\r\nEMULATION ERROR: %s at pc=0x%08x\r\n" % (exc, uc.reg_read(UC_ARM_REG_PC))).encode()

    def add_leaky_words(self, words=LEAKY_WORDS, after_ms=1000, flip=0x0008):
        written = {}

        def on_write(uc, access, addr, size, value, user):
            written[addr] = self.now()

        def on_read(uc, access, addr, size, value, user):
            t = written.get(addr)
            if t is not None and self.now() - t >= after_ms:
                v = struct.unpack("<H", uc.mem_read(addr, 2))[0] ^ flip
                uc.mem_write(addr, struct.pack("<H", v))
                written[addr] = None
        for w in words:
            a = SDRAM + 2 * w
            self.uc.hook_add(UC_HOOK_MEM_WRITE, on_write, begin=a, end=a + 1)
            self.uc.hook_add(UC_HOOK_MEM_READ, on_read, begin=a, end=a + 1)


class EmuDevice:
    """Same interface as capture_retention.SerialDevice: send(line), readline(timeout_s)."""

    def __init__(self, board):
        self.b = board
        self.b.go()                                      # boot; like SerialDevice, drop boot lines
        self.pos = len(self.b.out)

    def send(self, line):
        self.b.inp += (line + "\n").encode()

    def readline(self, timeout_s):
        while True:
            i = self.b.out.find(b"\n", self.pos)
            if i >= 0:
                line = self.b.out[self.pos:i].decode("ascii", "replace").strip()
                self.pos = i + 1
                if line:
                    return line
                continue
            before, had_input = len(self.b.out), bool(self.b.inp)
            self.b.go()
            if len(self.b.out) == before and not had_input:
                return None


def main():
    ap = argparse.ArgumentParser(description="Run the E6 firmware ELF on an emulated Cortex-M4.")
    ap.add_argument("--elf", default=DEFAULT_ELF)
    ap.add_argument("--no-hse", action="store_true", help="the crystal never starts (tests the HSI fallback)")
    ap.add_argument("--stuck-address-bit", type=int, help="SDRAM byte-address bit held low (tests the self-test)")
    ap.add_argument("--commands", nargs="+", default=["PING", "INFO", "TEMP", "SELFTEST", "RUN 1 C 0 0 0 0 1 250",
                                                      "RUN 2 A 1 0 0 64 1 250", "RUN 3 B 5 1 1234 1000 1 250",
                                                      "RUN 4 Q 0 0 0 0 1 250"])
    ap.add_argument("--campaign", action="store_true",
                    help="run capture_retention.py's campaign (ALL0/ALL1, 3 waits, 2 repeats) with 4 leaky words")
    ap.add_argument("--out", default="e6_emulated.log", help="log file for --campaign")
    a = ap.parse_args()
    if not os.path.exists(a.elf):
        sys.exit("%s not found: run make in code/T3_dram/stm32_retention first" % a.elf)
    b = Board(a.elf, hse_ok=not a.no_hse, stuck_bit=a.stuck_address_bit)
    if a.campaign:
        sys.path.insert(0, T3)
        import capture_retention as cr
        b.add_leaky_words()
        dev = EmuDevice(b)
        args = cr.make_parser().parse_args(["--temp-c", "25", "--repeats", "2", "--patterns", "ALL0", "ALL1",
                                            "--waits", "0.064", "1.024", "8.192", "--out", a.out])
        rc = cr.campaign(dev, args, a.out)
        print("campaign exit code %d; expect 4 failing bits in every 1.024 s and 8.192 s run, none at 64 ms" % rc)
        return rc
    b.inp += "".join(c + "\r\n" for c in a.commands).encode()
    b.go()
    print(b.out.decode("ascii", "replace").replace("\r\n", "\n"))
    print("--- FMC writes (first 12 of %d):" % len(b.fmc_log))
    for name, v in b.fmc_log[:12]:
        print("    %-6s 0x%08x" % (name, v))
    print("--- RCC CR 0x%08x  PLLCFGR 0x%08x  CFGR 0x%08x;  USART1 BRR 0x%x  CR1 0x%x" % (
        b.regs.get(("RCC", 0), 0), b.regs.get(("RCC", 4), 0), b.regs.get(("RCC", 8), 0),
        b.regs.get(("USART", 8), 0), b.regs.get(("USART", 0xC), 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
