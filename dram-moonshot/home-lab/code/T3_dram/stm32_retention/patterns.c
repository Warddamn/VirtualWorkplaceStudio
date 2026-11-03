/*
 * patterns.c -- REFERENCE CODE, UNTESTED ON HARDWARE (host-tested against retention_map.py).
 */
#include "patterns.h"

/* lowbias32 integer hash (public-domain construction by C. Wellons) */
uint32_t mix32(uint32_t x)
{
    x ^= x >> 16;
    x *= 0x7FEB352DU;
    x ^= x >> 15;
    x *= 0x846CA68BU;
    x ^= x >> 16;
    return x;
}

uint16_t pattern_word(uint32_t pattern, uint32_t inv, uint32_t seed, uint32_t w)
{
    uint32_t row = w / WORDS_PER_ROW;
    uint32_t col = w % WORDS_PER_ROW;
    uint32_t v;
    switch (pattern) {
    case PAT_ALL0:      v = 0x0000U; break;
    case PAT_ALL1:      v = 0xFFFFU; break;
    case PAT_CHECKER:   v = ((row ^ col) & 1U) ? 0xAAAAU : 0x5555U; break;
    case PAT_ROWSTRIPE: v = (row & 1U) ? 0xFFFFU : 0x0000U; break;
    case PAT_COLSTRIPE: v = (col & 1U) ? 0xFFFFU : 0x0000U; break;
    case PAT_RANDOM:    v = mix32(w ^ mix32(seed + 0x9E3779B9U)) & 0xFFFFU; break;
    default:            v = 0x0000U; break;
    }
    if (inv) {
        v ^= 0xFFFFU;
    }
    return (uint16_t)v;
}
