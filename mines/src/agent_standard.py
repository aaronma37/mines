#!/usr/bin/env python

from environment_classes import Mine_Data
from random import randint
import random
import xxhash
import time
import math
from sets import Set
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid
from agent_classes import Agent
import numpy as np
import sys
import rospy

''' This is the ros file that runs an agent'''

print "STARTING"




map_size=100


a = Agent(Mine_Data,map_size)
ai= Agent(Mine_Data,map_size)
s=Mine_Data(map_size)
si=Mine_Data(map_size)
pose= PoseStamped()


rospy.init_node('Agent', anonymous=True)
pose.header.frame_id= rospy.get_name()


pose_pub = rospy.Publisher('/pose',PoseStamped,queue_size=1)


def env_cb(grid):
	for i in range(map_size):
		for j in range(map_size):
			s.seen[i][j]=grid.data[i*map_size+j]


def run():
	while not rospy.is_shutdown():
		s.imprint(si)
		a.step(si,ai,.1)
		s.imprint(si)
		time.sleep(.1)
		a.decide(si,ai)
		pose.pose.position.x=a.x
		pose.pose.position.y=a.y
		pose.pose.position.z=a.battery
		pose_pub.publish(pose)

		




###MAIN
def main(args):



	environment_sub =rospy.Subscriber('/environment_matrix', OccupancyGrid , env_cb)#CHANGE TO MATRIX
	time.sleep(random.random())

	try:
		run()
		rospy.spin()

	except KeyboardInterrupt:
		print("Draw: Shutting down")



if __name__ == '__main__':
	main(sys.argv)

