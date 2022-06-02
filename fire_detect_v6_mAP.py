#########################
#ECE 183DA Team Melpomene 
#########################
#6th iteration of fire detection model that sends coordinates to the control algorithm

import numpy as np
import cv2
import time
import os

def pascal_writer (filename, xmin, ymin, width, height):
    # create pascal voc writer (image_path, width, height)
    filename = os.path.splitext(filename)[0]
    with open('review_object_detection_metrics/detections/' + filename + '.txt', 'w') as f:
        write_path = 'fire 100 {} {} {} {}\n'.format(xmin, ymin, width, height)
        f.write(write_path)

def make_720p():
    cap.set(3, 1280)
    cap.set(4, 720)

def make_480p():
    cap.set(3, 640)
    cap.set(4, 480)

def iterate_state(state):
    #state 0 = data collection
    #state 1 = extinguish
    #state 2 = reset
    if state == 2:
        state = 0
        return state
    state += 1
    return state

state = 0 #data collection
xml_path = r"C:\Users\Alex Chen\Google Drive (yoyohc10@g.ucla.edu)\Fourth Year 2021-2022\Winter Quarter\ECE183DA\algorithms\Fire Detection Algorithm\cascades\20_300_18.xml"
fire_cascade = cv2.CascadeClassifier(xml_path) #xml is the parameters of our classifier

pos_dir = r"C:\Users\Alex Chen\Google Drive (yoyohc10@g.ucla.edu)\Fourth Year 2021-2022\Winter Quarter\ECE183DA\algorithms\review_object_detection_metrics\firenet\images"
sorted = os.listdir(pos_dir)
print(sorted)
# cap = cv2.VideoCapture(video_file) #start video capturing
for filename in sorted:    # make_480p()
    file = os.path.join(pos_dir, filename)
    img = cv2.imread(file) 
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
            # img[y:y+h, x:x+w,:] = output[y:y+h, x:x+w,:]
            pascal_writer(filename, x,y,w,h)
            fire_present = True
            print( 'Fire area is ' + str(w*h) + ' pixels squared') 
            print( 'Center of fire is at pixel coordinates ' + str([int((x+(x+w))/2), int((y+(y+h))/2)])) #take middle of rectangle width and the bottom of the box as coordinates
        else:
            fire_present = False
        # print(img[int((x+(x+w))/2), int((y+(y+h))/2)])
        # time.sleep(0.2) #wait
        

    # cv2.imshow('img', img)
    # k = cv2.waitKey(100) & 0xff #press escape to exit the camera
    # if k == 27:
    #    break

# cap.release()
cv2.destroyAllWindows()