/*
 * sdram_fmc.c -- REFERENCE CODE, UNTESTED ON HARDWARE.
 *
 * Board: STM32F429I-DISC1 / 32F429IDISCOVERY. SDRAM: ISSI IS42S16400J (64 Mbit, 4 banks x 4096 rows
 * x 256 columns x 16 bit) on FMC SDRAM bank 2 (SDNE1, SDCKE1), mapped at 0xD0000000.
 * Pin list and timings follow ST's board-support package (stm32f429i_discovery_sdram.c) as
 * remembered [UNVERIFIED-PK]: check them against the board schematic in UM1670 before flashing.
 *
 * The MCU runs from its reset clock (HSI 16 MHz, no PLL), so SDCLK = 8 MHz (HCLK/2). That slow
 * clock is deliberate: the refresh timer COUNT field is 13 bits (max 8191), so a slower SDCLK
 * stretches the longest programmable refresh period to 4096 x 8192 / 8 MHz = 4.19 s.
 */
#include "regs_f429.h"
#include "sdram_fmc.h"

#define HCLK_HZ 16000000UL

typedef struct { uint8_t port; uint8_t pin; } pin_t;

/* 38 FMC pins: D0-D15, A0-A11, BA0-1, NBL0-1, SDCLK, SDCKE1, SDNE1, SDNWE, SDNRAS, SDNCAS */
static const pin_t k_sdram_pins[] = {
    {PORTB, 5}, {PORTB, 6},                                           /* SDCKE1, SDNE1 */
    {PORTC, 0},                                                       /* SDNWE */
    {PORTD, 0}, {PORTD, 1}, {PORTD, 8}, {PORTD, 9}, {PORTD, 10}, {PORTD, 14}, {PORTD, 15},
    {PORTE, 0}, {PORTE, 1}, {PORTE, 7}, {PORTE, 8}, {PORTE, 9}, {PORTE, 10}, {PORTE, 11},
    {PORTE, 12}, {PORTE, 13}, {PORTE, 14}, {PORTE, 15},
    {PORTF, 0}, {PORTF, 1}, {PORTF, 2}, {PORTF, 3}, {PORTF, 4}, {PORTF, 5}, {PORTF, 11},
    {PORTF, 12}, {PORTF, 13}, {PORTF, 14}, {PORTF, 15},
    {PORTG, 0}, {PORTG, 1}, {PORTG, 4}, {PORTG, 5}, {PORTG, 8}, {PORTG, 15},
};
#define SDNE1_PORT PORTB
#define SDNE1_PIN  6U

static uint32_t s_sdclk_hz = HCLK_HZ / 2U;

