/*
 * main.c -- E6 retention-tail firmware for the STM32F429I-DISC1.
 *
 * REFERENCE CODE, UNTESTED ON HARDWARE. It builds and links with arm-none-eabi-gcc 13.2.1, every
 * register value was checked against ST's CMSIS header, HAL and board-support code (comments in
 * regs_f429.h and sdram_fmc.c cite file:line), and it boots to HELLO/PONG in QEMU (netduinoplus2,
 * guide section 16). The pattern generator is host-tested against ../retention_map.py.
 *
 * What it does, per RUN command from the PC (capture_retention.py):
 *   1. write a data pattern to all 8 MB of SDRAM (normal refresh running);
 *   2. take refresh away for a while, by one of:
 *        A  relax: program the FMC refresh timer so each row is refreshed only every <wait_ms>
 *           (21 ms .. 4.19 s at SDCLK 8 MHz); hold 3 periods; restore the normal 64 ms rate.
 *        B  pause: precharge all banks, then hold chip select (SDNE1, PB6) high as a plain GPIO.
 *           With CS# high the SDRAM ignores every command, including the controller's refreshes.
 *           Wait <wait_ms>, hand the pin back to the FMC; normal refresh resumes at once.
 *           The chip's internal row counter stops while it ignores refreshes and resumes where it
 *           left off, so EVERY row goes unrefreshed for the pause plus exactly one normal window
 *           (4096 x 106 / 8 MHz = 54 ms). The END line reports that true interval.
 *        C  control: no pause at all (must give zero failures).
 *        Z  EXPERIMENTAL (only if built with -DENABLE_METHOD_Z) write COUNT = 0. ST's STM32H7 text
 *           says 0 means "no refresh"; RM0090 (F4) asks for COUNT >= 41, so 0 is outside the
 *           documented range here. Off by default; validate it against method B before trusting it.
 *      Self-refresh is useless here: the chip refreshes itself. Power-down is not used because the
 *      FMC's refresh behaviour in that mode is not confirmed.
 *   3. read every word back, compare with the regenerated pattern, stream each failing word as
 *      F,<id>,<word_hex>,<expected_hex>,<observed_hex> (first 20,000 words), then an END summary.
 *      If a precharge times out, the pause is skipped, "ERR,precharge timeout" is printed and END
 *      carries status ERR (the host keeps reading to END; the analysis drops ERR runs).
 *      If normal refresh cannot be proven restored after a pause (the refresh count does not read
 *      back, or PB6 does not return to the FMC), the run ends in ERR AND every later RUN or SELFTEST
 *      is refused ("ERR,sdram not initialised") until the board is reset, so no later run (a
 *      control run included) can silently use an SDRAM that is not being refreshed normally.
 *
 * Clock: 16 MHz from the board's 8 MHz HSE crystal through the PLL (M 4, N 64, P 8), so the baud
 * rate and every wait are crystal-accurate even when the board is hot. If the crystal or PLL does
 * not start, the firmware stays on the internal 16 MHz RC oscillator (HSI), which drifts a few % over
 * temperature [UNVERIFIED]. Both paths give the same 16 MHz, so every constant below is unchanged.
 * HELLO ends with HSE or HSI to say which one is running. Build with -DE6_CLOCK_HSI to force HSI.
 *
 * At boot: clock, UART, thermocouple, SDRAM init, then a 1 ms SDRAM bus self-test (SELFTEST,OK or
 * ERR,sdram selftest,...), then HELLO.
 *
 * Commands (one per line, 115200 8N1):
 *   PING | INFO | TEMP | SELFTEST |
 *   RUN <id> <A|B|C|Z> <pattern 0-5> <inv 0/1> <seed> <wait_ms> <repeat> <temp_x10>
 */
#include <stdint.h>
#include "regs_f429.h"
#include "sdram_fmc.h"
#include "patterns.h"
#include "uart.h"
#include "max31855.h"

