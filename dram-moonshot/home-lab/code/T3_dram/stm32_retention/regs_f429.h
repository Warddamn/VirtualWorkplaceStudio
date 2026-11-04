/*
 * regs_f429.h -- minimal STM32F429 register map for the E6 retention firmware.
 *
 * REFERENCE CODE, UNTESTED ON HARDWARE (it builds and links with arm-none-eabi-gcc 13.2.1; see the
 * guide, section 16).
 *
 * Every address, bit position and field value below was checked on 2026-11-04 against ST's own
 * sources, cloned from GitHub. The comments cite file:line in these exact commits:
 *   [CMSIS]  STMicroelectronics/cmsis-device-f4 @ 9192c7b9df75  Include/stm32f429xx.h
 *   [CORE]   STMicroelectronics/STM32CubeF4     @ 60c8abe0ae88  Drivers/CMSIS/Include/core_cm4.h
 *   [LLFMC]  STMicroelectronics/stm32f4xx_hal_driver @ 1f6451c3e077  Inc/stm32f4xx_ll_fmc.h
 *   [GPIOEX] same HAL driver commit, Inc/stm32f4xx_hal_gpio_ex.h (STM32F429xx block, lines 49-164)
 *   [BSP]    STMicroelectronics/32f429idiscovery-bsp @ d77779a2a4e9  stm32f429i_discovery_sdram.h
 * (Those three submodule commits are the ones STM32CubeF4 @ 60c8abe, package FW.F4.1.28.3, pins.)
 * home-lab/tools/e6_regcheck.py repeats the comparison by compiling the CMSIS header and this one
 * with arm-none-eabi-gcc and comparing the numbers.
 *
 * This header is self-contained on purpose: it doubles as the "stub header" that lets
 * `gcc -fsyntax-only` check the firmware on a PC without the vendor SDK.
 */
#ifndef REGS_F429_H
#define REGS_F429_H

#include <stdint.h>

#define REG32(addr) (*(volatile uint32_t *)(uintptr_t)(addr))

/* ---- RCC ---------------------------------------------------------------- */
#define RCC_BASE          0x40023800UL             /* [CMSIS]:1124 AHB1PERIPH_BASE + 0x3800 (:1049, :1029) */
#define RCC_CR            REG32(RCC_BASE + 0x00)   /* [CMSIS] RCC_TypeDef: CR at offset 0x00 */
#define RCC_PLLCFGR       REG32(RCC_BASE + 0x04)   /* [CMSIS] RCC_TypeDef: PLLCFGR at 0x04 */
#define RCC_CFGR          REG32(RCC_BASE + 0x08)   /* [CMSIS] RCC_TypeDef: CFGR at 0x08 */
#define RCC_AHB1ENR       REG32(RCC_BASE + 0x30)   /* [CMSIS] RCC_TypeDef: AHB1ENR at 0x30; bit n = GPIO port n */
#define RCC_AHB3ENR       REG32(RCC_BASE + 0x38)   /* [CMSIS] RCC_TypeDef: AHB3ENR at 0x38 */
#define RCC_APB2ENR       REG32(RCC_BASE + 0x44)   /* [CMSIS] RCC_TypeDef: APB2ENR at 0x44 */
#define RCC_AHB3ENR_FMCEN_BIT     (1UL << 0)       /* [CMSIS] RCC_AHB3ENR_FMCEN_Pos = 0 */
#define RCC_APB2ENR_USART1EN_BIT  (1UL << 4)       /* [CMSIS] RCC_APB2ENR_USART1EN_Pos = 4 */
#define RCC_CR_HSEON      (1UL << 16)              /* [CMSIS]:10521 */
#define RCC_CR_HSERDY     (1UL << 17)              /* [CMSIS]:10524 */
#define RCC_CR_HSEBYP     (1UL << 18)              /* [CMSIS]:10527 (not used: the board has an 8 MHz crystal) */
#define RCC_CR_PLLON      (1UL << 24)              /* [CMSIS]:10533 */
#define RCC_CR_PLLRDY     (1UL << 25)              /* [CMSIS]:10536 */
#define RCC_PLLCFGR_M(m)  ((uint32_t)(m) << 0)     /* [CMSIS]:10563 PLLM [5:0] */
#define RCC_PLLCFGR_N(n)  ((uint32_t)(n) << 6)     /* [CMSIS]:10573 PLLN [14:6] */
#define RCC_PLLCFGR_P(p)  ((uint32_t)(((p) / 2U) - 1U) << 16) /* [CMSIS]:10586 PLLP [17:16]; 2,4,6,8 -> 0..3 */
#define RCC_PLLCFGR_SRC_HSE (1UL << 22)            /* [CMSIS]:10592 PLLSRC */
#define RCC_PLLCFGR_Q(q)  ((uint32_t)(q) << 24)    /* [CMSIS]:10600 PLLQ [27:24] */
#define RCC_PLLCFGR_RSVD29 (1UL << 29)             /* reserved, 1 at reset ([CMSIS]:17127 RST_VALUE 0x24003010);
                                                      HAL stm32f4xx_hal_rcc_ex.h:5871 writes it as 0x20000000U */
