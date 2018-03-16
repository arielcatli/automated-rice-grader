# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 09:58:01 2018

@author: Ariel Domingo Catli
"""

import cv2
import numpy as np
import pickle
import os


class Chalky_classifier():
    def __init__(self):
        self.__isCalibrated = False
        self.__chalky_range = []

        
    def calibrate(self, chalky_range):
        for channel in chalky_range:
           if channel[0] < channel[1]:
               self.__chalky_range.append(channel)
               self.__isCalibrated = True
           else:
               print("Range is invalid")
               self.__isCalibrated = False
               break
            
    def add_test_dataset(self, grain_directory):
        images = os.listdir(grain_directory)
        if self.__isCalibrated:
            for image in images:
                file_name = grain_directory + image
                image_file = cv2.imread(file_name)
#                image_ = cv2.imread(file_name)
#                mask_image = cv2.threshold(cv2.GaussianBlur(image_file, (7,7), 0),127,255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
#                b = cv2.calcHist([image_], [0], mask_image[1], [256], [0,256])
#                #b_perc = (sum(b[self.__chalky_range[2][0]:self.__chalky_range[2][1]])/sum(b))[0]
#                g = cv2.calcHist([image_], [1], mask_image[1], [256], [0,256])
#                #g_perc = (sum(g[self.__chalky_range[1][0]:self.__chalky_range[1][1]])/sum(g))[0]
#                r = cv2.calcHist([image_], [2], mask_image[1], [256], [0,256])
#                #r_perc = (sum(r[self.__chalky_range[0][0]:self.__chalky_range[0][1]])/sum(r))[0]
                chalky_pixels = 0
                for row in image_file:
                    for column in row:                        
                        if(self.__within_range(column[0], self.__chalky_range[2]) and self.__within_range(column[1], self.__chalky_range[1]) and
                                           self.__within_range(column[2], self.__chalky_range[0])):
                            chalky_pixels += 1
                            
                total_pixels = image_file.shape[0] * image_file.shape[1]
                print(chalky_pixels, total_pixels)
                        
    def __within_range(self, number, range_):
        if number > range_[0] and number < range_[1]:
            return True
        else:
            return False
            
            


if __name__ == "__main__":
    chalk = Chalky_classifier()
    chalk.calibrate([[150,255],[150,255],[150,255]])
    chalk.add_test_dataset("../img-src/40/extracted/d/")
    img = cv2.imread("../img-src/40/extracted/d/p57.jpg")
    cv2.imshow("h", img)
    print(img[85,29])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
        