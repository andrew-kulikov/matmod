import math

import basic_rand

from ziggurat import Exponential, Uniform, Normal
from gammas import GA_2, GA_1, GS

EXPONENTIAL_THETA = 10.0


class Laplace:
    def __init__(self):
        self.rand = basic_rand.BasicRand()
        self.exp_rand = Exponential()

    def next(self, mu: float, b: float):
        E = self.exp_rand.next(1.0 / b)
        return mu + (E if self.rand.next() > 0 else -E)


class Lognormal: # needed 5
    def __init__(self):
        self.normal = Normal()

    def next(self, mu: float, sigma: float):
        return math.exp(self.normal.next(mu, sigma))


class Logistic:
    def __init__(self):
        self.uniform = Uniform()

    def next(self, mu: float, s: float):
        return mu + s * math.log(1.0 / self.uniform.next(0, 1) - 1)


class Cauchy: # needed 3
    def __init__(self):
        self.uniform = Uniform()

    def next(self, x0: float, gamma: float):
        x, y = 0, 0
        while True:
            x = self.uniform.next(-1, 1)
            y = self.uniform.next(-1, 1)
            if x ** 2 + y ** 2 < 1.0 or y == 0.0:
                break

        return x0 + gamma * x / y


class CauchyNormal:
    def __init__(self):
        self.normal = Normal()

    def next(self, x0: float, gamma: float):
        x, y = 0, 0
        x = self.normal.next(x0, gamma)
        y = self.normal.next(x0, gamma)

        return x0 + gamma * x / y


class ChiSquared: # needed 9  this is the real tai chi chuan
    def __init__(self):
        self.ga_1 = GA_1()
        self.ga_2 = GA_2()

    def next(self, k: int):
        if k >= 10.0:
            raise ValueError('no, god, please, no')
        x = (self.ga_2.next(0.5 * k) if (k & 1) else self.ga_1.next(k >> 1))
        return x ** 2


class Weibull: # needed 6
    def __init__(self):
        self.exponential = Exponential()

    def next(self, l: float, k: float):
        return l * math.pow(self.exponential.next(1), 1.0 / k)


class Pareto: # needed 4
    def __init__(self):
        self.uniform = Uniform()

    def next(self, xm: float, alpha: float):
        return xm / math.pow(self.uniform.next(0, 1), 1.0 / alpha)


class Beta:
    def __init__(self):
        self.gs = GS()

    def next(self, a: float, b: float):
        x = self.gs.next(a)
        return x / (x + self.gs.next(b))


class Rayleigh: #needed 10
    def __init__(self):
        self.exponential = Exponential()

    def next(self, sigma: float):
        return sigma * math.sqrt(self.exponential.next(0.5))


class Levy:
    def __init__(self):
        self.normal = Normal()

    def next(self, mu: float, c: float):
        N = self.normal.next(0, 1)
        return mu + c / (N**2)