#define FW_VERSION    "e6-ret-0.4"
#define HCLK_HZ       16000000UL
#define BAUD          115200UL
#define LOG_CAP       20000UL
#define HOLD_PERIODS  3U
#define MAX_WAIT_MS   3600000UL   /* refuse pauses over one hour */

#define HSE_START_MS  100U        /* HAL's HSE_STARTUP_TIMEOUT (100 ms) */
#define PLL_LOCK_MS   10U         /* HAL's PLL_TIMEOUT_VALUE is 2 ms; 10 ms of margin */

volatile uint32_t g_ms;
static int s_sdram_ok;
static const char *s_clk_src = "HSI";

void SysTick_Handler(void)
{
    g_ms++;
}

/* Any fault (for example an SDRAM access with the FMC misconfigured): say so, then stop. */
void HardFault_Handler(void)
{
    if (uart_ready()) {
        uart_puts("\r\nERR,hardfault\r\n");
    }
    for (;;) {
    }
}

static void systick_init(void)
{
    SYST_RVR = HCLK_HZ / 1000U - 1U;        /* 1 ms at 16 MHz */
    SYST_CVR = 0U;
    SYST_CSR = SYST_CSR_ENABLE_ALL;         /* processor clock, interrupt, enable */
}

void delay_ms(uint32_t ms)
{
    uint32_t t0 = g_ms;
    while ((uint32_t)(g_ms - t0) < ms) {
    }
}

/* HSE 8 MHz crystal (HSE_VALUE 8000000 in ST's FMC_SDRAM example, stm32f4xx_hal_conf.h:82; Zephyr's
 * board file uses the HSE without bypass, stm32f429i_disc1.dts:107-110) -> PLL: /M 4 = 2 MHz VCO input
 * (ST recommends 2 MHz), x N 64 = 128 MHz VCO (100-432 MHz), /P 8 = 16 MHz SYSCLK; /Q 8 = 16 MHz on the
 * unused 48 MHz domain. Ranges: HAL stm32f4xx_hal_rcc.h:1409-1413, stm32f4xx_hal_rcc_ex.h:6931.
 * Sequence as HAL_RCC_OscConfig / HAL_RCC_ClockConfig (stm32f4xx_hal_rcc.c): HSEON, wait HSERDY,
 * write PLLCFGR, PLLON, wait PLLRDY, SW = PLL, wait SWS = PLL. Flash stays at 0 wait states (16 MHz).
 * AHB, APB1 and APB2 prescalers stay at their reset value 1. Any timeout: back to HSI.
 * PLLCFGR bit 29 is reserved and reads 1 at reset (RCC_PLLCFGR_RST_VALUE 0x24003010, stm32f429xx.h:
 * 17127). ST is inconsistent about it: HAL_RCC_OscConfig, which ST's examples for this board call,
 * writes the register whole and clears it (stm32f4xx_hal_rcc.c:492-496), while the macro
 * __HAL_RCC_PLL_CONFIG sets it (stm32f4xx_hal_rcc_ex.h:5871). We keep it at its reset value, as
 * the macro does and as ST's usual "reserved, keep at reset value" rule asks [UNVERIFIED wording]. */
static void clock_init(void)
{
#ifndef E6_CLOCK_HSI
    uint32_t t0 = g_ms;
    RCC_CR |= RCC_CR_HSEON;
    while ((RCC_CR & RCC_CR_HSERDY) == 0U) {
        if ((uint32_t)(g_ms - t0) > HSE_START_MS) {
            RCC_CR &= ~RCC_CR_HSEON;
            return;
        }
    }
    RCC_PLLCFGR = RCC_PLLCFGR_RSVD29 | RCC_PLLCFGR_SRC_HSE | RCC_PLLCFGR_M(4) | RCC_PLLCFGR_N(64) |
                  RCC_PLLCFGR_P(8) | RCC_PLLCFGR_Q(8);
    RCC_CR |= RCC_CR_PLLON;
    t0 = g_ms;
    while ((RCC_CR & RCC_CR_PLLRDY) == 0U) {
        if ((uint32_t)(g_ms - t0) > PLL_LOCK_MS) {
            RCC_CR &= ~(RCC_CR_PLLON | RCC_CR_HSEON);
            return;
        }
    }
    RCC_CFGR = (RCC_CFGR & ~RCC_CFGR_SW_MASK) | RCC_CFGR_SW_PLL;
    t0 = g_ms;
    while ((RCC_CFGR & RCC_CFGR_SWS_MASK) != RCC_CFGR_SWS_PLL) {
        if ((uint32_t)(g_ms - t0) > PLL_LOCK_MS) {
            RCC_CFGR = (RCC_CFGR & ~RCC_CFGR_SW_MASK) | RCC_CFGR_SW_HSI;
            RCC_CR &= ~(RCC_CR_PLLON | RCC_CR_HSEON);
            return;
        }
    }
    s_clk_src = "HSE";
#endif
}

