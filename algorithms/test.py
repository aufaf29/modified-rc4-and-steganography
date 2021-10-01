import cv2
import numpy as np

from steganoimage import SteganoImage

steganomachine = SteganoImage()

print()

# Baca image
image = cv2.imread("./sample/image.bmp")

# Hitung kapasitas
capacity = steganomachine.calculate_capacity(cv2.imread("./sample/image.bmp"))
print("Capacity: " + str(capacity) + " Bytes")
print()

# Masukkan pesan ke dalam gambar
file, stegoimage = steganomachine.insert_file_to_image_LSB(open("./sample/insert.txt", "rb") , image, encrypt=True, randomize=True, stegokey="TEST", seed=11)

# Cek Skor PSNR
print("PSNR: " + str(cv2.PSNR(image, stegoimage)))
print()

# Simpan hasil gambar
cv2.imwrite("res.bmp", stegoimage)

# Cek LSB terenkripsi dengan password salah
print("False password checking:")
print(steganomachine.get_binary_from_image(cv2.imread("res.bmp"), stegokey="TES", seed=11))
print()

# Cek LSB terenkripsi dengan password benar
result = steganomachine.get_binary_from_image(cv2.imread("res.bmp"), stegokey="TEST", seed=11)
print("True password checking:")
print(result)

file = open("res.txt", "wb")
file.write(result)
file.close()


