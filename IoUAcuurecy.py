import os

def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    
    # compute the area of both the prediction and ground-truth rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    
    # compute the intersection over union
    iou = interArea / float(boxAArea + boxBArea - interArea)
    
    return iou

def read_annotations_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [[float(coord) for coord in line.strip().split()] for line in lines]

def calculate_iou_for_files(test_annotations_folder, predictions_annotations_folder, iou_threshold=0.1):
    ious = []
    for test_file_name in os.listdir(test_annotations_folder):
        test_file_path = os.path.join(test_annotations_folder, test_file_name)
        prediction_file_path = os.path.join(predictions_annotations_folder, test_file_name)
        
        test_annotations = read_annotations_file(test_file_path)
        prediction_annotations = read_annotations_file(prediction_file_path)
        
        # Calculate IoU for each bounding box pair
        iou_per_file = []
        for test_annotation in test_annotations:
            for prediction_annotation in prediction_annotations:
                iou = bb_intersection_over_union(test_annotation, prediction_annotation)
                if iou >= iou_threshold:
                    iou_per_file.append(iou)
                    break  # Stop comparing with other predictions if IoU exceeds threshold
        
        # Calculate average IoU for the file
        average_iou_per_file = sum(iou_per_file) / len(iou_per_file) if iou_per_file else 0
        ious.append(average_iou_per_file)
    
    # Calculate overall average IoU
    overall_average_iou = sum(ious) / len(ious) if ious else 0
    return overall_average_iou

# Example usage
test_annotations_folder = '/home/ruth/Documents/cyber/Project/test.v5i.yolov8/train/labels'
predictions_annotations_folder = '/home/ruth/Documents/cyber/Project/yolov8_labels'
combined_annotations_folder = '/home/ruth/Documents/cyber/Project/combined_labels_1'
easyocr_annotations_folder = '/home/ruth/Documents/cyber/Project/easyocr_labels'

average_iou = calculate_iou_for_files(test_annotations_folder, predictions_annotations_folder)
average_iou_combined = calculate_iou_for_files(test_annotations_folder, combined_annotations_folder)
average_iou_easyocr = calculate_iou_for_files(test_annotations_folder, easyocr_annotations_folder)

print("Average IoU yolov8:", average_iou)
print("Average IoU combined:", average_iou_combined)
print("Average IoU eacyocr:", average_iou_easyocr)
