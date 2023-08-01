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


def plasticCallback(msg):
    
    global plastic

    plastic = msg.data

    return plastic

def patrolSpeed(patSpeed):
    
    global plastic

    #plastic =  msg.data # plasticCallback(msg)

    if plastic == 1:
        patSpeed = patSpeed - 0.2
    
    elif plastic == 2:
        patSpeed = patSpeed + 0.2

    return patSpeed

# def getMSG(msg):
    
#     return msg

def main():

    global plastic

    # msg = getMSG

    usePlasticity = rospy.get_param("~usePlasticity", True)

    #initialise rosnode
    rospy.init_node("patrol")

    patSpeed = rospy.get_param("~initialSpeed", 0.2)

    initialTorq = rospy.get_param("core2/motors/torque_limit")
    
    rospy.loginfo('torque: ' + str(initialTorq))

    plastic = rospy.Subscriber('plasticTopic', Int32, plasticCallback)

    
    # create ros pub
    cmd_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
    
    while not rospy.is_shutdown():

        
        if usePlasticity:
            patSpeed = patrolSpeed(patSpeed)
            minPatSpeed = patSpeed - 0.15
            
        
        else:
            patSpeed = 0.25
            minPatSpeed = 0.1


        # getSpeed(msg, patSpeed, minPatSpeed)        


        rospy.set_param('max_vel_x', patSpeed)
        rospy.set_param('min_vel_x', minPatSpeed)

        # Publish 'max' as a ROS topic
        maxVelPub = rospy.Publisher('maxVelocity', Float32, queue_size=10)
        maxVelPub.publish(patSpeed)

        # Publish 'min' as a ROS topic
        minVelPub = rospy.Publisher('minVelocity', Float32, queue_size=10)
        minVelPub.publish(minPatSpeed)

        # rospy.loginfo('Max Speed: ', str(patSpeed))
        # rospy.loginfo('Min Speed: ', str(minPatSpeed))




    # rospy.on_shutdown(saveCSV)

    return


if __name__ == '__main__':
    # makeFolder()
    main()