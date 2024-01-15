#! /usr/bin/env python

import rospy
import actionlib
import assignment_2_2023
from nav_msgs.msg import Odometry
from assignment_2_2023.msg import PlanningAction, RobotInfo

client = None
sub = None
pub = None


def callback(msg):
    global pub
    # declare the mesage i want to publish
    msg_robot = RobotInfo()
    # assign the value msg_robot
    msg_robot.x = msg.pose.pose.position.x
    msg_robot.y = msg.pose.pose.position.y
    msg_robot.x_vel = msg.twist.twist.linear.x
    msg_robot.z_vel = msg.twist.twist.angular.z
    # publish the message
    pub.publish(msg_robot)


def input_cord():
    # function for input the cordinate
    while True:
        try:
            x = float(input("Insert x coordinate (float): "))
            y = float(input("Insert y coordinate (float): "))
            print(f"You entered coordinates: x = {x}, y = {y}")
            return x, y
        except ValueError:
            print("Error: Please enter valid floating-point numbers.")


def get_user_deleteGoal():
    #return true if the user wants to delete the actual goal
    #return false if the user wants to insert a new target 
    while True:
        user_input = input("Do you want to delete the actual goal (press 1) or insert a new target (press 2)")
        if user_input == "1":
            return True
        elif user_input == "2":
            return False
        else:
            print("Insert a correct key, press 1 or 2")

def set_user_newGoal():
    while True:
        user_input = input("Do you want to set a new Goal [y/n] ")
        if user_input == "y":
            return True
        elif user_input == "n":
            return False
        else:
            print("Insert a correct character, retry")


def target_client():
    global client
    coords_old = [None, None]
    # wait until the server process has started
    client.wait_for_server()
    # creates a goal to send to the action server
    goal = assignment_2_2023.msg.PlanningGoal()
    
    while not rospy.is_shutdown():
        # first round there is no goal, the user could decide to set a new goal
        if coords_old[0] is None or coords_old[1] is None:
            # first round there is no goal, the user could decide to set a new goal
            if set_user_newGoal(): #is true if user decide to set a new goal
                #this function retur the coordinat setted by user
                coords = input_cord()
                goal.target_pose.pose.position.x = coords[0]
                goal.target_pose.pose.position.y = coords[1]
                # Send goal to the action server
                client.send_goal(goal)
                #print to screen the coordinate of the target to reach
                rospy.loginfo("You sent the goal with: X = %f, Y = %f", goal.target_pose.pose.position.x, goal.target_pose.pose.position.y)
                # update the variable for the control of next loop
                coords_old = coords
            else:
                print("no goal is added, the robot has no goal to reach")
        else: # case when one goal is setted before
            if get_user_deleteGoal(): #returns true whn the user wants to delete the goal
                #cancel the goal
                if (client.get_state() == actionlib.GoalStatus.ACTIVE):
                    print("You canceled the goal with: X = ", goal.target_pose.pose.position.x," Y = ", goal.target_pose.pose.position.y)
                    client.cancel_goal() 
                else:
                    print("the goal is already deleted, press y and add a new goal")
                if set_user_newGoal(): #true if the user want to set a new goal after delete the last one
                    coords = input_cord()
                    goal.target_pose.pose.position.x = coords[0]
                    goal.target_pose.pose.position.y = coords[1]
                    # Send goal to the action server
                    client.send_goal(goal)
                    #prin to screen the new coordinate of the target
                    rospy.loginfo("You sent the goal with: X = %f, Y = %f", goal.target_pose.pose.position.x, goal.target_pose.pose.position.y)
                    coords_old = coords  
            else :#user wants to insert a new target to reach         
                coords = input_cord()
                goal.target_pose.pose.position.x = coords[0]
                goal.target_pose.pose.position.y = coords[1]
                # Send goal to the action server
                client.send_goal(goal)
                #prin to screen the new coordinate of the target
                rospy.loginfo("You sent the goal with: X = %f, Y = %f", goal.target_pose.pose.position.x, goal.target_pose.pose.position.y)
                coords_old = coords    
            
                             
        if client.get_state() == actionlib.GoalStatus.SUCCEEDED:
            rospy.loginfo("Goal reached successfully!")
        else:
            rospy.loginfo("Goal not reached.")
     
def main():
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node("trg_client")

        # create the SimpleActionClient, passing the type of action
        global client, sub, pub
        client = actionlib.SimpleActionClient(
            "/reaching_goal", assignment_2_2023.msg.PlanningAction
        )
        sub = rospy.Subscriber("/odom", Odometry, callback)
        pub = rospy.Publisher("/robot_info", RobotInfo, queue_size=1)
        target_client()

    except Exception as e:
        rospy.logerr(f"ERROR trg_client: {e}")


main()


