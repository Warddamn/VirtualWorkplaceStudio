# E6 retention firmware -- REFERENCE CODE, UNTESTED ON HARDWARE.
# Builds and links with arm-none-eabi-gcc 13.2.1 (Ubuntu 24.04 package gcc-arm-none-eabi 15:13.2.rel1-2).
#
# make          build e6_retention.elf/.bin and print the flash/RAM use (needs arm-none-eabi-gcc)
# make CROSS=/path/to/bin/arm-none-eabi-   use a toolchain that is not on PATH
# make flash    write it with st-flash (open-source stlink tools); STM32CubeProgrammer also works
# make syntax   host gcc -fsyntax-only check (no ARM toolchain needed)
# make hosttest compile and run the pattern generator on the PC
# make emu      build e6_emu.elf for QEMU's netduinoplus2 (STM32F405: 128 KB RAM, no FMC); see guide 16
CROSS   ?= arm-none-eabi-
CC      = $(CROSS)gcc
OBJCOPY = $(CROSS)objcopy
SIZE    = $(CROSS)size
# -fno-tree-loop-distribute-patterns stops GCC turning the startup copy/zero loops into memcpy/memset
# calls, which -nostdlib would leave undefined (a link error you could not debug on day one).
CFLAGS  = -mcpu=cortex-m4 -mthumb -mfloat-abi=soft -O2 -std=c11 -Wall -Wextra -ffreestanding \
          -ffunction-sections -fdata-sections -fno-tree-loop-distribute-patterns
LDFLAGS = -nostdlib -nostartfiles -Wl,--gc-sections
SRCS    = startup_f429.c main.c sdram_fmc.c patterns.c uart.c max31855.c

all: e6_retention.bin

e6_retention.elf: $(SRCS) *.h stm32f429_flash.ld
	$(CC) $(CFLAGS) $(SRCS) -T stm32f429_flash.ld $(LDFLAGS) -Wl,-Map=e6_retention.map -lgcc -o $@
	$(SIZE) $@

e6_retention.bin: e6_retention.elf
	$(OBJCOPY) -O binary $< $@

flash: e6_retention.bin
	st-flash --reset write e6_retention.bin 0x08000000

# Emulator build: same code, RAM shrunk to the F405's 128 KB, and -DE6_EMU so main() skips the SDRAM
# (QEMU has no FMC) and says so. Never flash this one.
e6_emu.elf: $(SRCS) *.h stm32f429_flash.ld
	sed 's/LENGTH = 192K/LENGTH = 128K/' stm32f429_flash.ld > e6_emu.ld
	$(CC) $(CFLAGS) -DE6_EMU $(SRCS) -T e6_emu.ld $(LDFLAGS) -lgcc -o $@

emu: e6_emu.elf

syntax:
	gcc -fsyntax-only -std=c11 -Wall -Wextra $(SRCS)
	gcc -fsyntax-only -std=c11 -Wall -Wextra -DENABLE_METHOD_Z $(SRCS)

hosttest:
	gcc -std=c11 -Wall -Wextra -o host_test_patterns host_test_patterns.c patterns.c && ./host_test_patterns | head -5

clean:
	rm -f e6_retention.elf e6_retention.bin e6_retention.map e6_emu.elf e6_emu.ld host_test_patterns

.PHONY: all flash emu syntax hosttest clean
