import numpy as np
import cv2
import sys
import time

TARGET_COLOR_MIN = np.array([0,100,100], np.uint8)
TARGET_COLOR_MAX = np.array([5,255,255], np.uint8)

def largest(capture):
	W, H = 640, 360
	screenMidX = W/2
	screenMidY = H/2
	speedCirclesDiff = H/12


	running = True
	while running:
		try:
			# This should be an numpy image array
			pixelarray = capture
			if pixelarray != None:
				# Convert RGB to BGR & make OpenCV Image
				frame = pixelarray[:, :, ::-1].copy()

				_frame = np.asarray(frame)
				frameHSV = cv2.cvtColor(_frame, cv2.COLOR_BGR2HSV)
				frameThreshold = cv2.inRange(frameHSV, TARGET_COLOR_MIN, TARGET_COLOR_MAX)

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
					#cv2.drawContours(frame,[cnt],0,(0,0,255),-1)

					# Draw a bounding rectangle
					x,y,w,h = cv2.boundingRect(cnt)
					cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

					# Draw a rotated bounding rectangle
					rect = cv2.minAreaRect(cnt)
					box = cv2.cv.BoxPoints(rect)
					box = np.int0(box)
					cv2.drawContours(frame,[box],0,(0,255,255),2)

					# Draw a circumcircle
					(x,y),radius = cv2.minEnclosingCircle(cnt)
					center = (int(x),int(y))
					radius = int(radius)
					cv2.circle(frame,center,radius,(255,0,255),2)

					# Draw line to center of screen
					cv2.line(frame, (screenMidX, screenMidY), center, (0,0,255),2)

					# Draw Speed Limit Circles and Determine Speed
					diff = speedCirclesDiff # Increment of radius of the Speed Limit Circles

					# Loop for drawing speed circles
					for i in range(1, 10):
						cv2.circle(frame, (screenMidX, screenMidY), diff*i,(0,0,255),2)

					# Center of the object
					x = center[0]
					y = center[1]


				cv2.imshow('Drone', frame)
		except:
			print "Failed"


		# Listen for Q Key Press
		if cv2.waitKey(1) & 0xFF == ord('q'):
			running = False
