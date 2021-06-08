#!/usr/bin/env python
import sys

import rospy
import cv2

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def subscriber():
    sub = rospy.Subscriber("/rexrov/rexrov/camera/camera_image", Image, callback)
    rospy.spin()

def callback(data):  #--- Callback function
    
    #--- Read the frame and convert it using bridge
    try:
       cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
       print(e)

    cv2.imshow("Image window", cv_image)
    cv2.waitKey(100)        

if __name__ == '__main__':
    rospy.init_node('image_converter', anonymous=True)
    bridge = CvBridge()
    subscriber()
	
