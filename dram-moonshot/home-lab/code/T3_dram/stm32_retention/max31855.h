/* max31855.h -- optional K-type thermocouple reader (bit-banged SPI). REFERENCE CODE, UNTESTED ON HARDWARE. */
#ifndef MAX31855_H
#define MAX31855_H
#include <stdint.h>
#define TEMP_INVALID ((int32_t)0x80000000)
void    thermo_init(void);
int32_t thermo_read_c_x100(void);   /* degrees C x 100, or TEMP_INVALID (fault / not fitted) */
#endif
