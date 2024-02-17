# ISB_plus
Expand Image Security Barrier implementation so it will include credit cards' patterns 

## Things that made me lose my mind
1. When you work on Jupyter Notebook and you import libraries and other shit,
   make sure you install everything you need on the notebook such as:
```!pip install opencv-python --upgrade
!pip install imutils --upgrade
!pip install pytesseract --upgrade
!pip install image-quality --upgrade
```
otherwise it will tell you to restart the kernel because it can't find the things it needs.
2. If you think you made it throught, think again!
   you still in deep shit.
   you need to install tesseract from a certain place in the internet
The error TesseractNotFoundError: tesseract is not installed or it's not in your PATH. indicates that the Tesseract OCR engine is either not installed on your system or it's not accessible from the Python environment.

At this point I'm not sure why don't people write their README file with all of these shit
It is not enough to upload the code itself.

