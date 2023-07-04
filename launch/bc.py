#!/usr/bin/env python3

import rospy
from ar_track_alvar_msgs.msg import AlvarMarkers
from pyzbar import pyzbar

def main():
    
    #initialise rosnode
    rospy.init_node("bc")
    
    # create ros pu
    cmd_pub = rospy.Publisher("", queue_size=1)
    

    
     
    
    return
 

if __name__ == '__main__':
    main()