/*
 * regs_f429.h -- minimal STM32F429 register map for the E6 retention firmware.
 *
 * REFERENCE CODE, UNTESTED ON HARDWARE.
 * Addresses and bit positions are written from memory of RM0090 and the CMSIS device header
 * (stm32f429xx.h). They are [UNVERIFIED-PK]: check every line against RM0090 sections 6 (RCC),
 * 8 (GPIO), 30 (USART) and 37 (FMC SDRAM controller) before flashing.
 *
 * This header is self-contained on purpose: it doubles as the "stub header" that lets
 * `gcc -fsyntax-only` check the firmware on a PC without the vendor SDK.
 */
#ifndef REGS_F429_H
#define REGS_F429_H

#include <stdint.h>

#define REG32(addr) (*(volatile uint32_t *)(uintptr_t)(addr))

/* ---- RCC ---------------------------------------------------------------- */
#define RCC_BASE          0x40023800UL
#define RCC_AHB1ENR       REG32(RCC_BASE + 0x30)   /* bit n = GPIO port n clock (A=0 .. K=10) */
#define RCC_AHB3ENR       REG32(RCC_BASE + 0x38)   /* bit 0 = FMCEN */
#define RCC_APB2ENR       REG32(RCC_BASE + 0x44)   /* bit 4 = USART1EN */

/* ---- GPIO --------------------------------------------------------------- */
#define GPIO_BASE(port)   (0x40020000UL + 0x400UL * (uint32_t)(port))
#define GPIO_MODER(p)     REG32(GPIO_BASE(p) + 0x00)
#define GPIO_OTYPER(p)    REG32(GPIO_BASE(p) + 0x04)
#define GPIO_OSPEEDR(p)   REG32(GPIO_BASE(p) + 0x08)
#define GPIO_PUPDR(p)     REG32(GPIO_BASE(p) + 0x0C)
#define GPIO_IDR(p)       REG32(GPIO_BASE(p) + 0x10)
#define GPIO_ODR(p)       REG32(GPIO_BASE(p) + 0x14)
#define GPIO_BSRR(p)      REG32(GPIO_BASE(p) + 0x18)
#define GPIO_AFRL(p)      REG32(GPIO_BASE(p) + 0x20)
#define GPIO_AFRH(p)      REG32(GPIO_BASE(p) + 0x24)
enum { PORTA = 0, PORTB, PORTC, PORTD, PORTE, PORTF, PORTG };
#define MODER_INPUT   0U
#define MODER_OUTPUT  1U
#define MODER_AF      2U

/* ---- USART1 (ST-LINK virtual COM port on PA9/PA10 by default) ------------ */
#define USART1_BASE       0x40011000UL
#define USART1_SR         REG32(USART1_BASE + 0x00)
#define USART1_DR         REG32(USART1_BASE + 0x04)
#define USART1_BRR        REG32(USART1_BASE + 0x08)
#define USART1_CR1        REG32(USART1_BASE + 0x0C)
#define USART_SR_RXNE     (1UL << 5)
#define USART_SR_TXE      (1UL << 7)
#define USART_SR_ORE      (1UL << 3)
#define USART_CR1_UE      (1UL << 13)
#define USART_CR1_TE      (1UL << 3)
#define USART_CR1_RE      (1UL << 2)

/* ---- SysTick ------------------------------------------------------------ */
#define SYST_CSR          REG32(0xE000E010UL)
#define SYST_RVR          REG32(0xE000E014UL)
#define SYST_CVR          REG32(0xE000E018UL)

/* ---- FMC SDRAM controller (FMC_Bank5_6 at FMC base 0xA0000000 + 0x140) --- */
#define FMC_SD_BASE       0xA0000140UL
#define FMC_SDCR1         REG32(FMC_SD_BASE + 0x00)
#define FMC_SDCR2         REG32(FMC_SD_BASE + 0x04)
#define FMC_SDTR1         REG32(FMC_SD_BASE + 0x08)
#define FMC_SDTR2         REG32(FMC_SD_BASE + 0x0C)
#define FMC_SDCMR         REG32(FMC_SD_BASE + 0x10)
#define FMC_SDRTR         REG32(FMC_SD_BASE + 0x14)
#define FMC_SDSR          REG32(FMC_SD_BASE + 0x18)

/* FMC_SDCRx fields */
#define SDCR_NC_8BIT      (0UL << 0)
#define SDCR_NR_12BIT     (1UL << 2)
#define SDCR_MWID_16      (1UL << 4)
#define SDCR_NB_4BANKS    (1UL << 6)
#define SDCR_CAS(n)       ((uint32_t)(n) << 7)    /* 1..3 */
#define SDCR_SDCLK_DIV2   (2UL << 10)             /* SDCLK = HCLK/2; only SDCR1 counts */
#define SDCR_SDCLK_DIV3   (3UL << 10)
#define SDCR_RPIPE(n)     ((uint32_t)(n) << 13)
/* FMC_SDTRx fields, each written as (cycles - 1) */
#define SDTR(tmrd, txsr, tras, trc, twr, trp, trcd) \
    ((uint32_t)((tmrd) - 1) | ((uint32_t)((txsr) - 1) << 4) | ((uint32_t)((tras) - 1) << 8) | \
     ((uint32_t)((trc) - 1) << 12) | ((uint32_t)((twr) - 1) << 16) | ((uint32_t)((trp) - 1) << 20) | \
     ((uint32_t)((trcd) - 1) << 24))
/* FMC_SDCMR fields */
#define SDCMR_MODE_NORMAL     0UL
#define SDCMR_MODE_CLK_EN     1UL
#define SDCMR_MODE_PALL       2UL
#define SDCMR_MODE_AUTOREF    3UL
#define SDCMR_MODE_LOADMODE   4UL
#define SDCMR_MODE_SELFREF    5UL   /* the SDRAM refreshes ITSELF: useless for a retention test */
#define SDCMR_MODE_POWERDOWN  6UL   /* FMC behaviour around refresh not confirmed: not used */
#define SDCMR_CTB2            (1UL << 3)
#define SDCMR_CTB1            (1UL << 4)
#define SDCMR_NRFS(n)         ((uint32_t)((n) - 1) << 5)
#define SDCMR_MRD(v)          ((uint32_t)(v) << 9)
/* FMC_SDRTR fields: COUNT is 13 bits [13:1], must be >= 41 (0x29) */
#define SDRTR_COUNT(n)        ((uint32_t)(n) << 1)
#define SDRTR_COUNT_MAX       8191U
#define SDRTR_COUNT_MIN       41U
/* FMC_SDSR */
#define SDSR_BUSY             (1UL << 5)

/* SDRAM bank 2 (SDNE1/SDCKE1) is mapped at 0xD0000000 */
#define SDRAM_BANK2_BASE      0xD0000000UL

#endif /* REGS_F429_H */
