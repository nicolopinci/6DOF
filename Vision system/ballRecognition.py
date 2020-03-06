#!/Users/vebjorn/anaconda3/envs/opencv-env python
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import cv2
from collections import deque
import imutils
from datetime import datetime

cap = cv2.VideoCapture(0)

bufflen  = 20;
pts = deque(maxlen=bufflen)

currentX = 0
currentY = 0
previousX = 0
previousY = 0

deltaX = 0
deltaY = 0

initialTime = datetime.now()

while(True):
    
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    blurred = cv2.GaussianBlur(frame,(11, 11),0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV) 
      
    # Threshold of red in HSV space
    lower_red_low = np.array([0, 100, 100]) 
    lower_red_up = np.array([10, 255, 255]) 
    
    upper_red_low = np.array([160, 100, 100]) 
    upper_red_up = np.array([179, 255, 255])
   
    # preparing the mask to overlay 
    mask1 = cv2.inRange(hsv, lower_red_low, lower_red_up)
    mask2 = cv2.inRange(hsv, upper_red_low, upper_red_up)
    
    mask = cv2.bitwise_or(mask1,mask2)
    
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None    
    
    # only proceed if at least one contour was found
    if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
		# only proceed if the radius meets a minimum size
        if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
	# update the points queue
    pts.appendleft(center)
    
    # loop over the set of tracked points
    for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
        if pts[i - 1] is None or pts[i] is None:
            continue
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
        thickness = int(np.sqrt(bufflen / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
      
    # Display the resulting frame
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 711,600)
    cv2.imshow('image',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if center is not None:
        previousX = currentX
        previousY = currentY
        
        currentX = center[0]
        currentY = center[1]
        
        deltaX = currentX - previousX
        deltaY = currentY - previousY
        
        deltaT = (datetime.now() - initialTime).total_seconds()
        
        deltaVx = deltaX/deltaT
        deltaVy = deltaY/deltaT
            
        initialTime = datetime.now()
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()