#define RCC_CFGR_SW_MASK  (3UL << 0)               /* [CMSIS]:10611 */
#define RCC_CFGR_SW_HSI   0UL                      /* [CMSIS]:10617 */
#define RCC_CFGR_SW_PLL   2UL                      /* [CMSIS]:10619 */
#define RCC_CFGR_SWS_MASK (3UL << 2)               /* [CMSIS]:10622 */
#define RCC_CFGR_SWS_PLL  8UL                      /* [CMSIS]:10630 */

/* ---- GPIO --------------------------------------------------------------- */
#define GPIO_BASE(port)   (0x40020000UL + 0x400UL * (uint32_t)(port))  /* [CMSIS]:1112-1118 GPIOA..GPIOG */
#define GPIO_MODER(p)     REG32(GPIO_BASE(p) + 0x00)   /* [CMSIS] GPIO_TypeDef offsets 0x00..0x24 */
#define GPIO_OTYPER(p)    REG32(GPIO_BASE(p) + 0x04)
#define GPIO_OSPEEDR(p)   REG32(GPIO_BASE(p) + 0x08)
#define GPIO_PUPDR(p)     REG32(GPIO_BASE(p) + 0x0C)
#define GPIO_IDR(p)       REG32(GPIO_BASE(p) + 0x10)
#define GPIO_ODR(p)       REG32(GPIO_BASE(p) + 0x14)
#define GPIO_BSRR(p)      REG32(GPIO_BASE(p) + 0x18)
#define GPIO_AFRL(p)      REG32(GPIO_BASE(p) + 0x20)   /* AFR[0] */
#define GPIO_AFRH(p)      REG32(GPIO_BASE(p) + 0x24)   /* AFR[1] */
enum { PORTA = 0, PORTB, PORTC, PORTD, PORTE, PORTF, PORTG };
#define MODER_INPUT   0U                 /* HAL stm32f4xx_hal_gpio.h:256-258 MODE_INPUT/OUTPUT/AF */
#define MODER_OUTPUT  1U
#define MODER_AF      2U
#define OSPEED_VERY_HIGH 3U              /* HAL stm32f4xx_hal_gpio.h:144 GPIO_SPEED_FREQ_VERY_HIGH */
#define PUPD_NONE     0U
#define PUPD_PULLUP   1U
#define GPIO_AF7_USART1  7U              /* [GPIOEX]:108 */
#define GPIO_AF12_FMC    12U             /* [GPIOEX]:146 */

