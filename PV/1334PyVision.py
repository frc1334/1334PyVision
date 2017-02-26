'''
Created on Feb 11, 2017

@author: FRC1334
'''
import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while(1):
    # Take each frame
    (ignore,frame) = cap.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([90,30,40])
    upper_blue = np.array([100,50,255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    _, contours , heirarchy = cv2.findContours(mask,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    
    
    cv2.imshow('frame',frame)
    cv2.drawContours(frame,contours,-1,(255,255,0),1)
    cv2.imshow('mask',mask)
    cv2.imshow('contours',frame)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()