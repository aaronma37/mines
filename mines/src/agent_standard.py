#!/usr/bin/env python


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

from mines.msg import trajectory
from mines.msg import environment
from mines.msg import performance
from std_msgs.msg import Bool
from mines.msg import uuv_data
from mines.msg import task as task_msg
from mines.msg import region as region_msg

from mines.msg import beta_set as beta_set_msg
from mines.msg import beta as beta_msg
from mines.msg import claimed_objective as claimed_objective_msg

from mines.msg import interaction_list as interaction_list_msg
from mines.msg import collective_beta as collective_beta_msg
from mines.msg import collective_interaction as collective_interaction_msg
from mines.msg import collective_trajectories as collective_trajectories_msg

import environment_classes

''' This is the ros file that runs an agent'''

f_path = rospy.get_param("/temp_file_path")


event_time_horizon = rospy.get_param("/event_time_horizon")
agent_poll_time = rospy.get_param("/agent_poll_time")
multi_agent_model = rospy.get_param("/multi_agent_model")
a_step_time = rospy.get_param("/agent_step_time")
agent_policy_steps = rospy.get_param("/agent_policy_steps")
agent_interaction_length = rospy.get_param("/agent_interaction_length")

agent_trajectory_length = int(rospy.get_param("/agent_trajectory_length"))


ready_msg=Bool()
ready_msg.data=True
task= PoseStamped()


rospy.init_node('Agent', anonymous=True)
a = Agent(event_time_horizon,rospy.get_name(),agent_trajectory_length,agent_interaction_length)

if rospy.get_name()=="/a1":
	print  "initializing /a1"
	sleep_time=0
elif rospy.get_name()=="/a2":
	print  "initializing /a2"
	sleep_time=a_step_time*event_time_horizon/16.
elif rospy.get_name()=="/a3":
	print  "initializing /a3"
	sleep_time=2.*a_step_time*event_time_horizon/16.
elif rospy.get_name()=="/a4":
	print  "initializing /a4"
	sleep_time=3.*a_step_time*event_time_horizon/16.
elif rospy.get_name()=="/a5":
	print  "initializing /a5"
	sleep_time=4.*a_step_time*event_time_horizon/16.
elif rospy.get_name()=="/a6":
	print  "initializing /a6"
	sleep_time=5.*a_step_time*event_time_horizon/16.
elif rospy.get_name()=="/a7":
	print  "initializing /a7"
	sleep_time=6.*a_step_time*event_time_horizon/16.
elif rospy.get_name()=="/a8":
	print  "initializing /a6"
	sleep_time=7.*a_step_time*event_time_horizon/16.
elif rospy.get_name()=="/a9":
	print  "initializing /a6"
	sleep_time=8.*a_step_time*event_time_horizon/16.
elif rospy.get_name()=="/a10":
	print  "initializing /a6"
	sleep_time=9.*a_step_time*event_time_horizon/16.
elif rospy.get_name()=="/a11":
	print  "initializing /a6"
	sleep_time=10.*a_step_time*event_time_horizon/16.
elif rospy.get_name()=="/a12":
	print  "initializing /a6"
	sleep_time=11.*a_step_time*event_time_horizon/16.
elif rospy.get_name()=="/a13":
	print  "initializing /a6"
	sleep_time=12.*a_step_time*event_time_horizon/16.
elif rospy.get_name()=="/a14":
	print  "initializing /a6"
	sleep_time=13.*a_step_time*event_time_horizon/16.
elif rospy.get_name()=="/a15":
	print  "initializing /a6"
	sleep_time=14.*a_step_time*event_time_horizon/16.
elif rospy.get_name()=="/a16":
	print  "initializing /a6"
	sleep_time=15.*a_step_time*event_time_horizon/16.

task.header.frame_id= rospy.get_name()


pose_pub = rospy.Publisher('/pose',uuv_data,queue_size=1)
beta_pub = rospy.Publisher('/Beta',beta_set_msg,queue_size=1)
interaction_pub = rospy.Publisher('/Interaction',interaction_list_msg,queue_size=1)

beta_message=beta_set_msg()
interaction_message=interaction_list_msg()


