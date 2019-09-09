import random
from statlib.rand.engine import RandEngine


class BasicRand:
    def __init__(self, engine: RandEngine):
        self.engine = engine

    def getDecimals(value: int):
        num = 0
        maxRand = value

        while maxRand:
            num += 1
            maxRand >>= 1

        return num

    def next(self):
        return self.engine.Next()

    def max_decimals(self):
        return getDecimals(self.engine.MaxValue())

    def max_val(self):
        return self.engine.MaxValue()

    def reseed(self, seed: int):
        self.engine.Reseed(seed)
