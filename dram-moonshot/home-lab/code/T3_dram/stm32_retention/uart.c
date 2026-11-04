/*
 * uart.c -- REFERENCE CODE, UNTESTED ON HARDWARE.
 * USART1 on PA9 (TX) / PA10 (RX), alternate function 7, 115200 8N1, polled.
 *
 * Checked on 2026-11-04 against:
 *   - ST's UART example for this board, STM32CubeF4 @ 60c8abe0ae88
 *     Projects/STM32F429I-Discovery/Examples/UART/UART_TwoBoards_ComPolling/Inc/main.h:32-46
 *     (USART1, TX = PA9, RX = PA10, GPIO_AF7_USART1);
 *   - stm32f4xx_hal_driver @ 1f6451c3e077 Inc/stm32f4xx_hal_gpio_ex.h:108 (GPIO_AF7_USART1 = 7) and
 *     Inc/stm32f4xx_hal_uart.h:860-868 (UART_BRR_SAMPLING16, which gives the same BRR as below:
 *     0x8B for 115200 and 0x20 for 500000 at 16 MHz);
 *   - Zephyr @ decee24b4fbc boards/st/stm32f429i_disc1: the console is USART1 on PA9/PA10 at 115200 8N1
 *     (stm32f429i_disc1.dts:19,146-147; doc/index.rst:84-85,109-110), seen on the PC as /dev/ttyACM0
 *     through the ST-LINK/V2-B (doc/index.rst:124,158).
 * On the DISC1 the ST-LINK routes its virtual COM port to PA9/PA10 through solder bridges SB11/SB15
 * [REPORTED, ST community; UM1670 itself not reachable]. Older boards without the VCP: wire a 3.3 V
 * USB-UART adapter to PA9/PA10 instead.
 */
#include "regs_f429.h"
#include "uart.h"

#define PCLK2_HZ 16000000UL   /* APB2 = HCLK = 16 MHz on both clock paths of main.c (APB2 prescaler 1) */

static volatile int s_ready;

int uart_ready(void) { return s_ready; }

void uart_init(uint32_t baud)
{
    RCC_AHB1ENR |= (1UL << PORTA);
    (void)RCC_AHB1ENR;
    RCC_APB2ENR |= RCC_APB2ENR_USART1EN_BIT;
    (void)RCC_APB2ENR;
    for (uint32_t pin = 9U; pin <= 10U; pin++) {
        uint32_t sh2 = pin * 2U;
        GPIO_MODER(PORTA) = (GPIO_MODER(PORTA) & ~(3UL << sh2)) | (MODER_AF << sh2);
        GPIO_AFRH(PORTA) = (GPIO_AFRH(PORTA) & ~(0xFUL << ((pin - 8U) * 4U))) |
                           (GPIO_AF7_USART1 << ((pin - 8U) * 4U));
        /* pull-up (ST's example uses none): keeps RX idle-high if no VCP or adapter is connected */
        GPIO_PUPDR(PORTA) = (GPIO_PUPDR(PORTA) & ~(3UL << sh2)) | (PUPD_PULLUP << sh2);
    }
    /* oversampling by 16: BRR = PCLK / baud (mantissa.fraction in 12.4 format) */
    USART1_BRR = (PCLK2_HZ + baud / 2U) / baud;
    USART1_CR1 = USART_CR1_UE | USART_CR1_TE | USART_CR1_RE;
    s_ready = 1;
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
