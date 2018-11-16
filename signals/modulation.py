import signal

class WideFrequencyModulation(signal.Signal):
    def generateFMSignal(amplitude, carrierFrequency, audioSignal, sampleRate, sineArray, phase=0.0):
        data = []
        phi = phase
        t = 1.0 / sampleRate
        for i in range(len(audioSignal)):
            if i != 0:
                phi += 2 * math.pi * (carrierFrequency + 75000.0*audioSignal[i]) * t
            data.append(amplitude * mySin(phi, sineArray))
        return np.array(data)
