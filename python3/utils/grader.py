# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 16:38:11 2018

@author: Ariel Domingo Catli
"""

from chalky_classifier import Chalky_classifier
from modeler import Classifier
from sizer import Sizer
import cv2
import pickle
import numpy as np
import os

class Grader:
    def __init__(self):
        #constants
        self.__LOG_TXT = r"../../img-src/log.txt"
        self.__SAMPLES = r"../../img-src/"
        
        #variables
        self.sample_directory = ""
        self.sample_id = ""
        self.sample_directory_bkn = ""
        self.sample_directory_nbkn = ""
        self.sample_directory_grn = ""
        self.sample_directory_ngrg = ""
        self.sample_directory_nylw = ""
        self.sample_directory_ylw = ""
        self.sample_directory_ndamaged = ""
        self.sample_directory_damaged = ""
        self.sample_directory_foreign = ""
        self.sample_directory_nforeign = ""
        self.sample_directory_nchalky = ""
        self.sample_directory_chalky = ""
        
        #classifiers
        self.classifier_bkn = ""
        self.classifier_grn = ""
        self.classifier_ylw = ""
        self.classifier_paddy = ""
        self.classifier_foreign = ""
        self.classifier_damaged = ""
        self.classifier_sizer = ""
        self.classifier_chalky = ""
        
        
        #-------------------------------------
        #bind the folders
        self.__instantiate_classifiers()
        self.__determine_directories()

        #load the models to the classifiers
        self.__load_models()


        
    def __instantiate_classifiers(self):
        self.classifier_bkn = Classifier(isHOG = True)
        self.classifier_grn = Classifier(isHOG = False)
        self.classifier_ylw = Classifier(isHOG = False)
        self.classifier_paddy = Classifier(isHOG = False)
        self.classifier_foreign = Classifier(isHOG = False)
        self.classifier_damaged = Classifier (isHOG = False)
        self.classifier_sizer = Sizer()
        self.classifier_chalky = Chalky_classifier()
        
    def __determine_directories(self):
        with open(self.__LOG_TXT, "r") as log_file:
            self.sample_id = log_file.read()
            self.sample_directory = self.__SAMPLES + self.sample_id + "/"
        
        self.sample_directory_extracted = self.sample_directory+"extracted/"
        self.sample_directory_extracted_e = self.sample_directory_extracted+"/e/"
        self.sample_directory_extracted_p = self.sample_directory_extracted+"/p/"
        self.sample_directory_bkn = self.sample_directory+"bkn/"
        self.sample_directory_nbkn = self.sample_directory+"nbkn/"
        self.sample_directory_grn = self.sample_directory+"grn/"
        self.sample_directory_ngrn = self.sample_directory+"ngrn/"
        self.sample_directory_nylw = self.sample_directory+"nylw/"
        self.sample_directory_ylw = self.sample_directory+"ylw/"
        self.sample_directory_ndamaged = self.sample_directory+"ndamaged/"
        self.sample_directory_damaged = self.sample_directory+"damaged/"
        self.sample_directory_foreign = self.sample_directory+"foreign/"
        self.sample_directory_nforeign = self.sample_directory+"nforeign/"
        self.sample_directory_nchalky = self.sample_directory+"nchalky/"
        self.sample_directory_chalky = self.sample_directory+"chalky/"
        self.sample_directory_paddy = self.sample_directory+"paddy/"
        self.sample_directory_npaddy = self.sample_directory+"npaddy/"
        
    def __load_models(self):
        self.classifier_bkn.set_model("../../training/bkn/bins/model_bkn.bin")
        self.classifier_ylw.set_model("../../training/ylw/bins/model_ylw.bin")
        self.classifier_paddy.set_model("../../training/paddy/bins/model_paddy.bin")
        self.classifier_grn.set_model("../../training/grn/bins/model_grn.bin")
        self.classifier_foreign.set_model("../../training/foreign/bins/model_foreign.bin")
        self.classifier_damaged.set_model("../../training/damaged/bins/model_damaged.bin")
        self.classifier_chalky.calibrate([[190, 255],[190, 255],[180, 255]])

    def classify(self):
        self.classifier_foreign.add_dataset(self.sample_directory_extracted_p)
        self.classifier_foreign.classify(self.sample_directory_nforeign, self.sample_directory_foreign)
        self.classifier_paddy.add_dataset(self.sample_directory_nforeign)
        self.classifier_paddy.classify(self.sample_directory_npaddy, self.sample_directory_paddy)
        
        self.classifier_bkn.add_dataset(self.sample_directory_npaddy)
        self.classifier_bkn.classify(self.sample_directory_nbkn, self.sample_directory_bkn)
        
        self.classifier_ylw.add_dataset(self.sample_directory_npaddy)
        self.classifier_ylw.classify(self.sample_directory_nylw, self.sample_directory_ylw)
        
        self.classifier_grn.add_dataset(self.sample_directory_npaddy)
        self.classifier_grn.classify(self.sample_directory_ngrn, self.sample_directory_grn)
        
        self.classifier_damaged.add_dataset(self.sample_directory_npaddy)
        self.classifier_damaged.classify(self.sample_directory_ndamaged, self.sample_directory_damaged)
        
        self.classifier_chalky.add_grains(self.sample_directory_npaddy)
        self.classifier_chalky.classify(self.sample_directory_nchalky, self.sample_directory_chalky)
        
        
if __name__ == "__main__":
    grader = Grader()
    grader.classify()
    #grader.classify_HOG()
    
