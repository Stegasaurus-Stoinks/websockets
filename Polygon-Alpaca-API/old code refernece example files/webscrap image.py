
# cv2.cvtColor takes a numpy ndarray as an argument 
import numpy as np 
import time  
import pytesseract 
  
# importing OpenCV 
import cv2 as cv
  
from PIL import ImageGrab 

trustedTraders = ["jonathanwoo","illproducer","skepticule","Muse","rush2ucd","13rainman","Nx","Pluto","hyp3rstr34m","Brayden","Clem","MrChaarlie","Xmptz","slam","Riley"]
last = []
  
def imToString(): 

    global last
  
    # Path of tesseract executable 
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    # ImageGrab-To capture the screen image in a loop.  
    # Bbox used to capture a specific area. 
    cap = ImageGrab.grab(bbox =(2130, 100, 2800, 1320))
    cap.save('test.png')
    #cap.show() 
    cap = cv.imread('test.png', cv.IMREAD_COLOR)
    #cap = cv.cvtColor(cap, cv.COLOR_BGR2GRAY)
    #cap = cv.medianBlur(cap, 5)
    #cap = cv.threshold(cap, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
    # Converted the image to monochrome for it to be easily  
    # read by the OCR and obtained the output String. 
    text = pytesseract.image_to_string(cap)
            
    
    text = text.splitlines()
    while("" in text):
        text.remove("")
            
    filteredArray = []    
    for i in range(0,len(text)):
        line = text[i]
        prevLine = text[i-1]
        if ("BTO" in line) or ("STC" in line) or ("stc" in line) or ("bto" in line):
            #print(prevLine)
            #print(line)
            for name in trustedTraders:
                if(name in prevLine):
                    #print("True")
                    filteredArray.append(prevLine)
                    filteredArray.append(line)
    
    #print(filteredArray)
                
    if filteredArray != []:            
        if filteredArray[-1] != last:
            print(filteredArray[-1])
            last = filteredArray[-1]
        
  
# Calling the function 
while(1):
    imToString()
    time.sleep(10)
    #print("check") 
