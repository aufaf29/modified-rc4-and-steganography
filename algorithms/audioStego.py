import wave
import random


class AudioStego:
    def __init__(self, file_name) -> None:
        self._input_file_name = file_name

    def encode(self, text, key, output_file_name):
        random.seed(key)
        audio = wave.open(self._input_file_name, "rb")

        # get every byte
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

        # mark the end of text with %
        text += "%"

        # turn text to list of bits
        bits = list(
            map(
                int,
                ''.join(bin(ord(i)).lstrip('0b').rjust(8, '0') for i in text),
            ))

        # changing the LSB
        length = len(frame_bytes)
        for bit in bits:
            i = int(random.random() * length)
            frame_bytes[i] = (frame_bytes[i] & 254) | bit
        frame_modified = bytes(frame_bytes)

        # save the output
        output_audio = wave.open(output_file_name, 'wb')
        output_audio.setparams(audio.getparams())
        output_audio.writeframes(frame_modified)

        audio.close()
        output_audio.close()

    def decode(self, key):
        random.seed(key)
        audio = wave.open(self._input_file_name, "rb")
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

        # get the bit message
        decoded = ""
        res = ""
        bits = []
        length = len(frame_bytes)
        while (res != "%"):
            i = int(random.random() * length)
            bits.append(frame_bytes[i] & 1)     # get LSB

            # get char from bits
            if len(bits) == 8:
                res = chr(int("".join(map(str, bits[:8])), 2))

                decoded += res
                bits = []

        decoded = decoded[:-1]

        audio.close()

        return decoded
