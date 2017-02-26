# 1334PyVision
This python 3 module is meant to be run on a raspberry pi in virtualenv

Instructions for Installing OpenCV 3 on a raspberry pi 3 with raspbian jessie can be found here on Adrian Rosebrock's website:
http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/

The bash script which it is run by (coming soon in this repository) is meant to be added to rc.local in order to run automatically when logged in

Make sure to remove/comment out debugging imshow commands and trackbars to increase performance at competition! Also make sure to set a static IP for your RoboRIO which matches the pynetworktables server you specify in the code.
