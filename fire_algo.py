#########################
#ECE 183DA Team Melpomene 
#########################
#Fire algorithm that interacts with the controls algorithm

import numpy as np
import cv2
import time
import motor_control_v2 as motor_control
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera

#STATES
DATACOLL = 0 
EXT = 1
RESET = 2

#masking function
def create_mask_for_plant(image):
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_hsv = np.array([0,105,255]) #used to [0,0,250]
    upper_hsv = np.array([30,220,255]) #used to [30,220,250]
    
    mask = cv2.inRange(image_hsv, lower_hsv, upper_hsv)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    return mask

#image segmentation function
def segment_image(image):
    mask = create_mask_for_plant(image)
    output = cv2.bitwise_and(image, image, mask = mask)
    return output/255

#sharpen the image
def sharpen_image(image):
    image_blurred = cv2.GaussianBlur(image, (0, 0), 3)
    image_sharp = cv2.addWeighted(image, 1.5, image_blurred, -0.5, 0)
    return image_sharp

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (480, 480) #(640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(480, 480))
# allow the camera to warmup
time.sleep(0.1)

#initialize GPIO
servo1, servo2 = motor_control.gpio_setup()
motor_control.startup() #indicate the system is starting up
count = 0
caps = 0
activated = False
motor_control.turn_motor(servo1, servo2, None, DATACOLL, activated) #DATA COLLECTION
# capture frames from the camera
try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        print("Count = " + str(count) + "; Captures = " + str(caps))
        # if count >= 10:
        #     break
        img = frame.array
        rawCapture.truncate(0)
        image_mask = create_mask_for_plant(img)
        #segmentation
        image_segmented = segment_image(img)
        #sharpen the image
        kernel_dilation = np.ones((3,3), np.uint8)
        dilation = cv2.dilate(image_mask, kernel_dilation, iterations=14)
        ret, thresh = cv2.threshold(dilation, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            state = 1 #extinguish
            cnt = contours[0]
            max_area = cv2.contourArea(cnt)
            for cont in contours:
                if cv2.contourArea(cont) > max_area:
                    cnt = cont
                    max_area = cv2.contourArea(cont)

            cv2.drawContours(img, [cnt], 0, (255, 255, 0), 3)
            x,y,w,h = cv2.boundingRect(cnt)
            coords = [x, y, w, h]
            activated = motor_control.position_handler(servo1, servo2, coords, activated)
            # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            # cv2.imwrite("results/result" + str(caps) +".jpg", img)
            # print("wrote image")
            caps += 1
        count += 1
    motor_control.cleanup()
    cv2.destroyAllWindows()

except KeyboardInterrupt:
    motor_control.cleanup()
    cv2.destroyAllWindows()