import cv2
import numpy as np
import serial
 
video_file = r"C:\Users\Alex Chen\Google Drive (yoyohc10@g.ucla.edu)\Fourth Year 2021-2022\Winter Quarter\ECE183DA\algorithms\Small Fire Video_Trim.mp4"
video = cv2.VideoCapture(video_file)
# ser = serial.Serial('COM5')
 
while True:
    (grabbed, frame) = video.read()
    if not grabbed:
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
    cv2.imshow("output", output)
    # print("output:", frame)
    if int(no_red) > 20000:
        print ('Fire detected')
    #     ser.write(b'A')
    #print(int(no_red))
   #print("output:".format(mask))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
video.release()
