import copy


class ModifiedRC4Cipher:
    def __init__(self, key_input="test") -> None:
        self._key = []

        self._key_scheduling(key_input)

    def _key_scheduling(self, key_input):
        # initialize
        for i in range(256):
            self._key.append(i)

        # permutation
        j = 0
        for i in range(256):
            j = (j + self._key[i] + ord(key_input[i % len(key_input)])) % 256

            # swap
            self._key[i], self._key[j] = self._key[j], self._key[i]

    def compute(self, text):
        # PRGA (Pseudo-random generation algorithm)
        i = 0
        j = 0
        result = ""

        # to make sure the key doesn't change
        temp_key = copy.copy(self._key)

        for char in text:
            i = (i + 1) % 256
            j = (j + temp_key[i]) % 256

            # swap
            temp_key[i], temp_key[j] = temp_key[j], temp_key[i]

            t = (temp_key[i] + temp_key[j]) % 256
            u = temp_key[t]

            result += chr(u ^ ord(char) ^ j)

        return result

    def compute_bytes(self, bytes):
        # PRGA (Pseudo-random generation algorithm)
        i = 0
        j = 0
        result = b''

        # to make sure the key doesn't change
        temp_key = copy.copy(self._key)

        for x in range(len(bytes)):
            i = (i + 1) % 256
            j = (j + temp_key[i]) % 256

            # swap
            temp_key[i], temp_key[j] = temp_key[j], temp_key[i]

            t = (temp_key[i] + temp_key[j]) % 256
            u = temp_key[t]
            
            result += (u ^ bytes[x] ^ j).to_bytes(1, "big")

        return result
