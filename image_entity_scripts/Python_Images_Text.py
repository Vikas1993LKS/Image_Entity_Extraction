# -*- coding: utf-8 -*-
"""
Created on Sun May 17 18:11:53 2020

@author: Vikas Gupta
"""


import pytesseract
import os
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#get colored
def get_colored(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# noise removal
def remove_noise_gaussian(image):
    return cv2.GaussianBlur(image,(1,1),0)
    #return cv2.bilateralFilter(image, 9, 450, 480)

# noise removal
def remove_noise_gaussian_(image):
    return cv2.GaussianBlur(image,(0,0), 3)
    #return cv2.bilateralFilter(image, 9, 460, 500)
 
#canny edge detection
def canny(image):
    return cv2.Canny(image, 250, 300)

#denoising
def denoised_image(image):
    denoised = cv2.fastNlMeansDenoising(image, None, 15, 10, 50)
    return denoised


def imageprocessing(filename):
    image_text = ""
    file_name = filename.split("\\")[-1]
    Read_Image = cv2.imread(filename)
    Read_Image = get_colored(Read_Image)
    Blur_Image = remove_noise_gaussian(Read_Image)
    Result_Image = cv2.addWeighted(Read_Image, 1.84, Blur_Image, -1.58, 38)
    image_text = pytesseract.image_to_string(Result_Image)
    image_text = image_text.replace("\\r\\n", "\\n")
    return image_text
            

def imageprocessing_canny(filename):
    image_text = ""
    file_name = filename.split("\\")[-1]
    Read_Image = cv2.imread(filename)
    Image_Gray = get_grayscale(Read_Image)
    Blur_Image = remove_noise_gaussian(Image_Gray)
    Canny = canny(Image_Gray)
    Result_Image = cv2.addWeighted(Blur_Image, 1.84, Canny, -1.58, 38)
    image_text = pytesseract.image_to_string(Result_Image)
    image_text = image_text.replace("\\r\\n", "\\n")
    return image_text 

def imageprocessing_(filename):
    image_text = ""
    file_name = filename.split("\\")[-1]
    Read_Image = cv2.imread(filename)
    Read_Image = get_colored(Read_Image)
    Blur_Image = remove_noise_gaussian_(Read_Image)
    Result_Image = cv2.addWeighted(Read_Image, 1.84, Blur_Image, -1.58, 38)
    image_text = pytesseract.image_to_string(Result_Image)
    image_text = image_text.replace("\\r\\n", "\\n")
    return image_text