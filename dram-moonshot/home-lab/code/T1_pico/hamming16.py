# hamming16.py -- extended Hamming (16,11) SECDED code for the 4x4 bench DRAM array (E1).
# REFERENCE CODE - UNTESTED ON HARDWARE. Pure Python: runs on MicroPython (Pico / Pico 2) and on a PC.
#
# Why: this is the FASTEST PROOF concept (raw-ber-contract) in miniature. With one-error correction
# per 16-cell word you may refresh at the retention of the SECOND-weakest cell instead of the weakest.
#
# Layout: bit 0 = overall parity; bits 1, 2, 4, 8 = Hamming parity; the other 11 positions carry data.
# Cell (row r, col c) of the 4x4 array stores codeword bit 4*r + c.

DATA_POS = (3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15)
PARITY_POS = (1, 2, 4, 8)

OK = 0            # no error
CORRECTED = 1     # one error fixed
DETECTED = 2      # two errors detected, data not trustworthy


def encode(data11):
    """11-bit integer -> list of 16 bits."""
    bits = [0] * 16
    for i, pos in enumerate(DATA_POS):
        bits[pos] = (data11 >> i) & 1
    for p in PARITY_POS:
        x = 0
        for pos in range(1, 16):
            if pos & p and pos != p:
                x ^= bits[pos]
        bits[p] = x
    overall = 0
    for pos in range(1, 16):
        overall ^= bits[pos]
    bits[0] = overall
    return bits


def decode(bits16):
    """list of 16 bits -> (data11, status, corrected_position or -1)."""
    bits = list(bits16)
    syndrome = 0
    for pos in range(1, 16):
        if bits[pos]:
            syndrome ^= pos
    parity = 0
    for pos in range(16):
        parity ^= bits[pos]
    status = OK
    fixed = -1
    if syndrome == 0 and parity == 0:
        status = OK
    elif parity == 1:
        # odd number of flips: assume one; syndrome 0 means the overall parity bit itself flipped
        fixed = syndrome
        bits[fixed] ^= 1
        status = CORRECTED
    else:
        status = DETECTED
    data = 0
    for i, pos in enumerate(DATA_POS):
        data |= bits[pos] << i
    return data, status, fixed


def self_check():
    """Exhaustive check of all single and double errors for a few data words. Returns True on pass."""
    for data in (0, 0x7FF, 0x555, 0x2AA, 0x123):
        cw = encode(data)
        d, s, _ = decode(cw)
        if d != data or s != OK:
            return False
        for i in range(16):
            e = list(cw)
            e[i] ^= 1
            d, s, pos = decode(e)
            if d != data or s != CORRECTED or pos != i:
                return False
            for j in range(i + 1, 16):
                e2 = list(e)
                e2[j] ^= 1
                d, s, _ = decode(e2)
                if s != DETECTED:
                    return False
    return True


if __name__ == "__main__":
    print("hamming16 self-check:", "PASS" if self_check() else "FAIL")
