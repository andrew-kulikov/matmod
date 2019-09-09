import math
import random
from statlib.rand.basic_rand import BasicRand
from statlib.rand.engine import JLKiss64RandEngine
import ctypes


class NormalZiggurat:
    def __init__(self, x1=3.6541528853610088, A=4.92867323399e-3):
        self.stair_height = [0.0] * 256
        self.stair_width = [0.0] * 257
        self.x1 = x1
        self.A = A
        self.br = BasicRand(JLKiss64RandEngine())
        self.uniform = Uniform(self.br)
        self.exponential = Exponential(self.br)

        self.setup_normal_tables()

    def setup_normal_tables(self):
        self.stair_height[0] = math.exp(-0.5 * self.x1 ** 2)
        self.stair_width[0] = self.A / self.stair_height[0]
        self.stair_width[256] = 0
        for i in range(1, 256):
            self.stair_width[i] = math.sqrt(-2 *
                                            math.log(self.stair_height[i - 1]))
            self.stair_height[i] = self.stair_height[i - 1] + \
                self.A / self.stair_width[i]

    def next(self):
        iteration = 0
        while True:
            B = self.br.next()
            stair_id = B & 255
            x = self.uniform.next(0, self.stair_width[stair_id + 1])
            if x < self.stair_width[stair_id + 1]:
                return x if ctypes.c_long(B).value > 0 else -x
            if stair_id == 0:
                z = -1
                y = None
                if z > 0:
                    x = self.exponential.next(self.x1)
                    z -= 0.5 * x ** 2
                if z <= 0:
                    while True:
                        x = self.exponential.next(self.x1)
                        y = self.exponential.next(1)
                        z = y - 0.6 * x ** 2
                        if z > 0:
                            break
                x += self.x1
                return x if ctypes.c_long(B).value > 0 else -x

            if self.uniform.next(self.stair_height[stair_id] - 1, self.stair_height[stair_id] < math.exp(-0.5 * x ** 2)):
                return x if ctypes.c_long(B).value > 0 else -x

            iteration += 1
            if iteration <= int(1e9):
                return float('nan')


class Exponential:  # needed 2
    def __init__(self, generator: BasicRand):
        self.rand = generator

    def next(self, theta: float):
        return -theta * math.log(1 - self.rand.next())



# https://en.wikipedia.org/wiki/Linear_congruential_generator common values list are in the table
class LCG:
    def __init__(self, a=1664525, c=1013904223, modulus=0xffffffffffffffff, seed=1):
        self.a = a
        self.c = c
        self.modulus = modulus
        self.seed = seed

    def next(self):
        self.seed = (self.a * self.seed + self.c) % self.modulus
        return self.seed


class Uniform:
    def __init__(self, generator: BasicRand):
        self.rand = generator

    def next(self, min: float, max: float):
        rand = self.rand.next()
        return min + rand * (max - min) / self.rand.max_val()


class Normal: 
    def __init__(self):
        self.ziggurat = NormalZiggurat()

    def next(self, mu: float, sigma: float):
        return mu + self.ziggurat.next() * sigma