trajectory_pub = rospy.Publisher('/trajectory',trajectory,queue_size=100)
ready_publisher = rospy.Publisher('/ready',Bool,queue_size=100)
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
		self.complete_environment=environment_classes.Complete_Environment()
		self.beta_set_message=beta_set_msg()
		self.sleep_time=0.

	def environment_cb(self,env_msg):
		self.complete_environment.update(env_msg)
		self.complete_environment.modify(a.claimed_objective_sets.effective_claimed_objectives)
		self.complete_environment.update_from_agent(a)
		self.update_flag=True


	def collective_interaction_cb(self,msg):
		a.interaction_list.update_others(msg)

	def collective_trajectories_cb(self,msg):
		a.update_collective_trajectories(msg)


	def collective_beta_cb(self,msg):
		a.claimed_objective_sets.collect_taken_objectives(msg)
		a.claimed_objective_sets.construct_effective_claimed_objectives(rospy.get_name(),a.interaction_list)


	def ready_pub(self):
		ready_publisher.publish(ready_msg)


	def alpha_pub(self):
		alpha.data=[]
		for i in alpha.alpha_rewards:
			alpha.data.append(i)
			
		alpha_pub.publish(alpha)

	def reset_cb(self,data):
		#self.reset_flag=True
		#self.reset_data=data
		time.sleep(.5)
		self.sleep_time=sleep_time
		a.reset(f_path)
		a.x=50
		a.y=50
		time.sleep(.5)


	def reset_fun(self,performance):
		#s.reset()
		#a.reset(s,performance,f_path,UUV_Data.frame_id)	
		time.sleep(1)	
		a = Agent(event_time_horizon,rospy.get_name(),agent_trajectory_length)
		a.x=50	
		a.y=50	

		print "HEREERE"
		
	def restart_cb(self,data):
		#a.restart(f_path)
		self.ready_pub()

		#write_file(a.solver.H,pose.header.frame_id)
		#time.sleep(random.random()*5.)
		#a.get_psi()


	def update_messages(self):
		UUV_Data.x=int(a.x)
		UUV_Data.y=int(a.y)

		UUV_Data.task_list=[]
		UUV_Data.current_trajectory.task_trajectory=[]

		for t in a.current_trajectory.task_list:
			task_message=task_msg()
			task_message.task=t.objectives[0][0]
			UUV_Data.task_list.append(task_message)
			UUV_Data.current_trajectory.task_trajectory.append(t.objectives[0][0])

		UUV_Data.region_list=[]
		UUV_Data.current_state=a.current_sub_environment.state
		UUV_Data.current_trajectory.state=a.current_sub_environment.state
		UUV_Data.current_trajectory.region_trajectory=[]
		UUV_Data.current_trajectory.frame_id=rospy.get_name()
		for i in range(len(a.current_sub_environment.region_list)):
			region_message=region_msg()
			region_message.x=a.current_sub_environment.region_list[i][0]
			region_message.y=a.current_sub_environment.region_list[i][1]
			UUV_Data.current_trajectory.region_trajectory.append(region_message)

			
		UUV_Data.current_trajectory.task_index=a.current_trajectory.current_index

		for r in a.current_sub_environment.region_list:
			region_message=region_msg()
			region_message.x=r[0]
			region_message.y=r[1]
			UUV_Data.region_list.append(region_message)

		a.update_claimed_objectives()


	def send_messages(self):
		pose_pub.publish(UUV_Data)

		beta_message=a.claimed_objective_sets.owned_objectives
		interaction_message=a.interaction_list.interaction_list



		beta_pub.publish(beta_message)	
		interaction_pub.publish(interaction_message)
			

				


	def run(self):
		while not rospy.is_shutdown():
			start=time.time()
			time.sleep(self.sleep_time)
			self.sleep_time=0.
			if a.available_flag is True or 1==1:
				if self.update_flag is True:
					self.update_flag=False
				if self.reset_flag is True:
					self.reset_fun(self.reset_data)
					self.reset_flag=False
				a.step(self.complete_environment,a_step_time/2.)
				a.move(self.complete_environment,a_step_time/2.)

				self.update_messages()
				self.send_messages()




			to_wait = start-time.time() + a_step_time
		





			if to_wait >0:
				time.sleep(to_wait)



		




###MAIN
def main(args):
	time.sleep(sleep_time)

	sim = Simulator()
	environment_sub =rospy.Subscriber('/environment', environment , sim.environment_cb)#CHANGE TO MATRIX
	reset_sub =rospy.Subscriber('/reset', performance , sim.reset_cb)#CHANGE TO MATRIX
	restart_sub =rospy.Subscriber('/restart', performance , sim.restart_cb)#CHANGE TO MATRIX
	#time.sleep(random.random()*5.)
	collective_beta_sub =rospy.Subscriber('/Collective_beta', collective_beta_msg , sim.collective_beta_cb)#CHANGE TO MATRIX
	collective_interact_sub =rospy.Subscriber('/Collective_interact', collective_interaction_msg , sim.collective_interaction_cb)#CHANGE TO MATRIX
	collective_trajectories_sub =rospy.Subscriber('/Collective_trajectories', collective_trajectories_msg , sim.collective_trajectories_cb)#CHANGE TO MATRIX

	try:
		sim.run()
		rospy.spin()

	except KeyboardInterrupt:
		print("Draw: Shutting down")



if __name__ == '__main__':
	main(sys.argv)

