/*
 * patterns.h -- data patterns for the E6 retention test.
 * REFERENCE CODE, UNTESTED ON HARDWARE (pure C; host-tested by host_test_patterns.c).
 * Must match pattern_words() in ../retention_map.py bit for bit.
 */
#ifndef PATTERNS_H
#define PATTERNS_H

#include <stdint.h>

#define WORDS_PER_ROW 256U   /* IS42S16400J: 8 column bits -> 256 x 16-bit words per row */

enum {
    PAT_ALL0 = 0,       /* every bit 0 */
    PAT_ALL1 = 1,       /* every bit 1 */
    PAT_CHECKER = 2,    /* 0x5555 / 0xAAAA, flips every word and every row */
    PAT_ROWSTRIPE = 3,  /* rows alternate 0x0000 / 0xFFFF */
    PAT_COLSTRIPE = 4,  /* columns alternate 0x0000 / 0xFFFF */
    PAT_RANDOM = 5      /* hash(seed, word index): regenerated at read-back, nothing stored */
};

uint32_t mix32(uint32_t x);
uint16_t pattern_word(uint32_t pattern, uint32_t inv, uint32_t seed, uint32_t word_index);

#endif
