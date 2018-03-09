from picamera import PiCamera
import cv2
import os
from extraction import extract

class Sample:
    def __init__(self):
        #constants
        self.DIR_SAMPLE = "/home/pi/grader/img-src"
        self.DIR_LOG_FILE = "/home/pi/grader/img-src/log.txt"
        
        #metadata
        self.sample_id = ""
        self.sample_directory = ""
        self.sample_directory_extracted = ""
        self.sample_image = ""
        self.sample_image_id = ""
        self.sample_count = ""
        
        #housekeeping
        self.check_src_dir()
        self.check_sample_log()
        self.__generate_id()
        print("Generated sample ID: " + str(self.sample_id))
        print("Last sample ID: " + str(self.get_last_sample_id()));
        if self.__create_sample_directory():
            print("The directory: " + self.sample_directory + " was created.")
        else:
            print("The directory: " + self.sample_directory + " already exists.")
        self.__update_log_file()
        
        #capture
        self.capture()

        #extraction
        #self.__extract()
        
    def check_src_dir(self):
        if not os.path.exists(self.DIR_SAMPLE):
            os.mkdir(self.DIR_SAMPLE, 0o777)

    def capture(self):
        camera = PiCamera()
        self.sample_image_id = self.sample_directory + "/" + str(self.sample_id) + ".jpg"
        camera.capture(self.sample_image_id)
        camera.close()
        #self.extract_grains
        #self.image = cv2.imread(

    def __create_sample_directory(self):
        if os.path.exists(self.sample_directory):
            return False
        else:
            os.mkdir(self.sample_directory)
            self.sample_directory_extracted = self.sample_directory + "/extracted/"
            os.mkdir(self.sample_directory_extracted)
            return True

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

    def get_last_sample_id(self):
        with open(self.DIR_LOG_FILE, "r") as log_file:
            return log_file.read()
        
    def __update_log_file(self):
        with open(self.DIR_LOG_FILE, "w+") as log_file:
            log_file.write(str(self.sample_id))

    def __extract(self):
        extract(self.sample_image_id, self.sample_directory_extracted)
        
if __name__ == "__main__":
    sample = Sample()
