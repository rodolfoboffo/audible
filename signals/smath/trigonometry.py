import math
import numpy as np
import const

class SineTable(object):

    def __init__(self, sinusoidDetail):
        self.sinusoidDetail = sinusoidDetail
        self.sineArray = self.initializeSineTable(self.sinusoidDetail)

    def initializeSineTable(self, sinusoidDetail):
        sin = []
        for i in range(sinusoidDetail):
            sin.append(math.sin(const.PI2 / sinusoidDetail * i))
        return np.array(sin)

    def sin(self, x):
        i = int(x / const.PI2 * len(self.sineArray)) % len(self.sineArray)
        return self.sineArray[i]

    def cos(self, x):
        i = int((const.PI_HALF - x) / const.PI2 * len(self.sineArray)) % len(self.sineArray)
        return self.sineArray[i]

SINE_TABLE = SineTable(2048)