static volatile uint16_t *const k_sdram = (volatile uint16_t *)(uintptr_t)SDRAM_BANK2_BASE;

static uint32_t pop16(uint32_t x)
{
    uint32_t n = 0;
    x &= 0xFFFFU;
    while (x) {
        x &= x - 1U;
        n++;
    }
    return n;
}

static void put_temp_line(uint32_t rid, const char *phase)
{
    int32_t t = thermo_read_c_x100();
    uart_puts("TEMP,");
    uart_put_u32(rid);
    uart_putc(',');
    uart_puts(phase);
    uart_putc(',');
    if (t == TEMP_INVALID) {
        uart_puts("nan");
    } else {
        uart_put_fixed(t, 2U);
    }
    uart_puts("\r\n");
}

static void hello(void)
{
    uart_puts("HELLO," FW_VERSION ",IS42S16400J,");
    uart_put_u32(SDRAM_N_WORDS);
    uart_puts(",16,");
    uart_put_u32(sdram_sdclk_hz());
    uart_puts(",A|B|C");
#ifdef ENABLE_METHOD_Z
    uart_puts("|Z");
#endif
    uart_putc(',');
    uart_puts(s_clk_src);
    uart_puts("\r\n");
}

/* Bus self-test; on failure the SDRAM is marked unusable and RUN is refused. */
static void selftest(void)
{
    uint32_t w = 0U, e = 0U, o = 0U;
    if (sdram_selftest(&w, &e, &o) == 0) {
        uart_puts("SELFTEST,OK\r\n");
        return;
    }
    s_sdram_ok = 0;
    uart_puts("ERR,sdram selftest,");
    uart_put_hex(w, 1U);
    uart_putc(',');
    uart_put_hex(e, 4U);
    uart_putc(',');
    uart_put_hex(o, 4U);
    uart_puts("\r\n");
}

