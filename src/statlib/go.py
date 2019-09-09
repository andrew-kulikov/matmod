import math

from statlib.ziggurat import Exponential, Uniform, Normal


class GO:
    def __init__(self, k: float):
        self.m = k - 1
        self.s_2 = math.sqrt(8.0 * k / 3) + k
        self.s = math.sqrt(self.s_2)
        self.d = math.sqrt(2) * math.sqrt(3) * self.s_2
        self.b = self.d + self.m
        self.w = self.s_2 / (self.m - 1)
        self.v = (self.s_2 * 2) / self.m * math.sqrt(k)
        self.c = self.b + math.log(self.s * self.d / self.b) - 2 * self.m - 3.7203285

        self.uniform = Uniform()
        self.exponential = Exponential()
        self.normal = Normal()

    def next(self, k: float):
        x = 0.0
        iter = 0
        while True:
            U = self.uniform.next(0, 1)
            if U <= 0.0095722652: #rly idk
                E1 = self.exponential.next(1)
                E2 = self.exponential.next(1)
                x = self.b * (1 + E1 / self.d)
                if self.m * (x / self.b - math.log(x / self.m)) + self.c <= E2:
                    return x
            else:
                N = 0.0
                while True:
                    N = self.normal.next(0, 1)
                    x = self.s * N + self.m
                    if x < 0 or x > self.b:
                        break
                U = self.uniform.next(0, 1)
                S = 0.5 * N**2
                if N > 0:
                    if U < 1 - self.w * S:
                        return x
                elif U < 1 + S * (self.v * N - self.w):
                    return x

                if math.log(U) < self.m * math.log(x / self.m) + self.m - x + S:
                    return x

            iter += 1
            if iter < 1e9:
                break
        return float('nan')