/* ---- USART1 (ST-LINK virtual COM port on PA9/PA10) ----------------------- */
#define USART1_BASE       0x40011000UL   /* [CMSIS]:1086 APB2PERIPH_BASE (:1048) + 0x1000 */
#define USART1_SR         REG32(USART1_BASE + 0x00)   /* [CMSIS] USART_TypeDef: SR 0x00, DR 0x04 */
#define USART1_DR         REG32(USART1_BASE + 0x04)
#define USART1_BRR        REG32(USART1_BASE + 0x08)   /* BRR 0x08, CR1 0x0C */
#define USART1_CR1        REG32(USART1_BASE + 0x0C)
#define USART_SR_RXNE     (1UL << 5)     /* [CMSIS] USART_SR_RXNE_Pos = 5 */
#define USART_SR_TXE      (1UL << 7)     /* [CMSIS] USART_SR_TXE_Pos = 7 */
#define USART_SR_ORE      (1UL << 3)     /* [CMSIS] USART_SR_ORE_Pos = 3 */
#define USART_CR1_UE      (1UL << 13)    /* [CMSIS] USART_CR1_UE_Pos = 13 */
#define USART_CR1_TE      (1UL << 3)     /* [CMSIS] USART_CR1_TE_Pos = 3 */
#define USART_CR1_RE      (1UL << 2)     /* [CMSIS] USART_CR1_RE_Pos = 2 */

/* ---- SysTick ------------------------------------------------------------ */
#define SYST_CSR          REG32(0xE000E010UL)   /* [CORE]:1550,1555 SysTick_BASE = 0xE000E000 + 0x10; CTRL */
#define SYST_RVR          REG32(0xE000E014UL)   /* LOAD */
#define SYST_CVR          REG32(0xE000E018UL)   /* VAL */
#define SYST_CSR_ENABLE_ALL 7UL                 /* [CORE]:776-783 CLKSOURCE(2) | TICKINT(1) | ENABLE(0) */

/* ---- FMC SDRAM controller (FMC_Bank5_6 at FMC base 0xA0000000 + 0x140) --- */
#define FMC_SD_BASE       0xA0000140UL   /* [CMSIS]:1160 FMC_Bank5_6_R_BASE = FMC_R_BASE (:1031) + 0x140 */
#define FMC_SDCR1         REG32(FMC_SD_BASE + 0x00)   /* [CMSIS]:561-568 FMC_Bank5_6_TypeDef: SDCR[2] */
#define FMC_SDCR2         REG32(FMC_SD_BASE + 0x04)
#define FMC_SDTR1         REG32(FMC_SD_BASE + 0x08)   /* SDTR[2] */
#define FMC_SDTR2         REG32(FMC_SD_BASE + 0x0C)
#define FMC_SDCMR         REG32(FMC_SD_BASE + 0x10)
#define FMC_SDRTR         REG32(FMC_SD_BASE + 0x14)
#define FMC_SDSR          REG32(FMC_SD_BASE + 0x18)

/* FMC_SDCRx fields ([CMSIS]:8503-8546; values as [LLFMC]:801-880) */
#define SDCR_NC_8BIT      (0UL << 0)              /* [LLFMC]:801 FMC_SDRAM_COLUMN_BITS_NUM_8 = 0x0 */
#define SDCR_NR_12BIT     (1UL << 2)              /* [LLFMC]:813 FMC_SDRAM_ROW_BITS_NUM_12 = 0x4 */
#define SDCR_MWID_16      (1UL << 4)              /* [LLFMC]:823 FMC_SDRAM_MEM_BUS_WIDTH_16 = 0x10 */
#define SDCR_NB_4BANKS    (1UL << 6)              /* [LLFMC]:833 FMC_SDRAM_INTERN_BANKS_NUM_4 = 0x40 */
#define SDCR_CAS(n)       ((uint32_t)(n) << 7)    /* [LLFMC]:842-843 CAS 2 = 0x100, CAS 3 = 0x180 */
#define SDCR_WP           (1UL << 9)              /* [CMSIS]:8531 write protection (left at 0) */
#define SDCR_SDCLK_DIV2   (2UL << 10)             /* [LLFMC]:861 FMC_SDRAM_CLOCK_PERIOD_2 = 0x800 */
#define SDCR_SDCLK_DIV3   (3UL << 10)             /* [LLFMC]:862 FMC_SDRAM_CLOCK_PERIOD_3 = 0xC00 */
#define SDCR_SDCLK_MASK   (3UL << 10)             /* [CMSIS]:8535-8536 */
#define SDCR_RBURST       (1UL << 12)             /* [CMSIS]:8541; 0 = [LLFMC]:870 RBURST_DISABLE */
#define SDCR_RPIPE(n)     ((uint32_t)(n) << 13)   /* [LLFMC]:880 FMC_SDRAM_RPIPE_DELAY_1 = 0x2000 */
#define SDCR_RPIPE_MASK   (3UL << 13)             /* [CMSIS]:8545-8546 */
/* FMC_SDTRx fields, each written as (cycles - 1): TMRD [3:0], TXSR [7:4], TRAS [11:8], TRC [15:12],
 * TWR [19:16], TRP [23:20], TRCD [27:24] ([CMSIS]:8601-8647; packing as HAL stm32f4xx_ll_fmc.c:1259-1266) */
