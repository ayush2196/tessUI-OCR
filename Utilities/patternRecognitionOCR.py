from PIL import Image
import pytesseract
from pytesseract import Output
import argparse
import cv2
import os
import re

#pytesseract.pytesseract.tesseract_cmd = r"C:\Users\AvelinaK\Documents\Machine Learning\tesseract.exe"

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
#                 help="path to input image to be OCR'd")
# ap.add_argument("-p", "--preprocess", type=str, default="thresh",
#                 help="type of preprocessing to be done")
# args = vars(ap.parse_args())

# load the example image and convert it to grayscale
#image = cv2.imread(args["image"])

def convert_toText(path,pattern, inputRegex):

    text = ""
    dateText = ""
    emailText = ""
    panText = ""
    otherText = ""

    img = cv2.imread(path)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    # gray = cv2.threshold(gray, 0, 255,
    # 					 cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # gray = cv2.medianBlur(gray, 3)

    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    keys = list(d.keys())

    date_pattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$'
    email_pattern = '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    pancard_pattern = '[A-Z]{5}[0-9]{4}[A-Z]{1}'

    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:

            # if re.match(date_pattern, d['text'][i]) or re.match(email_pattern, d['text'][i]) or re.match(
            #         pancard_pattern, d['text'][i]):
            #     #print(d['text'][i])
            #     text += d['text'][i] + "\n"

            if(pattern == "date" and not inputRegex):
                if re.match(date_pattern, d['text'][i]):
                    dateText += "DATE: " + d['text'][i] + "\n"
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            elif (pattern == "email" and not inputRegex):
                if re.match(email_pattern, d['text'][i]):
                    emailText += " EMAIL: " + d['text'][i] + "\n"
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            elif (pattern == "pan" and not inputRegex):
                if re.match(pancard_pattern, d['text'][i]):
                    panText = " PAN Number: " + d['text'][i] + "\n"
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            elif (pattern == "others"):
                if re.match(inputRegex, d['text'][i]):
                    otherText += " Extracted text based on your pattern: " + d['text'][i] + "\n"
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # To create the boundary around the text
            # (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            # img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        text = dateText + "\n" + emailText + "\n" + panText + "\n" + otherText
        im = Image.fromarray(img)
        im.save("images/" + pattern + ".jpg")
    return text, im
