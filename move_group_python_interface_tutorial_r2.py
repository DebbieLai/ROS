#!/usr/bin/env python

# Software License Agreement (BSD License)
#
# Copyright (c) 2013, SRI International
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of SRI International nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Acorn Pooley, Mike Lautman

## BEGIN_SUB_TUTORIAL imports
##
## To use the Python MoveIt interfaces, we will import the `moveit_commander`_ namespace.
## This namespace provides us with a `MoveGroupCommander`_ class, a `PlanningSceneInterface`_ class,
## and a `RobotCommander`_ class. (More on these below)
##
## We also import `rospy`_ and some messages that we will use:
##

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
## END_SUB_TUTORIAL


def test_callback(msg):
    #print(msg)
    tutorial = MoveGroupPythonIntefaceTutorial()

    print "============ Press `Enter` to execute a movement using a joint state goal ..."
    #raw_input()
    
    # rate = rospy.Rate(300)
    # print(type(msg.vector.y))
    #while(1):
    	#print("in")
    	#type()
	#print(msg.vector.y)
    # now = rospy.get_rostime()
    # rospy.loginfo("Current time %i %i", now.secs, now.nsecs)
    # seconds = rospy.get_time()
    
    x_coefficiency=0
    y_coefficiency=0
    z_coefficiency=0
    print("x=")
    print(msg.vector.x)
    print("y=")
    print(msg.vector.y)
    print("z=")
    print(msg.vector.z)
    
    # now2 = rospy.get_rostime()
    # rospy.loginfo("Current time %i %i", now2.secs, now2.nsecs)
    # seconds2 = rospy.get_time()
    # print('time=')
    # print(seconds2-seconds)
    if(msg.vector.x>2):
      x_coefficiency=1
    if(msg.vector.x<-2):
      x_coefficiency=-1
    if(msg.vector.y>2):
      y_coefficiency=1
    if(msg.vector.y<-2):
      y_coefficiency=-1
    if(msg.vector.z>2):
      z_coefficiency=1
    if(msg.vector.z<-2):
      z_coefficiency=-1  
    
    if(x_coefficiency!=0 or y_coefficiency!=0 or z_coefficiency!=0):
      # print("x=")
      # print(-x_coefficiency)
      tutorial.plan_cartesian_path(1,float(x_coefficiency)/100,float(y_coefficiency)/100,float(-z_coefficiency)/100)
    #rospy.sleep(1)  

def all_close(goal, actual, tolerance):
  """
  Convenience method for testing if a list of values are within a tolerance of their counterparts in another list
  @param: goal       A list of floats, a Pose or a PoseStamped
  @param: actual     A list of floats, a Pose or a PoseStamped
  @param: tolerance  A float
  @returns: bool
  """
  all_equal = True
  if type(goal) is list:
    for index in range(len(goal)):
      if abs(actual[index] - goal[index]) > tolerance:
        return False

  elif type(goal) is geometry_msgs.msg.PoseStamped:
    return all_close(goal.pose, actual.pose, tolerance)

  elif type(goal) is geometry_msgs.msg.Pose:
    return all_close(pose_to_list(goal), pose_to_list(actual), tolerance)

  return True