#define SDTR(tmrd, txsr, tras, trc, twr, trp, trcd) \
    ((uint32_t)((tmrd) - 1) | ((uint32_t)((txsr) - 1) << 4) | ((uint32_t)((tras) - 1) << 8) | \
     ((uint32_t)((trc) - 1) << 12) | ((uint32_t)((twr) - 1) << 16) | ((uint32_t)((trp) - 1) << 20) | \
     ((uint32_t)((trcd) - 1) << 24))
#define SDTR_TRC_POS      12U
#define SDTR_TRP_POS      20U
#define SDTR_TRC_MASK     (0xFUL << SDTR_TRC_POS)
#define SDTR_TRP_MASK     (0xFUL << SDTR_TRP_POS)
/* FMC_SDCMR fields ([CMSIS]:8707-8731; modes as [LLFMC]:889-895, target as [LLFMC]:903-904) */
#define SDCMR_MODE_MASK       7UL
#define SDCMR_MODE_NORMAL     0UL
#define SDCMR_MODE_CLK_EN     1UL
#define SDCMR_MODE_PALL       2UL
#define SDCMR_MODE_AUTOREF    3UL
#define SDCMR_MODE_LOADMODE   4UL
#define SDCMR_MODE_SELFREF    5UL   /* the SDRAM refreshes ITSELF: useless for a retention test */
#define SDCMR_MODE_POWERDOWN  6UL   /* FMC behaviour around refresh not confirmed: not used */
#define SDCMR_CTB2            (1UL << 3)    /* FMC_SDRAM_CMD_TARGET_BANK2 = FMC_SDCMR_CTB2 */
#define SDCMR_CTB1            (1UL << 4)
#define SDCMR_NRFS(n)         ((uint32_t)((n) - 1) << 5)   /* 1..15 ([LLFMC]:165) */
#define SDCMR_MRD(v)          ((uint32_t)(v) << 9)         /* 13 bits ([LLFMC]:166) */
/* FMC_SDRTR fields ([CMSIS]:8735-8744): CRE bit 0, COUNT [13:1], REIE bit 14.
 * COUNT is 13 bits (HAL accepts 0..8191: [LLFMC]:167). RM0090 asks for COUNT >= 41 [REPORTED, search
 * snippet; the RM text itself was not reachable]. */
#define SDRTR_CRE             (1UL << 0)
#define SDRTR_COUNT(n)        ((uint32_t)(n) << 1)
#define SDRTR_COUNT_FIELD(r)  (((r) >> 1) & 0x1FFFUL)
#define SDRTR_COUNT_MAX       8191U
#define SDRTR_COUNT_MIN       41U
/* FMC_SDSR ([CMSIS]:8748-8764): RE bit 0, MODES1 [2:1], MODES2 [4:3], BUSY bit 5 */
#define SDSR_MODES2_MASK      (3UL << 3)
#define SDSR_BUSY             (1UL << 5)

/* SDRAM bank 2 (SDNE1/SDCKE1) is mapped at 0xD0000000: [BSP] .h:63 SDRAM_DEVICE_ADDR, 8 MB (.h:64) */
#define SDRAM_BANK2_BASE      0xD0000000UL

#endif /* REGS_F429_H */
