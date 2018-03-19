# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 16:38:11 2018

@author: Ariel Domingo Catli
"""

from chalky_classifier import Chalky_classifier
from grain_sizer import Grain_sizer
from modeler import Classifier
from sizer import Sizer
import cv2
import pickle
import numpy as np
import os
import tkinter as tk
from tkinter import ttk


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
        self.sample_directory_ngrn = ""
        self.sample_directory_nylw = ""
        self.sample_directory_ylw = ""
        self.sample_directory_ndamaged = ""
        self.sample_directory_damaged = ""
        self.sample_directory_foreign = ""
        self.sample_directory_nforeign = ""
        self.sample_directory_nchalky = ""
        self.sample_directory_chalky = ""
        self.count_bkn = 0
        self.count_nbkn = 0
        self.count_grn = 0
        self.count_ngrn = 0
        self.count_ylw = 0
        self.count_nylw = 0
        self.count_damaged = 0
        self.count_ndamaged = 0
        self.count_foreign = 0
        self.count_nforeign = 0
        self.count_chalky = 0
        self.count_nchalky = 0
        self.count_paddy = 0
        self.count_npaddy = 0
        self.count_red = 0
        self.count_nred = 0
        self.count_brewer = 0
        self.count_nbrewer = 0
        self.count_size = []
        
        #classifiers
        self.classifier_bkn = ""
        self.classifier_grn = ""
        self.classifier_ylw = ""
        self.classifier_paddy = ""
        self.classifier_foreign = ""
        self.classifier_damaged = ""
        self.classifier_sizer = ""
        self.classifier_chalky = ""
        self.classifier_red = ""
        self.classifier_sizer = ""
        
        
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
        self.classifier_sizer = Grain_sizer()
        self.classifier_chalky = Chalky_classifier()
        self.classifier_red = Classifier(isHOG = False)
        
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
        self.sample_directory_nred = self.sample_directory+"nred/"
        self.sample_directory_red = self.sample_directory+"red/"
        self.sample_directory_nbrewer = self.sample_directory+"nbrewer/"
        self.sample_directory_brewer = self.sample_directory+"brewer/"
        
    def __load_models(self):
        self.classifier_bkn.set_model("../../training/bkn/bins/model_bkn.bin")
        self.classifier_ylw.set_model("../../training/ylw/bins/model_ylw.bin")
        self.classifier_paddy.set_model("../../training/paddy/bins/model_paddy.bin")
        self.classifier_red.set_model("../../training/red/bins/model_red.bin")
        self.classifier_grn.set_model("../../training/grn/bins/model_grn.bin")
        self.classifier_foreign.set_model("../../training/foreign/bins/model_foreign.bin")
        self.classifier_damaged.set_model("../../training/damaged/bins/model_damaged.bin")
        self.classifier_chalky.calibrate([[190, 255],[190, 255],[180, 255]])
        
        
        

    def classify(self):
        self.classifier_foreign.add_dataset(self.sample_directory_extracted_p)
        self.classifier_foreign.classify(self.sample_directory_nforeign, self.sample_directory_foreign)
        print("DONE: foreign material detection.")
        
        self.classifier_paddy.add_dataset(self.sample_directory_nforeign)
        self.classifier_paddy.classify(self.sample_directory_npaddy, self.sample_directory_paddy)
        print("DONE: paddy detection.")
        
        self.classifier_bkn.add_dataset(self.sample_directory_npaddy)
        self.classifier_bkn.classify(self.sample_directory_nbkn, self.sample_directory_bkn)
        print("DONE: broken kernel detection.")
        
        self.classifier_ylw.add_dataset(self.sample_directory_npaddy)
        self.classifier_ylw.classify(self.sample_directory_nylw, self.sample_directory_ylw)
        print("DONE: yellow kernel detection.")
        
        self.classifier_red.add_dataset(self.sample_directory_npaddy)
        self.classifier_red.classify(self.sample_directory_nred, self.sample_directory_red)
        print("DONE: red kernel detection.")
        
        self.classifier_grn.add_dataset(self.sample_directory_npaddy)
        self.classifier_grn.classify(self.sample_directory_ngrn, self.sample_directory_grn)
        print("DONE: immature kernel detection.")
        
        self.classifier_damaged.add_dataset(self.sample_directory_npaddy)
        self.classifier_damaged.classify(self.sample_directory_ndamaged, self.sample_directory_damaged)
        print("DONE: damaged kernel detection.")
        
        self.classifier_chalky.add_grains(self.sample_directory_npaddy)
        self.classifier_chalky.classify(self.sample_directory_nchalky, self.sample_directory_chalky)
        print("DONE: chalky kernel detection.")
        
        self.classifier_sizer.add_dataset(self.sample_directory_nbkn)
        self.count_size = self.classifier_sizer.grain_size_classification(self.classifier_sizer.average_size())
        print("DONE: size classification.")
        
        self.classifier_sizer.find_brewers(self.sample_directory_bkn, self.sample_directory_nbrewer, self.sample_directory_brewer)
        print("DONE: brewer detection.")
        
        
        
        
        self.__generate_report()
        
    def __generate_report(self):
        report = ""
        self.count_bkn = len(os.listdir(self.sample_directory_bkn))
        self.count_nbkn = len(os.listdir(self.sample_directory_nbkn))
        self.count_grn = len(os.listdir(self.sample_directory_grn))
        self.count_ngrn = len(os.listdir(self.sample_directory_ngrn))
        self.count_ylw = len(os.listdir(self.sample_directory_ylw))
        self.count_nylw = len(os.listdir(self.sample_directory_nylw))
        self.count_damaged = len(os.listdir(self.sample_directory_damaged))
        self.count_ndamaged = len(os.listdir(self.sample_directory_ndamaged))
        self.count_foreign = len(os.listdir(self.sample_directory_foreign))
        self.count_nforeign = len(os.listdir(self.sample_directory_nforeign))
        self.count_chalky = len(os.listdir(self.sample_directory_chalky))
        self.count_nchalky = len(os.listdir(self.sample_directory_nchalky))
        self.count_paddy = len(os.listdir(self.sample_directory_paddy))
        self.count_npaddy = len(os.listdir(self.sample_directory_npaddy))
        self.count_total = len(os.listdir(self.sample_directory_nforeign))
        self.count_red = len(os.listdir(self.sample_directory_red))
        self.count_nred = len(os.listdir(self.sample_directory_nred))
        self.count_nbrewer = len(os.listdir(self.sample_directory_nbrewer))
        self.count_brewer = len(os.listdir(self.sample_directory_brewer))
        
        self.__counts = {"bkn":self.count_bkn/self.count_total,
                       "brewer":self.count_brewer/self.count_total,
                       "grn":self.count_grn/self.count_total,
                       "ylw":self.count_ylw/self.count_total,
                       "damaged":self.count_damaged/self.count_total,
                       "foreign":self.count_foreign/self.count_total,
                       "chalky":self.count_chalky/self.count_total,
                       "paddy":self.count_paddy/self.count_total,
                       "red":self.count_red/self.count_total}
        
        report += "{:25} {:10}{:15.1%}\n".format("BROKEN: ", self.count_bkn, self.__counts["bkn"])
        report += "{:25} {:10}{:15.1%}\n".format("BREWERS: ", self.count_brewer, self.__counts["brewer"])
        report += "{:25} {:10}{:15.1%}\n".format("IMMATURE/GREEN: ", self.count_grn, self.__counts["grn"])
        report += "{:25} {:10}{:15.1%}\n".format("FERMENTED/YELLOW: ", self.count_ylw, self.__counts["ylw"])
        report += "{:25} {:10}{:15.1%}\n".format("DAMAGED: ", self.count_damaged, self.__counts["damaged"])
        report += "{:25} {:10}{:15.1%}\n".format("FOREIGN MATERIALS: ", self.count_foreign, self.__counts["foreign"])
        report += "{:25} {:10}{:15.1%}\n".format("CHALKY: ", self.count_chalky, self.__counts["chalky"])
        report += "{:25} {:10}{:15.1%}\n".format("PADDY: ", self.count_paddy, self.__counts["paddy"])
        report += "{:25} {:10}{:15.1%}\n".format("RED: ", self.count_red, self.__counts["red"])
        report += "{:25} {:10.2f}mm{:>13}\n".format("SIZE: ", self.count_size[0], self.count_size[1])
        report += "\n{:25} {:10}\n".format("TOTAL GRAIN COUNT: ", self.count_total)
        self.report = report
        print(report)
        self.show_report()
        
    def show_report(self):
        #font_mono = tkFont.Font(family='Consolas', size=15, weight='bold')
        self.__root = tk.Tk()
        self.__root.title("Grade Report")
        self.__root_frame1 = ttk.Frame(self.__root, padding=50)
        self.__root_frame1.grid(column=0, row=0)
        self.__root_frame2 = ttk.Frame(self.__root, padding=50)
        self.__root_frame2.grid(column=1, row=0)
        ttk.Label(self.__root_frame1, text=self.report, font='TkFixedFont', justify=tk.LEFT).pack()
        self.__root.attributes("-fullscreen", True)
        ttk.Label(self.__root_frame2, text=self.__grade()[0], font='TkFixedFont', justify=tk.LEFT).pack()
        self.__btn_close = tk.Button(self.__root_frame2, text="BACK", command=self.__btn_close)
        self.__btn_close.pack()
        self.__root.mainloop()
        
    def __btn_close(self):
        self.__root.destroy()
        
    def __grade(self):
        grade = ["PREMIUM", "GRADE 1", "GRADE 2", "GRADE 3", "GRADE 4", "GRADE 5"]
        grade_structure = {"bkn" : [5.0, 10.0, 15.0, 25.0, 35.0, 45.0],
                           "brewer" : [0.10, 0.20, 0.40, 0.60, 1.00, 2.00],
                           "grn" : [0.20, 0.30, 0.50, 2.00, 2.00, 2.00],
                           "ylw" : [0.50, 0.70, 1.00, 3.00, 5.00, 8.00],
                           "damaged" : [0.50, 0.70, 1.00, 1.50, 2.00, 3.00],
                           "chalky" : [4.00, 5.00, 7.00, 7.00, 10.00, 15.00],
                           "red" : [1.00, 2.00, 4.00, 5.00, 5.00, 7.00],
                           "foreign" : [0.025, 0.10, 0.15, 0.17, 0.20, 0.25],
                           "paddy" : [10.00, 15.00, 20.00, 25.00, 25.00, 25.00]}
        grade_report = "{:<10}{:>15}{:>15}{:>10}\n".format("GRAIN", "PERCENTAGE", "GRADE POINT", "GRADE")
        
        max_step = 0
        max_step_global = 0
        for count in self.__counts:
            max_step = 0
            basis = grade_structure[count]
            if len(basis) != 0:
                 for i,grade_step in enumerate(basis):
                     if self.__counts[count]*100 > grade_step:
                         max_step = i
            
            else:
                print("No reference data provided")
            
            if max_step > max_step_global:
                max_step_global = max_step
            
            grade_report += "{:<10}{:>15.2%}{:>15.2%}{:>10}\n".format(count, self.__counts[count], (grade_structure[count])[max_step]/100, grade[max_step])
            
            
        print(grade_report)
        return(grade_report, grade[max_step])
                         
        
        
        
        
        
        
        
        
        
        for percentage in self.__counts:
            print(percentage)
        
       
        
        
        
if __name__ == "__main__":
    grader = Grader()
    grader.classify()
    #grader.classify_HOG()
    
