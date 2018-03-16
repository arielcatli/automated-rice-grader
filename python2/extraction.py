import cv2
import numpy as np
from math import ceil

def extract(sample_image_directory, sample_directory_extracted_e, sample_directory_extracted_p, start):
    ret_image = cv2.imread(sample_image_directory)
    sample_image = cv2.imread(sample_image_directory)
    sample_image = cv2.cvtColor(sample_image, cv2.COLOR_BGR2GRAY)
    sample_image = cv2.medianBlur(sample_image, 7)
    sample_image = cv2.threshold(sample_image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    canny_sample_image = cv2.Canny(sample_image[1], 128, 255)
    #cv2.imshow("Sample", canny_sample_image)
        
    original_image = cv2.imread(sample_image_directory)
    contours = cv2.findContours(canny_sample_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = np.array(contours)
    original_image = cv2.imread(sample_image_directory)
    cv2.drawContours(sample_image[1], contours[0], -1, (0,0,255), 1)
    #cv2.imshow("Sample", original_image)
      
   
    #cv2.imshow("Platform", platform)
    grain_count = 0
    grain_list_masked = []
    grain_list_platform = []
    for (i, contour) in enumerate(contours[0]):
        platform = np.zeros([128,64,3], np.uint8)
        (x,y,w,h) = cv2.boundingRect(contour)
        if h > 10:
            grain_mask = sample_image[1][y:y+h, x:x+w]
            #cv2.imshow(str(i),grain_mask)
            grain = original_image[y:y+h, x:x+w]
            #mask = np.zeros(grain[:2], np.uint8)
            masked = cv2.bitwise_and(grain, grain, mask = grain_mask)
            if(masked.shape[1] > 10):
                grain_list_masked.append(sample_directory_extracted_e+"e"+str(i+start)+".jpg")
                cv2.imwrite(sample_directory_extracted_e+"/e"+str(i+start)+".jpg", masked)
                grain_count += 1
                
                
            if(platform.shape[0] >= masked.shape[0] and platform.shape[1] >= masked.shape[1] and masked.shape[1] > 10):
                vertical_offset = int(ceil((platform.shape[0] - masked.shape[0])/2))
                horizontal_offset = int(ceil((platform.shape[1] - masked.shape[1])/2))
                platform[vertical_offset:(vertical_offset+masked.shape[0]), horizontal_offset:(horizontal_offset+masked.shape[1])] = masked
                grain_list_platform.append(sample_directory_extracted_p+"p"+str(i+start)+".jpg")
                cv2.imwrite(sample_directory_extracted_p+"/p"+str(i+start)+".jpg", platform)
                
            
        else:
            pass
        
    
    print "The grain count is " + str(grain_count)
    return [grain_count, grain_list_masked, grain_list_platform]
   

if __name__ == "__main__":
    extract("../img-src/29/29.jpg", "../img-src/29/extracted", 40)
    
