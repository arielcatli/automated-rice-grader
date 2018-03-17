# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 10:27:16 2018

@author: Ariel Domingo Catli
"""

from sizer import Sizer
import os
import cv2
import shutil

class Grain_sizer:
    def __init__(self):
        self.sizer = Sizer()
        self.sizer.calibrate("../../coin.jpg", 24)
        
    def add_dataset(self, sample_directory):
        if os.path.exists(sample_directory):
            self.sizer.add_images(sample_directory)
            
        else:
            print("Directory " + sample_directory + " doesn't exists.")
    
    def average_size(self):
            return self.sizer.average_size()
        
    def find_brewers(self, sample_directory, nbrewer_folder, brewer_folder):
        images = os.listdir(sample_directory)
        
        for image in images:
            file_name = sample_directory+image
            image = cv2.imread(file_name,0)
            thresh, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            binary_image = cv2.Canny(cv2.GaussianBlur(binary_image, (31,31), 0), 30, 150)
            contours = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            max_height = 0
            max_contour = []
            
            for i,contour in enumerate(contours[1]):
                x,y,w,h = cv2.boundingRect(contour)
                if max_height < h:
                    max_height = h
                    max_contour = contour
            
            
            if(len(max_contour) != 0):
                x,y,w,h = cv2.boundingRect(max_contour)
            else:
                continue
            
            if self.sizer.pixelToMm(max_height) < 1.44:
                shutil.copy(file_name, brewer_folder)
            else:
                shutil.copy(file_name, nbrewer_folder)
    
    def grain_size_classification(self, average_size):
        classification = ""
        if average_size < 5.5:
            classification = "SHORT"
        elif average_size >= 5.5 and average_size < 6.3:
            classification = "MEDIUM"
        elif average_size >= 6.3 and average_size < 7.4:
            classification = "LONG"
        elif average_size >= 7.5:
            classification = "VERY LONG"
        
        return [average_size, classification]
        
if __name__ == "__main__":
    s = Grain_sizer()
    s.sizer.calibrate("../../coin.jpg", 24)
    s.find_brewers("../../img-src/38/extracted/p/", "../../img-src/61/nbrewer/", "../../img-src/61/brewer/")
    
    
        