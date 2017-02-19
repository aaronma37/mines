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

ON=1
OFF=0

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
		start=time.time()
		s.imprint(si)
		a.step(si,ai,.5)
		s.imprint(si)
		to_wait = start-time.time() + .2
		if to_wait >0:
			time.sleep(to_wait)
		a.decide(si,ai)
		pose.pose.position.x=a.x
		pose.pose.position.y=a.y
		pose.pose.position.z=a.battery
		pose.pose.orientation.x=a.current_action.index
		pose.pose.orientation.y=ON
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

