# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 16:38:11 2018

@author: Ariel Domingo Catli
"""

from modeler import Classifier
from sizer import Sizer
import cv2
import pickle
import numpy as np

class Grader:
    def __init__(self):
        
        #constants
        self.__LOG_TXT = "../../img-src/log.txt"
        self.__SAMPLES = "../../img-src/"
        
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
        self.lassifier_ylw = ""
        self.classifier_paddy = ""
        self.classifier_foreign = ""
        self.classifier_damaged = ""
        self.classifier_sizer = ""
        
        
        #-------------------------------------
        #bind the folders
        self.__instantiate_classifiers()
        self.__determine_directories()
        
    def __instantiate_classifiers(self):
        self.classifier_bkn = Classifier(isHOG = True)
        self.classifier_grn = Classifier(isHOG = False)
        self.lassifier_ylw = Classifier(isHOG = False)
        self.classifier_paddy = Classifier(isHOG = False)
        self.classifier_foreign = Classifier(isHOG = False)
        self.classifier_damaged = Classifier (isHOG = False)
        self.classifier_sizer = Sizer()
        
    def __determine_directories(self):
        with open(self.__LOG_TXT, "r") as log_file:
            self.sample_id = log_file.read()
            self.sample_directory = self.__SAMPLES + self.sample_id + "/"
        
        self.sample_directory_extracted = self.sample_directory+"extracted"
        self.sample_directory_extracted_e = self.sample_directory_extracted+"/e/"
        self.sample_directory_extracted_p = self.sample_directory_extracted+"/p/"
        self.sample_directory_bkn = self.sample_directory+"bkn"
        self.sample_directory_nbkn = self.sample_directory+"nbkn"
        self.sample_directory_grn = self.sample_directory+"grn"
        self.sample_directory_ngrg = self.sample_directory+"ngrn"
        self.sample_directory_nylw = self.sample_directory+"nylw"
        self.sample_directory_ylw = self.sample_directory+"ylw"
        self.sample_directory_ndamaged = self.sample_directory+"ndamaged"
        self.sample_directory_damaged = self.sample_directory+"damaged"
        self.sample_directory_foreign = self.sample_directory+"foreign"
        self.sample_directory_nforeign = self.sample_directory+"nforeign"
        self.sample_directory_nchalky = self.sample_directory+"nchalky"
        self.sample_directory_chalky = self.sample_directory+"chalky"
    
        
        
if __name__ == "__main__":
    grader = Grader()
    grader.classifier_bkn.set_model("../../training/bkn/bins/model_bkn.bin")
    grader.classifier_bkn.add_dataset()
    
    