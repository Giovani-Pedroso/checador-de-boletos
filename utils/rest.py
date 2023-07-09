import cv2
import numpy as np
from pdf2image import convert_from_path, convert_from_bytes

# images = convert_from_path('/home/belval/example.pdf')
# img = cv2.imread('./imgs/boleto_qr_3.jpg')
# img = cv2.imread('./imgs/boleto_qr_4.jpg')
# img = cv2.imread('./imgs/bar1.jpg')
# img = cv2.imread('./imgs/bar2.png')
img = cv2.imread('./imgs/bar4.jpg')
# img = cv2.imread('./imgs/2023-07-04_20-25.png')

# img = cv2.imread('./imgs/boleto_qr_1.jpg')
bd = cv2.barcode.BarcodeDetector()

qcd = cv2.QRCodeDetector()

retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)
retval_bar, decoded_info_bar,  points_bar = bd.detectAndDecode(img)
# # retval, decoded_info, decoded_type  = bd.detectAndDecode(img)
print(bd.detectAndDecode(img))

print("There is some qr codes: ")
print(retval)
print("There is some barcodes: ")
print(retval_bar)
# print(decoded_info)
