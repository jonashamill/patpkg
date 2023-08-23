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


def patrolSpeed():
    
    global plastic

    #plastic =  msg.data # plasticCallback(msg)

    if plastic == 0:
        maxPatSpeed = 0.25
        minPatSpeed = 0.1
        patacc = 1.0
    
    
    elif plastic == 1:

        maxPatSpeed = 0.1
        minPatSpeed = 0.1
        patacc = 1.0
    
    elif plastic == 2:
        maxPatSpeed = 0.5
        minPatSpeed = 0.3
        patacc = 1.0

    return maxPatSpeed, minPatSpeed, patacc



# def getMSG(msg):
    
#     return msg

def main():

    global plastic

    # msg = getMSG

    usePlasticity = rospy.get_param("usePlasticity", True)

    maxPatSpeed = rospy.get_param('/max_vel_x', 0.25)
    minPatSpeed = rospy.get_param('/min_vel_x', 0.1)
    patacc = rospy.get_param('/acc_lim_x', 1.0)

    #initialise rosnode
    rospy.init_node("patrol")

    # patSpeed = rospy.get_param("initialSpeed")
    # patacc = rospy.get_param("/TrajectoryPlannerROS/acc_lim_x")

    # print ('patac 1: ', patacc)

    
    plastic = rospy.Subscriber('plasticTopic', Int32, plasticCallback)

    rospy.loginfo('Plastic set to: %s', str(plastic))

    
    # create ros pub
    cmd_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
    
    while not rospy.is_shutdown():

        
        if usePlasticity:
            maxPatSpeed, minPatSpeed, patacc = patrolSpeed()
            
        
        # else:
        #     maxPatSpeed = 0.25
        #     minPatSpeed = 0.1
        #     patacc = 1.0

        # rospy.loginfo('/max_vel_x: %f', maxPatSpeed)
        # rospy.loginfo('/min_vel_x: %f', minPatSpeed)
        # rospy.loginfo('/acc_lim_x: %f', patacc)




        # rospy.set_param('/max_vel_x', maxPatSpeed)
        # rospy.set_param('/min_vel_x', minPatSpeed)
        # rospy.set_param('/acc_lim_x', patacc)


        # getSpeed(msg, patSpeed, minPatSpeed)  

         # Create a Twist message to control linear and angular velocity
        # cmd_vel = Twist()
        # cmd_vel.linear.x = patSpeed
        # # cmd_vel.angular.z = 0.0      

        # cmd_pub.publish(cmd_vel)


        # rospy.set_param('/TrajectoryPlannerROS/max_vel_x', patSpeed)
        # rospy.set_param('/TrajectoryPlannerROS/acc_lim_x', patacc)
        # rospy.set_param('max_vel_x', patSpeed)
        # rospy.set_param('acc_lim_x', patacc)

        # patacc = rospy.get_param("acc_lim_x")

        # print ('patac 2: ', patacc)

        # rospy.set_param('min_vel_x', minPatSpeed)

        # # Publish 'max' as a ROS topic
        # maxVelPub = rospy.Publisher('maxVelocity', Float32, queue_size=10)
        # maxVelPub.publish(patSpeed)

        # # Publish 'min' as a ROS topic
        # minVelPub = rospy.Publisher('minVelocity', Float32, queue_size=10)
        # minVelPub.publish(minPatSpeed)


        # rospy.loginfo('Max Speed: ', str(patSpeed))
        # rospy.loginfo('Min Speed: ', str(minPatSpeed))




    # rospy.on_shutdown(saveCSV)

    return


if __name__ == '__main__':
    # makeFolder()
    main()