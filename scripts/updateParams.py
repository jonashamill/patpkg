#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
import time

def plasticCallback(msg):

    plastic = msg.data

    return plastic

def patrolSpeed(plastic):

    patSpeed = rospy.get_param("~initialSpeed", 0.2)

    #plastic =  msg.data # plasticCallback(msg)

    if plastic == 1:
        patSpeed = patSpeed - 0.02
    
    elif plastic == 2:
        patSpeed = patSpeed + 0.02

    return patSpeed



def main():

    usePlasticity = rospy.get_param("~usePlasticity", True)

    #initialise rosnode
    rospy.init_node("patrol")
    
    plastic = rospy.Subscriber('plasticTopic', Int32, plasticCallback)

    
    # create ros pub
    cmd_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
    
    while not rospy.is_shutdown():

        
        if usePlasticity:
            patSpeed = patrolSpeed(plastic)
            minPatSpeed = patSpeed - 0.15
        
        else:
            patSpeed = 0.25
            minPatSpeed = 0.1

            


        rospy.set_param('max_vel_x', patSpeed)
        rospy.set_param('min_vel_x', minPatSpeed)

        rospy.loginfo('Max Speed: ', patSpeed)
        rospy.loginfo('Min Speed: ', minPatSpeed)

           

    return


if __name__ == '__main__':
    main()