/*
 * uart.c -- REFERENCE CODE, UNTESTED ON HARDWARE.
 * USART1 on PA9/PA10 (AF7) reaches the PC through the ST-LINK virtual COM port on the
 * STM32F429I-DISC1 when solder bridges SB11/SB15 are closed (the reported default).
 * Older boards without the VCP: wire a 3.3 V USB-UART adapter to PA9/PA10 instead.
 */
#include "regs_f429.h"
#include "uart.h"

#define PCLK2_HZ 16000000UL   /* APB2 = HCLK = HSI 16 MHz after reset */

void uart_init(uint32_t baud)
{
    RCC_AHB1ENR |= (1UL << PORTA);
    RCC_APB2ENR |= (1UL << 4);                          /* USART1EN */
    (void)RCC_APB2ENR;
    for (uint32_t pin = 9U; pin <= 10U; pin++) {
        uint32_t sh2 = pin * 2U;
        GPIO_MODER(PORTA) = (GPIO_MODER(PORTA) & ~(3UL << sh2)) | (MODER_AF << sh2);
        GPIO_AFRH(PORTA) = (GPIO_AFRH(PORTA) & ~(0xFUL << ((pin - 8U) * 4U))) | (7UL << ((pin - 8U) * 4U));
        GPIO_PUPDR(PORTA) = (GPIO_PUPDR(PORTA) & ~(3UL << sh2)) | (1UL << sh2);   /* pull-up */
    }
    /* oversampling by 16: BRR = PCLK / baud (mantissa.fraction in 12.4 format) */
    USART1_BRR = (PCLK2_HZ + baud / 2U) / baud;
    USART1_CR1 = USART_CR1_UE | USART_CR1_TE | USART_CR1_RE;
}

void uart_putc(char c)
{
    while ((USART1_SR & USART_SR_TXE) == 0U) {
    }
    USART1_DR = (uint32_t)(uint8_t)c;
}

void uart_puts(const char *s)
{
    while (*s) {
        uart_putc(*s++);
    }
}

void uart_put_u32(uint32_t v)
{
    char buf[11];
    int i = 10;
    buf[i] = '\0';
    do {
        buf[--i] = (char)('0' + (v % 10U));
        v /= 10U;
    } while (v && i > 0);
    uart_puts(&buf[i]);
}

void uart_put_hex(uint32_t v, unsigned min_digits)
{
    static const char hex[] = "0123456789abcdef";
    char buf[9];
    int i = 8;
    buf[i] = '\0';
    do {
        buf[--i] = hex[v & 0xFU];
        v >>= 4;
        if (min_digits) {
            min_digits--;
        }
    } while ((v || min_digits) && i > 0);
    uart_puts(&buf[i]);
}

void uart_put_fixed(int32_t v, unsigned decimals)
{
    uint32_t scale = 1U;
    for (unsigned i = 0; i < decimals; i++) {
        scale *= 10U;
    }
    if (v < 0) {
        uart_putc('-');
        v = -v;
    }
    uart_put_u32((uint32_t)v / scale);
    if (decimals) {
        uint32_t frac = (uint32_t)v % scale;
        uart_putc('.');
        for (uint32_t d = scale / 10U; d > 0U; d /= 10U) {
            uart_putc((char)('0' + (frac / d) % 10U));
        }
    }
}

uint32_t uart_getline(char *buf, uint32_t max_len)
{
    uint32_t n = 0;
    for (;;) {
        if (USART1_SR & USART_SR_ORE) {
            (void)USART1_DR;                            /* clear overrun */
        }
        if ((USART1_SR & USART_SR_RXNE) == 0U) {
            continue;
        }
        char c = (char)(USART1_DR & 0xFFU);
        if (c == '\r' || c == '\n') {
            if (n == 0U) {
                continue;
            }
            buf[n] = '\0';
            return n;
        }
        if (n + 1U < max_len) {
            buf[n++] = c;
        }
    }
}
