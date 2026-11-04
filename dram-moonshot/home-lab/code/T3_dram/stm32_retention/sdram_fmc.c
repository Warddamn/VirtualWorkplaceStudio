/*
 * sdram_fmc.c -- REFERENCE CODE, UNTESTED ON HARDWARE.
 *
 * Board: STM32F429I-DISC1 / 32F429IDISCOVERY. SDRAM: ISSI IS42S16400J (64 Mbit, 4 banks x 4096 rows
 * x 256 columns x 16 bit) on FMC SDRAM bank 2 (SDNE1, SDCKE1), mapped at 0xD0000000.
 *
 * Checked on 2026-11-04 against ST's own code, cloned from GitHub (file:line in these commits):
 *   [BSPC] STMicroelectronics/32f429idiscovery-bsp @ d77779a2a4e9  stm32f429i_discovery_sdram.c
 *   [BSPH] same commit, stm32f429i_discovery_sdram.h
 *   [EX]   STMicroelectronics/STM32CubeF4 @ 60c8abe0ae88
 *          Projects/STM32F429I-Discovery/Examples/FMC/FMC_SDRAM/Src/{main.c,stm32f4xx_hal_msp.c}
 *   [LLC]  STMicroelectronics/stm32f4xx_hal_driver @ 1f6451c3e077  Src/stm32f4xx_ll_fmc.c
 *   [ZEP]  zephyrproject-rtos/zephyr @ decee24b4fbc  boards/st/stm32f429i_disc1/stm32f429i_disc1.dts
 * Register addresses and bit fields: see regs_f429.h.
 *
 * The MCU runs at 16 MHz (HSE crystal + PLL, or HSI if the crystal does not start; main.c), so
 * SDCLK = 8 MHz (HCLK/2). That slow clock is deliberate: the refresh timer COUNT field is 13 bits
 * (max 8191), so a slower SDCLK stretches the longest programmable refresh period to
 * 4096 x 8192 / 8 MHz = 4.19 s. At 8 MHz one SDRAM clock is 125 ns, so every nanosecond minimum of
 * the datasheet is met with a large margin by ST's 90 MHz cycle counts, used here unchanged.
 */
#include "regs_f429.h"
#include "sdram_fmc.h"

#define HCLK_HZ 16000000UL

typedef struct { uint8_t port; uint8_t pin; } pin_t;

/* 38 FMC pins: D0-D15, A0-A11, BA0-1, NBL0-1, SDCLK, SDCKE1, SDNE1, SDNWE, SDNRAS, SDNCAS.
 * Identical to ST's BSP pin table and code, [BSPC]:325-385 (PG4/PG5 = BA0/BA1 appear in the code at
 * :383-384 though not in the comment table). Zephyr's board file [ZEP]:215-226 lists the same pins plus
 * PG2/PG3 (FMC_A12/A13), which a 12-row-bit part does not use; ST's BSP leaves them out, and so do we. */
static const pin_t k_sdram_pins[] = {
    {PORTB, 5}, {PORTB, 6},                                           /* SDCKE1, SDNE1  [BSPC]:341-342 */
    {PORTC, 0},                                                       /* SDNWE          [BSPC]:343 */
    {PORTD, 0}, {PORTD, 1}, {PORTD, 8}, {PORTD, 9}, {PORTD, 10}, {PORTD, 14}, {PORTD, 15}, /* :363-365 */
    {PORTE, 0}, {PORTE, 1}, {PORTE, 7}, {PORTE, 8}, {PORTE, 9}, {PORTE, 10}, {PORTE, 11},  /* :369-372 */
    {PORTE, 12}, {PORTE, 13}, {PORTE, 14}, {PORTE, 15},
    {PORTF, 0}, {PORTF, 1}, {PORTF, 2}, {PORTF, 3}, {PORTF, 4}, {PORTF, 5}, {PORTF, 11},   /* :376-379 */
    {PORTF, 12}, {PORTF, 13}, {PORTF, 14}, {PORTF, 15},
    {PORTG, 0}, {PORTG, 1}, {PORTG, 4}, {PORTG, 5}, {PORTG, 8}, {PORTG, 15},               /* :383-384 */
};
#define SDNE1_PORT PORTB          /* PB6 = FMC_SDNE1: [BSPC]:342, [ZEP]:218 */
#define SDNE1_PIN  6U

static uint32_t s_sdclk_hz = HCLK_HZ / 2U;

/* Alternate function 12, push-pull, no pull ([BSPC]:349-352). Speed: very high, as ST's FMC_SDRAM
 * example ([EX] stm32f4xx_hal_msp.c:91); the BSP uses "fast" = high ([BSPC]:350). Either is fine at 8 MHz. */
