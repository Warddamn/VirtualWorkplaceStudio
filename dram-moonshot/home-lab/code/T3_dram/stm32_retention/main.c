/*
 * main.c -- E6 retention-tail firmware for the STM32F429I-DISC1.
 *
 * REFERENCE CODE, UNTESTED ON HARDWARE. Syntax-checked on a PC with `make syntax`; the pattern
 * generator is host-tested against ../retention_map.py. Treat every register value as a claim to
 * verify against RM0090 and UM1670 before you flash.
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
 *        Z  (only if built with -DENABLE_METHOD_Z) write COUNT = 0. The STM32H7 manual text says
 *           0 means "no refresh"; that is NOT confirmed for the F4, so Z is off by default.
 *      Self-refresh is useless here: the chip refreshes itself. Power-down is not used because the
 *      FMC's refresh behaviour in that mode is not confirmed.
 *   3. read every word back, compare with the regenerated pattern, stream each failing word as
 *      F,<id>,<word_hex>,<expected_hex>,<observed_hex> (first 20,000 words), then an END summary.
 *      If a precharge times out, the pause is skipped, "ERR,precharge timeout" is printed and END
 *      carries status ERR (the host keeps reading to END; the analysis drops ERR runs).
 *
 * Clock: the internal 16 MHz RC oscillator (HSI). It drifts a few % over temperature
 * [UNVERIFIED]; that scales every wait (harmless) and the baud rate (garbled text only when hot).
 *
 * Commands (one per line, 115200 8N1):
 *   PING | INFO | TEMP | RUN <id> <A|B|C|Z> <pattern 0-5> <inv 0/1> <seed> <wait_ms> <repeat> <temp_x10>
 */
#include <stdint.h>
#include "regs_f429.h"
#include "sdram_fmc.h"
#include "patterns.h"
#include "uart.h"
#include "max31855.h"

#define FW_VERSION    "e6-ret-0.2"
#define HCLK_HZ       16000000UL
#define BAUD          115200UL
#define LOG_CAP       20000UL
#define HOLD_PERIODS  3U
#define MAX_WAIT_MS   3600000UL   /* refuse pauses over one hour */

volatile uint32_t g_ms;
static int s_sdram_ok;

void SysTick_Handler(void)
{
    g_ms++;
}

static void systick_init(void)
{
    SYST_RVR = HCLK_HZ / 1000U - 1U;
    SYST_CVR = 0U;
    SYST_CSR = 7U;                          /* processor clock, interrupt, enable */
}

static void delay_ms(uint32_t ms)
{
    uint32_t t0 = g_ms;
    while ((uint32_t)(g_ms - t0) < ms) {
    }
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
        sdram_set_refresh_count(count);
        delay_ms(HOLD_PERIODS * (period_us / 1000U) + 1U);
        sdram_set_refresh_count(sdram_normal_count());
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
        sdram_deselect(1);
        t0 = g_ms;
        delay_ms(wait_ms);
        sdram_deselect(0);
        /* true unrefreshed time = pause + one full normal refresh window (a fixed ~54 ms) */
        interval_ms = (g_ms - t0) + (sdram_period_us_for_count(sdram_normal_count()) + 500U) / 1000U;
        break;
    }
#ifdef ENABLE_METHOD_Z
    case 'Z': {
        uint32_t t0 = g_ms;
        sdram_set_refresh_count(0U);
        delay_ms(wait_ms);
        sdram_set_refresh_count(sdram_normal_count());
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
    systick_init();
    uart_init(BAUD);
    thermo_init();
    s_sdram_ok = (sdram_init(2U) == 0);
    if (!s_sdram_ok) {
        uart_puts("ERR,sdram init failed\r\n");
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
