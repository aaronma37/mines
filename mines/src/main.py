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
from mines.msg import environment
from mines.msg import performance
from mines.msg import trajectory
from mines.msg import uuv_data
from mines.msg import beta_set as beta_set_msg
from mines.msg import collective_beta as collective_beta_msg
from mines.msg import collective_interaction as collective_interaction_msg
from mines.msg import collective_trajectories as collective_trajectories_msg
from mines.msg import interaction_list as interaction_list_msg
from std_msgs.msg import Int32
from agent_classes import Agent
from mines.msg import reset as reset_msg
import sys
from pynput import mouse
from multiprocessing import Process
from draw import gui_data

time_increment = rospy.get_param("/time_increment")

parameter_file = rospy.get_param("/parameter_file")

regulation_time = rospy.get_param("/regulation_time")
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
agent_interaction_length = rospy.get_param("/agent_interaction_length")
test_counter = rospy.get_param("/test_counter")
test_type = rospy.get_param("/test_type")
a_step_time = rospy.get_param("/agent_step_time")
agent_policy_steps = rospy.get_param("/agent_policy_steps")

total_time=regulation_time*agent_policy_steps

rospy.init_node('main', anonymous=True)
env_pub =rospy.Publisher('/environment', environment, queue_size=100)

reset_publisher = rospy.Publisher('/reset', reset_msg, queue_size=100)#CHANGE TO MATRIX
restart_publisher = rospy.Publisher('/restart', performance, queue_size=100)#CHANGE TO MATRIX


collective_beta_pub = rospy.Publisher('/Collective_beta', collective_beta_msg, queue_size=100)#CHANGE TO MATRIX
collective_interaction_pub = rospy.Publisher('/Collective_interaction', collective_interaction_msg, queue_size=100)#CHANGE TO MATRIX
collective_trajectory_pub = rospy.Publisher('/Collective_trajectories', collective_trajectories_msg, queue_size=100)#CHANGE TO MATRIX




region = [(10,10),(10,30),(10,50),(10,70),(10,90),(30,10),(50,10),(70,10),(90,10),(30,30),(50,30),(70,30),(90,30),(30,50),(50,50),(70,50),(90,50),(30,70),(50,70),(70,70),(90,70),(30,90),(50,90),(70,90),(90,90)]

region_size=10


gd=gui_data()






agent_dict = {}# {Agent Identity:Agent}
performance_msg = performance()
performance_msg.exploration=0
performance_msg.mines=0

reset_ = Int32()
reset_.data = 0

restart_=Int32()
restart_.data=0

networks = OccupancyGrid()

env_msg=environment()
env_msg.frame_id="environment"
test_type_flag=False


