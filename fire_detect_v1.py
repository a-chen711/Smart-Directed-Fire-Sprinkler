#########################
#ECE 183DA Team Melpomene 
#########################
#1st iteration of fire detection model that has rudimentary threshold-based
#fire-detection in the HSV colorspace

import cv2
import numpy as np
import serial
 
video_file = r"C:\Users\Alex Chen\Google Drive (yoyohc10@g.ucla.edu)\Fourth Year 2021-2022\Winter Quarter\ECE183DA\algorithms\Fire Detection Algorithm\tree_fire_Trim.mp4"
video = cv2.VideoCapture(1)
# ser = serial.Serial('COM5')
print(video.read())
while (video.isOpened()):
    (grabbed, frame) = video.read()
    if not grabbed:
        print("breaking")
        break
 
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
    
    output = cv2.bitwise_and(frame, hsv, mask=mask)
    no_red = cv2.countNonZero(mask)

    # print("output:", frame)
    # print(no_red)
    if int(no_red) > 40000:
        print ('Fire detected')
        # cv2.imshow("output", output)
    #     ser.write(b'A')
    cv2.imshow("output", hsv)
    print(int(no_red))
   #print("output:".format(mask))
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
video.release()