/* stm32f429_flash.ld -- REFERENCE, UNTESTED ON HARDWARE (links with GNU ld 2.42).
 * 2 MB flash at 0x08000000 and 192 KB of contiguous SRAM1-3 at 0x20000000: cmsis-device-f4 @ 9192c7b9df75
 * Include/stm32f429xx.h:1024-1037 (FLASH_BASE, SRAM1 112 KB, SRAM2 16 KB, SRAM3 64 KB, FLASH_END), and
 * ST's own linker script for this board, STM32CubeF4 @ 60c8abe0ae88 Projects/STM32F429I-Discovery/
 * Examples/FMC/FMC_SDRAM/STM32CubeIDE/STM32F429ZITX_FLASH.ld:40,49-50 (RAM 192K, ROM 2048K).
 * The 64 KB CCM RAM at 0x10000000 is not used. */
ENTRY(Reset_Handler)
MEMORY
{
  FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 2048K
  RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 192K
}
_estack = ORIGIN(RAM) + LENGTH(RAM);
SECTIONS
{
  .isr_vector : { KEEP(*(.isr_vector)) } > FLASH
  .text : { *(.text*) *(.rodata*) . = ALIGN(4); } > FLASH
  _sidata = LOADADDR(.data);
  .data : { . = ALIGN(4); _sdata = .; *(.data*) . = ALIGN(4); _edata = .; } > RAM AT > FLASH
  .bss (NOLOAD) : { . = ALIGN(4); _sbss = .; *(.bss*) *(COMMON) . = ALIGN(4); _ebss = .; } > RAM AT> RAM
}
