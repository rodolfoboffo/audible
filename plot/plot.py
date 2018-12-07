import matplotlib.pyplot as pyplot

class SignalPlot(object):

    def __init__(self, signals):
        self.signals = [signals] if not isinstance(signals, list) else signals
        self.sampleRate = self.signals[0].getSampleRate()
        self.xAxisFunction = lambda samples: range(len(samples))

    def setXAxisFunction(self, f):
        self.xAxisFunction = f

    def plotSeconds(self, seconds):
        return self.plotSamples(seconds * self.sampleRate)

    def plotSamples(self, numberOfSamples):
        for signal in self.signals:
            samples = signal.getRange(end=numberOfSamples)
            pyplot.plot(self.xAxisFunction(samples), samples)
        return pyplot.show()