#!/usr/bin/env python

from environment_classes import Mine_Data
from random import randint
import random
import xxhash
import time
import math
from sets import Set
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Int32
from nav_msgs.msg import OccupancyGrid
from agent_classes import Agent
import numpy as np
import sys
import rospy
import Regions
from Heuristics import write_file

''' This is the ros file that runs an agent'''

region = [(10,10),(10,30),(10,50),(10,70),(10,90),(30,10),(50,10),(70,10),(90,10),(30,30),(50,30),(70,30),(90,30),(30,50),(50,50),(70,50),(90,50),(30,70),(50,70),(70,70),(90,70),(30,90),(50,90),(70,90),(90,90)]

region_size=20


map_size=100

a = Agent(Mine_Data,map_size)
ai= Agent(Mine_Data,map_size)
s=Mine_Data(map_size)
si=Mine_Data(map_size)

s_old=Mine_Data(map_size)

pose= PoseStamped()


rospy.init_node('Agent', anonymous=True)
pose.header.frame_id= rospy.get_name()


pose_pub = rospy.Publisher('/pose',PoseStamped,queue_size=1)

# need to modify to get sold and snew


class Simulator:
	def __init__(self):
		self.update_flag=False

	def s_cb(self,grid):
		#if a.x > grid.info.origin.position.x -  grid.info.origin.position.z/2 and a.x <  grid.info.origin.position.x +  grid.info.origin.position.z/2+1:
			#if a.y >  grid.info.origin.position.y -  grid.info.origin.position.z/2 and a.y <  grid.info.origin.position.y +  grid.info.origin.position.z/2+1:

		#TEMP TURN OFF PARTIAL NETWORK
		#SOMETHING IS WRONG WITH NETWORK
		a.time_away_from_network=0
		for i in range(map_size):
			for j in range(map_size):
				s.seen[i][j]=grid.data[i*map_size+j]

		s.pre_num_unknown_locations = grid.info.origin.orientation.x


		for i in range(map_size):
			for j in range(map_size):
				s_old.seen[i][j]=int(grid.data[i*map_size+j+map_size*map_size])

		s_old.pre_num_unknown_locations = grid.info.origin.orientation.y

		#print s.get_reward()-s_old.get_reward(),s_old.get_reward(),sum(s_old.seen)

		self.update_flag=True

	def work_load_cb(self,grid):
		for i in range(len(Regions.region)):
			a.work_load[i]=grid.data[i]
		if a.current_action.index > 0:
			if a.work_load[a.current_action.index-1] == 0:
				a.work_load[a.current_action.index-1]=1


	def reset_cb(self,data):
		s.reset()
		a.reset(s)


		write_file(a.solver.H,pose.header.frame_id)


	def run(self):
		a.new_A.update_all(s,a)
		while not rospy.is_shutdown():
			start=time.time()
			s.imprint(si)
			a.step(si,ai,.1)
			s.imprint(si)
			to_wait = start-time.time() + .1
			

			if to_wait >0:
				time.sleep(to_wait)

			if self.update_flag is True:
				a.update_heuristics(s_old,s)
				self.update_flag=False
			#else:
			#	a.predict_A()
				#predict si


			a.decide(s)

			pose.pose.position.x=a.x
			pose.pose.position.y=a.y
			pose.pose.position.z=a.battery
			pose.pose.orientation.x=a.current_action.index-1
			pose.pose.orientation.y=a.time_away_from_network
			pose_pub.publish(pose)

		




###MAIN
def main(args):


	sim = Simulator()
	environment_sub =rospy.Subscriber('/environment_matrix', OccupancyGrid , sim.s_cb)#CHANGE TO MATRIX

	occ_sub =rospy.Subscriber('/work_load', OccupancyGrid , sim.work_load_cb)#CHANGE TO MATRIX
	reset_sub =rospy.Subscriber('/reset', Int32 , sim.reset_cb)#CHANGE TO MATRIX
	#time.sleep(random.random()*10	)

	try:
		sim.run()
		rospy.spin()

	except KeyboardInterrupt:
		print("Draw: Shutting down")



if __name__ == '__main__':
	main(sys.argv)

