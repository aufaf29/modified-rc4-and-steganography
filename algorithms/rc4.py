class RC4:
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

        for char in text:
            i = (i + 1) % 256
            j = (j + self._key[i]) % 256

            # swap
            self._key[i], self._key[j] = self._key[j], self._key[i]

            t = (self._key[i] + self._key[j]) % 256
            u = self._key[t]

            result += chr(u ^ ord(char))

        return result
