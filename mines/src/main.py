#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
from PIL import Image
import numpy as numpy
from agent_classes import Agent
import environment_classes
import draw
import math
import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Bool
from mines.msg import event
from mines.msg import event_region
from mines.msg import event_time
from mines.msg import performance
from mines.msg import trajectory
from mines.msg import map_info
from mines.msg import uuv_data

from std_msgs.msg import Int32
from agent_classes import Agent

import sys
from pynput import mouse
from multiprocessing import Process
from draw import gui_data
from mobile_buoy_classes import Agent_buoy
from mobile_buoy_environment import Mobile_Buoy_Environment
import Regions

import POMDP_Values as v

L_MAX=v.L_MAX
number_of_charging_docks = rospy.get_param("/number_of_charging_docks")
number_of_mines = rospy.get_param("/number_of_mines")
agent_policy_steps = rospy.get_param("/agent_policy_steps")
event_time_horizon = rospy.get_param("/event_time_horizon")
agent_poll_time = rospy.get_param("/agent_poll_time")
a_step_time = rospy.get_param("/agent_step_time")
load_q_flag = rospy.get_param("/load_q")
write_q_flag = rospy.get_param("/write_q")
write_psi_flag = rospy.get_param("/write_psi")
f_path = rospy.get_param("/temp_file_path")
trial_time = rospy.get_param("/total_trial_time")

rospy.init_node('main', anonymous=True)
env_pub =rospy.Publisher('/environment_matrix', map_info, queue_size=100)#CHANGE TO MATRIX

reset_publisher = rospy.Publisher('/reset', performance, queue_size=100)#CHANGE TO MATRIX
restart_publisher = rospy.Publisher('/restart', performance, queue_size=100)#CHANGE TO MATRIX
request_action_pub = rospy.Publisher('/request_action', event, queue_size=100)#CHANGE TO MATRIX

region = [(10,10),(10,30),(10,50),(10,70),(10,90),(30,10),(50,10),(70,10),(90,10),(30,30),(50,30),(70,30),(90,30),(30,50),(50,50),(70,50),(90,50),(30,70),(50,70),(70,70),(90,70),(30,90),(50,90),(70,90),(90,90)]

region_size=10


gd=gui_data()

objective_parameter_list=[]
objective_parameter_list.append(('All',3))


sb=Mobile_Buoy_Environment(map_size)
agent_dict = {}# {Agent Identity:Agent}
buoy_dict = {}
environment_information = map_info()
performance_msg = performance()
performance_msg.exploration=0
performance_msg.mines=0


Exploration_Event=event()
for region in range(len(Regions.region)):
	Exploration_Event.region.append(event_region())
	for t in range(event_time_horizon):
		Exploration_Event.region[region].time.append(event_time())

Exploration_Event.event_id=0

reset_ = Int32()
reset_.data = 0

restart_=Int32()
restart_.data=0

networks = OccupancyGrid()






for i in range(map_size):
	for j in range(map_size):
		environment_information.grid.append(0)

for i in range(map_size):
	for j in range(map_size):
		environment_information.grid.append(0)





class Simulator:

	def __init__(self):
		self.complete_environment=environment_classes.Complete_Environment(objective_parameter_list)

		self.sim_count=0
		self.num_eval=1
		self.sim_time=50
		self.total_sims=500
		self.cull=20

		self.wait_flag=False



	def pose_cb(self,uuv_data):
		if uuv_data.frame_id not in agent_dict:
			agent_dict[uuv_data.frame_id]=Agent(agent_poll_time,event_time_horizon,uuv_data.frame_id,agent_policy_steps)
	 



		agent_dict[uuv_data.frame_id].x=int(uuv_data.x)
		agent_dict[uuv_data.frame_id].y=int(uuv_data.y)
		agent_dict[uuv_data.frame_id].battery=int(uuv_data.battery)
		agent_dict[uuv_data.frame_id].work=int(uuv_data.work)
		agent_dict[uuv_data.frame_id].display_action=uuv_data.display_action
		agent_dict[uuv_data.frame_id].time_away_from_network=int(uuv_data.time_away_from_network)
		agent_dict[uuv_data.frame_id].current_state=uuv_data.current_state
		agent_dict[uuv_data.frame_id].measure(self.complete_environment,False)
		agent_dict[uuv_data.frame_id].mine(self.complete_environment,False)


	def trajectory_cb(self,data):
		if data.frame_id not in agent_dict:
			agent_dict[data.header.frame_id]=Agent(agent_poll_time,event_time_horizon,data.frame_id,agent_policy_steps)

		agent_dict[data.frame_id].trajectory.action_trajectory=data.action_trajectory
		agent_dict[data.frame_id].trajectory.region_trajectory=data.region_trajectory


	
		self.append_events(data)

	def pub_objectives(self):
		mine_objective_publisher.publish(mine_objective_msg)

	def ready_cb(self,data):
		self.wait_flag=False

	def reset_pub(self,recalculate_policy_flag):
	
		batteries=0

		for k,a in agent_dict.items():
			if a.battery>0:
				batteries+=1

		print batteries

		self.wait_flag=True
		performance_msg.exploration=self.complete_environment.get_reward_1()
		performance_msg.mines=self.complete_environment.get_reward_2()
		performance_msg.battery=batteries
		self.complete_state.reset()
		reset_publisher.publish(performance_msg)
		time.sleep(2)
		self.complete_state.reset()	

		restart_publisher.publish(performance_msg)





	def run(self):

		start = time.time()
		start2= time.time()
		asynch_timer=time.time()
		self.wait_flag=False
		self.complete_environment.reset()
		self.sim_count=0

		while not rospy.is_shutdown():
			draw.render_once(self.complete_environment,agent_dict,map_size,buoy_dict,gd,self.reset_pub,time.time()-start2)
			#if time.time()-start > 100:
				#s.reset()
			#	start = time.time()

			if self.wait_flag==True:
				start2=time.time()

			agents=list(agent_dict.keys())
			self.agent_num = len(agents)
			if self.agent_num > 0:
				if (time.time() - asynch_timer) > (agent_poll_time*a_step_time/self.agent_num):
					asynch_timer=time.time()
					self.pub2()

			if time.time()-start > .025:
				self.pub()
				#self.pub2()
				#self.pub_to_buoys()
				start = time.time()

			if time.time()-start2 > trial_time:
				self.sim_count+=1
				if self.sim_count > self.total_sims:
					return
				if self.sim_count%self.num_eval==0 or self.sim_count==1:
					self.reset_pub(True)
				else:
					self.reset_pub(False)

				#start2=time.time()


###MAIN
def main(args):

	sim=Simulator()
	posesub =rospy.Subscriber('/pose', uuv_data, sim.pose_cb)#CHANGE TO MATRIX
	agent_trajectory_sub =rospy.Subscriber('/trajectory', trajectory, sim.trajectory_cb)#CHANGE TO MATRIX
	ready_sub =rospy.Subscriber('/ready', Bool, sim.ready_cb)#CHANGE TO MATRIX

	try:
	
		sim.run()
		rospy.spin()



#
	except KeyboardInterrupt:
		print("Draw: Shutting down")
		


if __name__ == '__main__':
	main(sys.argv)






