static void pin_af12(uint32_t port, uint32_t pin)
{
    uint32_t sh2 = pin * 2U;
    GPIO_MODER(port)   = (GPIO_MODER(port) & ~(3UL << sh2)) | (MODER_AF << sh2);
    GPIO_OSPEEDR(port) |= (3UL << sh2);                 /* very high speed */
    GPIO_OTYPER(port)  &= ~(1UL << pin);                /* push-pull */
    GPIO_PUPDR(port)   &= ~(3UL << sh2);                /* no pull */
    if (pin < 8U) {
        GPIO_AFRL(port) = (GPIO_AFRL(port) & ~(0xFUL << (pin * 4U))) | (12UL << (pin * 4U));
    } else {
        GPIO_AFRH(port) = (GPIO_AFRH(port) & ~(0xFUL << ((pin - 8U) * 4U))) | (12UL << ((pin - 8U) * 4U));
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

static int fmc_cmd(uint32_t mode, uint32_t nrfs, uint32_t mrd)
{
    if (wait_not_busy() != 0) {
        return -1;
    }
    FMC_SDCMR = mode | SDCMR_CTB2 | (nrfs ? SDCMR_NRFS(nrfs) : 0U) | SDCMR_MRD(mrd);
    return wait_not_busy();
}

static void spin_us(uint32_t us)
{
    /* crude: ~4 CPU cycles per iteration at 16 MHz -> 4 iterations per microsecond */
    for (volatile uint32_t i = 0; i < us * 4U; i++) {
    }
}

uint32_t sdram_sdclk_hz(void) { return s_sdclk_hz; }

/* RM0090 formula: COUNT = (refresh period / rows) x SDCLK - 20 (20-cycle safety margin) */
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

void sdram_set_refresh_count(uint32_t count)
{
#ifndef ENABLE_METHOD_Z
    if (count < SDRTR_COUNT_MIN) {
        count = SDRTR_COUNT_MIN;
    }
#endif
    if (count > SDRTR_COUNT_MAX) {
        count = SDRTR_COUNT_MAX;
    }
    FMC_SDRTR = SDRTR_COUNT(count);   /* CRE = 0, REIE = 0; the timer restarts on write */
}

int sdram_precharge_all(void)
{
    return fmc_cmd(SDCMR_MODE_PALL, 0U, 0U);
}

void sdram_deselect(int on)
{
    uint32_t sh2 = SDNE1_PIN * 2U;
    if (on) {
        GPIO_BSRR(SDNE1_PORT) = (1UL << SDNE1_PIN);  /* output latch = 1 (chip select inactive) */
        GPIO_MODER(SDNE1_PORT) = (GPIO_MODER(SDNE1_PORT) & ~(3UL << sh2)) | (MODER_OUTPUT << sh2);
    } else {
        GPIO_MODER(SDNE1_PORT) = (GPIO_MODER(SDNE1_PORT) & ~(3UL << sh2)) | (MODER_AF << sh2);
    }
}

int sdram_init(uint32_t sdclk_div)
{
    uint32_t div_bits = (sdclk_div == 3U) ? SDCR_SDCLK_DIV3 : SDCR_SDCLK_DIV2;
    s_sdclk_hz = HCLK_HZ / ((sdclk_div == 3U) ? 3U : 2U);

    RCC_AHB1ENR |= (1UL << PORTB) | (1UL << PORTC) | (1UL << PORTD) | (1UL << PORTE) |
                   (1UL << PORTF) | (1UL << PORTG);
    RCC_AHB3ENR |= 1UL;                                  /* FMCEN */
    (void)RCC_AHB3ENR;                                   /* read back: let the clock settle */

    for (uint32_t i = 0; i < sizeof k_sdram_pins / sizeof k_sdram_pins[0]; i++) {
        pin_af12(k_sdram_pins[i].port, k_sdram_pins[i].pin);
    }

    /* SDCLK, RBURST and RPIPE are only taken from SDCR1, even when bank 2 is used */
    FMC_SDCR1 = (FMC_SDCR1 & ~((3UL << 10) | (1UL << 12) | (3UL << 13))) | div_bits | SDCR_RPIPE(1);
    FMC_SDCR2 = SDCR_NC_8BIT | SDCR_NR_12BIT | SDCR_MWID_16 | SDCR_NB_4BANKS | SDCR_CAS(3);
    /* TRC and TRP are only taken from SDTR1 */
    FMC_SDTR1 = (FMC_SDTR1 & ~((0xFUL << 12) | (0xFUL << 20))) | ((7UL - 1U) << 12) | ((2UL - 1U) << 20);
    /* TMRD 2, TXSR 7, TRAS 4, TRC 7, TWR 3, TRP 2, TRCD 2 (BSP values for 90 MHz, generous at 8 MHz,
     * except TWR). TWR 3: RM0090 needs TWR >= TRAS - TRCD and TWR >= TRC - TRCD - TRP [UNVERIFIED] */
    FMC_SDTR2 = SDTR(2, 7, 4, 7, 3, 2, 2);

    if (fmc_cmd(SDCMR_MODE_CLK_EN, 0U, 0U) != 0) return -1;
    spin_us(1000U);                                      /* >= 100 us power-up delay */
    if (fmc_cmd(SDCMR_MODE_PALL, 0U, 0U) != 0) return -2;
    if (fmc_cmd(SDCMR_MODE_AUTOREF, 8U, 0U) != 0) return -3;
    /* mode register: burst length 1, sequential, CAS 3, standard, single-location write */
    if (fmc_cmd(SDCMR_MODE_LOADMODE, 0U, 0x0230U) != 0) return -4;
    sdram_set_refresh_count(sdram_normal_count());
    return 0;
}
