import util.crc
from signals.signal import DigitalSignal

AGGREGATE_WORD_A = 0xFC
AGGREGATE_WORD_B = 0x198
AGGREGATE_WORD_C = 0x168
AGGREGATE_WORD_C_LINE = 0x350
AGGREGATE_WORD_D = 0x1B4
AGGREGATE_WORD_E = 0x00
EOT = 0x0D

CRC_KEY = 0x5B9

class RadioDataSystem(object):

    def __init__(self, pi):
        self.pi = pi & 0xFFFF

    def getRadioTextSignal(self, text, sampleRate, clock=1187.5):
        byteStream = self.getByteStream(text)
        s = DigitalSignal(byteStream, clock, sampleRate, low=-1.0, high=1.0)
        return s

    def getByteStream(self, text):
        byteStream = []
        text = map(lambda c: ord(c), text + chr(EOT))
        textLength = len(text) if len(text) <= 64 else 64
        croppedText = text[:textLength]
        for i in range(textLength/2):
            byteStream += self.getRadioTextGroup(croppedText[i*2:i*2+1], i)
        return byteStream

    def getRadioTextGroup(self, chars, address):
        group = self.makeBlocks(chars, address)
        byteStream = self.getBytesFromGroup(group)
        return byteStream

    def getBytesFromGroup(self, group):
        bytes = []
        for i in range(2):
            bigint = (group[i*2] << 26) + group[i*2+1]
            for j in range(6):
                b = (bigint & 0xFF0000000000) >> 40
                bigint = bigint << 8
                bytes.append(b)
        return bytes

    def makeBlocks(self, chars, address):
        blocks = []
        blocks.append(self.getBlockWithCRC(self.pi, AGGREGATE_WORD_A))
        blocks.append(self.getBlockWithCRC(int("0b001000000000", 2) << 4 + address, AGGREGATE_WORD_B))
        blocks.append(self.getBlockWithCRC(chars[0], AGGREGATE_WORD_C))
        blocks.append(self.getBlockWithCRC(chars[1] if len(chars) == 2 else 0, AGGREGATE_WORD_D))
        return blocks

    def getBlockWithCRC(self, word, aggWord):
        return self.getWordWithCRC(word) + aggWord

    def getWordWithCRC(self, word):
        return (word << 10) + util.crc.crc(word, CRC_KEY, 16, 10)


def main():
    rds = RadioDataSystem(0x00)
    rds.getRadioTextSignal()

if __name__ == "__main__":
    main()