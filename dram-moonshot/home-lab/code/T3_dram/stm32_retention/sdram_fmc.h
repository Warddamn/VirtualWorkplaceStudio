/*
 * sdram_fmc.h -- FMC SDRAM control for the STM32F429I-DISC1 (IS42S16400J on FMC bank 2).
 * REFERENCE CODE, UNTESTED ON HARDWARE.
 */
#ifndef SDRAM_FMC_H
#define SDRAM_FMC_H

#include <stdint.h>

#define SDRAM_ROWS_PER_BANK  4096U     /* 4K refresh cycles per 64 ms (datasheet; BSP "15.62 us" = 64 ms / 4096) */
#define SDRAM_N_WORDS        4194304UL /* 4 banks x 4096 rows x 256 columns x 16 bit = 8 MB (BSP: 0x800000 bytes) */

/* Provided by main.c: busy-wait on the 1 ms SysTick counter. */
void     delay_ms(uint32_t ms);

int      sdram_init(uint32_t sdclk_div);           /* 2 or 3; returns 0 on success, <0 = failed step */
uint32_t sdram_sdclk_hz(void);
uint32_t sdram_count_for_period_ms(uint32_t period_ms);
uint32_t sdram_period_us_for_count(uint32_t count);
uint32_t sdram_normal_count(void);
int      sdram_set_refresh_count(uint32_t count);  /* clamps to 41..8191 unless count == 0 (method Z);
                                                      returns -1 if the register does not read back */
int      sdram_precharge_all(void);
int      sdram_deselect(int on);                   /* 1: hold SDNE1 (chip select) high = no commands;
                                                      returns -1 if the pin is not in the wanted state */
int      sdram_selftest(uint32_t *bad_word, uint32_t *expected, uint32_t *observed);
                                                   /* data-bus and address-bus test; 0 = pass. Destroys data */

#endif
