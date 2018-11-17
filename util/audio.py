import scipy.io.wavfile
import numpy as np
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

def main():
    inputWavFile = r"C:\Users\rodolfo\Documents\HDSDR\input.wav"
    signals = extractSignalsFromWav(inputWavFile)
    print signals

if __name__ == "__main__":
    main()