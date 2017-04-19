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
from mines.msg import trajectory
from Heuristics import write_file
from mines.msg import event
from mines.msg import event_region
from mines.msg import event_time
from mines.msg import map_info
from mines.msg import uuv_data

''' This is the ros file that runs an agent'''

f_path = rospy.get_param("/temp_file_path")

region = [(10,10),(10,30),(10,50),(10,70),(10,90),(30,10),(50,10),(70,10),(90,10),(30,30),(50,30),(70,30),(90,30),(30,50),(50,50),(70,50),(90,50),(30,70),(50,70),(70,70),(90,70),(30,90),(50,90),(70,90),(90,90)]

region_size=20


map_size=100
event_time_horizon = rospy.get_param("/event_time_horizon")
agent_poll_time = rospy.get_param("/agent_poll_time")
multi_agent_model = rospy.get_param("/multi_agent_model")
a_step_time = rospy.get_param("/agent_step_time")



s=Mine_Data(map_size,0)
si=Mine_Data(map_size,0)

s_old=Mine_Data(map_size,0)


task= PoseStamped()


rospy.init_node('Agent', anonymous=True)
a = Agent(agent_poll_time,event_time_horizon,rospy.get_name())

task.header.frame_id= rospy.get_name()


pose_pub = rospy.Publisher('/pose',uuv_data,queue_size=1)

trajectory_pub = rospy.Publisher('/trajectory',trajectory,queue_size=100)
alpha_pub = rospy.Publisher('/alpha',OccupancyGrid,queue_size=1)

alpha = OccupancyGrid()

alpha.header.frame_id= rospy.get_name()
# need to modify to get sold and snew
UUV_Data= uuv_data()
UUV_Data.frame_id= rospy.get_name()

class Simulator:
	def __init__(self):
		self.update_flag=False
		self.reset_flag=False

	def environment_cb(self,e):
		a.time_away_from_network=0

		for i in range(map_size):
			for j in range(map_size):
				s.seen[i][j]=e.grid[i*map_size+j]

		s.pre_num_unknown_locations = e.new_exploration_reward
		s.update_charging_dock_locations(e.charging_dock_x,e.charging_dock_y)
		s.update_mine_locations(e.mines_x,e.mines_y)

		for i in range(map_size):
			for j in range(map_size):
				s_old.seen[i][j]=int(e.grid[i*map_size+j+map_size*map_size])

		s_old.pre_num_unknown_locations = e.old_exploration_reward

		self.update_flag=True

		
		

	def action_request_cb(self,Event):
		if Event.requested_agent==rospy.get_name():
			s.imprint(si)
			a.calculate_A(si)
			a.decide(si)
			
			a.clear_events()
			a.update_events(Event)

			trajectory_pub.publish(a.trajectory)






	def alpha_pub(self):
		alpha.data=[]
		for i in alpha.alpha_rewards:
			alpha.data.append(i)
			
		alpha_pub.publish(alpha)

	def reset_cb(self,data):
		self.reset_flag=True
		self.reset_data=data

	def reset_fun(self,data):
		s.reset()
		a.reset(s,data.data,f_path,UUV_Data.frame_id)

	def restart_cb(self,data):
		a.restart(f_path)


		#write_file(a.solver.H,pose.header.frame_id)
		#time.sleep(random.random()*5.)
		#a.get_psi()


	def run(self):
		a.new_A.update_all(s,a)
		while not rospy.is_shutdown():
			start=time.time()
			if a.available_flag is True:
				if self.update_flag is True:
					self.update_flag=False
				if self.reset_flag is True:
					self.reset_fun(self.reset_data)
					self.reset_flag=False


				s.imprint(si)
				a.calculate_A(si)
				a.move(s)

				UUV_Data.x=a.x
				UUV_Data.y=a.y
				UUV_Data.battery=int(a.battery)
				UUV_Data.work=a.current_action.index-1
				UUV_Data.time_away_from_network=a.time_away_from_network
				UUV_Data.display_action=a.display_action
				pose_pub.publish(UUV_Data)


				a.step(si,a_step_time/2.)
				#s.imprint(si)



				#else:
				#	a.predict_A()
					#predict si

			to_wait = start-time.time() + a_step_time
		





			if to_wait >0:
				time.sleep(to_wait)



		




###MAIN
def main(args):
	time.sleep(1)

	sim = Simulator()
	environment_sub =rospy.Subscriber('/environment_matrix', map_info , sim.environment_cb)#CHANGE TO MATRIX

	request_sub =rospy.Subscriber('/request_action', event , sim.action_request_cb)#CHANGE TO MATRIX
	reset_sub =rospy.Subscriber('/reset', Int32 , sim.reset_cb)#CHANGE TO MATRIX
	restart_sub =rospy.Subscriber('/restart', Int32 , sim.restart_cb)#CHANGE TO MATRIX
	#time.sleep(random.random()*5.)

	try:
		sim.run()
		rospy.spin()

	except KeyboardInterrupt:
		print("Draw: Shutting down")



if __name__ == '__main__':
	main(sys.argv)

