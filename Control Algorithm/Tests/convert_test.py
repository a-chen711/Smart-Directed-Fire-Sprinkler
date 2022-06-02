import math
#########################
#ECE 183DA Team Melpomene 
#########################
#8th iteration of fire detection model that uses purely contour detection and dilation to bridge gaps between small contours

import numpy as np
import cv2
import time
import os
import matplotlib.pyplot as plt

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

async def main():
    video_file = r"C:\Users\Alex Chen\Google Drive (yoyohc10@g.ucla.edu)\Fourth Year 2021-2022\Winter Quarter\ECE183DA\algorithms\Fire Detection Algorithm\fire_fighter.mp4"
    hor_res = 1280
    vert_res = 720
    vert_center = vert_res/2 #center pixel vertically CHANGE THIS
    hor_center = hor_res/2 #center pixel horizontally CHANGE THIS
    height_constant = 1 #depends on the resolution CHANGE

    cap = cv2.VideoCapture(video_file) #start video capturing
    while cap.isOpened():
        # make_480p()
        ret, img = cap.read() #capture a frame
        image_mask = create_mask_for_plant(img)
        #segmentation
        image_segmented = segment_image(img)
        #sharpen the image
        kernel_dilation = np.ones((3,3), np.uint8)
        dilation = cv2.dilate(image_mask, kernel_dilation, iterations=14)
        ret, thresh = cv2.threshold(dilation, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            cnt = contours[0]
            max_area = cv2.contourArea(cnt)
            for cont in contours:
                if cv2.contourArea(cont) > max_area:
                    cnt = cont
                    max_area = cv2.contourArea(cont)

            cv2.drawContours(img, [cnt], 0, (255, 255, 0), 3)
            # # draw in blue the contours that were founded
            # cv2.drawContours(img, contours, -1, 255, 3)
            
            # # find the biggest countour (c) by the area
            # c = max(cnt, key = cv2.contourArea)
            x,y,w,h = cv2.boundingRect(cnt)

            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.line(img, (int(hor_center),int(vert_center)), (x,y), (255,0,0), 3)
            #define the min and max as some percentage rather than the actual .min()
            # azimuth = math.atan((x - hor_center)/height_constant) #angle along the horizontal axis
            # elevation = math.atan((y - vert_center)/height_constant) #angle along the vertical axis
            # hor_percent = azimuth/(math.pi*0.7)
            # vert_percent = elevation/(math.pi*0.7)
                

            #Normalized distance between box and center pixel between 0-90 degrees
            azimuth = ((x - hor_center)/hor_center)*45 #angle along the horizontal axis
            elevation = -((y - vert_center)/vert_center)*45 #angle along the vertical axis (negative because pixel values grow downwards)

            #for sweeping implementation, you can use the width and height and just use those as boundaries



            hor_percent = azimuth/45
            vert_percent = elevation/45
            # servo1.start(0)
            # servo2.start(0)"
            print("azi: " + str(azimuth) + "; x: " + str(x) + "; elev: " + str(elevation) + "; y: " + str(y))
        # show the images
        cv2.imshow("Result", img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        # k = cv2.waitKey(0) & 0xff #press escape to exit the camera
        # if k == 27:
        #    break
main()


