import wave


class AudioStego:
    def __init__(self, file_name) -> None:
        self._input_file_name = file_name

    def encode(self, text, output_file_name):
        audio = wave.open(self._input_file_name, "rb")

        # get every byte
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

        # pad the text with % as marker
        text += int((len(frame_bytes) - (len(text) * 8 * 8)) / 8) * '%'

        # turn text to list of bits
        bits = list(
            map(
                int,
                ''.join(bin(ord(i)).lstrip('0b').rjust(8, '0') for i in text),
            ))

        # changing the last bit
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit
        self._frame_modified = bytes(frame_bytes)

        # save the output
        output_audio = wave.open(output_file_name, 'wb')
        output_audio.setparams(audio.getparams())
        output_audio.writeframes(self._frame_modified)

        audio.close()
        output_audio.close()

    def decode(self):
        audio = wave.open(self._input_file_name, "rb")
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

        # get the bit message
        bits = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]

        string = "".join(
            chr(int("".join(map(str, bits[i:i + 8])), 2))
            for i in range(0, len(bits), 8))
        decoded = string.split("###")[0]

        audio.close()

        return decoded
