import math

from statlib.rand import basic_rand

# TODO: try to generate normal
class Cauchy:
    def __init__(self, generator):
        self.uniform = Uniform(generator)

    def next(self, x0: float, gamma: float):
        x, y = 0, 0
        while True:
            x = self.uniform.next(-1, 1)
            y = self.uniform.next(-1, 1)
            if x ** 2 + y ** 2 <= 1.0 or y == 0.0:
                break

        return x0 + gamma * x / y