class MoveGroupPythonIntefaceTutorial(object):
  """MoveGroupPythonIntefaceTutorial"""
  def __init__(self):
    super(MoveGroupPythonIntefaceTutorial, self).__init__()
    
    #print("in")
    ## BEGIN_SUB_TUTORIAL setup
    ##
    ## First initialize `moveit_commander`_ and a `rospy`_ node:
    moveit_commander.roscpp_initialize(sys.argv)
    
    rospy.init_node('move_group_python_interface_tutorial',anonymous=True)              
    ## Instantiate a `RobotCommander`_ object. This object is the outer-level interface to
    ## the robot:
    
    robot = moveit_commander.RobotCommander()

    ## Instantiate a `PlanningSceneInterface`_ object.  This object is an interface
    ## to the world surrounding the robot:
    
    scene = moveit_commander.PlanningSceneInterface()

    ## Instantiate a `MoveGroupCommander`_ object.  This object is an interface
    ## to one group of joints.  In this case the group is the joints in the Panda
    ## arm so we set ``group_name = panda_arm``. If you are using a different robot,
    ## you should change this value to the name of your robot arm planning group.
    ## This interface can be used to plan and execute motions on the Panda:
    group_name = "manipulator"
    
    group = moveit_commander.MoveGroupCommander(group_name)
    print("in")
    ## We create a `DisplayTrajectory`_ publisher which is used later to publish
    ## trajectories for RViz to visualize:
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=20)

    ## END_SUB_TUTORIAL

    ## BEGIN_SUB_TUTORIAL basic_info
    ##
    ## Getting Basic Information
    ## ^^^^^^^^^^^^^^^^^^^^^^^^^
    # We can get the name of the reference frame for this robot:
    planning_frame = group.get_planning_frame()
    print "============ Reference frame: %s" % planning_frame

    # We can also print the name of the end-effector link for this group:
    eef_link = group.get_end_effector_link()
    print "============ End effector: %s" % eef_link

    # We can get a list of all the groups in the robot:
    group_names = robot.get_group_names()
    print "============ Robot Groups:", robot.get_group_names()

    # Sometimes for debugging it is useful to print the entire state of the
    # robot:
    print "============ Printing robot state"
    print robot.get_current_state()
    print ""
    ## END_SUB_TUTORIAL

    # Misc variables
    self.box_name = ''
    self.robot = robot
    self.scene = scene
    self.group = group
    self.display_trajectory_publisher = display_trajectory_publisher
    self.planning_frame = planning_frame
    self.eef_link = eef_link
    self.group_names = group_names

  def go_to_original_state(self,joi1,joi2,joi3,joi4,joi5,joi6):
    group = self.group

    joint_goal = group.get_current_joint_values()
    joint_goal[0] = joi1
    joint_goal[1] = joi2
    joint_goal[2] = joi3
    joint_goal[3] = joi4
    joint_goal[4] = joi5
    joint_goal[5] = joi6
   # joint_goal[6] = 0

    group.go(joint_goal, wait=True)

    group.stop()

    current_joints = self.group.get_current_joint_values()
    return all_close(joint_goal, current_joints, 0.01)


  def plan_cartesian_path(self, scale,xp,yp,zp,xor, yor ,zor,velocity_scale):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    group = self.group

    waypoints = []

    print("displacemanet : ({:.5f}, {:.5f}, {:.5f} ,{:.5f} ,{:.5f} ,{:.5f})".format(xp, yp, zp ,xor ,yor ,zor))

    wpose = group.get_current_pose().pose

    print("origin : ({:.5f}, {:.5f}, {:.5f}, {:.5f}, {:.5f}, {:.5f})".format(wpose.position.x, wpose.position.y, wpose.position.z , 
        wpose.orientation.x ,wpose.orientation.y ,wpose.orientation.z))

    wpose.position.x += scale * xp  # First move up (z)
    wpose.position.y += scale * yp  # and sideways (y)
    wpose.position.z += scale * zp

    # wpose.orientation.x += scale * xor
    # wpose.orientation.y += scale * yor
    # wpose.orientation.z += scale * zor

    waypoints.append(copy.deepcopy(wpose))
    wpose.orientation.x += scale * xor
    wpose.orientation.y += scale * yor
    wpose.orientation.z += scale * zor

    waypoints.append(copy.deepcopy(wpose))

    # # We want the Cartesian path to be interpolated at a resolution of 1 cm
    # # which is why we will specify 0.01 as the eef_step in Cartesian
    # # translation.  We will disable the jump threshold by setting it to 0.0 disabling:
    (plan, fraction) = group.compute_cartesian_path(
                                       waypoints,   # waypoints to follow
                                       0.01,        # eef_step
                                       0.0)         # jump_threshold

    plan=group.retime_trajectory(self.robot.get_current_state(),plan,velocity_scale)

    group.execute(plan, wait=True)

    
    print("goal : ({:.5f}, {:.5f}, {:.5f}, {:.5f}, {:.5f}, {:.5f})".format(waypoints[0].position.x, waypoints[0].position.y, waypoints[0].position.z ,
        waypoints[0].orientation.x,waypoints[0].orientation.y,waypoints[0].orientation.z))

    wpose_after = group.get_current_pose().pose
    print("after : ({:.5f}, {:.5f}, {:.5f}, {:.5f}, {:.5f}, {:.5f})".format(wpose_after.position.x, wpose_after.position.y, wpose_after.position.z ,
        wpose_after.orientation.x ,wpose_after.orientation.y ,wpose_after.orientation.z))

    print("error : ({:.5f}, {:.5f}, {:.5f}, {:.5f}, {:.5f}, {:.5f})".format(
            wpose_after.position.x - waypoints[0].position.x,
            wpose_after.position.y - waypoints[0].position.y,
            wpose_after.position.z - waypoints[0].position.z,
            wpose_after.orientation.x - waypoints[0].orientation.x,
            wpose_after.orientation.y - waypoints[0].orientation.y,
            wpose_after.orientation.z - waypoints[0].orientation.z))

    # Note: We are just planning, not asking move_group to actually move the robot yet:
    return plan, fraction

    ## END_SUB_TUTORIAL




  def get_pose(self):
    group = self.group

    wpose = group.get_current_pose().pose

    print("pose : ({:.5f}, {:.5f}, {:.5f},{:.5f} ,{:.5f} ,{:.5f})".format(wpose.position.x, wpose.position.y, wpose.position.z , 
        wpose.orientation.x ,wpose.orientation.y ,wpose.orientation.z))

    ## END_SUB_TUTORIAL




