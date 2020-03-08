import scipy.io.wavfile
import numpy as np
import signals.signal
from signals.signal import Signal

def extractSignalsFromWav(path):
    file = scipy.io.wavfile.read(path)
    sampleRate = file[0]
    numberOfSamples = len(file[1])
    signals = []
    if numberOfSamples > 0:
        if isinstance(file[1][0], np.ndarray):
            channels = zip(*file[1])
            for channel in channels:
                signals.append(Signal(channel, sampleRate))
        else:
            signals.append(Signal(file[1], sampleRate))
    return signals

def exportWavFromSignal(signal, samples, path):
    if isinstance(signal, signals.signal.Signal):
        scipy.io.wavfile.write(path, int(signal.getSampleRate()), signal.getRange(0, samples or signal.getLength()))
    else:
        sampleRate = None
        samplesArray = []
        for s in signal:
            sampleRate = s.getSampleRate()
            samplesArray.append(s.getRange(0, samples or s.getLength()))
        scipy.io.wavfile.write(path, int(sampleRate), np.array(zip(*samplesArray)))

def main():
    inputWavFile = r"C:\Users\rodolfo\Documents\HDSDR\input.wav"
    signals = extractSignalsFromWav(inputWavFile)
    print(signals)

if __name__ == "__main__":
    main()