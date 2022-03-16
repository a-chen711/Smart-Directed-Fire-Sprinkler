#########################
#ECE 183DA Team Melpomene 
#########################
#3rd iteration of fire detection model that now applies a haar classifier to our code
#Puts a bounding box around fires in the frame
#however, this only works with the stuff we trained it on, so not all fires will work
#1st iteration was too rudimentary and only relied on the color
import numpy as np
import cv2
import serial
import time

xml_path = r"C:\Users\Alex Chen\Google Drive (yoyohc10@g.ucla.edu)\Fourth Year 2021-2022\Winter Quarter\ECE183DA\algorithms\Fire Detection Algorithm\cascade.xml"
fire_cascade = cv2.CascadeClassifier(xml_path) #xml is the parameters of our classifier

video_file = r"C:\Users\Alex Chen\Google Drive (yoyohc10@g.ucla.edu)\Fourth Year 2021-2022\Winter Quarter\ECE183DA\algorithms\Fire Detection Algorithm\tree_fire_Trim.mp4"
cap = cv2.VideoCapture(video_file) #start video capturing
count = 0
while cap.isOpened():
    ret, img = cap.read() #capture a frame
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #convert image to grayscale
    fire = fire_cascade.detectMultiScale(img, 12, 5) #test for fire detection
    for (x,y,w,h) in fire:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) #highlight the area of image with fire
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        print( 'Fire is detected..!' + str(count)) 
        count = count + 1
        # ser1.write(str.encode('p')) #write 'p' on serial COM port to arduino
        time.sleep(0.2) #wait
        
    cv2.imshow('img', roi_color)
    # ser1.write(str.encode('s')) #write 's' if there is no fire
    k = cv2.waitKey(100) & 0xff
    if k == 27:
       break

# ser1.close()
cap.release()
cv2.destroyAllWindows()