"""
This program performs polynomial multiplication. The default irreducible
polynomial is the AES irreducible. Polynomials are represented by a
binary string.
"""
def mul(a, b):
    p = 0b100011011  # AES irreducible
    res = 0b0
    while b != 0b0:
        if b&0b1 == 0b1:
            res ^= a  # Add (XOR) with a if b is odd
        b >>= 1  # Half
        a <<= 1  # Double
        if a > 0xff:
            a ^= p  # Mod by P(x)
    return res


if __name__ == "__main__":
    # print("{0:02x}".format(mul(0x1e, 0x37)))
    
    # print("{0:02x}".format(mul(0x0E, 0x47) ^ mul(0x0B, 0x37) ^ mul(0x0D, 0x94) ^ mul(0x09, 0xED)))
    # print("{0:02x}".format(mul(0x09, 0x47) ^ mul(0x0E, 0x37) ^ mul(0x0B, 0x94) ^ mul(0x0D, 0xED)))
    # print("{0:02x}".format(mul(0x0D, 0x47) ^ mul(0x09, 0x37) ^ mul(0x0E, 0x94) ^ mul(0x0B, 0xED)))
    # print("{0:02x}".format(mul(0x0B, 0x47) ^ mul(0x0D, 0x37) ^ mul(0x09, 0x94) ^ mul(0x0E, 0xED)))

    # print("{0:02x}".format(mul(0x0E, 0xFF) ^ mul(0x0B, 0x94) ^ mul(0x0D, 0x9C) ^ mul(0x09, 0x6E)))
    # print("{0:02x}".format(mul(0x09, 0xFF) ^ mul(0x0E, 0x94) ^ mul(0x0B, 0x9C) ^ mul(0x0D, 0x6E)))
    # print("{0:02x}".format(mul(0x0D, 0xFF) ^ mul(0x09, 0x94) ^ mul(0x0E, 0x9C) ^ mul(0x0B, 0x6E)))
    # print("{0:02x}".format(mul(0x0B, 0xFF) ^ mul(0x0D, 0x94) ^ mul(0x09, 0x9C) ^ mul(0x0E, 0x6E)))
    
    print("{0:02x}".format(mul(0xDD, 0xF9)))
