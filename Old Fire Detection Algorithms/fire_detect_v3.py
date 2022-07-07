#########################
#ECE 183DA Team Melpomene 
#########################
#3rd iteration of fire detection model that now applies a haar classifier to our code
#Puts a bounding box around fires in the frame
#however, this only works with the stuff we trained it on, so not all fires will work
#1st iteration was too rudimentary and only relied on the color
import numpy as np
import cv2
import time

def make_720p():
    cap.set(3, 1280)
    cap.set(4, 720)

def make_480p():
    cap.set(3, 640)
    cap.set(4, 480)

xml_path = r"C:\Users\Alex Chen\Google Drive (yoyohc10@g.ucla.edu)\Fourth Year 2021-2022\Winter Quarter\ECE183DA\algorithms\Fire Detection Algorithm\cascade.xml"
fire_cascade = cv2.CascadeClassifier(xml_path) #xml is the parameters of our classifier

video_file = r"C:\Users\Alex Chen\Google Drive (yoyohc10@g.ucla.edu)\Fourth Year 2021-2022\Winter Quarter\ECE183DA\algorithms\Fire Detection Algorithm\tree_fire_Trim.mp4"
cap = cv2.VideoCapture(video_file) #start video capturing
count = 0
while cap.isOpened():
    # make_480p()
    ret, img = cap.read() #capture a frame
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #convert image to grayscale
    #detectmultiscale returns a list of rectangles that are detected as fires
    fire = fire_cascade.detectMultiScale(gray, 12, 5) #detectMultiScale expects a grayscale image. Can try with img instead of gray
    for (x,y,w,h) in fire: #(x,y) is the coordinate of the top left of the bounding box
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) #create bounding box around fire detected
        roi_gray = gray[y:y+h, x:x+w] #roi in grayscale to send to control algo
        roi_color = img[y:y+h, x:x+w] #roi in color to send to control algo
        print( 'Fire area is ' + str(w*h) + ' pixels squared') 
        print( 'Center of fire is at pixel coordinates ' + str([(x+(x+w))/2, (y+(y+h))/2])) #take middle of rectangle width and the bottom of the box as coordinates
        count = count + 1
        time.sleep(0.2) #wait
        

    cv2.imshow('img', img)
    k = cv2.waitKey(100) & 0xff #press escape to exit the camera
    if k == 27:
       break

cap.release()
cv2.destroyAllWindows()