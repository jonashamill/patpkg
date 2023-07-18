#!/usr/bin/env python3

import rospy
from geographic_msgs.msg import PointStamped
import csv
import rospkg
import os

from datetime import datetime

def getTime():

    #grabbing time and date to provide unique ID for logs
    dateTime = datetime.now()
    dtString = dateTime.strftime("%Y%m%d%H%M%S") #ISO 8601 Standard

    return dtString


def getPath():

    timenow = 'test' #getTime()

    rp = rospkg.RosPack()
    packagePath = rp.get_path('patpkg')

    path = os.path.join(packagePath, "waypoints")

    fullpath = os.path.join(path, 'waypoint_' + timenow + ".csv")

    print (fullpath)

    return path, fullpath





def main():

    rp = rospkg.rospack()













if __name__ == '__main__':
    main()