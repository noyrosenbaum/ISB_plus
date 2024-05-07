import os
import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt
import easyocr
import re
import datetime
# converting easyocr format to yolov8 in order to check accuracy between them


start = datetime.datetime.now()

# Path to the directory containing test images
images_dir = '/home/ruth/Documents/cyber/Project/test'

# Output directory for processed images
output_dir = '/home/ruth/Documents/cyber/Project/output_images_combined'
labels_folder = '/home/ruth/Documents/cyber/Project/combined_labels_1'
# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(labels_folder, exist_ok=True)

# Load the YOLO model
model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')
model = YOLO(model_path)


# Threshold for object detection
threshold_YOLO = 0.3

# Threshold for OCR
threshold_OCR = 0.12

# Initialize OCR reader
reader = easyocr.Reader(['en'])

# Function to perform object detection using YOLO
def detect_objects(image):
    return model(image)[0]

# Function to recognize text in an image using OCR
def recognize_text(image):
    return reader.readtext(image)

def WriteLabels(labels, labels_filepath):        
    with open(labels_filepath, 'w') as txt_file:
        for label in labels:
            txt_file.write(label + '\n')

# Function to perform OCR on an image and save the processed image
def perform_ocr_on_image(image, labels_filepath):
    labels = []
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = recognize_text(image_rgb)

    
    for (bbox, text, prob) in results:
        if prob >= threshold_OCR:
            (top_left, _, bottom_right, _) = bbox
            top_left = (int(top_left[0]), int(top_left[1]))
            bottom_right = (int(bottom_right[0]), int(bottom_right[1]))

            num = text.strip()
            nuk = len(num)

            credit_card_pattern = r'^\d{16}$'
            card_expiry = '\d{2}/\d{2}'
            card_name = '^[a-zA-Z]+(?: [a-zA-Z]+)?$'

            if nuk >= 4 and sum(c.isdigit() for c in num) >= 2:
                cv2.rectangle(image, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)
                cv2.putText(image, 'card_number', (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                labels.append(f"1 {top_left[0] / 640} {top_left[1] / 640} {bottom_right[0] / 640} {bottom_right[1] / 640}")
            elif re.findall(card_expiry, num):
                cv2.rectangle(image, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)
                cv2.putText(image, 'exp_date', (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                labels.append(f"2 {top_left[0] / 640} {top_left[1] / 640} {bottom_right[0] / 640} {bottom_right[1] / 640}")

            # elif re.findall(card_name, num):
            #     cv2.rectangle(image, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=-1)
            #     cv2.putText(image, 'holder_name', (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            #     labels.append(f"4 {top_left[0]} {top_left[1]} {bottom_right[0]} {bottom_right[1]}")

    #WriteLabels(labels, labels_filepath)
    return (image, labels)


# Process each image in the images_dir directory
for image_name in os.listdir(images_dir):
    if image_name.lower().endswith(('.png', '.jpg', '.jpeg', 'webp')):
        image_path = os.path.join(images_dir, image_name)
        output_filepath = os.path.join(output_dir, image_name)
        labels_filepath = os.path.join(labels_folder, os.path.splitext(image_name)[0] + '.txt')
        image = cv2.imread(image_path)

        if image is None:
            print(f"Error: Unable to read image '{image_path}'")
            continue
        
        labels = []

        # Perform object detection
        results = detect_objects(image)

        # Initialize a flag to keep track of the detected classes other than front_side and back_side
        other_classes_detected = False
        image_height, image_width, _ = image.shape
        # Draw bounding boxes on the image
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result

            if score > threshold_YOLO:
                x_center = (x1 + x2) / (2 * image_width)
                y_center = (y1 + y2) / (2 * image_height)
                box_width = (x2 - x1) / image_width
                box_height = (y2 - y1) / image_height

                # Append label to the list
                labels.append(f"{int(class_id)} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}")
                # Get the class name
                class_name = results.names[int(class_id)].lower()
                if class_name in ["front_side", "back_side"]:
                    continue
                other_classes_detected = True

                if class_name in ["card_number", "exp_date", "holder_name"]:
                    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)

                    label_yolo = cv2.putText(image, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
                
                    # Blacken the area within the bounding box
                    image[int(y1):int(y2), int(x1):int(x2)] = 0    
                    # ocr_image, ocr_labels = perform_ocr_on_image(image, labels_filepath)
                    # labels.extend(ocr_labels) 

        if not other_classes_detected:
            # Perform OCR on the image and save the processed image
            ocr_image, ocr_labels = perform_ocr_on_image(image, labels_filepath)
            labels.extend(ocr_labels)

        
        WriteLabels(labels, labels_filepath)

          # Generate output and labels filepath
        cv2.imwrite(output_filepath, image)

end = datetime.datetime.now()
elapsed_time = (end - start).total_seconds()
print(f"{elapsed_time} seconds")



   
