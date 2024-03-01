import os
import cv2
from ultralytics import YOLO
import easyocr
import re


# List of test images
test_images = ["2ajh064.jpg", "774328f6-f9fb-4e01-9690-40bae05a5cbf.jpeg", "aeonJAL[1].png"]

# Path to the directory containing test images
images_dir = '/mnt/c/Users/noyro/Documents/ISB_plus/tozip/credit_card_resize_640'

# Output directory for processed images
output_dir = '/mnt/c/Users/noyro/Documents/ISB_plus/tozip/processed_images'

# Load the YOLO model
model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')
model = YOLO(model_path)

# Threshold for object detection
threshold_YOLO = 0.5

# Thresehold for OCR
threshold_OCR = 0.12

# OCR part
reader = easyocr.Reader(['en'])
recognized_objects = []  # List to store recognized objects and their class names

def perform_ocr_on_image(image, coordinates, class_name):
    x1, y1, x2, y2 = map(int, coordinates)  # Extract coordinates
    cropped_img = image[y1:y2, x1:x2]  # Crop image based on coordinates

    gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_RGB2GRAY)
    results = reader.readtext(gray_img)

    card_expiry = '\d{2}/\d{2}'
    card_name = '^[a-zA-Z]+(?: [a-zA-Z]+)?$'

    for res in results:
        text = res[1]
        if res[0] and res[1] and (res[2] >= threshold_OCR):
            if re.findall(card_expiry, text) or class_name == "exp_date":
                recognized_objects.append((text, "exp_date"))  # Store recognized object and its class name
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
                print("This is a credit card expiry: " + text)
            elif len(text) >= 4 and sum(c.isdigit() for c in text) >= 2 or class_name == "card_number":
                recognized_objects.append((text, "card_number"))  # Store recognized object and its class name
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
                print("This is a credit card number: " + text)
            elif re.match(card_name, text) and class_name == "holder_name":
                recognized_objects.append((text, "holder_name"))  # Store recognized object and its class name
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
                print("This is the name of the holder: " + text)
            else:
                recognized_objects.append((text, "unrecognized"))  # Store unrecognized object and its class name
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 4)  # Mark unrecognized text in blue
                print("Unrecognized text: " + text)

    return recognized_objects

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Initialize flag to check if any of the specified classes are detected
class_detected = False

# Process each image in the images_dir directory
for image_name in os.listdir(images_dir):
    # Check if the file is an image
    if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Read the image
        image_path = os.path.join(images_dir, image_name)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Error: Unable to read image '{image_path}'")
            continue

        # Perform object detection
        results = model(image)[0]

        # Draw bounding boxes on the image
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result

            if score > threshold_YOLO:
                # Get the class name
                class_name = results.names[int(class_id)].lower()
                if class_name in ["card_number", "exp_date", "holder_name"]:
                    text_ocr = perform_ocr_on_image(image, (x1, y1, x2, y2), class_name)
                    label_ocr = text_ocr
                    class_detected = True  # Set flag if any of the specified classes are detected
                # Draw rectangle around the detected object
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                label_yolo = cv2.putText(image, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
                
                 # Iterate over recognized objects from OCR and compare class names with YOLO
                for obj_text, obj_class in recognized_objects:
                    if obj_class == class_name:
                        print(f"OCR and YOLO detected the same class: {class_name}, Text: {obj_text}")

                # Check if the class is "card_number", "exp_dates", or "holder_name"
                if class_name in ["card_number", "exp_date", "holder_name"]:
                    # Blacken the area within the bounding box
                    image[int(y1):int(y2), int(x1):int(x2)] = 0
                

         # If none of the specified classes are detected, perform OCR on the entire image
        if not class_detected:
            text_ocr = perform_ocr_on_image(image, (0, 0, image.shape[1], image.shape[0]), "unknown")    

        # Save the processed image to the output directory
        output_path = os.path.join(output_dir, f'result_{image_name}')
        cv2.imwrite(output_path, image)
