import os
import cv2
import numpy as np
import easyocr
from pyzbar.pyzbar import decode
import re
import datetime


start = datetime.datetime.now()


def process_imgs_in_folder(input_folder, output_folder, labels_folder):
    # Ensure output folders exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(labels_folder, exist_ok=True)
    
    # Iterate over each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png', 'webp')):  # Consider only img files
            input_filepath = os.path.join(input_folder, filename)
            output_filepath = os.path.join(output_folder, filename)
            labels_filepath = os.path.join(labels_folder, os.path.splitext(filename)[0] + '.txt')
            overlay_ocr_text(input_filepath, output_filepath, labels_filepath)


def recognize_text(img_path):
    reader = easyocr.Reader(['en'])
    return reader.readtext(img_path)


def overlay_ocr_text(input_filepath, output_filepath, labels_filepath):
    # Loads the img
    img = cv2.imread(input_filepath)
    img_height, img_width, _ = img.shape

    # Recognizes text in the img
    result = recognize_text(input_filepath)

    # Processing the recognized text
    labels = []
    for (bbox, text, prob) in result:
        if prob >= 0:
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = (int(top_left[0]), int(top_left[1]))
            bottom_right = (int(bottom_right[0]), int(bottom_right[1]))

            # Checking if recognized text matches specific patterns (e.g., PAN card number)
            num = text.strip()
            nuk = len(num)

            credit_card_pattern = r'^\d{16}$'
            card_expiry = '\d{2}/\d{2}'
            card_name = '^[a-zA-Z]+(?: [a-zA-Z]+)?$'
            if nuk >= 4 and sum(c.isdigit() for c in num) >= 2:
                cv2.rectangle(img, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)
                cv2.putText(img, 'card_number', (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                labels.append(f"1 {top_left[0] / 640} {top_left[1] / 640} {bottom_right[0] / 640} {bottom_right[1] / 640}")
            elif re.findall(card_expiry, num):
                cv2.rectangle(img, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)
                cv2.putText(img, 'exp_date', (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                labels.append(f"2 {top_left[0] / 640} {top_left[1] / 640} {bottom_right[0] / 640} {bottom_right[1] / 640}")
            elif re.findall(card_name, num):
                cv2.rectangle(img, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)
                cv2.putText(img, 'holder_name', (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                labels.append(f"4 {top_left[0] / 640} {top_left[1] / 640} {bottom_right[0] / 640} {bottom_right[1] / 640}")

    # Save labels to a text file
    with open(labels_filepath, 'w') as labels_file:
        for label in labels:
            labels_file.write(label + '\n')

    # Save the processed img (optional)
    cv2.imwrite(output_filepath, img)


# Example usage
input_folder = '/home/ruth/Documents/cyber/Project/test'
output_folder = '/home/ruth/Documents/cyber/Project/output_images_easyocr'
labels_folder = '/home/ruth/Documents/cyber/Project/easyocr_labels'
process_imgs_in_folder(input_folder, output_folder, labels_folder)
end = datetime.datetime.now()
elapsed_time = (end - start).total_seconds()
print(f"{elapsed_time} seconds")