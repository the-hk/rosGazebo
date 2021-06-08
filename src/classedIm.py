#!/usr/bin/env python

# SIMPLE SCRIPT TO TEST CV_BRIDGE PACKAGE
#
#- ON THE RASPI: roslaunch raspicam_node camerav2_1280x960.launch enable_raw:=true
#

import sys

import rospy
import cv2

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
        cameraY = 600
        cameraX = 800   
        cv_image = cv2.resize(cv_image, (cameraX, cameraY))
        original = cv_image.copy()
        cv2.rectangle(original, (395, 295),
                    (405, 305), (0, 128, 50), -1)
        blurred = cv2.medianBlur(cv_image, 3)
        # blurred = cv2.GaussianBlur(hsv,(3,3),0)

        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,(0,0,0), (40, 255, 80))
        rospy.loginfo("girdi")
        _,cnts,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        minArea = []
        minC = []
        for c in cnts:
            area = cv2.contourArea(c)
            if area > 400:
                approx = cv2.approxPolyDP(c, 0.125 * cv2.arcLength(c, True), True)
                if(len(approx) == 4): 
                    minArea.append(area)
                    minC.append([area, c])
        if minArea:
            minArea.sort()
            print(minArea)
            mArea = minArea[0]
            mC = []
            for x in minC:
                if x[0] == mArea:
                    mC = x[1]
            M = cv2.moments(mC)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x = cx - cameraX/2
            y = (cy - cameraY/2) * -1
            print(cx, cy  , x , y)
            cv2.rectangle(original, (cx - 5, cy - 5),
                        (cx + 5, cy + 5), (0, 128, 255), -1)
            cv2.drawContours(original, [approx], 0, (0, 0, 255), 5)
        error1 = [x,y]
        self.msg_to_publish.error = error1
        cv2.imshow('mask', mask)
        cv2.imshow('original', original)
       
        cv2.waitKey(3)

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
    rospy.init_node('image_error', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        
    #--- In the end remember to close all cv windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)