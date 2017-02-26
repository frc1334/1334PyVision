from __future__ import print_function
from networktables import NetworkTables
from threading import Thread
import cv2
import numpy as np
import datetime
import argparse

#FPS measuring class
class FPS:
    #init with a start time, end time, and frame counter
    def __init__(self):
        self._start = None
        self._end = None
        self._numFrames = 0
    #set the start time when called
    def start(self):
        self._start = datetime.datetime.now()
        return self
    #set the stop time when called
    def stop(self):
        self._end = datetime.datetime.now()
    #increment the numbe of frames processed
    def update(self):
        self._numFrames += 1
    #calculate elapsed time
    def elapsed(self):
        return(self._end - self._start).total_seconds()
    #calculate FPS
    def fps(self):
        return self._numFrames / self.elapsed()
    #separate thread for image grabbing
class WebcamVideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(10,0)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
    def start(self):
        Thread(target=self.update, args=()).start()
        return self
    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()
    def read(self):
        return self.frame
    def stop(self):
        self.stopped = True
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--display", type = int, default = -1, help ="Whether or not frames should be displayed")
args = vars(ap.parse_args())
def nothing(x):
    pass
cv2.namedWindow('HSV Threshold')
Lh,Ls,Lv = 0,0,0
Hh,Hs,Hv = 180,255,255
#trackbars for tuning at events

cv2.createTrackbar('High hue', 'HSV Threshold',Hh,180,nothing)
cv2.createTrackbar('High saturation', 'HSV Threshold',Hs,255,nothing)
cv2.createTrackbar('High value', 'HSV Threshold',Hv,255,nothing)
cv2.createTrackbar('Low hue', 'HSV Threshold',Lh,179,nothing)
cv2.createTrackbar('Low saturation', 'HSV Threshold',Ls,255,nothing)
cv2.createTrackbar('Low value', 'HSV Threshold',Lv,255,nothing)
NetworkTables.initialize(server='10.13.34.2')

Pitable = NetworkTables.getTable('Pitable')
print("[INFO] sampling THREADED frames from webcam")
vs = WebcamVideoStream(src=0).start()
while (vs.stream.isOpened()):
    frame = vs.read()
    if args["display"] > 0:
        #trackbars for tuning at events
        Hh = cv2.getTrackbarPos('High hue','HSV Threshold')
        Hs = cv2.getTrackbarPos('High saturation','HSV Threshold')
        Hv = cv2.getTrackbarPos('High value','HSV Threshold')
        Lh = cv2.getTrackbarPos('Low hue','HSV Threshold')
        Ls = cv2.getTrackbarPos('Low saturation','HSV Threshold')
        Lv = cv2.getTrackbarPos('Low value','HSV Threshold')
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blue = (Lh,Ls,Lv)#60,0,150
        upper_blue = (Hh,Hs,Hv)#95,255,255
        mask = cv2.inRange(hsv,lower_blue,upper_blue)
        blur = cv2.medianBlur(mask,5)
        kernel = np.ones((2,2),np.uint8)
        dilation = cv2.dilate(blur,kernel,iterations = 1)
        erosion = cv2.erode(dilation,kernel,iterations = 1)
        _, contours , heirarchy = cv2.findContours(erosion,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        valid = []
        Avalid = []
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            a = cv2.contourArea(c)
            if(a>650):
                Avalid.append(c)
        Avalid.sort(key=lambda x: cv2.contourArea(x), reverse = True)
      
        for a in range(len(Avalid)):
            print(cv2.matchShapes(Avalid[a],Avalid[(a+1)%len(Avalid)],1,parameter = 0))
            if(cv2.matchShapes(Avalid[a],Avalid[(a+1)%len(Avalid)],1,parameter = 0)<0.15):
                valid.append(Avalid[a])
                valid.append(Avalid[(a+1)%len(Avalid)])
    
        """
        int a = x+w/2
        int b = x+w/2
        int c = (a+b)/2
        """
        #cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)

        validcontours = 0
        for c in range(len(valid)):
            x,y,w,h = cv2.boundingRect(valid[c])
            validcontours= validcontours + 1
            cv2.drawContours(frame,valid[c],-1,(0,0,255),1)
            if(c%2 == 0):
                Pitable.putNumber('x', x)
                Pitable.putNumber('y', y)
                Pitable.putNumber('w', w)
                Pitable.putNumber('h', h)
                Pitable.flush()
            if(c%2 == 1): 
                Pitable.putNumber('x2', x)
                Pitable.putNumber('y2', y)
                Pitable.putNumber('w2', w)
                Pitable.putNumber('h2', h)
                Pitable.flush()
                
        #cv2.imshow('blurcontour', frame)   
        
        print(validcontours)
        
        key = cv2.waitKey(30) &0xFF
        if key == 27:
            break
"""    
print("[INFO]elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO]approx. FPS: {:.2f}".format(fps.fps()))

 
"""
vs.stop()
cv2.destroyAllWindows()
print('end')




