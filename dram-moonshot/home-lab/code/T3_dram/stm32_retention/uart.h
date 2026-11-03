/* uart.h -- USART1 on PA9 (TX) / PA10 (RX), polled. REFERENCE CODE, UNTESTED ON HARDWARE. */
#ifndef UART_H
#define UART_H
#include <stdint.h>
void     uart_init(uint32_t baud);
void     uart_putc(char c);
void     uart_puts(const char *s);
void     uart_put_u32(uint32_t v);
void     uart_put_hex(uint32_t v, unsigned min_digits);
void     uart_put_fixed(int32_t v, unsigned decimals);   /* v = value x 10^decimals */
uint32_t uart_getline(char *buf, uint32_t max_len);       /* blocking; strips CR/LF */
#endif