static void run_test(uint32_t rid, char method, uint32_t pat, uint32_t inv, uint32_t seed,
                     uint32_t wait_ms, uint32_t repeat, int32_t temp_x10)
{
    uint32_t interval_ms = 0U;
    uint32_t fail_words = 0U, fail_bits = 0U, b10 = 0U, b01 = 0U, logged = 0U;
    uint32_t bad = 0U;                        /* 1: the pause was skipped; END says ERR */

    uart_puts("RUN,");
    uart_put_u32(rid);
    uart_putc(',');
    uart_putc(method);
    uart_putc(',');
    uart_put_u32(pat);
    uart_putc(',');
    uart_put_u32(inv);
    uart_putc(',');
    uart_put_u32(seed);
    uart_putc(',');
    uart_put_u32(wait_ms);
    uart_putc(',');
    uart_put_u32(repeat);
    uart_putc(',');
    uart_put_fixed(temp_x10, 1U);
    uart_puts("\r\n");
    put_temp_line(rid, "start");

    /* 1. write the pattern (normal refresh) */
    for (uint32_t w = 0; w < SDRAM_N_WORDS; w++) {
        k_sdram[w] = pattern_word(pat, inv, seed, w);
    }

    /* 2. take refresh away. Code and stack live in internal flash/SRAM: no SDRAM access here. */
    switch (method) {
    case 'A': {
        uint32_t count = sdram_count_for_period_ms(wait_ms);
        uint32_t period_us = sdram_period_us_for_count(count);
        /* close the rows left open by the write loop: at a relaxed rate the next auto-refresh
         * (which precharges) can be ~1 ms away, beyond tRAS(max) */
        if (sdram_precharge_all() != 0) {
            uart_puts("ERR,precharge timeout\r\n");
            bad = 1U;
            break;
        }
        if (sdram_set_refresh_count(count) != 0) {
            uart_puts("ERR,refresh count readback\r\n");
            bad = 1U;
        } else {
            delay_ms(HOLD_PERIODS * (period_us / 1000U) + 1U);
        }
        if (sdram_set_refresh_count(sdram_normal_count()) != 0) {
            uart_puts("ERR,refresh count readback\r\n");
            bad = 1U;
            s_sdram_ok = 0;                           /* normal refresh not proven back: refuse RUN until reset */
        }
        interval_ms = (period_us + 500U) / 1000U;     /* the retention interval actually tested */
        break;
    }
    case 'B': {
        uint32_t t0;
        if (sdram_precharge_all() != 0) {
            uart_puts("ERR,precharge timeout\r\n");
            bad = 1U;
            break;                                /* never deselect with a bank still open */
        }
        t0 = g_ms;
        if (sdram_deselect(1) != 0) {
            uart_puts("ERR,sdne1 pin\r\n");          /* PB6 did not go to GPIO-high */
            bad = 1U;
        } else {
            delay_ms(wait_ms);
        }
        if (sdram_deselect(0) != 0) {
            uart_puts("ERR,sdne1 pin\r\n");          /* PB6 did not return to the FMC */
            bad = 1U;
            s_sdram_ok = 0;                           /* the SDRAM may get no refresh at all: refuse RUN until reset */
        }
        /* true unrefreshed time = pause + one full normal refresh window (a fixed ~54 ms) */
        interval_ms = (g_ms - t0) + (sdram_period_us_for_count(sdram_normal_count()) + 500U) / 1000U;
        break;
    }
#ifdef ENABLE_METHOD_Z
    case 'Z': {
        uint32_t t0 = g_ms;
        if (sdram_precharge_all() != 0) {
            uart_puts("ERR,precharge timeout\r\n");
            bad = 1U;
        } else if (sdram_set_refresh_count(0U) != 0) {
            uart_puts("ERR,refresh count readback\r\n");
            bad = 1U;
        } else {
            delay_ms(wait_ms);
        }
        if (sdram_set_refresh_count(sdram_normal_count()) != 0) {
            uart_puts("ERR,refresh count readback\r\n");
            bad = 1U;
            s_sdram_ok = 0;                           /* normal refresh not proven back: refuse RUN until reset */
        }
        interval_ms = g_ms - t0;
        break;
    }
#endif
    case 'C':
    default:
        interval_ms = 0U;
        break;
    }
    put_temp_line(rid, "end");

    /* 3. read back (normal refresh again, so late rows do not keep decaying) */
    for (uint32_t w = 0; w < SDRAM_N_WORDS; w++) {
        uint32_t v = k_sdram[w];
        uint32_t e = pattern_word(pat, inv, seed, w);
        if (v != e) {
            uint32_t x = (v ^ e) & 0xFFFFU;
            fail_words++;
            fail_bits += pop16(x);
            b10 += pop16(e & x);              /* stored 1, read 0 */
            b01 += pop16(~e & x);             /* stored 0, read 1 */
            if (logged < LOG_CAP) {
                uart_puts("F,");
                uart_put_u32(rid);
                uart_putc(',');
                uart_put_hex(w, 1U);
                uart_putc(',');
                uart_put_hex(e, 4U);
                uart_putc(',');
                uart_put_hex(v, 4U);
                uart_puts("\r\n");
                logged++;
            }
        }
    }
    uart_puts("END,");
    uart_put_u32(rid);
    uart_putc(',');
    uart_put_u32(fail_words);
    uart_putc(',');
    uart_put_u32(fail_bits);
    uart_putc(',');
    uart_put_u32(b10);
    uart_putc(',');
    uart_put_u32(b01);
    uart_putc(',');
    uart_put_u32(logged);
    uart_putc(',');
    uart_put_u32(interval_ms);
    uart_puts(bad ? ",ERR\r\n" : (logged < fail_words ? ",TRUNC\r\n" : ",OK\r\n"));
}

