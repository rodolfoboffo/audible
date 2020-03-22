import math
import numpy as np

def getMagnitudesFromDFT(dft):
    return list(map(lambda i: np.abs(i), dft))

def getDFTFrequencies(n, sampleRate):
    return list(map(lambda x: 1.0 * x * sampleRate / (2 * n), range(n)))