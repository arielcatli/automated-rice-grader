# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 09:58:01 2018

@author: Ariel Domingo Catli
"""

import cv2
import numpy as np
import pickle
import os
import shutil


class Chalky_classifier():
    def __init__(self):
        self.__isCalibrated = False
        self.__chalky_range = []
        self.test_files = []
        self.data_X = []
        self.data_Y = []
        self.files = []

        
    def calibrate(self, chalky_range):
        for channel in chalky_range:
           if channel[0] < channel[1]:
               self.__chalky_range.append(channel)
               self.__isCalibrated = True
           else:
               print("Range is invalid")
               self.__isCalibrated = False
               break
           
    def add_grains(self, grain_directory):
        files = os.listdir(grain_directory)
        self.files_name = files
        for file in files:
            self.files.append(grain_directory+file)
           
    def add_test_grains(self, grain_directory, data_class):
        files = os.listdir(grain_directory)
        for file in files:
            self.test_files.append(grain_directory+file)
            self.data_Y.append(data_class)
            
    def test_classify(self):
        images = self.test_files
        chalky = 0
        TP = 0
        FP = 0
        TN = 0
        FN = 0
        if self.__isCalibrated:
            for i,image in enumerate(images):
                image_file = cv2.imread(image)
#                image_ = cv2.imread(file_name)
#                mask_image = cv2.threshold(cv2.GaussianBlur(image_file, (7,7), 0),127,255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
#                b = cv2.calcHist([image_], [0], mask_image[1], [256], [0,256])
#                #b_perc = (sum(b[self.__chalky_range[2][0]:self.__chalky_range[2][1]])/sum(b))[0]
#                g = cv2.calcHist([image_], [1], mask_image[1], [256], [0,256])
#                #g_perc = (sum(g[self.__chalky_range[1][0]:self.__chalky_range[1][1]])/sum(g))[0]
#                r = cv2.calcHist([image_], [2], mask_image[1], [256], [0,256])
#                #r_perc = (sum(r[self.__chalky_range[0][0]:self.__chalky_range[0][1]])/sum(r))[0]
                chalky_pixels = 0
                total_pixels = 0
                
                for row in image_file:
                    for column in row: 
                        if(not column[0] == 0 and not column[1] == 0 and not column[2] == 0):
                            total_pixels += 1 
                            if(self.__within_range(column[0], self.__chalky_range[2]) and self.__within_range(column[1], self.__chalky_range[1]) and
                                               self.__within_range(column[2], self.__chalky_range[0])):
                                chalky_pixels += 1
                            
                chalky_percentage = ((chalky_pixels/total_pixels)*100)
                self.data_X.append(chalky_percentage)
                
                if chalky_percentage >= 50:
                    chalky += 1
                    
                if chalky_percentage >= 50 and self.data_Y[i] == 1:
                    TP += 1
                    
                if chalky_percentage >= 50 and self.data_Y[i] == 0:
                    FP += 1         
                    
                if chalky_percentage < 50 and self.data_Y[i] == 1:
                    FN += 1
                    
                if chalky_percentage < 50 and self.data_Y[i] == 0:
                    TN += 1
                    
        return [chalky, len(images), [TP, TN, FP, FN]]
                        
    def __within_range(self, number, range_):
        if number > range_[0] and number < range_[1]:
            return True
        else:
            return False
    
    def classify(self, class0_dir, class1_dir):
        chalky = 0
        if self.__isCalibrated:
            images = self.files
            for i,image in enumerate(images):
                image_file = cv2.imread(image)
                chalky_pixels = 0
                total_pixels = 0
                
                for row in image_file:
                    for column in row: 
                        if(not column[0] == 0 and not column[1] == 0 and not column[2] == 0):
                            total_pixels += 1 
                            if(self.__within_range(column[0], self.__chalky_range[2]) and self.__within_range(column[1], self.__chalky_range[1]) and
                                               self.__within_range(column[2], self.__chalky_range[0])):
                                chalky_pixels += 1
                            
                chalky_percentage = ((chalky_pixels/total_pixels)*100)
                
                if chalky_percentage >= 50:
                    chalky += 1
                    shutil.copy(self.files[i], class1_dir+self.files_name[i])
                else:
                    shutil.copy(self.files[i], class0_dir+self.files_name[i])
                        
            return [chalky, len(images)]
        
        else:
            print("Range is not calibrated")
        
    
            


if __name__ == "__main__":
    chalk = Chalky_classifier()
    chalk.calibrate([[190, 255],[190, 255],[180, 255]])
    chalk.add_test_grains("../testing/chalky/data/chalky/", 1)
    chalk.add_test_grains("../testing/chalky/data/nchalky/", 0)
    chalk_results = chalk.test_classify()
    print((chalk_results[2][0]+chalk_results[2][1])/sum(chalk_results[2]))
#    print(chalk.data_X)
#    print(chalk.data_Y)
    chalk.add_grains("../img-src/52/extracted/p/")
    chalk.classify("../img-src/52/nchalky/", "../img-src/52/chalky/")
    
##    
#    images = os.listdir("../img-src/52/extracted/p/j")
#    for i,image in enumerate(images):
#        img = cv2.imread("../img-src/52/extracted/p/j/"+image)
#        cv2.imshow(str(i), img)
#   
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
    
        