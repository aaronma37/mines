#!/usr/bin/env python

from mobile_buoy_environment import Mobile_Buoy_Environment
from random import randint
import random
import xxhash
import time
import math
from sets import Set
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Bool
from mobile_buoy_classes import Agent_buoy
import numpy as np
import sys
import rospy

''' This is the ros file that runs an agent'''

print "STARTING"

region = [(10,10),(10,30),(10,50),(10,70),(10,90),(30,10),(50,10),(70,10),(90,10),(30,30),(50,30),(70,30),(90,30),(30,50),(50,50),(70,50),(90,50),(30,70),(50,70),(70,70),(90,70),(30,90),(50,90),(70,90),(90,90)]

region_size=10

map_size=100

ON=1
OFF=0

a = Agent_buoy(Mobile_Buoy_Environment,map_size)
ai= Agent_buoy(Mobile_Buoy_Environment,map_size)
s=Mobile_Buoy_Environment(map_size)
si=Mobile_Buoy_Environment(map_size)
pose= PoseStamped()


rospy.init_node('Mobile Buoy', anonymous=True)
pose.header.frame_id= rospy.get_name()


pose_pub = rospy.Publisher('/mobile_buoy',PoseStamped,queue_size=1)

def score_cb(grid):
	for i in range(len(region)):
		s.score[i]=grid.data[i]

def worked_cb(grid):
	a.update_worked(grid.data)

def reset_cb(data):
	print "r"
	if data.data is True:
		print "s"
		a.reset()
		s.reset()



def run():
	while not rospy.is_shutdown():
		start=time.time()

		s.imprint(si)
		a.step(si,ai,.2)
		s.imprint(si)
		to_wait = start-time.time() + .2
		if to_wait >0:
			time.sleep(to_wait)

		a.solver.update_transition_and_reward_functions(s,a)
		a.decide(si,ai)
		pose.pose.position.x=a.x
		pose.pose.position.y=a.y
		pose.pose.orientation.x=a.current_action.index

		pose_pub.publish(pose)

		




###MAIN
def main(args):

	score_sub =rospy.Subscriber('/buoy_scores', Int32MultiArray , score_cb)#CHANGE TO MATRIX
	work_sub =rospy.Subscriber('/buoy_targets', Int32MultiArray , worked_cb)#CHANGE TO MATRIX
	reset_sub =rospy.Subscriber('/reset', Bool , reset_cb)#CHANGE TO MATRIX
	time.sleep(random.random())

	try:
		run()
		rospy.spin()

	except KeyboardInterrupt:
		print("Draw: Shutting down")



if __name__ == '__main__':
	main(sys.argv)

