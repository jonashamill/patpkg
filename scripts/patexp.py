#!/usr/bin/env python3


import rospy
import math
import pandas as pd
import rospkg
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus, GoalStatusArray
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler
import os

def getPath():

        rp = rospkg.RosPack()
        packagePath = rp.get_path('patpkg')

        path = os.path.join(packagePath, "waypoints")

        csvPath = os.path.join(path, "exp.csv")

        print (csvPath)

        return path, csvPath



class Patroller():

    def rosInit():

        rospy.init_node("patroller")


    def main(self):

        _, csvPath = getPath()

        df = pd.read_csv(csvPath, sep=',', header=None)
        self.theta = list(df.loc[:, 3].values)
        wayPoint = df.loc[:, 0:2]
        self.waypoints = []
        wayPoint = wayPoint.values.tolist()

        for sublist in wayPoint:
             for item in sublist:
                  self.waypoints.append(item)

        
        wayPointAngle =  self.waypoints #heading angle
        wayPointCoord = self.theta # coordinates for each waypoint


        poseList = list()

        self.pose_seq = list()
        self.goal_cnt = 0
        for yawangle in wayPointCoord:
            
            poseList.append(Quaternion(*(quaternion_from_euler(0, 0, yawangle*math.pi/180, axes='sxyz'))))

        n = 3

        points = [wayPointAngle[i:i+n] for i in range (0, len(poseList), n)]

        for point in points:
            self.pose_seq.append(Pose(Point(*point), poseList[n-3]))
            n += 1
        

        #Create action client
        



        



if __name__ == '__main__':
    Patroller()