#!/usr/bin/env python


import sys

import rospy
import cv2
import numpy as np

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from test_pub_sub.msg import test_custom_msg

#--- Define our Class
class image_converter:

    def __init__(self):
        #--- Publisher of the edited frame
        self.image_pub = rospy.Publisher("error",test_custom_msg,queue_size=1)

        #--- Subscriber to the camera flow
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/rexrov/rexrov/camera/camera_image",Image,self.callback)
        self.msg_to_publish = test_custom_msg()

    def callback(self,data):  #--- Callback function
    
        #--- Read the frame and convert it using bridge
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        
        # height, width, number of channels in image
        x=0
        y=0
        camY = 600
        camX = 800   
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray,(11,11),0)
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1.2, 20, param1 = 10,param2 = 100, minRadius = 5, maxRadius = 100)

    # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
        if circles is not None:
            rospy.loginfo("girdi")

            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(cv_image, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(cv_image, (x - 5, y - 5),
                            (x + 5, y + 5), (0, 128, 255), -1)
                x = x - camX/2
                y = y - camY/2
            error1 = [x,y]
            self.msg_to_publish.error = error1
        cv2.imshow('circle',cv_image )
        cv2.waitKey(1)
        

        #--- Publish the modified frame to a new topic
        try:
            self.image_pub.publish(self.msg_to_publish)
        except CvBridgeError as e:
            print(e)

#--------------- MAIN LOOP
def main(args):
    #--- Create the object from the class we defined before
    ic = image_converter()
    
    #--- Initialize the ROS node
    rospy.init_node('image_error_circle', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        
    #--- In the end remember to close all cv windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)