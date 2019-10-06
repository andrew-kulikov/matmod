import random


class BasicRand:
    def __init__(self, gen):
        self.gen = gen

    def next(self):
        return self.gen.next() / self.max_val()

    def max_val(self):
        return self.engine.max_val()

    def reseed(self, seed):
        self.engine.reseed(seed)
