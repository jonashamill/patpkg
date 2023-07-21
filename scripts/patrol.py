#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

def plasticCallback(msg):

    plastic = msg.data

    return plastic

def patrolSpeed(plastic):

    patSpeed = 1.0

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

        for _ in range (20):

            drive(patSpeed,0.0, cmd_pub)
        
        for _ in range (5):

            drive(0.0,1.0, cmd_pub) 
        
     
    return


if __name__ == '__main__':
    main()