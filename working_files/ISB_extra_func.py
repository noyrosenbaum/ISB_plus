# Image Security Barrier.py
# Imports for ISB base code
import cv2
import numpy as np
import easyocr  # For OCR
import matplotlib.pyplot as plt
from pyzbar.pyzbar import decode
import re
from PIL import Image


# Simport tesseract

# Scan image using OCR for text recognition
def recognize_text(img_path):
    reader = easyocr.Reader(['en'])
    return reader.readtext(img_path)


# Function for overlaying recognized text and hiding sensitive information
def overlay_ocr_text(img_path):
    # Loads the image
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Sets up matplotlib for visualization
    fig_width = 10  # initialize to a default value
    dpi = 10
    fig_height = int(img.shape[1] / dpi)
    if img.shape[0] > img.shape[1]:
        fig_width = int(img.shape[1] / img.shape[0] * fig_height)
    plt.figure()
    f, axarr = plt.subplots(1, 2, figsize=(fig_width, fig_height))
    axarr[0].imshow(img)

    # Recognizes text in the image
    result = recognize_text(img_path)
    print(result)

    # QR and bar code detection
    code = decode(img)
    print(code)

    for barcode in decode(img):
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.drawContours(img, [pts], -1, color=(255, 0, 0), thickness=-1)

    # Processing the recognized text
    for (bbox, text, prob) in result:
        if prob >= 0:
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = (int(top_left[0]), int(top_left[1]))
            bottom_right = (int(bottom_right[0]), int(bottom_right[1]))

            string1 = text

            # Opening a text file containing sensitive keywords
            file1 = open("sensitive_words.txt", "r")
            readfile = file1.read()

            # Checking if recognized text contains sensitive keywords
            if string1 in readfile:
                cv2.rectangle(img=img, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)
            else:
                print('String', string1, 'Not Found')

            file1.close()

            # Checking if recognized text matches specific patterns (e.g., PAN card number)
            num = text.strip()
            nuk = (len(num))
            # if nuk == 10 and all(map(tesseract.exstr.isalpha, num[:5])) and all(map(str.isnumeric, num[5:9])) and num[9].isalpha():
            #     cv2.rectangle(img=img, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)
            # else:
            # print("This is not a PAN card.")
            if nuk == 8 and re.match(r'^[A-Z]{3}\d{3}[A-Z]\d$', num):
                cv2.rectangle(img=img, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)

            if nuk == 14 and re.match(r'^\d{4} \d{4} \d{4}$', num):
                cv2.rectangle(img=img, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)
            else:
                print("This is not an Aadhar card.")

            if "+91" in num:
                cv2.rectangle(img=img, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)

            if "Plot no" in num:
                cv2.rectangle(img=img, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)

            if "1234" in num:
                cv2.rectangle(img=img, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)

            #  Noy's addition
            credit_card_pattern = r'^\d{16}$'
            card_expiry = '\d{2}/\d{2}'
            if num == 16 and re.match(credit_card_pattern, num):
                cv2.rectangle(img=img, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)
            else:
                print("This is not a credit card number")
                
            if re.findall(card_expiry, num):
                cv2.rectangle(img=img, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)
                print("This is a credit card expiry!!!!!!!!!!!!!!!!!!!!!!")
            else:
                print("This is not a card expiry")
            

    # # Noy's addition for credit cards detection below #

    # def recognize_names(img_path):
    #     # Recognizes text in the image
    #     result = recognize_text(img_path)

    #     # Processing the recognized text
    #     names = []
    #     for (bbox, text, prob) in result:
    #         if prob >= 0.5:
    #             # Considering only text with high confidence level
    #             if text.isupper():  # Assuming names are in uppercase
    #                 names.append(text)
    #     return names

    # Show and save the processed image
    axarr[1].imshow(img)
    plt.savefig('overlay.png', bbox_inches='tight')
    plt.show()


# Example usage
im_1_path = '61.jpg'
if hasattr(Image, 'Resampling'):
    print("Resampling attribute exists")
else:
    print("Resampling attribute does not exist")
overlay_ocr_text(im_1_path)