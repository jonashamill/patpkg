#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32, Float32
import time
from datetime import datetime
import os
import rospkg
import csv

plastic = 0
tagMSG = False


def plasticCallback(msg):

    global plastic

    plastic = msg.data

def tagCallback(msg):

    global tagMSG
    
    tagMSG = msg.data

def drive(linear, angular, cmd_pub):
    # Initialize ROS message object
    twist = Twist()
    twist.linear.x = linear
    twist.angular.z = angular

    cmd_pub.publish(twist) # publish message


def main():

    global plastic
    global tagMSG


    usePlasticity = rospy.get_param("usePlasticity", True)

    #initialise rosnode
    rospy.init_node("patrol")

    # Create ROS publisher
    cmd_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)

    
    rospy.Subscriber('plasticTopic', Int32, plasticCallback)

    rospy.loginfo('Plastic set to: %s', str(plastic))

    rospy.Subscriber('tagTopic', Int32, tagCallback)

    
    # create ros pub
    cmd_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
    
    while not rospy.is_shutdown():
        
        if usePlasticity:
            if plastic == 1 and tagMSG == True:
                rospy.loginfo("pausing")
                for _ in range (20)
                    drive(0.0,0.0,cmd_pub)
                rospy.sleep(0.9)
                
                # Publish 'tag' as a ROS topic
                tagPub = rospy.Publisher('tagTopic', Int32, queue_size=10)
                tagPub.publish(False)

            

    return


if __name__ == '__main__':
    # makeFolder()
    main()