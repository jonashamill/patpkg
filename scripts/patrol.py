#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

def drive(linear, angular, cmd_pub):
    
    #init Ros message object
    twist = Twist()
    twist.linear.x = linear
    twist.angular.z = angular

    cmd_pub.publish(twist)



def main():
    

    #initialise rosnode
    rospy.init_node("patrol")
    
    # create ros pub
    cmd_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
    
    while (1):

    # for _ in range (20):

        drive(1.0,0.0, cmd_pub)
    
     
    
    return


if __name__ == '__main__':
    main()