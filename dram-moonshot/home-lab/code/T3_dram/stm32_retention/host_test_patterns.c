/*
 * host_test_patterns.c -- runs on a PC. Prints "pattern inv seed word value" lines that
 * retention_map.py --selftest compares with its own pattern_words().
 * Build: gcc -std=c11 -Wall -Wextra -o host_test_patterns host_test_patterns.c patterns.c
 */
#include <stdio.h>
#include "patterns.h"

int main(void)
{
    static const uint32_t words[] = {0U, 1U, 2U, 255U, 256U, 257U, 4095U, 65536U, 1048575U,
                                     1048576U, 2097151U, 3000001U, 4194303U};
    static const uint32_t seeds[] = {0U, 1U, 1234U, 0xFFFFFFFFU};
    for (uint32_t p = 0; p <= 5U; p++) {
        for (uint32_t inv = 0; inv <= 1U; inv++) {
            for (unsigned s = 0; s < sizeof seeds / sizeof seeds[0]; s++) {
                for (unsigned i = 0; i < sizeof words / sizeof words[0]; i++) {
                    printf("%u %u %u %u 0x%04x\n", (unsigned)p, (unsigned)inv, (unsigned)seeds[s],
                           (unsigned)words[i], (unsigned)pattern_word(p, inv, seeds[s], words[i]));
                }
            }
        }
    }
    return 0;
}
