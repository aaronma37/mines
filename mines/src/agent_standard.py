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

import environment_classes

''' This is the ros file that runs an agent'''

f_path = rospy.get_param("/temp_file_path")


event_time_horizon = rospy.get_param("/event_time_horizon")
agent_poll_time = rospy.get_param("/agent_poll_time")
multi_agent_model = rospy.get_param("/multi_agent_model")
a_step_time = rospy.get_param("/agent_step_time")
agent_policy_steps = rospy.get_param("/agent_policy_steps")


ready_msg=Bool()
ready_msg.data=True
task= PoseStamped()


rospy.init_node('Agent', anonymous=True)
a = Agent(50,rospy.get_name())

task.header.frame_id= rospy.get_name()


pose_pub = rospy.Publisher('/pose',uuv_data,queue_size=1)

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

	def environment_cb(self,env_msg):
		self.complete_environment.update(env_msg)
		self.update_flag=True



	def ready_pub(self):
		ready_publisher.publish(ready_msg)


	def alpha_pub(self):
		alpha.data=[]
		for i in alpha.alpha_rewards:
			alpha.data.append(i)
			
		alpha_pub.publish(alpha)

	def reset_cb(self,data):
		self.reset_flag=True
		self.reset_data=data

	def reset_fun(self,performance):
		s.reset()
		a.reset(s,performance,f_path,UUV_Data.frame_id)

	def restart_cb(self,data):
		a.restart(f_path)
		self.ready_pub()

		#write_file(a.solver.H,pose.header.frame_id)
		#time.sleep(random.random()*5.)
		#a.get_psi()


	def run(self):
		while not rospy.is_shutdown():
			start=time.time()
			if a.available_flag is True or 1==1:
				if self.update_flag is True:
					self.update_flag=False
				if self.reset_flag is True:
					self.reset_fun(self.reset_data)
					self.reset_flag=False
				a.step(self.complete_environment,a_step_time/2.)
				a.move(self.complete_environment)

				UUV_Data.x=int(a.x)
				UUV_Data.y=int(a.y)

				UUV_Data.task_list=[]
				for t in a.current_trajectory.task_list:
					task_message=task_msg()
					task_message.task=t.objectives[0][0]
					UUV_Data.task_list.append(task_message)

				UUV_Data.region_list=[]
				for r in a.current_sub_environment.region_list:
					region_message=region_msg()
					region_message.x=r[0]
					region_message.y=r[1]
					UUV_Data.region_list.append(region_message)

				

				pose_pub.publish(UUV_Data)



			to_wait = start-time.time() + a_step_time
		





			if to_wait >0:
				time.sleep(to_wait)



		




###MAIN
def main(args):
	time.sleep(1)

	sim = Simulator()
	environment_sub =rospy.Subscriber('/environment', environment , sim.environment_cb)#CHANGE TO MATRIX
	reset_sub =rospy.Subscriber('/reset', performance , sim.reset_cb)#CHANGE TO MATRIX
	restart_sub =rospy.Subscriber('/restart', performance , sim.restart_cb)#CHANGE TO MATRIX
	#time.sleep(random.random()*5.)

	try:
		sim.run()
		rospy.spin()

	except KeyboardInterrupt:
		print("Draw: Shutting down")



if __name__ == '__main__':
	main(sys.argv)

