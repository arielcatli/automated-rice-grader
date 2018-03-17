# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 13:22:01 2018

@author: Ariel Domingo Catli
"""
import cv2
import numpy as np
import os
import pickle

class Sizer:
    def __init__(self):
        self.__isCalibrated = False
        self.__sum = 0
        self.grain_count = 0
        self.avg_size = None
        self.unitPerPixel = 0
        
    def add_images(self, sample_directory):
        images = os.listdir(sample_directory)
        self.grain_count+= len(images)
        for image in images:
            file_name = sample_directory+"/"+image
            image = cv2.imread(file_name,0)
            thresh, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            binary_image = cv2.Canny(cv2.GaussianBlur(binary_image, (31,31), 0), 30, 150)
            contours = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
            max_height = 0
            max_contour = 0
            for i,contour in enumerate(contours[1]):
                x,y,w,h = cv2.boundingRect(contour)
                if max_height < h:
                    max_height = h
                    max_contour = contour
                    
            x,y,w,h = cv2.boundingRect(max_contour)
            self.__sum += h
            
            
            
    def average_size(self):
        if self.__isCalibrated and self.grain_count != 0:
            self.avg_size = self.__sum/self.grain_count
            return self.avg_size*self.unitPerPixel
                
        else:
            print("Error: Sizer not calibrated or no data to size")
            return None
    
    def calibrate(self, calibration_file, object_size):
        image = cv2.imread(calibration_file,0)
        thresh, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        binary_image = cv2.Canny(cv2.GaussianBlur(binary_image, (31,31), 0), 30, 150)
        contours = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        max_height = 0
        max_contour = 0
        for i,contour in enumerate(contours[1]):
            x,y,w,h = cv2.boundingRect(contour)
            if max_height < h:
                max_height = h
                max_contour = contour
                
        x,y,w,h = cv2.boundingRect(max_contour)  
        self.__isCalibrated = True
        unitPerPixel = object_size/h
        self.unitPerPixel = unitPerPixel
        return unitPerPixel
    
    def generate_report(self, report_directory):
        with open(report_directory, "wb") as report:
            pickle.dump([self.avg_size, self.grain_count, self.unitPerPixel], report)
            
    def pixelToMm(self, pixel):
        return pixel*self.unitPerPixel
        
        
if __name__ == "__main__":
    sizer = Sizer()    
    #sizer.add_images("../img-src/38/extracted/p/")
    sizer.calibrate("../../coin.jpg", 24)
    #print(sizer.size_up("dfs"))
    #sizer.generate_report("../img-src/38/extracted/report.bin")
    