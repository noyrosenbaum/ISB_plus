# Sensitive data detection with EasyOCR and YOLOv8 Models

## Abstract
Text detection or in general object detection has been an area of intensive research accelerated with deep learning. 
Today, object detection, and in our case, text detection, can be achieved through two approaches: Region-Based detectors and Single Shot detectors. In Region-Based methods, the first objective is to find all the regions which have the objects and then pass those regions to a classifier, which gives us the locations of the required objects. So, it is a two-step process. 
Firstly, it finds the bounding box and afterwards, the class of it. This approach is considered more accurate but is comparatively slow as compared to the Single Shot approach. 
Single Shot detectors, however, predict both the boundary box and the class at the same time. Being a single step process, it is much faster. However, it must be noted that Single Shot detectors perform badly while detecting smaller objects.

## Achieved Contribution 
ISB utilizes a dataset as a collection of keywords to detect sensitive data in images effectively. Due to the vast number of keywords required, a prebuilt dataset is essential for accurate detection and protection of sensitive data. As we expand ISBs’ capabilities to identify sensitive data it has not encountered before, the keyword list gets longer thus the running time grows. We created our own dataset in order to examine our improvement ideally – detect sensitive data using general patterns and object detection techniques. The dataset comprises images of credit cards, annotated to delineate various components including the front and back sides of the card, the name of the cardholder, the credit card number, and the expiration date. The dataset was partitioned into three subsets for training, validation, and testing, consisting of 738, 110, and 112 images, respectively. Horizontal and vertical flipping augmentation techniques were applied during the training process to augment the dataset and enhance model robustness. Our approach is reduce the running time and leverage the IoU rate by using YOLOv8 for detecting potential sensitive data objects within the image, and using EasyOCR to recognize objects such as: number of the card and expiration date that YOLOv8 didn’t detect. In light of the inherent capabilities and limitations of EasyOCR, which entails the comprehensive extraction of text from images, we deliberated the inclusion of cardholder name recognition within our scope. 
However, upon rigorous consideration, we resolved to exclude this component from our analysis. This decision was motivated by apprehensions regarding the susceptibility of the EasyOCR system to misidentify irrelevant text as the cardholder’s name, potentially leading to erroneous classifications and reduced overall accuracy. Thus, in order to mitigate the introduction of noise and maintain the integrity of our recognition process, we determined that omitting the cardholder name recognition would be prudent.

## ISB Work
The work focuses on developing a software called Image Security Barrier (ISB) to address the issue of sensitive information leakage through images shared on the internet and social media platforms. ISB acts as a protective shield by detecting sensitive data such as Aadhar numbers, PAN numbers, addresses etc. using keywords and patterns, and hiding it before sharing the image.

### Methodology of ISB
ISB first takes an image input, scans it using EasyOCR to extract text from images, it maps sensitive data followed by keyword detection and pattern recognition to identify sensitive information and hides it at the end. It also has the capability to recognize QR codes and barcodes within images for further data protection.

## Our Work - "ISB Plus"
Our purpose was to widen sensitive data detection abilities into something as general as we can, creating an implementation that will cover wide variety of sensitive data patterns with the use of existing implementations such as YOLOv8 model and generate generic regular expressions as much as possible to minimize dependencies. 
We created an algorithm that combines both YOLOv8 (a single shot detector) and EasyOCR (a region-based detector) to ensure maximal detection accuracy while keeping it effective and fast with minimal dependencies.
In evaluating the accuracy of our object detection model, we utilized the Intersection over Union (IoU) metric. It used to evaluate the accuracy of an object detection algorithm by measuring the overlap between the predicted bounding box and the ground truth bounding box. It is calculated as the ratio of the area of intersection between the predicted and ground truth bounding boxes to the area of their union. A higher IoU indicates a better alignment between the predicted and ground truth bounding boxes.

### Methodology of ISB Plus
The combined methodology integrates the YOLOv8 and EasyOCR models to facilitate the detection of sensitive information within images. Initially, the YOLOv8 model processes the input image, generating bounding boxes delineating objects potentially containing sensitive data, based on its training phase consisting of 100 epochs and utilizing a threshold of 0.3. Subsequently, in scenarios where the YOLOv8 output exclusively identifies front and back sides, EasyOCR is invoked to extract further details. Leveraging predefined regular expressions tailored to specific card elements such as credit card numbers and expiry dates, EasyOCR employs its algorithmic capabilities to detect these objects within the image.

## Results
We conducted comparisons between 3 algorithms: ISB, YOLOv8, and a combined code that includes YOLOv8 and EasyOCR. The most important parameters were average IoU rate and running time because of the trade-off. Given our custom dataset (labeled credit cards images).

### Average IoU
The combined model has a slightly higher average IoU (0.935266) compared to
both ISB (0.536656) and YOLOv8 (0.9288805). This indicates that the combined model performs better in terms of object detection accuracy.

### Runtime
The combined model has a higher runtime (20.233 seconds) compared to YOLOv8 (12.570 seconds) but significantly lower than ISB (439.845 seconds). 
Although the combined model’s runtime is higher than YOLOv8, it is much more efficient than ISB.