static void pin_af12(uint32_t port, uint32_t pin)
{
    uint32_t sh2 = pin * 2U;
    GPIO_MODER(port)   = (GPIO_MODER(port) & ~(3UL << sh2)) | (MODER_AF << sh2);
    GPIO_OSPEEDR(port) = (GPIO_OSPEEDR(port) & ~(3UL << sh2)) | (OSPEED_VERY_HIGH << sh2);
    GPIO_OTYPER(port)  &= ~(1UL << pin);                /* push-pull */
    GPIO_PUPDR(port)   = (GPIO_PUPDR(port) & ~(3UL << sh2)) | (PUPD_NONE << sh2);
    if (pin < 8U) {
        GPIO_AFRL(port) = (GPIO_AFRL(port) & ~(0xFUL << (pin * 4U))) | (GPIO_AF12_FMC << (pin * 4U));
    } else {
        GPIO_AFRH(port) = (GPIO_AFRH(port) & ~(0xFUL << ((pin - 8U) * 4U))) |
                          (GPIO_AF12_FMC << ((pin - 8U) * 4U));
    }
}

static int wait_not_busy(void)
{
    for (uint32_t i = 0; i < 1000000UL; i++) {
        if ((FMC_SDSR & SDSR_BUSY) == 0U) {
            return 0;
        }
    }
    return -1;
}

/* One SDCMR write, as HAL FMC_SDRAM_SendCommand ([LLC]:1384-1401): mode | target | (NRFS - 1) | MRD,
 * then wait for BUSY to clear. Target is bank 2 only (CTB2). */
static int fmc_cmd(uint32_t mode, uint32_t nrfs, uint32_t mrd)
{
    if (wait_not_busy() != 0) {
        return -1;
    }
    FMC_SDCMR = mode | SDCMR_CTB2 | SDCMR_NRFS(nrfs ? nrfs : 1U) | SDCMR_MRD(mrd);
    return wait_not_busy();
}

uint32_t sdram_sdclk_hz(void) { return s_sdclk_hz; }

/* ST's formula, [BSPH]:95-97: COUNT = (refresh period / rows) x SDCLK - 20 = 15.62 us x 8 MHz - 20 = 105.
 * The full-array window is then 4096 x (105 + 1) / 8 MHz = 54.3 ms. */
uint32_t sdram_normal_count(void)
{
    return (uint32_t)((64000ULL * s_sdclk_hz) / (SDRAM_ROWS_PER_BANK * 1000000ULL)) - 20U;
}

/* For a deliberately relaxed period we want the period itself, so no margin:
 * full-array refresh period = rows x (COUNT + 1) / SDCLK  ->  COUNT = period x SDCLK / rows - 1 */
uint32_t sdram_count_for_period_ms(uint32_t period_ms)
{
    uint64_t c = ((uint64_t)period_ms * s_sdclk_hz) / (1000ULL * SDRAM_ROWS_PER_BANK);
    if (c < SDRTR_COUNT_MIN + 1U) {
        c = SDRTR_COUNT_MIN + 1U;
    }
    if (c > SDRTR_COUNT_MAX + 1U) {
        c = SDRTR_COUNT_MAX + 1U;
    }
    return (uint32_t)(c - 1U);
}

uint32_t sdram_period_us_for_count(uint32_t count)
{
    return (uint32_t)(((uint64_t)SDRAM_ROWS_PER_BANK * (count + 1U) * 1000000ULL) / s_sdclk_hz);
}

/* Write COUNT (CRE = 0, REIE = 0), as HAL FMC_SDRAM_ProgramRefreshRate ([LLC]:1411-1420), and read it
 * back. Changing COUNT after initialisation is what method A does; RM0090 is reported to advise against
 * reprogramming it after init "to avoid modifying the refresh rate" [REPORTED, H7 text via search
 * snippet; F4 wording UNVERIFIED], which is exactly the effect wanted here. */
int sdram_set_refresh_count(uint32_t count)
{
#ifndef ENABLE_METHOD_Z
    if (count < SDRTR_COUNT_MIN) {
        count = SDRTR_COUNT_MIN;
    }
#endif
    if (count > SDRTR_COUNT_MAX) {
        count = SDRTR_COUNT_MAX;
    }
    FMC_SDRTR = SDRTR_COUNT(count);
    return (SDRTR_COUNT_FIELD(FMC_SDRTR) == count) ? 0 : -1;
}

