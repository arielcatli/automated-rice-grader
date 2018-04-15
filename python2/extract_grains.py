# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 15:30:34 2018

@author: Ariel Domingo Catli
"""

import cv2
import numpy as np
import os
from math import ceil


def extract_grains(sample_image_directory, sample_directory_extracted_e, sample_directory_extracted_p, start):
    original_image = cv2.imread(sample_image_directory)
    image = cv2.imread(sample_image_directory, 0)
    image = cv2.medianBlur(image, 7)
#    image = cv2.bilateralFilter(image, 20, 31, 21)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
#   image = cv2.Canny(image[1], 128, 255)
    
    masked_image = cv2.bitwise_and(original_image, original_image, mask = image)
#    cv2.imshow("Original", original_image)
#    cv2.imshow("masked", image)
#    __clean_windows()
    contours = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = np.array(contours)
    lists = __bound(masked_image, contours[1], sample_directory_extracted_e, sample_directory_extracted_p, start)
    
    return[len(contours[1]), lists[0], lists[1]]
    
    
def __bound(image, contours, sample_directory_extracted_e, sample_directory_extracted_p, start):
    images = []
    for i,item in enumerate(contours):
        if not (len(item)<3):
            rectangle = cv2.minAreaRect(item)
            box = cv2.boxPoints(rectangle)
            box = np.int0(box)
            rotation_matrix = cv2.getRotationMatrix2D(rectangle[0], rectangle[2], 1)
            rotated_image = cv2.warpAffine(image.copy(), rotation_matrix, (image.shape[1], image.shape[0]))
            
            #new_rectangle = (rectangle[0], rectangle[1], 0.0)
            box = cv2.boxPoints(rectangle)
            new_box = np.int0(cv2.transform(np.array([box]), rotation_matrix))[0]
            
            cropped = rotated_image[new_box[1][1] : new_box[0][1], new_box[1][0] : new_box[2][0]]
            
            if cropped.shape[0] < cropped.shape[1]:
#                center = (int(cropped.shape[1]/2), int(cropped.shape[0]/2))
#                rotation_matrix_cropped = cv2.getRotationMatrix2D(center, -90, 1)
#                cropped = cv2.warpAffine(cropped, rotation_matrix_cropped, (cropped.shape[0], cropped.shape[1]))
                cropped = np.rot90(cropped)
            
            images.append(cropped)
            
    lists = __write_images(images, sample_directory_extracted_e, sample_directory_extracted_p, start)
    return lists
    
def __clean_windows():
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def __write_images(images, sample_directory_extracted_e, sample_directory_extracted_p, start):
    grain_list_masked = []
    grain_list_platform = []
    for i,image in enumerate(images):
        if os.path.exists(sample_directory_extracted_e):
            cv2.imwrite(sample_directory_extracted_e + "e" + str(i) + ".jpg", image)
            grain_list_masked.append(sample_directory_extracted_e + "e" + str(i) + ".jpg")
        else:
            print("The directory: " + sample_directory_extracted_e + " does not exists.")
        
        if os.path.exists(sample_directory_extracted_p):
            if image.shape[0] < 128 and image.shape[1] <64:
                platform = np.zeros([128,64,3], np.uint8)
                vertical_offset = int(ceil((platform.shape[0] - image.shape[0])/2))
                horizontal_offset = int(ceil((platform.shape[1] - image.shape[1])/2))
                platform[vertical_offset:(vertical_offset+image.shape[0]), horizontal_offset:(horizontal_offset+image.shape[1])] = image
                
                cv2.imwrite(sample_directory_extracted_p + "p" + str(i) + ".jpg", platform)
                grain_list_platform.append(sample_directory_extracted_p + "p" + str(i) + ".jpg")
        else:
            print("The directory: " + sample_directory_extracted_p + " does not exists.")
            
    return [grain_list_masked, grain_list_platform]
    
    
if __name__ == "__main__":
    print(extract_grains("grain.jpg", "e/", "p/", 0))
    