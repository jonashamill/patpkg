#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PointStamped
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



def makeFolder():

    path, _ = getPath()

    testFile = None

    # test folder permisions
    try:
        testFile = open(os.path.join(path, 'test.txt'), 'w+')
    except IOError:
        try:
            os.mkdir(path)
        except OSError:
            print("No waypoint folder created")
        else:
            print("waypoint folder created")

    testFile.close()
    os.remove(testFile.name)


def saveCSV(msg):
    
    _, filename = getPath()

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([msg.point.x, msg.point.y, 0])


def main():

    _, fullpath = getPath()

    rospy.init_node('savewaypoint', anonymous=True)
    rospy.point_pub = rospy.Subscriber('/clicked_point', PointStamped, saveCSV)
    rospy.spin()



if __name__ == '__main__':
    main()