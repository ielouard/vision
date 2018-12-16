# import the necessary packages
import argparse
import cv2
import numpy as np

class HSV_Getter:

    # initialize the list of reference points and boolean indicating
    # whether cropping is being performed or not
    refPt = []
    cropping = False
    image = None

    def click_and_crop(self,event, x, y, flags, param):
    	# grab references to the global variables

    	# if the left mouse button was clicked, record the starting
    	# (x, y) coordinates and indicate that cropping is being
    	# performed
    	if event == cv2.EVENT_LBUTTONDOWN:
    		self.refPt = [(x, y)]
    		self.cropping = True

    	# check to see if the left mouse button was released
    	elif event == cv2.EVENT_LBUTTONUP:
    		# record the ending (x, y) coordinates and indicate that
    		# the cropping operation is finished
    		self.refPt.append((x, y))
    		self.cropping = False

    		# draw a rectangle around the region of interest
    		cv2.rectangle(self.image, self.refPt[0], self.refPt[1], (0, 255, 0), 2)
    		cv2.imshow("image", self.image)

    def get_hsv(self, image):
        # construct the argument parser and parse the arguments


        # load the image, clone it, and setup the mouse callback function
        self.image = cv2.imread(image)
        clone = self.image.copy()
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.click_and_crop)

        # keep looping until the 'q' key is pressed
        while True:
        	# display the image and wait for a keypress
        	cv2.imshow("image", self.image)
        	key = cv2.waitKey(1) & 0xFF

        	# if the 'r' key is pressed, reset the cropping region
        	if key == ord("r"):
        		self.image = clone.copy()

        	# if the 'c' key is pressed, break from the loop
        	elif key == ord("c"):
        		break

        # if there are two reference points, then crop the region of interest
        # from teh image and display it
        if len(self.refPt) == 2:
            roi = clone[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]
            color = self.image[self.refPt[0][0], self.refPt[1][1]]
            # if image type is b g r, then b g r value will be displayed.
            # if image is gray then color intensity will be displayed.
            average = roi.mean(axis=0).mean(axis=0)
            # average=np.array([int(i) for i in average])
            average=average.astype(int)
            color=np.uint8([[average]])
            hsv_color = cv2.cvtColor(color,cv2.COLOR_BGR2HSV)
            cv2.destroyAllWindows()
            return hsv_color


        # close all open windows
        cv2.destroyAllWindows()
