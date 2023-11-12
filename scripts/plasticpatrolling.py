#!/usr/bin/env python3

import rospy
import csv
import datetime
import rospkg
import time
import os
from std_msgs.msg import Int32
from ar_track_alvar_msgs.msg import AlvarMarkers


#Global vars
idList = []
timeList = []
timeSinceList = []
stateList = []


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

    testFile.close()
    os.remove(testFile.name)

def saveCSV():
    
    _, filename = getPath()

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Time', 'Timesince', 'State'])
        
        for i in range(len(idList)):
            writer.writerow([idList[i], timeList[i], timeSinceList[i], stateList[i]])


def rosInit():

    rospy.init_node("arLogger")


    ar_subscriber = rospy.Subscriber("ar_pose_marker", AlvarMarkers, getTag)

    # rospy.Subscriber('maxVelocity', Float32, maxVelocityCallback)
    # rospy.Subscriber('minVelocity', Float32, minVelocityCallback)

    
    rospy.on_shutdown(saveCSV)


def checkDuplicate(iterable,check):
    for i in iterable:
        if i == check:
            return True

def getTag(msg):

    global idList
    global currentMarker
    global timeTaken
    global stateList

    for marker in msg.markers:
        

        if marker.id != currentMarker:
            
            finish = time.perf_counter()

            
            timeTaken = round(finish-start, 2)
            currentMarker = marker.id
            
            
            

            if checkDuplicate(idList, currentMarker) == True:
                continue
            else:

                if len(timeList) > 0:
                    rospy.loginfo('timelist: ' + str(timeList))
                    rospy.loginfo('timelist-1:  ' + str(timeList[-1]))
                    lastTimestamp = timeList[-1]
                    timeSinceLast = round(timeTaken - lastTimestamp, 2)
                    rospy.loginfo('timesincelast: ' + str(timeSinceLast))

                    
                else:
                    rospy.loginfo('timesince: 0')
                    timeSinceLast = 0

                #timeSinceLast = round(finish - lastTimestamp.get(marker.id, finish), 5)
                # lastTimestamp[currentMarker] = finish

                # Publish 'tag' as a ROS topic
                tagPub = rospy.Publisher('tagTopic', Int32, queue_size=10)
                tagPub.publish(True)

                timeList.append(timeTaken)
                idList.append(currentMarker)
                timeSinceList.append(timeSinceLast)
                stateList.append(plastic)
            

                timeSince(timeSinceLast)


            rospy.loginfo(currentMarker)
            rospy.loginfo(timeTaken)
            rospy.loginfo(idList)
            

def timeSince(timeSinceLast):

    # Get the 'timeThresholdLow' and 'timeThresholdHigh' parameters from the parameter server
    timeThresholdLow = rospy.get_param("~timeThresholdLow", 2)
    timeThresholdHigh = rospy.get_param("~timeThresholdHigh", 6)

    
    rospy.loginfo('Time since last: %s', str(timeSinceLast))

    plastic = 0

    if currentMarker > 0: 
        
        if timeSinceLast < timeThresholdHigh:
            
            plastic = 1

            rospy.loginfo('decreasing speed- log')

        elif timeSinceLast > timeThresholdLow:
            
            plastic = 0

            rospy.loginfo('increasing speed - log')

   

        # Publish 'plastic' as a ROS topic
        plasticPub = rospy.Publisher('plasticTopic', Int32, queue_size=10)
        plasticPub.publish(plastic)

def main ():


    return

if __name__ == '__main__':
    makeFolder()
    rosInit()

    rospy.spin()