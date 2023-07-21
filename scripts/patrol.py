#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
import time

def plasticCallback(msg):

    plastic = msg.data

    return plastic

def patrolSpeed(plastic):

    patSpeed = rospy.get_param("~initialSpeed", 1.0)

    #plastic =  msg.data # plasticCallback(msg)

    if plastic == 1:
        patSpeed = patSpeed - 0.2
    
    elif plastic == 2:
        patSpeed = patSpeed + 0.2

    return patSpeed


def drive(linear, angular, cmd_pub):
    
    #init Ros message object
    twist = Twist()
    twist.linear.x = linear
    twist.angular.z = angular

    cmd_pub.publish(twist)



def main():

    usePlasticity = rospy.get_param("~usePlasticity", True)

    linearRange = rospy.get_param("~linearRange", 1000)
    angularRange = rospy.get_param("~angularRange", 500)
    
    rospy.loginfo('LinearRange: ', linearRange)
    rospy.loginfo('angularRange: ', angularRange)

    #initialise rosnode
    rospy.init_node("patrol")
    
    plastic = rospy.Subscriber('plasticTopic', Int32, plasticCallback)

    
    # create ros pub
    cmd_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
    
    while not rospy.is_shutdown():

        
        if usePlasticity:
            patSpeed = patrolSpeed(plastic)
        
        else:
            patSpeed = 1.0

        for i in range (50000):

            drive(patSpeed,0.0, cmd_pub)

           


        time.sleep(1)

        rospy.loginfo('Turning')

        for _ in range (10000):

            drive(0.0,1.0, cmd_pub) 
            
        
     
        time.sleep(1) 

    return


if __name__ == '__main__':
    main()