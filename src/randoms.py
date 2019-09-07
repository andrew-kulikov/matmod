from datetime import datetime

LM = 2147483647
ULM = 4294967295
LLM = 9223372036854775807
ULLM = 18446744073709551615

class RandEngine:
    dummy = 123456789

    def mix(a: int, b: int, c: int):
        a = a - b
        a = a - c
        a = a ^ (c >> 13)
        b = b - c
        b = b - a
        b = b ^ ((a << 8) % ULM)
        c = c - a
        c = c - b
        c = c ^ (b >> 13)
        a = a - b
        a = a - c
        a = a ^ (c >> 12)
        b = b - c
        b = b - a
        b = b ^ ((a << 16) % ULM)
        c = c - a
        c = c - b
        c = c ^ (b >> 5)
        a = a - b
        a = a - c
        a = a ^ (c >> 3)
        b = b - c
        b = b - a
        b = b ^ ((a << 10) % ULM)
        c = c - a
        c = c - b
        c = c ^ (b >> 15)

        return c

    def getRandomSeed() -> int:
        RandEngine.dummy = (RandEngine.dummy + 1) % ULM
        # / 1000?
        return RandEngine.mix(datetime.now().microsecond % ULM, 5, RandEngine.dummy)

    def MinValue(self) -> int:
        pass
    
    def MaxValue(self) -> int:
        pass

    def Reseed(self, seed: int) -> int:
        pass

    def Next(self) -> int:
        pass


class JKissRandEngine(RandEngine):
    def __init__(self):
        self.x = 0
        self.c = 0
        self.y = 0
        self.z = 0
        self.Reseed(JKissRandEngine.getRandomSeed())

    def MinValue(self) -> int:
        return 0

    def MaxValue(self) -> int:
        return 4294967295
    
    def Reseed(self, seed: int):
        self.x = 123456789 ^ seed
        self.c = 6543217
        self.y = 987654321
        self.z = 43219876
    
    def Next(self):
        t = ((698769069 * self.z) % ULLM + self.c) % ULLM

        self.x = (self.x * 69069) % ULM
        self.x = (self.x + 12345) % ULM

        self.y ^= (self.y << 13) % ULM
        self.y ^= self.y >> 17
        self.y ^= (self.y << 5) % ULM

        self.c = (t >> 32) % ULM
        self.z = t % ULM

        return ((self.x + self.y) % ULM + self.z) % ULM


class JLKiss64RandEngine(RandEngine):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z1 = 0
        self.z2 = 0
        self.c1 = 0
        self.c2 = 0
        self.Reseed(JLKiss64RandEngine.getRandomSeed())

    def MinValue(self) -> int: 
        return 0

    def MaxValue(self) -> int:
        return 18446744073709551615

    def Reseed(self, seed: int):
        self.x = 123456789123 ^ seed
        self.y = 987654321987
        self.z1 = 43219876
        self.z2 = 6543217
        self.c1 = 21987643
        self.c2 = 1732654

    def Next(self):
        self.x = ((1490024343005336237 * self.x) % ULLM + 123456789) % ULLM

        self.y ^= (self.y << 21) % ULLM
        self.y ^= self.y >> 17
        self.y ^= (self.y << 30) % ULLM

        t = ((4294584393 * self.z1) % ULLM + self.c1) % ULLM
        self.c1 = (t >> 32) % ULM
        self.z1 = t % ULM

        t = ((4246477509 * self.z2) % ULLM + self.c2) % ULLM
        self.c2 = (t >> 32) % ULM
        self.z2 = t % ULM

        return (((self.x + self.y) % ULLM + self.z1) % ULLM + (self.z2 << 32) % ULLM) % ULLM


class PCGRandEngine(RandEngine):
    def __init__(self):
        self.state = 0
        self.inc = 0
        self.Reseed(self.getRandomSeed())

    def MinValue(self) -> int:
        return 0

    def MaxValue(self) -> int:
        return 4294967295

    def Reseed(self, seed: int):
        self.state = seed
        self.inc = seed

    def Next(self):
        oldstate = self.state
        self.state = oldstate * 6364136223846793005 + (self.inc | 1)
        xorshifted = ((oldstate >> 18) ^ oldstate) >> 27
        rot = oldstate >> 59

        return (xorshifted >> rot) | (xorshifted << ((-rot) & 31))


class BasicRandGenerator:
    def __init__(self):
        self.engine = None

    def getDecimals(value: int):
        num = 0
        maxRand = value

        while maxRand:
            num += 1
            maxRand >>= 1

        return num

    def Variate(self):
        return engine.Next()
        
    def maxDecimals(self):
        return getDecimals(engine.MaxValue())

    def MaxValue(self):
        return engine.MaxValue()

    def Reseed(self, seed: int):
        engine.Reseed(seed)
