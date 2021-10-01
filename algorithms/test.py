import copy
import os
import cv2
import random
import numpy as np

from steganoimage import SteganoImage

steganomachine = SteganoImage()
image = cv2.imread("./sample/small_image.bmp")
capacity = steganomachine.calculate_capacity(cv2.imread("./sample/small_image.bmp"))
file, stegoimage = steganomachine.insert_file_to_image_LSB(open("./sample/insert.txt", "rb") , image, encrypt=True, randomize=True, stegokey="TEST", seed=11)

print(capacity)

cv2.imwrite("res.bmp", stegoimage)

result = steganomachine.get_binary_from_image(cv2.imread("res.bmp"), stegokey="TEST", seed=11)
print("========")
print(result)

file = open("res.txt", "wb")
file.write(result)
file.close()

print(cv2.PSNR(image, stegoimage))
