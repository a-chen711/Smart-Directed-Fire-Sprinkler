#########################
#ECE 183DA Team Melpomene 
#########################
#7th iteration of fire detection model that uses purely contours and a strict color range for fires

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

#SINGLE IMAGE TEST#
#get an image
def image_test():
    image_file = r"C:\Users\Alex Chen\Google Drive (yoyohc10@g.ucla.edu)\Fourth Year 2021-2022\Winter Quarter\ECE183DA\algorithms\Fire Detection Algorithm\img (31).jpg"
    img = cv2.imread(image_file) 
    #mask
    image_mask = create_mask_for_plant(img)
    #segmentation
    image_segmented = segment_image(img)
    #sharpen the image
    # image_sharpen = sharpen_image(image_segmented)

    cv2.imshow("image", image_mask)
    cv2.waitKey(0)
###################

# # function to get an image
# def read_img(filepath, size):
#     data_folder = "haar_trainer\008_cascade_classifier\fire-dataset\train\images"
#     img = image.load_img(os.path.join(data_folder, filepath), target_size=size)
#     #convert image to array
#     img = image.img_to_array(img)
#     return img



# cv2.imwrite("test.jpg", img)
# cv2.imwrite("image_seg.jpg", image_segmented)
# cv2.imwrite("image_sharpen.jpg", image_sharpen)

# fig, ax = plt.subplots(1, 4, figsize=(10, 5));
# plt.suptitle('SAMPLE PROCESSED IMAGE', x=0.5, y=0.8)
# plt.tight_layout()

# ax[0].set_title('ORIG.', fontsize=12)
# ax[1].set_title('MASK', fontsize=12)
# ax[2].set_title('SEGMENTED', fontsize=12)
# ax[3].set_title('SHARPEN', fontsize=12)


# ax[0].imshow((img/255).astype('uint8'));
# ax[1].imshow(image_mask.astype('uint8'));
# ax[2].imshow(image_segmented.astype('uint8'));
# ax[3].imshow(image_sharpen.astype('uint8'));

video_file = r"C:\Users\Alex Chen\Google Drive (yoyohc10@g.ucla.edu)\Fourth Year 2021-2022\Winter Quarter\ECE183DA\algorithms\Fire Detection Algorithm\tree_fire_Trim.mp4"

cap = cv2.VideoCapture(video_file) #start video capturing
while cap.isOpened():
    # make_480p()
    ret, frame = cap.read() #capture a frame
    image_mask = create_mask_for_plant(frame)
    #segmentation
    image_segmented = segment_image(frame)
    #sharpen the image
    # image_sharpen = sharpen_image(image_segmented)
    # cv2.imshow('img', image_segmented)
    contours, hierarchy = cv2.findContours(image_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(frame, contours, -1, 255, 3)

        # find the biggest countour (c) by the area
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)

        # draw the biggest contour (c) in green
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        no_red = cv2.countNonZero(image_mask[y:y+h, x:x+w]) #count number of fire pixels within the bounding box frame
        print(no_red)
        if no_red > 200:
            print( 'Fire area is ' + str(w*h) + ' pixels squared') 
            print( 'Center of fire is at pixel coordinates ' + str([int((x+(x+w))/2), int((y+(y+h))/2)])) #take middle of rectangle width and the bottom of the box as coordinates
    # show the images
    cv2.imshow("Result", frame)
    k = cv2.waitKey(100) & 0xff #press escape to exit the camera
    if k == 27:
       break