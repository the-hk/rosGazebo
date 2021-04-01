#!/usr/bin/env python

import rospy
from test_pub_sub.msg import test_custom_msg

def subscriber():

    sub=rospy.Subscriber("yayinlanan_konu", test_custom_msg, callback_function)

    rospy.spin()
def callback_function(message):
    string_received = message.data
    counter_received = message.counter
    rospy.loginfo("alinan : %s"%string_received)    
    rospy.loginfo("alinan 2 : %d"%counter_received)    


if __name__=="__main__":
    rospy.init_node("mesaj_alan_node")
    subscriber()