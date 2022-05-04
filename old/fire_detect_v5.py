#########################
#ECE 183DA Team Melpomene 
#########################
#5th iteration of fire detection model that now combines the colormasking and haar classifier
#edited the lower and upper bounds for the colormask as well

import numpy as np
import cv2
import time

def make_720p():
    cap.set(3, 1280)
    cap.set(4, 720)

def make_480p():
    cap.set(3, 640)
    cap.set(4, 480)

xml_path = r"C:\Users\Alex Chen\Google Drive (yoyohc10@g.ucla.edu)\Fourth Year 2021-2022\Winter Quarter\ECE183DA\algorithms\Fire Detection Algorithm\cascades\cascade_24_300_18.xml"
fire_cascade = cv2.CascadeClassifier(xml_path) #xml is the parameters of our classifier

video_file = r"C:\Users\Alex Chen\Google Drive (yoyohc10@g.ucla.edu)\Fourth Year 2021-2022\Winter Quarter\ECE183DA\algorithms\Fire Detection Algorithm\Small Fire Video_Trim.mp4"
cap = cv2.VideoCapture(video_file) #start video capturing
while cap.isOpened():
    # make_480p()
    ret, img = cap.read() #capture a frame

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #convert image to grayscale

    blur = cv2.GaussianBlur(img, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    
    lower = [0, 0, 255] #white
    upper = [30, 255, 255] #yellow
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
    
    output = cv2.bitwise_and(img, hsv, mask=mask)
    #detectmultiscale returns a list of rectangles that are detected as fires
    fire = fire_cascade.detectMultiScale(gray, 12, 5) #detectMultiScale expects a grayscale image. Can try with img instead of gray
    for (x,y,w,h) in fire: #(x,y) is the coordinate of the top left of the bounding box
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) #create bounding box around fire detected
        roi_gray = gray[y:y+h, x:x+w] #roi in grayscale to send to control algo
        roi_color = img[y:y+h, x:x+w] #roi in color to send to control algo
        no_red = cv2.countNonZero(mask[y:y+h, x:x+w]) #count number of fire pixels within the bounding box frame
        print(no_red)
        if no_red > 60:
            img[y:y+h, x:x+w,:] = output[y:y+h, x:x+w,:]
            print( 'Fire area is ' + str(w*h) + ' pixels squared') 
            print( 'Center of fire is at pixel coordinates ' + str([int((x+(x+w))/2), int((y+(y+h))/2)])) #take middle of rectangle width and the bottom of the box as coordinates
        # print(img[int((x+(x+w))/2), int((y+(y+h))/2)])
        time.sleep(0.1) #wait
        

    cv2.imshow('img', img)
    k = cv2.waitKey(100) & 0xff #press escape to exit the camera
    if k == 27:
       break

cap.release()
cv2.destroyAllWindows()