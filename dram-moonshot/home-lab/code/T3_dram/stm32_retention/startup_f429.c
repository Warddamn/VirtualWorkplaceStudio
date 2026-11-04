/*
 * startup_f429.c -- minimal Cortex-M4 vector table and reset handler.
 * REFERENCE CODE, UNTESTED ON HARDWARE (boots in QEMU; see the guide, section 16).
 * Only the 16 core vectors are filled: the firmware enables no peripheral interrupt.
 * The order (initial SP, Reset, NMI, HardFault, MemManage, BusFault, UsageFault, 4 reserved, SVC,
 * DebugMon, reserved, PendSV, SysTick) matches ST's startup file, cmsis-device-f4 @ 9192c7b9df75
 * Source/Templates/gcc/startup_stm32f429xx.s:126-143. Like ST's file, the reset handler copies .data
 * from flash and zeroes .bss; it does not call SystemInit, so the core starts on the 16 MHz HSI
 * (system_stm32f4xx.c:137, SystemCoreClock = 16000000) until main() switches to the crystal.
 */
#include <stdint.h>

extern uint32_t _sidata, _sdata, _edata, _sbss, _ebss, _estack;
int main(void);

void Reset_Handler(void);
void Default_Handler(void);
void NMI_Handler(void) __attribute__((weak, alias("Default_Handler")));
void HardFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void MemManage_Handler(void) __attribute__((weak, alias("Default_Handler")));
void BusFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void UsageFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void SVC_Handler(void) __attribute__((weak, alias("Default_Handler")));
void DebugMon_Handler(void) __attribute__((weak, alias("Default_Handler")));
void PendSV_Handler(void) __attribute__((weak, alias("Default_Handler")));
void SysTick_Handler(void) __attribute__((weak, alias("Default_Handler")));

typedef void (*vector_t)(void);

__attribute__((section(".isr_vector"), used))
const vector_t g_vectors[16] = {
    (vector_t)(uintptr_t)&_estack,
    Reset_Handler, NMI_Handler, HardFault_Handler, MemManage_Handler, BusFault_Handler,
    UsageFault_Handler, 0, 0, 0, 0, SVC_Handler, DebugMon_Handler, 0, PendSV_Handler,
    SysTick_Handler,
};

void Default_Handler(void)
{
    for (;;) {
    }
}

void Reset_Handler(void)
{
    uint32_t *src = &_sidata;
    for (uint32_t *dst = &_sdata; dst < &_edata;) {
        *dst++ = *src++;
    }
    for (uint32_t *dst = &_sbss; dst < &_ebss;) {
        *dst++ = 0U;
    }
    (void)main();
    for (;;) {
    }
}