/* ---- tiny command parser ------------------------------------------------------------------ */
static const char *next_tok(const char *s, char *tok, uint32_t max)
{
    uint32_t n = 0;
    while (*s == ' ') {
        s++;
    }
    while (*s && *s != ' ' && n + 1U < max) {
        tok[n++] = *s++;
    }
    tok[n] = '\0';
    return s;
}

static int parse_i32(const char *t, int32_t *out)
{
    int32_t sign = 1, v = 0;
    if (*t == '-') {
        sign = -1;
        t++;
    }
    if (!*t) {
        return -1;
    }
    while (*t) {
        int32_t d;
        if (*t < '0' || *t > '9') {
            return -1;
        }
        d = (int32_t)(*t++ - '0');
        if (v > (2147483647 - d) / 10) {
            return -1;                            /* would overflow int32: reject */
        }
        v = v * 10 + d;
    }
    *out = sign * v;
    return 0;
}

static int streq(const char *a, const char *b)
{
    while (*a && *a == *b) {
        a++;
        b++;
    }
    return *a == *b;
}

int main(void)
{
    char line[96], tok[16];
    int rc;
    systick_init();
    clock_init();                             /* before the UART: the baud divider assumes 16 MHz */
    uart_init(BAUD);
    thermo_init();
#ifdef E6_EMU
    rc = -100;                                /* emulator build (make emu): QEMU has no FMC, skip it */
#else
    rc = sdram_init(2U);
#endif
    s_sdram_ok = (rc == 0);
    if (!s_sdram_ok) {
        uart_puts("ERR,sdram init failed,step ");
        uart_put_u32((uint32_t)(-rc));
        uart_puts("\r\n");
    } else {
        selftest();
    }
    hello();
    for (;;) {
        const char *p;
        uart_getline(line, sizeof line);
        p = next_tok(line, tok, sizeof tok);
        if (streq(tok, "PING")) {
            uart_puts("PONG\r\n");
        } else if (streq(tok, "INFO")) {
            hello();
        } else if (streq(tok, "TEMP")) {
            put_temp_line(0U, "now");
        } else if (streq(tok, "SELFTEST")) {
            if (s_sdram_ok) {
                selftest();
            } else {
                uart_puts("ERR,sdram not initialised\r\n");
            }
        } else if (streq(tok, "RUN")) {
            int32_t v[8];
            if (!s_sdram_ok) {                    /* an SDRAM access now would HardFault */
                uart_puts("ERR,sdram not initialised\r\n");
                continue;
            }
            char method = 'C';
            int ok = 1;
            for (int i = 0; i < 8 && ok; i++) {
                p = next_tok(p, tok, sizeof tok);
                if (i == 1) {
                    method = tok[0];
                    v[i] = 0;
                } else if (parse_i32(tok, &v[i]) != 0) {
                    ok = 0;
                }
            }
            if (!ok || v[2] < 0 || v[2] > 5 || v[6] < 0 || v[5] < 0 || (uint32_t)v[5] > MAX_WAIT_MS ||
                !(method == 'A' || method == 'B' || method == 'C' || method == 'Z')) {
                uart_puts("ERR,bad RUN command\r\n");
                continue;
            }
            run_test((uint32_t)v[0], method, (uint32_t)v[2], (uint32_t)(v[3] != 0), (uint32_t)v[4],
                     (uint32_t)v[5], (uint32_t)v[6], v[7]);
        } else {
            uart_puts("ERR,unknown command\r\n");
        }
    }
}
