#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
import time
from datetime import datetime
import os
import rospkg
import csv


#Global vars
timeList = []
minList = []
maxList = []
start = time.perf_counter()
currentMarker = 999

def getTime():

    #grabbing time and date to provide unique ID for logs
    dateTime = datetime.now()
    dtString = dateTime.strftime("%Y%m%d%H%M%S") #ISO 8601 Standard

    return dtString


def getPath():

    timenow = getTime()

    rp = rospkg.RosPack()
    packagePath = rp.get_path('patpkg')

    path = os.path.join(packagePath, "logs")

    fullpath = os.path.join(path, "arlog_" + timenow + ".csv")

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
            print("No log folder created")
        else:
            print("Log folder created")

    else:

        testFile.close()
        os.remove(testFile.name)

def saveCSV():
    
    _, filename = getPath()

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Velocity Min', 'Velocity Max'])
        
        for i in range(len(maxList)):
            writer.writerow([timeList[i], minList[i], maxList[i]])



def checkDuplicate(iterable,check):
    for i in iterable:
        if i == check:
            return True


def getSpeed(msg, patSpeed, minPatSpeed):

    for marker in msg.markers:
        global currentMarker

        if marker.id != currentMarker:
            
            finish = time.perf_counter()
            timeTaken = round(finish-start, 5)
            currentMarker = marker.id


            if checkDuplicate(timeTaken, currentMarker) == True:
                continue
            else:
                timeList.append(timeTaken)
                maxList.append(patSpeed)
                minList.append(minPatSpeed)
            

            rospy.loginfo(currentMarker)
            rospy.loginfo(timeTaken)


def plasticCallback(msg):

    plastic = msg.data

    return plastic

def patrolSpeed(plastic):

    patSpeed = rospy.get_param("~initialSpeed", 0.2)

    #plastic =  msg.data # plasticCallback(msg)

    if plastic == 1:
        patSpeed = patSpeed - 0.2
    
    elif plastic == 2:
        patSpeed = patSpeed + 0.2

    return patSpeed



def main():

    global msg


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


        getSpeed(msg, patSpeed, minPatSpeed)        


        rospy.set_param('max_vel_x', patSpeed)
        rospy.set_param('min_vel_x', minPatSpeed)

        # rospy.loginfo('Max Speed: ', str(patSpeed))
        # rospy.loginfo('Min Speed: ', str(minPatSpeed))

           
    rospy.on_shutdown(saveCSV)

    return


if __name__ == '__main__':
    makeFolder()
    main()