# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 21:38:07 2018

@author: Ariel Domingo Catli
"""

import numpy as np
import cv2
import pickle
import os
from sklearn.svm import SVC
import shutil

class Classifier:
    
    def __init__(self):
        self.dataset_X = []
        self.dataset_Y = []
        self.dataset = []
        self.__model = []
        self.dataset_X_test = []
        self.dataset_Y_test = []
        self.dataset_filenames_test = []
        self.dataset_filenames_nodir_test = []
        self.dataset_test = []
        
    def add_model_dataset(self, data_folder, data_class, isHOG = True):
        if os.path.exists(data_folder):
            images = os.listdir(data_folder)
            
            if isHOG:
                HOG = cv2.HOGDescriptor()
                for image in images:
                    file_name = data_folder + image
                    image = cv2.imread(file_name)
                    image_hog = HOG.compute(image)
                    self.dataset_X.append(image_hog)
                    self.dataset_Y.append(data_class)
    
    def build_model_dataset(self, model_dataset_folder, model_dataset_name):
        self.dataset_X = np.array(self.dataset_X).reshape(-1,3780)
        self.dataset_Y = np.array(self.dataset_Y)
        self.dataset = [self.dataset_X, self.dataset_Y]
        with open(model_dataset_folder+model_dataset_name+".bin", "wb") as dataset:
            pickle.dump(self.dataset, dataset)
            
    def add_test_dataset(self, data_folder, data_class, isHOG = True):
        if os.path.exists(data_folder):
            images = os.listdir(data_folder)
            
            if isHOG:
                HOG = cv2.HOGDescriptor()
                for image in images:
                    file_name = data_folder + image
                    image_ = cv2.imread(file_name)
                    image_hog = HOG.compute(image_)
                    self.dataset_X_test.append(image_hog)
                    self.dataset_Y_test.append(data_class)
                    self.dataset_filenames_nodir_test.append(image)
                    self.dataset_filenames_test.append(file_name)
    
    def build_test_dataset(self, test_dataset_folder, test_dataset_name):
        self.dataset_X_test = np.array(self.dataset_X_test).reshape(-1,3780)
        self.dataset_Y_test= np.array(self.dataset_Y_test)
        self.dataset_test = [self.dataset_X_test, self.dataset_Y_test, self.dataset_filenames_test, self.dataset_filenames_nodir_test]
        with open(test_dataset_folder+test_dataset_name+".bin", "wb") as dataset:
            pickle.dump(self.dataset_test, dataset)
            
    def build_model(self, model_folder, model_name):
        self.__model = SVC(gamma = 0.0001, C=100)
        if(len(self.dataset) != 0):
            self.__model.fit(self.dataset_X, self.dataset_Y)
        
        with open(model_folder+model_name+".bin", "wb") as model:
            pickle.dump(self.__model, model)
            
    def load_model(self, model_folder):
        with open(model_folder, "rb") as dataset:
            return pickle.load(dataset)  
        
            
    def load_dataset(self, dataset_folder):
        with open(dataset_folder, "rb") as dataset:
            return pickle.load(dataset)
    
    #def test(class1_dest, class0_dest, dataset=self.dataset_test, model=self.__model):
        
    def classify(self, class0_dest, class1_dest):
        count = 0
        correct = 0
        results = self.__model.predict(self.dataset_test[0])
        count = len(results)
        for i, result in enumerate(results):
            if result == 1:
                shutil.copy(self.dataset_filenames_test[i], class1_dest+self.dataset_filenames_nodir_test[i])
            else:
                shutil.copy(self.dataset_filenames_test[i], class0_dest+self.dataset_filenames_nodir_test[i])
                
            if result == self.dataset_Y_test[i]:
                correct += 1
            
        
        return [results, self.dataset_filenames_test, [correct, count]]
                
    
    #def add_test_dataset(self): 
        
if __name__ == "__main__":
    bkn = Classifier()
    bkn.add_model_dataset("../../training/bkn/data/bkn/", 0)
    bkn.add_model_dataset("../../training/bkn/data/unbkn/", 1)
    bkn.build_model_dataset("../../training/bkn/bins/", "bkn_dataset")
    bkn.build_model("../../training/bkn/bins/", "model_bkn")
    bkn.add_test_dataset("../../testing/bkn/data/bkn/", 0)
    bkn.add_test_dataset("../../testing/bkn/data/unbkn/", 1)
    bkn.build_test_dataset("../../testing/bkn/bins/", "bkn_test_dataset")
    #print(bkn.load_dataset("../../testing/bkn/bins/bkn_test_dataset.bin"))
    results = bkn.classify("../../testing/bkn/results/bkn/", "../../testing/bkn/results/unbkn/")
    
    print(results[2])
    