from picamera import PiCamera
import cv2
import os
from extraction import extract
from extract_grains import extract_grains
import Tkinter as tk
import pickle
import numpy as np

class Capture:
    def __init__(self):
        #constants
        self.DIR_SAMPLE = "/home/pi/automated-rice-grader/img-src"
        self.DIR_LOG_FILE = "/home/pi/automated-rice-grader/img-src/log.txt"
        self.__grain_list_masked = []
        self.__grain_list_platform = []
        
        #housekeeping
        self.check_src_dir()
        self.check_sample_log()
        self.__generate_id()
        self.__create_sample_directory()
        self.__update_log_file()

        #gui
        self.__create_gui()
        

    def __create_gui(self):
        self.__root = tk.Tk()
        self.__root.geometry = "200x200"
        tk.Label(self.__root, text="CURRENT GRAIN COUNT").pack()
        self.__entry_count_str = tk.StringVar()
        self.__entry_count = tk.Entry(self.__root, state="readonly", width=20, textvariable=self.__entry_count_str)
        self.__entry_count.pack()
        self.__btn_ext = tk.Button(self.__root, text="EXTRACT", command=self.__start_capture)
        self.__btn_ext.pack()
        self.__btn_cancel = tk.Button(self.__root, text="CANCEL", command=self.__exit)
        self.__btn_cancel.pack()        
        self.__root.mainloop()

        
        

    def __exit(self):   
        self.__root_summary.destroy()
        self.__root.destroy()
        self.__generate_report()

    def __generate_report(self):
        self.report_directory_masked= self.sample_directory + "/masked.txt"
        with open(self.report_directory_masked, "w") as report:
            report.write(str(self.__extracted_count)+"\n")
            masked = ""
            for file in self.__grain_list_masked:
                masked += "\n".join(file) + "\n"
            report.write(masked)
            
        self.report_directory_platform = self.sample_directory + "/platform.txt"
        with open(self.report_directory_platform, "w") as p_report:
            p_report.write(str(self.__extracted_count)+"\n")
            platform = ""
            for file in self.__grain_list_platform:
                platform += "\n".join(file) + "\n" 
            p_report.write(platform)
            
        
        
    def __start_capture(self):
        camera = PiCamera()
        current = self.sample_directory + "/" + str(self.whole_sample) + ".jpg"
        camera.capture(current)
        self.whole_sample += 1
        camera.close()
#        self.__extr = extract(current, self.sample_directory_extracted_e, self.sample_directory_extracted_p, self.__extracted_count)
        self.__extr = extract(current, self.sample_directory_extracted_e, self.sample_directory_extracted_p, self.__extracted_count)
        self.__grain_list_masked.append(self.__extr[1])
        self.__grain_list_platform.append(self.__extr[2])
        self.__extracted_count += self.__extr[0]
        self.__entry_count_str.set(str(self.__extracted_count))
        if self.__extracted_count > 100:
            self.__root_summary = tk.Tk()
            self.__root_summary.title("SUMMARY")
            tk.Label(self.__root_summary, text="TOTAL: "+ str(self.__extracted_count)).pack()
            self.__btn_root_ok = tk.Button(self.__root_summary, text="OK", command=self.__exit)
            self.__btn_root_ok.pack()
            self.__root.withdraw()
            self.__root_summary.mainloop()
            
                
        
        

        
    def check_src_dir(self):
        if not os.path.exists(self.DIR_SAMPLE):
            os.mkdir(self.DIR_SAMPLE, 0o777)
            print "DIR: " + self.DIR_SAMPLE + " created"

    def check_sample_log(self):
        if os.path.exists(self.DIR_LOG_FILE):
            print("Log file exists")
        else:
            print("Log file doesn't exists. Creating...")
            with open(self.DIR_LOG_FILE, "a") as log_file:
                log_file.write("0")
                
    def __generate_id(self):
        with open(self.DIR_LOG_FILE, "r") as log_file:
            self.sample_id = int(log_file.read()) + 1
            self.sample_directory = self.DIR_SAMPLE + "/" + str(self.sample_id)
            self.DIR_BIN_FILE = self.sample_directory + "/objects.bin"
            self.whole_sample = self.sample_id
            self.__extracted_count = 0
            print "ID: " + self.sample_directory

    def __create_sample_directory(self):
        if os.path.exists(self.sample_directory):
            return False
        else:
            os.mkdir(self.sample_directory)
            self.sample_directory_extracted = self.sample_directory + "/extracted/"
            os.mkdir(self.sample_directory_extracted)
            self.sample_directory_extracted_e = self.sample_directory_extracted + "e/"
            self.sample_directory_extracted_p = self.sample_directory_extracted + "p/"
            self.sample_directory_bkn = self.sample_directory + "/bkn/"
            self.sample_directory_nbkn = self.sample_directory + "/nbkn/"
            os.mkdir(self.sample_directory_bkn)
            os.mkdir(self.sample_directory_nbkn)
            self.sample_directory_nylw = self.sample_directory + "/nylw/"
            self.sample_directory_ylw = self.sample_directory + "/ylw/"
            os.mkdir(self.sample_directory_ylw)
            os.mkdir(self.sample_directory_nylw)
            self.sample_directory_grn = self.sample_directory + "/grn/"
            self.sample_directory_ngrn = self.sample_directory + "/ngrn/"
            os.mkdir(self.sample_directory_grn)
            os.mkdir(self.sample_directory_ngrn)
            self.sample_directory_npaddy = self.sample_directory + "/npaddy/"
            self.sample_directory_paddy = self.sample_directory + "/paddy/"
            os.mkdir(self.sample_directory_paddy)
            os.mkdir(self.sample_directory_npaddy)
            self.sample_directory_nchalky = self.sample_directory + "/nchalky/"
            self.sample_directory_chalky = self.sample_directory + "/chalky/"
            os.mkdir(self.sample_directory_chalky)
            os.mkdir(self.sample_directory_nchalky)
            self.sample_directory_nforeign = self.sample_directory + "/nforeign/"
            self.sample_directory_foreign = self.sample_directory + "/foreign/"
            os.mkdir(self.sample_directory_nforeign)
            os.mkdir(self.sample_directory_foreign)
            self.sample_directory_ndamaged = self.sample_directory + "/ndamaged/"
            self.sample_directory_damaged = self.sample_directory + "/damaged/"
            os.mkdir(self.sample_directory_ndamaged)
            os.mkdir(self.sample_directory_damaged)
            self.sample_directory_nred = self.sample_directory + "/nred/"
            self.sample_directory_red = self.sample_directory + "/red/"
            os.mkdir(self.sample_directory_nred)
            os.mkdir(self.sample_directory_red)
            
            os.mkdir(self.sample_directory_extracted_e)
            os.mkdir(self.sample_directory_extracted_p)
            print "Created: " + self.sample_directory_extracted
            print "Created: " + self.sample_directory_extracted_e
            print "Created: " + self.sample_directory_extracted_p
            return True

    def __update_log_file(self):
        with open(self.DIR_LOG_FILE, "w+") as log_file:
            log_file.write(str(self.sample_id))
        
if __name__ == "__main__":
    sample = Capture()
