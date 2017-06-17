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
from mines.msg import reset as reset_msg

import environment_classes

''' This is the ros file that runs an agent'''

pre_train_time = rospy.get_param("/pre_train_time")
f_path = rospy.get_param("/temp_file_path")
regulation_time = rospy.get_param("/regulation_time")
time_increment = rospy.get_param("/time_increment")
event_time_horizon = rospy.get_param("/event_time_horizon")
agent_poll_time = rospy.get_param("/agent_poll_time")
multi_agent_model = rospy.get_param("/multi_agent_model")
a_step_time = rospy.get_param("/agent_step_time")
agent_policy_steps = rospy.get_param("/agent_policy_steps")
agent_interaction_length = rospy.get_param("/agent_interaction_length")

agent_trajectory_length = int(rospy.get_param("/agent_trajectory_length"))

test_case=True

ready_msg=Bool()
ready_msg.data=True
task= PoseStamped()


rospy.init_node('Agent', anonymous=True)
a = Agent(event_time_horizon,rospy.get_name(),agent_trajectory_length,agent_interaction_length)


sp=regulation_time
num_ag=5.
total_agents=5.

if rospy.get_name()=="/a1":
	print  "initializing /a1"
	sleep_time=0
	agent_index=0
elif rospy.get_name()=="/a2":
	print  "initializing /a2"
	sleep_time=sp*event_time_horizon/num_ag
	sleep_time=.5
	agent_index=1
elif rospy.get_name()=="/a3":
	print  "initializing /a3"
	sleep_time=2.*sp*event_time_horizon/num_ag
	sleep_time=1.
	agent_index=2
elif rospy.get_name()=="/a4":
	print  "initializing /a4"
	sleep_time=3.*sp*event_time_horizon/num_ag
	sleep_time=1.5
	agent_index=3
elif rospy.get_name()=="/a5":
	print  "initializing /a5"
	sleep_time=4.*sp*event_time_horizon/num_ag
	sleep_time=2.
	agent_index=4
elif rospy.get_name()=="/a6":
	print  "initializing /a6"
	sleep_time=5.*sp*event_time_horizon/num_ag
elif rospy.get_name()=="/a7":
	print  "initializing /a7"
	sleep_time=6.*sp*event_time_horizon/num_ag
elif rospy.get_name()=="/a8":
	print  "initializing /a6"
	sleep_time=7.*sp*event_time_horizon/num_ag
elif rospy.get_name()=="/a9":
	print  "initializing /a6"
	sleep_time=8.*sp*event_time_horizon/16.
elif rospy.get_name()=="/a10":
	print  "initializing /a6"
	sleep_time=9.*sp*event_time_horizon/16.
elif rospy.get_name()=="/a11":
	print  "initializing /a6"
	sleep_time=10.*sp*event_time_horizon/16.
elif rospy.get_name()=="/a12":
	print  "initializing /a6"
	sleep_time=11.*sp*event_time_horizon/16.
elif rospy.get_name()=="/a13":
	print  "initializing /a6"
	sleep_time=12.*sp*event_time_horizon/16.
elif rospy.get_name()=="/a14":
	print  "initializing /a6"
	sleep_time=13.*sp*event_time_horizon/16.
elif rospy.get_name()=="/a15":
	print  "initializing /a6"
	sleep_time=14.*sp*event_time_horizon/16.
