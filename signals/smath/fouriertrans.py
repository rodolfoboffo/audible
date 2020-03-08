import math

# def hanningFunction(sampleIndex, totalSamples, sineArray):
#     return 0.5 - 0.5 * myCos(2 * math.pi * sampleIndex / totalSamples, sineArray)
#
#
# def discreteFourierTransform(signal, nBins, sineArray):
#     reals, img = [], []
#     windowingFunction = hanningFunction
#     for m in range(nBins):
#         reals.append(0.0)
#         img.append(0.0)
#         for n in range(nBins):
#             reals[-1] += windowingFunction(n, nBins, sineArray) * signal[n] * myCos(2 * math.pi * n * m / nBins,
#                                                                                     sineArray)
#             img[-1] += windowingFunction(n, nBins, sineArray) * signal[n] * mySin(2 * math.pi * n * m / nBins,
#                                                                                   sineArray)
#     return reals, img
#
#
def getMagnitudesFromDFT(dft):
    mags, phases = [], []
    for i in range(len(dft)):
        mags.append(math.sqrt(dft[i].real * dft[i].real + dft[i].imag * dft[i].imag))
        phases.append(360.0 * math.atan(dft[i].imag / dft[i].real) / (2 * math.pi))
    return mags