def main():
  #try:
    print "============ Press `Enter` to begin the tutorial by setting up the moveit_commander (press ctrl-d to exit) ..."
    raw_input()
    #print("in")
    tutorial = MoveGroupPythonIntefaceTutorial()

    # print "============ Press `Enter` to execute a movement using a joint state goal ..."
    # raw_input()
    
    # while(1):
    # 	if(msg.vector.y>2):
    # 	  tutorial.go_to_joint_state(0,pi/6,0)
    # 	elif(msg.vector.y<2):
    # 	  tutorial.go_to_joint_state(0,-pi/6,0)
    # 	else:
    #       continue

    # print "============ Press `Enter` to execute a movement using a pose goal ..."
    # raw_input()
    # tutorial.go_to_pose_goal(1.0,0.4,0.1,0.4)

    # print "============ Press `Enter` to execute a movement using a pose goal ..."
    # raw_input()
    # tutorial.go_to_pose_goal(0,0,0,0)
    
    # print "============ Press `Enter` to get pose ..."
    # raw_input()
    # tutorial.get_pose()

    print "============ Press `Enter` to go to original state ..."
    raw_input()
    tutorial.go_to_original_state(0,0,0,0,0,0)

    #start
    print "============ Press `Enter` to go to original state ..."
    raw_input()
    tutorial.go_to_original_state(   0.00971,0.63994,0.12533,-0.04457,-0.76466,-1.59901)

    # # print "============ Press `Enter` to get pose ..."
    # # raw_input()
    # # tutorial.get_pose()
    #rough location


    # print "============ Press `Enter` to plan and display a Cartesian path ..."
    # raw_input()
    # # # (1, 0.62407-0.51503, 0.00063-0.00004, 0.37743-0.71200,-0.66515 ,0.00754 ,0.00723 , 0.5)path
    # # # (1, 0.62398-0.51503, 0.00811-0.00004, 0.37745-0.71200,-0.67 ,0. ,0.01669, 0.5) goal
    # cartesian_plan, fraction = tutorial.plan_cartesian_path(1, 0.62407-0.51503, 0.00063-0.00004, 0.37743-0.71200,-0.66515 ,0.00754 ,0.00723 , 0.5)


    # print "============ Press `Enter` to plan and display a Cartesian path ..."
    # raw_input()
    # # (1, 0.62407-0.51503, 0.00063-0.00004, 0.37743-0.71200,-0.66515 ,0.00754 ,0.00723 , 0.5)path
    # # (1, 0.62398-0.51503, 0.00811-0.00004, 0.37745-0.71200,-0.67 ,0. ,0.01669, 0.5) goal
    # cartesian_plan, fraction = tutorial.plan_cartesian_path(1, 0, 0.2, 0, -0.35 , 0 ,0.01669, 0.5) 

    
    #first drill
    print "============ Press `Enter` to plan and display a Cartesian path ..."
    raw_input()
    cartesian_plan, fraction = tutorial.plan_cartesian_path(1 , -0.01, -0.02 , -0.04, 0, 0, 0, 0.01)

    # print "============ Press `Enter` to plan and display a Cartesian path ..."
    # raw_input()
    cartesian_plan, fraction = tutorial.plan_cartesian_path(1 , 0.01, 0.02 , 0.04, 0, 0, 0,0.01)

    #second drill
    # print "============ Press `Enter` to plan and display a Cartesian path ..."
    # raw_input()
    cartesian_plan, fraction = tutorial.plan_cartesian_path(1 , 0.01, -0.01 , -0.04, 0, 0, 0,0.01)

    # print "============ Press `Enter` to plan and display a Cartesian path ..."
    # raw_input()
    cartesian_plan, fraction = tutorial.plan_cartesian_path(1 , -0.01, 0.01 , 0.04, 0, 0, 0,0.01)

    #third drill
    # print "============ Press `Enter` to plan and display a Cartesian path ..."
    # raw_input()
    cartesian_plan, fraction = tutorial.plan_cartesian_path(1 , -0.005, -0.005 , -0.04, 0, 0, 0,0.01)

    # print "============ Press `Enter` to plan and display a Cartesian path ..."
    # raw_input()
    cartesian_plan, fraction = tutorial.plan_cartesian_path(1 , 0.005, 0.005 , 0.04, 0, 0, 0,0.01)



if __name__ == '__main__':
  #tutorial = MoveGroupPythonIntefaceTutorial()
  main()

  
  #rospy.Subscriber("/force_sensor", geometry_msgs.msg.Vector3Stamped, test_callback,queue_size=1,buff_size=52428800)

  #go_to_pose_goal()
  

  # print "============ Press `Enter` to plan and display a Cartesian path ..."
  # raw_input()
  # cartesian_plan, fraction = tutorial.plan_cartesian_path(1,0,0,0.01)
  #rospy.spin()
