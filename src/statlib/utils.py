import math
import struct
import numpy as np


def C(n, k):
    return math.factorial(n) / (math.factorial(n - k) * math.factorial(k))


def build_sample(gen, n):
    return np.array([gen.next() for _ in range(n)], dtype=np.float64)


def binary(num):
    bits = []
    for c in struct.pack('!f', num):
        bits.append(bin(c).replace('0b', '').rjust(8, '0'))

    return ''.join(bits)
