from PIL import Image
import pytesseract
import argparse
import cv2
import os


def convert_toText(path):

    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.threshold(gray, 0, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.medianBlur(gray, 3)
    text = pytesseract.image_to_string(gray)
    #print(text)

    return text