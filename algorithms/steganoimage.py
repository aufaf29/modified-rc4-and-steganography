import copy
import random

from .rc4 import ModifiedRC4Cipher

class SteganoImage:
    def __init__(self):
        pass

    def insert_file_to_image_LSB(self, file, image, encrypt=False, randomize=False, stegokey=None, seed=None):
        file = file.read()

        if(encrypt):
            cipher = ModifiedRC4Cipher(stegokey) if stegokey is not None else ModifiedRC4Cipher()
            file = cipher.compute_bytes(file)
            
        (_, width, depth) = image.shape

        binary_length = self.padding_binary(bin(8 * len(file))[2:], 4)
        encrypt_bin = self.padding_binary(bin(1 if encrypt else 0)[2:], 1)
        randomize_bin = self.padding_binary(bin(1 if randomize else 0)[2:], 1)

        if(randomize):
            stegoimage = copy.copy(image)

            binary = encrypt_bin + randomize_bin + binary_length
            for itr in range(len(binary)):
                i = itr // (width * depth)
                j = (itr % (width * depth)) // depth
                k = (itr % depth)
                stegoimage[i][j][k] = self.change_LSB(image[i][j][k], binary[itr])

            binary = self.get_binary_repr(file)
            generator = self.create_sequential_index(seed, 48, len(binary))
            count = 0
            for itr in generator:
                i = itr // (width * depth)
                j = (itr % (width * depth)) // depth
                k = (itr % depth)
                stegoimage[i][j][k] = self.change_LSB(image[i][j][k], binary[count])
                count += 1
        else:
            stegoimage = copy.copy(image)
            binary = encrypt_bin + randomize_bin + binary_length + self.get_binary_repr(file)
            for itr in range(len(binary)):
                i = itr // (width * depth)
                j = (itr % (width * depth)) // depth
                k = (itr % depth)
                stegoimage[i][j][k] = self.change_LSB(image[i][j][k], binary[itr])
        
        return file, stegoimage
    
    def get_binary_from_image(self, image, stegokey=None, seed=None):
        (height, width, depth) = image.shape

        LSBs = ""

        for i in range(height):
            for j in range(width):
              for k in range(depth):
                LSBs += str(self.get_LSB(image[i][j][k]))

        encrypt = int(LSBs[0:8], 2)
        randomize = int(LSBs[8:16], 2)
        binary_length = int(LSBs[16:48], 2)
        binary = b''

        if(randomize == 1):
            generator = self.create_sequential_index(seed, 48, binary_length)
            count = 0
            temp = ""
            for itr in generator:
                i = itr // (width * depth)
                j = (itr % (width * depth)) // depth
                k = (itr % depth)
                count += 1
                temp += str(self.get_LSB(image[i][j][k]))
                if(count % 8 == 0):
                    binary += self.binary_to_bytes(temp)
                    count = 0
                    temp = ""
        else:
            for i in range(48, binary_length + 48, 8):
                binary += self.binary_to_bytes(LSBs[i:i+8])
        
        if(encrypt == 1):
            cipher = ModifiedRC4Cipher(stegokey) if stegokey is not None else ModifiedRC4Cipher()
            binary = cipher.compute_bytes(binary)
        

        return binary
    
    def padding_binary(self, binary, length):
        return binary if(len(binary) % (8 * length) == 0) else "0" * ((8 * length) - (len(binary) % (8 * length))) + binary
    
    def binary_to_bytes(self, binary):
        binary_int = int(binary, 2)
        byte_number = len(binary) // 8 
        binary_array = binary_int.to_bytes(byte_number, "big")
        return binary_array
    
    def calculate_capacity(self, image):
        (height, width, depth) = image.shape
        return ((height*width*depth)//8)-6
    
    def get_LSB(self, value):
        value = int.from_bytes(value, "big")
        return value % 2

    def change_LSB(self, value, bit):
        LSB = value % 2
        bit = int(bit)
        if(LSB != bit):
            value = (value+1) if(bit==1) else (value-1)
        return value

    def get_binary_repr(self, val):
        binary = int.from_bytes(val, "big")
        binary = bin(binary)[2:]
        binary = "0" * ((8 * len(val)) - (len(binary))) + binary
        return binary

    def create_sequential_index(self, stegokey, minval, length):
        random.seed(stegokey)
        return random.sample(range(minval, length + minval), length)