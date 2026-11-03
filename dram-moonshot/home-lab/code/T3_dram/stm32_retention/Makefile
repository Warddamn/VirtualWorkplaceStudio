# E6 retention firmware -- REFERENCE CODE, UNTESTED ON HARDWARE.
# make          build e6_retention.elf/.bin (needs arm-none-eabi-gcc)
# make flash    write it with st-flash (open-source stlink tools); STM32CubeProgrammer also works
# make syntax   host gcc -fsyntax-only check (no ARM toolchain needed)
# make hosttest compile and run the pattern generator on the PC
CC      = arm-none-eabi-gcc
OBJCOPY = arm-none-eabi-objcopy
# -fno-tree-loop-distribute-patterns stops GCC turning the startup copy/zero loops into memcpy/memset
# calls, which -nostdlib would leave undefined (a link error you could not debug on day one).
CFLAGS  = -mcpu=cortex-m4 -mthumb -O2 -std=c11 -Wall -Wextra -ffreestanding -ffunction-sections -fno-tree-loop-distribute-patterns
LDFLAGS = -T stm32f429_flash.ld -nostdlib -nostartfiles -Wl,--gc-sections
SRCS    = startup_f429.c main.c sdram_fmc.c patterns.c uart.c max31855.c

all: e6_retention.bin

e6_retention.elf: $(SRCS) *.h stm32f429_flash.ld
	$(CC) $(CFLAGS) $(SRCS) $(LDFLAGS) -lgcc -o $@

e6_retention.bin: e6_retention.elf
	$(OBJCOPY) -O binary $< $@

flash: e6_retention.bin
	st-flash write e6_retention.bin 0x08000000

syntax:
	gcc -fsyntax-only -std=c11 -Wall -Wextra $(SRCS)
	gcc -fsyntax-only -std=c11 -Wall -Wextra -DENABLE_METHOD_Z $(SRCS)

hosttest:
	gcc -std=c11 -Wall -Wextra -o host_test_patterns host_test_patterns.c patterns.c && ./host_test_patterns | head -5

clean:
	rm -f e6_retention.elf e6_retention.bin host_test_patterns

.PHONY: all flash syntax hosttest clean
