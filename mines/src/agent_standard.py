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

region = [(10,10),(10,30),(10,50),(10,70),(10,90),(30,10),(50,10),(70,10),(90,10),(30,30),(50,30),(70,30),(90,30),(30,50),(50,50),(70,50),(90,50),(30,70),(50,70),(70,70),(90,70),(30,90),(50,90),(70,90),(90,90)]

region_size=20


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
	if a.x > grid.info.origin.position.x -  grid.info.origin.position.z/2 and a.x <  grid.info.origin.position.x +  grid.info.origin.position.z/2+1:
		if a.y >  grid.info.origin.position.y -  grid.info.origin.position.z/2 and a.y <  grid.info.origin.position.y +  grid.info.origin.position.z/2+1:
			a.time_away_from_network=0
			for i in range(map_size):
				for j in range(map_size):
					s.seen[i][j]=grid.data[i*map_size+j]



def occ_cb(grid):
	if a.x > map_size/2 - 10 and a.x < map_size/2 + 11:
		if a.y > map_size/2 - 10 and a.y < map_size/2 + 11:
			for i in range(len(region)):
				s.occupied[i]=grid.data[i]





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
		pose.pose.orientation.y=a.time_away_from_network
		pose_pub.publish(pose)

		




###MAIN
def main(args):



	environment_sub =rospy.Subscriber('/environment_matrix', OccupancyGrid , env_cb)#CHANGE TO MATRIX
	occ_sub =rospy.Subscriber('/environment_occupied', OccupancyGrid , occ_cb)#CHANGE TO MATRIX
	time.sleep(random.random())

	try:
		run()
		rospy.spin()

	except KeyboardInterrupt:
		print("Draw: Shutting down")



if __name__ == '__main__':
	main(sys.argv)

