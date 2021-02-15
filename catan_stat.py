import cv2
import pytesseract
import numpy as np
from PIL import Image

img = cv2.imread('overview.png')
# def get_grayscale(image):
#     return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# def thresholding(image):
#     return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
# def opening(image):
#     kernel = np.ones((5,5),np.uint8)
#     return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
# gray = get_grayscale(img)
# thresh = thresholding(gray)
# opening = opening(gray)
# custom_config = r'--oem 3 --psm 6'
# # pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
# print(pytesseract.image_to_string(opening, config=custom_config))
norm_img = np.zeros((img.shape[0], img.shape[1]))
img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
img = cv2.GaussianBlur(img, (1, 1), 0)
text = pytesseract.image_to_string(img)
print(text)