class Simulator:

	def __init__(self):
		self.complete_environment=environment_classes.Complete_Environment()
		#self.map_for_test=[(1,.1),(1,.3162),(1,1.),(1,3.162),(1,10.),(1,31.62),(1,100.)]
		t_list=[.0001,.0003162,.001,.003162,.01,.03162,.1,.3162,1.,3.162]#,10.]
		self.map_for_test=[]
		self.think_steps={}
		self.expected_final_performance={}
		for n in range(3):

			self.think_steps[n]={}
			self.expected_final_performance[n]={}
			for t in t_list:
				self.think_steps[n][t]=[]
				self.expected_final_performance[n][t]=[]

		for k in range(100):
			for t in t_list:
				for n in range(3):
					self.map_for_test.append((n,t))

		#self.map_for_test=[(0,.001),(0,.003162),(0,.01),(0,.03162),(0,.1),(0,.3162),(0,1.),(0,3.162),(0,10.),(0,31.62),(0,100.)]
		self.sim_count=0
		self.num_eval=1
		self.sim_time=50
		self.total_sims=500
		self.cull=20

		self.initial_cost=self.complete_environment.get_aggregate_cost()
		self.wait_flag=False
		self.collective_beta_message=collective_beta_msg()
		self.collective_interaction_message=collective_interaction_msg()
		self.final_performance=[]
		self.collective_trajectory_message=collective_trajectories_msg()
		self.a_step_time=a_step_time
		self.total_time=total_time
		self.trigger_agent="/a1"
		self.test_counter=0

		self.agent_dict={}
		self.test_num=0
		self.num_agent_traj=self.map_for_test[self.test_num][0]
		self.var_step_time=self.map_for_test[self.test_num][1]

	def agent_cb(self,agent_data):
		#if test_type_flag==False or agent_data.frame_id=="/a3":
		if agent_data.frame_id not in self.agent_dict:
			self.agent_dict[agent_data.frame_id]=Agent(30,agent_data.frame_id,4,0)

		if agent_data.frame_id=="/a1":
			self.trigger_agent="/a2"
		elif agent_data.frame_id=="/a2":
			self.trigger_agent="/a3"
			#test_type_flag=True
		elif agent_data.frame_id=="/a3":
			self.trigger_agent="/a4"



		self.agent_dict[agent_data.frame_id].x=int(agent_data.x)
		self.agent_dict[agent_data.frame_id].y=int(agent_data.y)
	#	self.agent_dict[agent_data.frame_id].current_sub_environment.state=agent_data.current_state

		#self.complete_environment.execute_objective("service",(agent_dict[agent_data.frame_id].x,agent_dict[agent_data.frame_id].y))
		try:
			self.agent_dict[agent_data.frame_id].my_action=str(agent_data.current_trajectory.task_trajectory[int(agent_data.current_trajectory.task_index)])
			self.agent_dict[agent_data.frame_id].my_action_index=str(int(agent_data.current_trajectory.task_index))
			self.complete_environment.execute_objective(self.agent_dict[agent_data.frame_id].my_action,(self.agent_dict[agent_data.frame_id].x,self.agent_dict[agent_data.frame_id].y))
			self.agent_dict[agent_data.frame_id].current_state=agent_data.current_trajectory.state
			self.agent_dict[agent_data.frame_id].expected_reward=agent_data.expected_reward
			self.agent_dict[agent_data.frame_id].think_step=agent_data.steps
		except IndexError:
			''' '''

		flag=None

		for i in range(len(self.collective_trajectory_message.agent_trajectory)):
			if self.collective_trajectory_message.agent_trajectory[i].frame_id==agent_data.current_trajectory.frame_id:
				self.collective_trajectory_message.agent_trajectory[i]=agent_data.current_trajectory
				flag=i
				break

		if flag is None:
			self.collective_trajectory_message.agent_trajectory.append(agent_data.current_trajectory)
		else:
			self.collective_trajectory_message.agent_trajectory[i]=agent_data.current_trajectory




		if agent_data.frame_id=="/a3":
			self.reset_pub(True)


	def trajectory_cb(self,data):
		if data.frame_id not in self.agent_dict:
			self.agent_dict[data.header.frame_id]=Agent(agent_poll_time,event_time_horizon,data.frame_id,agent_policy_steps)

		self.agent_dict[data.frame_id].trajectory.action_trajectory=data.action_trajectory
		self.agent_dict[data.frame_id].trajectory.region_trajectory=data.region_trajectory




		self.append_events(data)

	def ready_cb(self,data):
		self.wait_flag=False




	def beta_cb(self,msg):
		for i in range(len(self.collective_beta_message.agent_beta)):
			if self.collective_beta_message.agent_beta[i].frame_id==msg.frame_id:
				self.collective_beta_message.agent_beta[i]=msg
				return
		self.collective_beta_message.agent_beta.append(msg)



	def interaction_cb(self,msg):
		for i in range(len(self.collective_interaction_message.agent_interaction)):
			if self.collective_interaction_message.agent_interaction[i].frame_id==msg.frame_id:
				self.collective_interaction_message.agent_interaction[i]=msg
				return
		self.collective_interaction_message.agent_interaction.append(msg)


	def beta_pub(self):
		collective_beta_pub.publish(self.collective_beta_message)

	def interaction_pub(self):
		collective_interaction_pub.publish(self.collective_interaction_message)

	def environment_pub(self):
		env_pub.publish(self.complete_environment.generate_environment_msg(self.collective_trajectory_message,self.trigger_agent,self.num_agent_traj,self.var_step_time))




	def traj_pub(self):
		collective_trajectory_pub.publish(self.collective_trajectory_message)


	def write_performance(self,performance):
		print "Summary- - - \n N=", str(self.num_agent_traj),'\n step time: ',str(self.var_step_time),
		self.final_performance.append(performance)

		for a in self.agent_dict.values():
			if int(a.think_step)<1:
				if a.id=="/a3":
					self.test_counter-=1
					print "FAILURE"
					return

		self.expected_final_performance[self.num_agent_traj][self.var_step_time].append(0.)
		self.think_steps[self.num_agent_traj][self.var_step_time].append(0.)
		for a in self.agent_dict.values():
			if test_type=="famine":
				if a.id=="/a3":
					self.expected_final_performance[self.num_agent_traj][self.var_step_time][-1]+=a.expected_reward
					self.think_steps[self.num_agent_traj][self.var_step_time][-1]+=a.think_step
			else:
				self.expected_final_performance[self.num_agent_traj][self.var_step_time][-1]+=a.expected_reward
				self.think_steps[self.num_agent_traj][self.var_step_time][-1]+=a.think_step

		#print self.expected_final_performance[self.num_agent_traj][self.var_step_time], self.think_steps[self.num_agent_traj][self.var_step_time]
		print '\n Avg expected performance',sum( self.expected_final_performance[self.num_agent_traj][self.var_step_time])/len( self.expected_final_performance[self.num_agent_traj][self.var_step_time]),'\n Avg num trials', sum( self.think_steps[self.num_agent_traj][self.var_step_time])/len( self.think_steps[self.num_agent_traj][self.var_step_time]),'\n Num tests:',len( self.expected_final_performance[self.num_agent_traj][self.var_step_time])


		#test 6 is plethora test#
		#test 7 is third agent, starving#
		#test 11 is ?#
		print '-----------------------', self.test_counter/test_counter*100., '% complete'
		file = open(f_path+'/'+parameter_file+'_' + str(self.num_agent_traj) + ".0_" + str(self.var_step_time) +'.txt','w')

		for r in self.expected_final_performance[self.num_agent_traj][self.var_step_time]:
			file.write(str(r)+", ")

		file.write("\n\n")

		for r in self.think_steps[self.num_agent_traj][self.var_step_time]:
			file.write(str(r)+", ")

		file.close()
		print '\n'


	def reset_pub(self,recalculate_policy_flag):

		#self.wait_flag=True
		#performance_msg.exploration=self.complete_environment.get_reward_1()
		#performance_msg.mines=self.complete_environment.get_reward_2()
		self.collective_trajectory_message=collective_trajectories_msg()
		self.write_performance(self.initial_cost-self.complete_environment.get_aggregate_cost())
		self.test_counter+=1
		if self.test_counter<test_counter:
			self.complete_environment.reset()
			#if test_type!="famine":
			self.agent_dict={}
			reset_publisher.publish(performance_msg)
		#restart_publisher.publish(performance_msg)
			self.initial_cost=self.complete_environment.get_aggregate_cost()
			time.sleep(1)
			self.complete_environment.reset()
			#time.sleep(2)
			#self.complete_state.reset()	

			#restart_publisher.publish(performance_msg)
			self.a_step_time+=time_increment
			self.total_time=regulation_time*agent_policy_steps
			self.trigger_agent="/a1"
		else:
			if len(self.map_for_test)+1>=self.test_num is None:
				rospy.signal_shutdown("Test finished")
			else:
				#self.expected_final_performance=[]
				#self.think_steps=[]
				self.test_num+=1
				self.test_counter=0
				self.num_agent_traj=self.map_for_test[self.test_num][0]
				self.var_step_time=self.map_for_test[self.test_num][1]

				self.complete_environment.reset()
				self.agent_dict={}
				reset_message=reset_msg()
				reset_message.max_interaction_num=self.num_agent_traj
				reset_publisher.publish(reset_message)
			#restart_publisher.publish(performance_msg)
				self.initial_cost=self.complete_environment.get_aggregate_cost()
				time.sleep(1)
				self.complete_environment.reset()
				#time.sleep(2)
				#self.complete_state.reset()	

				#restart_publisher.publish(performance_msg)
				self.a_step_time+=time_increment
				self.total_time=regulation_time*agent_policy_steps
				self.trigger_agent="/a1"



	def run(self):

		start = time.time()
		start2= time.time()
		asynch_timer=time.time()
		self.wait_flag=False
		self.complete_environment.reset()
		self.sim_count=0

		while not rospy.is_shutdown():
			draw.render_once(self.complete_environment,self.agent_dict,gd,self.reset_pub,time.time()-start2)

			#if time.time()-start > 100:
				#s.reset()
			#	start = time.time()

			if self.wait_flag==True:
				start2=time.time()

			agents=list(self.agent_dict.keys())
			self.agent_num = len(agents)

			if time.time()-start > regulation_time:
				self.environment_pub()
				self.beta_pub()
				self.interaction_pub()
				self.traj_pub()
				start = time.time()

			if time.time()-start2 > self.total_time:
				#self.sim_count+=1
				#if self.sim_count > self.total_sims:
				#	return
				#if self.sim_count%self.num_eval==0 or self.sim_count==1:
				self.reset_pub(True)
				#else:
				#	self.reset_pub(False)


###MAIN
def main(args):

	sim=Simulator()
	posesub =rospy.Subscriber('/pose', uuv_data, sim.agent_cb)#CHANGE TO MATRIX
	agent_trajectory_sub =rospy.Subscriber('/trajectory', trajectory, sim.trajectory_cb)#CHANGE TO MATRIX
	ready_sub =rospy.Subscriber('/ready', Bool, sim.ready_cb)#CHANGE TO MATRIX
	beta_sub = rospy.Subscriber('/Beta',beta_set_msg,sim.beta_cb)
	beta_sub = rospy.Subscriber('/Interaction',interaction_list_msg,sim.interaction_cb)

	try:
		sim.run()
		rospy.spin()



#
	except KeyboardInterrupt:
		print("Draw: Shutting down")


if __name__ == '__main__':
	main(sys.argv)






