int sdram_precharge_all(void)
{
    return fmc_cmd(SDCMR_MODE_PALL, 0U, 0U);
}

/* Method B: hand SDNE1 (PB6) to a plain GPIO output held high, so the SDRAM sees COMMAND INHIBIT
 * (CS# high) on every clock and ignores the FMC's auto-refresh commands; then give it back.
 * Checks the pin really is where it should be. */
int sdram_deselect(int on)
{
    uint32_t sh2 = SDNE1_PIN * 2U;
    if (on) {
        GPIO_BSRR(SDNE1_PORT) = (1UL << SDNE1_PIN);  /* output latch = 1 (chip select inactive) */
        GPIO_MODER(SDNE1_PORT) = (GPIO_MODER(SDNE1_PORT) & ~(3UL << sh2)) | (MODER_OUTPUT << sh2);
        /* IDR samples the pin once per AHB1 clock; if the switch landed while the FMC was driving
         * SDNE1 low for a command, give the input path a few clocks before reading it, so a stale
         * sample cannot cause a false "ERR,sdne1 pin" [ESTIMATE: margin, not a measured need]. */
        (void)GPIO_IDR(SDNE1_PORT);
        (void)GPIO_IDR(SDNE1_PORT);
        if (((GPIO_MODER(SDNE1_PORT) >> sh2) & 3UL) != MODER_OUTPUT ||
            (GPIO_IDR(SDNE1_PORT) & (1UL << SDNE1_PIN)) == 0U) {
            return -1;
        }
    } else {
        GPIO_MODER(SDNE1_PORT) = (GPIO_MODER(SDNE1_PORT) & ~(3UL << sh2)) | (MODER_AF << sh2);
        if (((GPIO_MODER(SDNE1_PORT) >> sh2) & 3UL) != MODER_AF) {
            return -1;
        }
    }
    return 0;
}

int sdram_init(uint32_t sdclk_div)
{
    uint32_t div_bits = (sdclk_div == 3U) ? SDCR_SDCLK_DIV3 : SDCR_SDCLK_DIV2;
    s_sdclk_hz = HCLK_HZ / ((sdclk_div == 3U) ? 3U : 2U);

    /* clocks: FMC and GPIOB..G, as [BSPC]:311-322; read back once so the clocks are on before use */
    RCC_AHB1ENR |= (1UL << PORTB) | (1UL << PORTC) | (1UL << PORTD) | (1UL << PORTE) |
                   (1UL << PORTF) | (1UL << PORTG);
    (void)RCC_AHB1ENR;
    RCC_AHB3ENR |= RCC_AHB3ENR_FMCEN_BIT;
    (void)RCC_AHB3ENR;

    for (uint32_t i = 0; i < sizeof k_sdram_pins / sizeof k_sdram_pins[0]; i++) {
        pin_af12(k_sdram_pins[i].port, k_sdram_pins[i].pin);
    }

    /* Control, as HAL FMC_SDRAM_Init for bank 2 ([LLC]:1208-1225): SDCLK, RBURST and RPIPE are only
     * taken from SDCR1; the rest goes in SDCR2. Values as the BSP ([BSPC]:106-117, [BSPH]:70-88):
     * 8 column bits, 12 row bits, 16-bit bus, 4 internal banks, CAS 3, no write protection,
     * SDCLK = HCLK/2, read burst off, read pipe delay 1 HCLK. */
    FMC_SDCR1 = (FMC_SDCR1 & ~(SDCR_SDCLK_MASK | SDCR_RBURST | SDCR_RPIPE_MASK)) | div_bits | SDCR_RPIPE(1);
    FMC_SDCR2 = SDCR_NC_8BIT | SDCR_NR_12BIT | SDCR_MWID_16 | SDCR_NB_4BANKS | SDCR_CAS(3);

    /* Timing, as HAL FMC_SDRAM_Timing_Init for bank 2 ([LLC]:1266-1281): TRC and TRP are only taken
     * from SDTR1; the rest goes in SDTR2 (its TRC/TRP fields are don't-care). Cycle counts as the BSP
     * ([BSPC]:90-103): TMRD 2, TXSR 7, TRAS 4, TRC 7, TRP 2, TRCD 2, except TWR = 3 (BSP: 2). RM0090
     * requires TWR >= TRAS - TRCD (= 2) and TWR >= TRC - TRCD - TRP (= 3) [REPORTED: search snippets
     * of RM0090 Rev 18 and of ST's STM32H5 FMC text, 2026-11-04; the manual itself was not reachable];
     * 3 meets both, and costs nothing at 8 MHz. The same text says that with one SDRAM device the
     * unused bank's TWR stays at its reset value 0xF: SDTR1 below changes only TRC and TRP, so it does.
     * RM0090 also says COUNT must not equal TWR + TRP + TRC + TRCD + 4 cycles (= 18 here) [REPORTED,
     * same snippet]; every COUNT this firmware writes is >= 41 (or 0 in the experimental method Z). */
    FMC_SDTR1 = (FMC_SDTR1 & ~(SDTR_TRC_MASK | SDTR_TRP_MASK)) | ((7UL - 1U) << SDTR_TRC_POS) |
                ((2UL - 1U) << SDTR_TRP_POS);
    FMC_SDTR2 = SDTR(2, 7, 4, 7, 3, 2, 2);

    /* JEDEC power-up sequence, as [BSPC]:141-194 */
    if (fmc_cmd(SDCMR_MODE_CLK_EN, 0U, 0U) != 0) return -1;        /* [BSPC]:146-152 */
    delay_ms(100U);                     /* >= 100 us; the BSP waits 1 ms ([BSPC]:156), ST's example
                                           100 ms ([EX] main.c:261) */
    if (fmc_cmd(SDCMR_MODE_PALL, 0U, 0U) != 0) return -2;          /* [BSPC]:159-165 */
    if (fmc_cmd(SDCMR_MODE_AUTOREF, 8U, 0U) != 0) return -3;       /* BSP sends 4 ([BSPC]:170); 8 is
                                                                      harmless (each costs only tRC) */
    /* mode register 0x0230: burst length 1, sequential, CAS 3, standard, single-location write,
     * exactly [BSPC]:177-181 with [BSPH]:110-120 */
    if (fmc_cmd(SDCMR_MODE_LOADMODE, 0U, 0x0230U) != 0) return -4; /* [BSPC]:183-189 */
    if (sdram_set_refresh_count(sdram_normal_count()) != 0) return -5;   /* [BSPC]:191-193 */
    if ((FMC_SDSR & SDSR_MODES2_MASK) != 0U) return -6;           /* bank 2 must report normal mode */
    return 0;
}

