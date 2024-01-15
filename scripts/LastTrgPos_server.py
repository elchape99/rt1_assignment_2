#! /usr/bin/env python3

import rospy
import assignment_2_2023.msg
import assignment_2_2023.srv
from assignment_2_2023.msg import PlanningActionGoal 
from assignment_2_2023.srv import LastTrgPos, LastTrgPosResponse

service = None
pub = None
x_cord = None
y_cord = None


def srvCallback(req):
    global x_cord, y_cord    
    return LastTrgPosResponse(x_cord, y_cord)
    

def subCallback(msg):
    global x_cord, y_cord
    # I subscribe to the publisher /reach_goal/goal
    # The data are in format PlanningGoal    
    x_cord = msg.goal.target_pose.pose.position.x
    y_cord = msg.goal.target_pose.pose.position.y

def last_target_server():
    global service, pub
    #initialize the service 
    rospy.init_node("LastTrgPos_server")
    service = rospy.Service('/LastTrgPos', LastTrgPos, srvCallback )
    rospy.loginfo("Service LastTrgPos is ready")
    # nee to subscribe to reach_goal/goal for see the information about the goal
    sub = rospy.Subscriber("/reaching_goal/goal", PlanningActionGoal, subCallback)
    rospy.spin()
    
        
last_target_server()
