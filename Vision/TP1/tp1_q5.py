#!/usr/bin/env python

'''
Track a green ball using OpenCV.

    Copyright (C) 2015 Conan Zhao and Simon D. Levy

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as 
    published by the Free Software Foundation, either version 3 of the 
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License 
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import cv2
import numpy as np

# For OpenCV2 image display
WINDOW_NAME = 'GreenBallTracker' 

def track(image,color):
    
    screenMidX = 1260/2
    screenMidY = 960/2
    speedCirclesDiff = 960/12
    '''Accepts BGR image as Numpy array
       Returns: (x,y) coordinates of centroid if found
                (-1,-1) if no centroid was found
                None if user hit ESC
    '''

    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(image, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    frame = image[:, :, ::-1].copy()
    # Threshold the HSV image for only green colors
    if color=='b':
      lower = np.array([100,150,150])
      upper = np.array([115,250,250])
    elif color=='p':
      lower = np.array([135,50,50])
      upper = np.array([195,200,200])
    elif color=='y':
      lower = np.array([10,100,100])
      upper = np.array([40,255,255])
    else:
      lower = np.array([50,50,50])
      upper = np.array([80,200,200])

    # Threshold the HSV image to get only green colors
    frameThreshold = cv2.inRange(hsv, lower, upper)
				
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))
    frameThreshold = cv2.erode(frameThreshold,element, iterations=1)
    frameThreshold = cv2.dilate(frameThreshold,element, iterations=1)
    frameThreshold = cv2.erode(frameThreshold,element)
				
    # Blurs to smoothen frame
    frameThreshold = cv2.GaussianBlur(frameThreshold,(9,9),2,2)
    frameThreshold = cv2.medianBlur(frameThreshold,5)
    # Find Contours
    contours, hierarchy = cv2.findContours(frameThreshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
				
    showingCNTs = [] # Contours that are visible
    areas = [] # The areas of the contours
				
    # Find Specific contours
    for cnt in contours:
     approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
     #if len(approx)==4:
     area = cv2.contourArea(cnt)
     if area > 300:
      areas.append(area)
      showingCNTs.append(cnt)
				
    # Only Highlight the largest object
    if len(areas)>0:
      m = max(areas)
      maxIndex = 0
      for i in range(0, len(areas)):
       if areas[i] == m:
        maxIndex = i
      cnt = showingCNTs[maxIndex]
					
      # Highlight the Object Red
      cv2.drawContours(image,[cnt],0,(0,0,255),-1)
					
      # Draw a bounding rectangle
      x,y,w,h = cv2.boundingRect(cnt)
      cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
					
      # Draw a rotated bounding rectangle
      rect = cv2.minAreaRect(cnt)
      box = cv2.cv.BoxPoints(rect)
      box = np.int0(box)
      cv2.drawContours(image,[box],0,(0,255,255),2)
					
      # Draw a circumcircle
      (x,y),radius = cv2.minEnclosingCircle(cnt)
      center = (int(x),int(y))
      radius = int(radius)
      cv2.circle(image,center,radius,(255,0,255),2)
					
      # Draw line to center of screen
      #cv2.line(image, (screenMidX, screenMidY), center, (0,0,255),2)
					
      # Draw Speed Limit Circles and Determine Speed
      #diff = speedCirclesDiff # Increment of radius of the Speed Limit Circles
					
      # Loop for drawing speed circles
      #for i in range(1, 10):
       #cv2.circle(frame, (screenMidX, screenMidY), diff*i,(0,0,255),2)
					
      # Center of the object	
      x = center[0]
      y = center[1]	
    else:
      x=0
      y=0
    # Assume no centroid
    ctr = (-1,-1)

    # Use centroid if it exists
    if x != None and y != None:

        ctr = (x, y)

        # Put black circle in at centroid in image
        cv2.circle(image, ctr, 10, (0,0,125), -1)






    # Display full-color image
    cv2.imshow(WINDOW_NAME, image)

    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
        ctr = None
    
    # Return coordinates of centroid
    return ctr

# Test with input from camera
if __name__ == '__main__':
    
    color=raw_input("Entrez votre couleur(blue : b, pink : p,yellow : y,green : g) : ")
    capture = cv2.VideoCapture('ballchap.mp4')

    while True:

        okay, image = capture.read()

        if okay:

            if not track(image,color):
                break
          
            if cv2.waitKey(1) & 0xFF == 27:
                break

        else:

           print('Capture failed')
           break

