import matplotlib.pyplot as pyplot

class SignalPlot(object):

    def __init__(self, signals):
        self.signals = signals
        self.sampleRate = signals[0].getSampleRate()

    def plotSeconds(self, seconds):
        return self.plotSamples(seconds * self.sampleRate)

    def plotSamples(self, numberOfSamples):
        for signal in self.signals:
            samples = signal.getRange(end=numberOfSamples)
            pyplot.plot(range(len(samples)), samples)
        return pyplot.show()