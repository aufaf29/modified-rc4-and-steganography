import copy
import os
import cv2
import random
import numpy as np

from rc4 import RC4
from steganoimage import SteganoImage

steganomachine = SteganoImage()
image = cv2.imread("./sample/image.bmp")
capacity = steganomachine.calculate_capacity(cv2.imread("./sample/image.bmp"))
file, stegoimage = steganomachine.insert_file_to_image_LSB(open("./sample/schedule.pdf", "rb") , image, encrypt=True, randomize=True, stegokey="TEST")

print(capacity)

cv2.imwrite("res.bmp", stegoimage)

result = steganomachine.get_binary_from_image(cv2.imread("res.bmp"), stegokey="TEST")

file = open("res.pdf", "wb")
file.write(result)
file.close()

print(cv2.PSNR(image, stegoimage))
