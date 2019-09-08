import random
from statlib.rand.engine import RandEngine

RAND_MIN = 0
RAND_MAX = 0xffffffffffffffff


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
        
    def maxDecimals(self):
        return getDecimals(self.engine.MaxValue())

    def maxValue(self):
        return self.engine.MaxValue()

    def reseed(self, seed: int):
        self.engine.Reseed(seed)
