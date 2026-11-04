/*
 * max31855.c -- REFERENCE CODE, UNTESTED ON HARDWARE.
 * Adafruit MAX31855 breakout on three spare pins. Defaults PE2 = SCK, PE3 = CS, PE4 = SO (MISO).
 * Evidence that PE2-PE4 are free: ST's board-support package configures port E only for the FMC
 * (PE0, PE1, PE7-PE15: 32f429idiscovery-bsp @ d77779a2a4e9 stm32f429i_discovery_sdram.c:369-372) and
 * no other BSP file touches port E; Zephyr's board file assigns no PE2-PE6 function; one ST community
 * user reports PE2-PE5 free [REPORTED, anecdote]. PE2, PE3 and PE4 double as SYS_TRACECLK,
 * SYS_TRACED0 and SYS_TRACED1 (ST's CubeMX pin database, STMicroelectronics/STM32_open_pin_data
 * @ 7d1f1514ed55 mcu/STM32F429ZITx.xml). They are plain GPIO unless a debugger sets DBGMCU_CR
 * TRACE_IOEN (the bit exists in stm32f429xx.h; "0 at reset" is from memory [UNVERIFIED]); the
 * ST-LINK's SWD link does not use them. UM1670's free-I/O table itself was not reachable [UNVERIFIED]:
 * confirm on the board before wiring. Power the breakout from 3V3 and GND.
 * MAX31855 frame: D31..D18 = thermocouple temperature, signed, 0.25 C per LSB; D16 = fault.
 */
#include "regs_f429.h"
#include "max31855.h"

#define TC_PORT PORTE
#define TC_SCK  2U
#define TC_CS   3U
#define TC_SO   4U

static void short_delay(void)
{
    for (volatile uint32_t i = 0; i < 20U; i++) {
    }
}

void thermo_init(void)
{
    RCC_AHB1ENR |= (1UL << TC_PORT);
    (void)RCC_AHB1ENR;
    GPIO_MODER(TC_PORT) = (GPIO_MODER(TC_PORT) & ~((3UL << (TC_SCK * 2U)) | (3UL << (TC_CS * 2U)) |
                                                   (3UL << (TC_SO * 2U)))) |
                          (MODER_OUTPUT << (TC_SCK * 2U)) | (MODER_OUTPUT << (TC_CS * 2U));
    GPIO_PUPDR(TC_PORT) = (GPIO_PUPDR(TC_PORT) & ~(3UL << (TC_SO * 2U))) | (1UL << (TC_SO * 2U));
    GPIO_BSRR(TC_PORT) = (1UL << TC_CS);                 /* CS high (idle) */
    GPIO_BSRR(TC_PORT) = (1UL << (TC_SCK + 16U));        /* SCK low */
}

int32_t thermo_read_c_x100(void)
{
    uint32_t d = 0;
    GPIO_BSRR(TC_PORT) = (1UL << (TC_CS + 16U));         /* CS low: conversion stops, data out */
    short_delay();
    for (int i = 31; i >= 0; i--) {
        GPIO_BSRR(TC_PORT) = (1UL << (TC_SCK + 16U));    /* SCK low */
        short_delay();
        d <<= 1;
        if (GPIO_IDR(TC_PORT) & (1UL << TC_SO)) {
            d |= 1U;
        }
        GPIO_BSRR(TC_PORT) = (1UL << TC_SCK);            /* SCK high */
        short_delay();
    }
    GPIO_BSRR(TC_PORT) = (1UL << TC_CS);
    if (d & (1UL << 16)) {
        return TEMP_INVALID;                             /* fault bit, or nothing fitted (pull-up) */
    }
    int32_t raw = (int32_t)(d >> 18);
    if (raw & 0x2000) {
        raw -= 0x4000;                                   /* sign-extend 14 bits */
    }
    return raw * 25;                                     /* 0.25 C per LSB -> x100 */
}
