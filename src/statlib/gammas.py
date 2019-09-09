import math

from statlib.ziggurat import Exponential, Uniform, Normal


class GA_1():
    def __init__(self):
        self.exponential = Exponential(1)

    def next(self, k: int):
        x = 0.0
        for i in range(0, k):
            x += self.exponential.next(1)
        return x


class GA_2: # needed maybe 8
    def __init__(self):
        self.normal = Normal()
        self.exponential = Exponential()

    def next(self, k: float):
        x = self.normal.next(0, 1)
        x *= 0.5 * x
        i = 1
        while i < k:
            x += self.exponential.next(1)
            i += 1
        return x


class GS:
    def __init__(self):
        self.uniform = Uniform()
        self.exponential = Exponential()

    def next(self, k: float):
        x = 0.0
        iter = 0
        while True:
            U = self.uniform.next(0, 1 + k / math.e)
            W = self.exponential.next(1)
            if U <= 1:
                x = math.pow(U, 1.0 / k)
                if x <= W:
                    return x
            else:
                x = -math.log((1 - U) / k + 1.0 / math.e)
                if (1 - k) * math.log(x) <= W:
                    return x

            iter += 1
            if iter < int(1e9):
                break
        return float('nan')