/* ---- power-on self-test ------------------------------------------------------------------------
 * Catches wiring, pin-mapping and bank-mapping errors in a few milliseconds, before any campaign.
 * Data bus: walking one and walking zero at word 0, with the complement written to word 1 in between
 * so a floating bus cannot "remember" the value. Address bus: the classic test of every word-address
 * bit (column A0-A7, row A0-A11, bank BA0-BA1 = 22 bits), for bits stuck high, stuck low or shorted. */
static volatile uint16_t *const k_mem = (volatile uint16_t *)(uintptr_t)SDRAM_BANK2_BASE;

static int st_fail(uint32_t w, uint32_t e, uint32_t o, uint32_t *bw, uint32_t *be, uint32_t *bo)
{
    *bw = w;
    *be = e;
    *bo = o;
    return -1;
}

int sdram_selftest(uint32_t *bad_word, uint32_t *expected, uint32_t *observed)
{
    const uint16_t pat = 0xAAAAU, anti = 0x5555U;
    uint32_t v, j, k;

    for (k = 0; k < 32U; k++) {                       /* 16 walking ones, then 16 walking zeros */
        uint16_t d = (uint16_t)(1U << (k & 15U));
        if (k >= 16U) {
            d = (uint16_t)~d;
        }
        k_mem[0] = d;
        k_mem[1] = (uint16_t)~d;
        v = k_mem[0];
        if (v != d) {
            return st_fail(0U, d, v, bad_word, expected, observed);
        }
    }
    for (k = 0; k < 22U; k++) {
        k_mem[1UL << k] = pat;
    }
    k_mem[0] = anti;
    for (k = 0; k < 22U; k++) {                       /* address bit stuck high */
        v = k_mem[1UL << k];
        if (v != pat) {
            return st_fail(1UL << k, pat, v, bad_word, expected, observed);
        }
    }
    k_mem[0] = pat;
    for (j = 0; j < 22U; j++) {                       /* address bit stuck low or shorted */
        k_mem[1UL << j] = anti;
        v = k_mem[0];
        if (v != pat) {
            return st_fail(0U, pat, v, bad_word, expected, observed);
        }
        for (k = 0; k < 22U; k++) {
            if (k != j) {
                v = k_mem[1UL << k];
                if (v != pat) {
                    return st_fail(1UL << k, pat, v, bad_word, expected, observed);
                }
            }
        }
        k_mem[1UL << j] = pat;
    }
    return 0;
}
