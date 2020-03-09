import numpy as np
from const import RADIANS, SAMPLES, PI2

def getZeroCrossIndexes(singal, sampleInterval=None):
    zeroCrosses = []
    if not sampleInterval:
        sampleInterval = (0, singal.getLength())
    for i in range(int(sampleInterval[0]),  int(sampleInterval[1])-1):
        if singal.get(i) > 0.0 and singal.get(i+1) <= 0.0:
            zeroCrosses.append(i)
    return zeroCrosses

def phaseDetector(s1, s2, sampleRate, sampleInterval=None, frequency=None, result=SAMPLES):
    zeroCrossS1 = getZeroCrossIndexes(s1, sampleInterval=sampleInterval)
    zeroCrossS2 = getZeroCrossIndexes(s2, sampleInterval=sampleInterval)
    minLen = min(len(zeroCrossS1), len(zeroCrossS2))
    if minLen == 0:
        raise Exception('One or both signals do not zero-cross.')
    diffs = list(map(lambda samplePair: samplePair[0] - samplePair[1], zip(zeroCrossS1[:minLen], zeroCrossS2[:minLen])))
    mean, stdDev = np.mean(diffs), np.std(diffs)
    if result == RADIANS:
        return list(map(lambda v: (v/sampleRate)*frequency*PI2, (mean, stdDev)))
    return mean, stdDev


