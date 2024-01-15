# Assignment 2 Research Track

This project is based on the use of ros and python. The main task is about writing a node and two service node that interact with a system provided by prfessor.
The system provided is a roboth with some sensors, and an arena.
The robot is also simulate with gazebo and rvitz, for simulate the motion. The robot consins on a non holonomic robot, so it can move long his x-axe and rotate around its z-axe. My ilmpelemtantion was about:
- in the first node the user could send a goal to robot, and the robot start going to it ad give back some information about the state, and know when the goal is reached. Also this node subscribe to a certain topic /odom. This topic is about the motion, catch the robot position and velocity (x, y, x_vel, z_vel) using a custome message called in my case RobotInfo. This node also publish this custom message on a topic called /robot_info
- service node, LastTrgPos_server, when it is called it returnsthe coordinate of the last target sent by user
- the last service node InfoRobot_server thaht return when called a distance of robot respect to goal and a robot speed average considering a certain windows of value.

## Installation

For the isntallation, clone this git repository inside the src folder of the ros workspace. afer clone change to branch master


git checkout master

before running the code is importanto to install using apt the pakage xterm
 sudo apt update
 sudo apt instll xterm

After the isntallations of xterm, in the srv folder of ros workspace run the command catkin_make. This command will built all the exeguibile files in the repository.
At this point the gazebo and rvitz will open and yuo can see the arena with the robot, and the data coming from sensors looking in rvitz.

In the window will be open also another terminal, xterm, in wicht folowing the instruction you will add a goal. After add the gol the first time you will delete it or change it. 

Also when the simulator is running is possible to run the two service.
For know the information about the last insereted goal you can use the service /LastTrgPos usig in terminal the line
rosservice call InfoRObot

For know the information about the distance from robot to goal and the average speed of the robot you can use the service /InfoRobot calling in the terminal
rosservice call InfoRobot
