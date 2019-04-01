''' To produce images of every frame in a video '''

import cv2
import math
import os

count = 0
videoFile = "video.mp4"
cap = cv2.VideoCapture(videoFile)  
frameRate = cap.get(5) 
x=1
while(cap.isOpened()):
    frameId = cap.get(1) 
    ret, frame = cap.read()
    if (ret != True):
        break
    if (frameId % math.floor(frameRate) == 0):
        filename ="frame%d.jpg" % count;count+=1
        cv2.imwrite(filename, frame)
cap.release()
print ("Done!")