elif rospy.get_name()=="/a16":
	print  "initializing /a6"
	sleep_time=15.*sp*event_time_horizon/16.

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
		self.trigger=False
		self.over=False
		self.complete_environment=environment_classes.Complete_Environment()
		self.beta_set_message=beta_set_msg()
		self.sleep_time=0.
		self.a_step_time=a_step_time
		self.agent_interaction_length=agent_trajectory_length

	def environment_cb(self,env_msg):
		self.complete_environment.update(env_msg)
		self.complete_environment.modify(a.claimed_objective_sets.beta_hash)
		self.complete_environment.update_from_agent(a)

		if env_msg.trigger==rospy.get_name():
			if self.over==False:
				#print "trigger", rospy.get_name()
				self.trigger=True
				#print env_msg.step_time
				self.a_step_time=env_msg.step_time
				self.agent_interaction_length=env_msg.num_agent_traj
		else:
			self.trigger=False
		self.update_flag=True

	def update_environment(self):
		self.complete_environment.execute_objective('mine',(a.x,a.y))
		#self.complete_environment.execute_objective('service',(a.x,a.y))

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

	def reset_cb(self,reset_message):
		#self.reset_flag=True
		#self.reset_data=data
		time.sleep(.5)
		self.trigger=False
		self.over=False
		self.sleep_time=0
		self.complete_environment=environment_classes.Complete_Environment()
		a.reset(f_path,[reset_message.max_interaction_num])

		a.x=50
		a.y=50
		#time.sleep(.5)
		self.a_step_time+=time_increment


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

		if a.current_trajectory is None or a.current_sub_environment is None:
			return

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
			try:
				region_message.x=a.current_sub_environment.region_list[i][0]
				region_message.y=a.current_sub_environment.region_list[i][1]
			except IndexError:
				''' '''

			UUV_Data.current_trajectory.region_trajectory.append(region_message)

                # print a.think_step
		UUV_Data.expected_reward=a.expected_reward

			
		UUV_Data.current_trajectory.task_index=a.current_trajectory.current_index
		UUV_Data.steps=int(a.think_step)

		for r in a.current_sub_environment.region_list:
			region_message=region_msg()
			region_message.x=r[0]
			region_message.y=r[1]
			UUV_Data.region_list.append(region_message)

		a.update_claimed_objectives()


        def request_pre_train(self,pt_msg):
            if pt_msg.data==True:
                a.step(self.complete_environment,pre_train_time)

	def send_messages(self):
		if len(UUV_Data.task_list)>0 and self.trigger==True:
			pose_pub.publish(UUV_Data)
			UUV_Data.task_list=[]
			self.trigger=False
			self.over=True

		beta_message=a.claimed_objective_sets.owned_objectives
		interaction_message=a.interaction_list.interaction_list



		beta_pub.publish(beta_message)	
		interaction_pub.publish(interaction_message)
			

				


	def run(self):
		while not rospy.is_shutdown():
			start=time.time()
			#time.sleep(self.sleep_time)
			self.sleep_time=0.
			if a.available_flag is True or 1==1:
				if self.update_flag is True:
					self.update_flag=False
				if self.reset_flag is True:
					self.reset_fun(self.reset_data)
					self.reset_flag=False

				if test_case==False:
					a.step(self.complete_environment,self.a_step_time/2.)
					a.move(self.complete_environment,self.a_step_time/2.)
					to_wait = start-time.time() + regulation_time #self.a_step_time
				else:
					if self.trigger==True:
					#a.test_case_choose(self.complete_environment,self.a_step_time/2.)
						#print rospy.get_name(), " is beginning"
						a.step_test(self.complete_environment,self.a_step_time)

						a.test_case_move(agent_index,total_agents,self.complete_environment,self.a_step_time)
					#a.move(self.complete_environment,self.a_step_time/2.)	
						self.update_messages()
						self.send_messages()
						self.trigger=False
						self.over=True
					to_wait = .1
				self.update_messages()
				self.send_messages()
				self.update_environment()

		





			if to_wait >0:
				time.sleep(to_wait)



		




###MAIN
def main(args):
	time.sleep(sleep_time)

	sim = Simulator()
        pt_sub = rospy.Subscriber('/pt',Bool,sim.request_pre_train)
	environment_sub =rospy.Subscriber('/environment', environment , sim.environment_cb)#CHANGE TO MATRIX
	reset_sub =rospy.Subscriber('/reset', reset_msg , sim.reset_cb)#CHANGE TO MATRIX
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

