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

    usePlasticity = rospy.get_param("usePlasticity", True)

    #initialise rosnode
    rospy.init_node("patrol")

    patSpeed = rospy.get_param("~initialSpeed", 0.2)
    
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

         # Create a Twist message to control linear and angular velocity
        # cmd_vel = Twist()
        # cmd_vel.linear.x = patSpeed
        # # cmd_vel.angular.z = 0.0      

        # cmd_pub.publish(cmd_vel)


        # rospy.set_param('max_vel_x', patSpeed)
        # rospy.set_param('min_vel_x', minPatSpeed)

        # Publish 'max' as a ROS topic
        maxVelPub = rospy.Publisher('maxVelocity', Float32, queue_size=10)
        maxVelPub.publish(patSpeed)

        # Publish 'min' as a ROS topic
        minVelPub = rospy.Publisher('minVelocity', Float32, queue_size=10)
        minVelPub.publish(minPatSpeed)

        rospy.set_param('/cmd_vel/linear/x', patSpeed)

        # rospy.loginfo('Max Speed: ', str(patSpeed))
        # rospy.loginfo('Min Speed: ', str(minPatSpeed))




    # rospy.on_shutdown(saveCSV)

    return


if __name__ == '__main__':
    # makeFolder()
    main()