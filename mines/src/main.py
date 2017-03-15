#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
from PIL import Image
import numpy as numpy
from agent_classes import Agent
from environment_classes import get_sqr_loc
from environment_classes import get_norm_size
from environment_classes import Mine_Data
import draw
import math
import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import Int32MultiArray

from std_msgs.msg import Int32
from agent_classes import Agent

import sys
from pynput import mouse
from multiprocessing import Process
from draw import gui_data
from mobile_buoy_classes import Agent_buoy
from mobile_buoy_environment import Mobile_Buoy_Environment
import Regions




rospy.init_node('main', anonymous=True)
env_pub =rospy.Publisher('/environment_matrix', OccupancyGrid, queue_size=100)#CHANGE TO MATRIX

agent_occ =rospy.Publisher('/work_load', OccupancyGrid, queue_size=100)#CHANGE TO MATRIX
score_pub =rospy.Publisher('/buoy_scores', Int32MultiArray, queue_size=100)#CHANGE TO MATRIX
worker_pub =rospy.Publisher('/buoy_targets', Int32MultiArray, queue_size=100)#CHANGE TO MATRIX
reset_publisher = rospy.Publisher('/reset', Int32, queue_size=100)#CHANGE TO MATRIX


region = [(10,10),(10,30),(10,50),(10,70),(10,90),(30,10),(50,10),(70,10),(90,10),(30,30),(50,30),(70,30),(90,30),(30,50),(50,50),(70,50),(90,50),(30,70),(50,70),(70,70),(90,70),(30,90),(50,90),(70,90),(90,90)]

region_size=10


gd=gui_data()

map_size=100


sb=Mobile_Buoy_Environment(map_size)
agent_dict = {}# {Agent Identity:Agent}
buoy_dict = {}
o = OccupancyGrid()
o2= OccupancyGrid()
o3= Int32MultiArray()
o4= Int32MultiArray()
reset_ = Int32()
reset_.data = 0

networks = OccupancyGrid()






for i in range(map_size):
	for j in range(map_size):
		o.data.append(0)

for i in range(map_size):
	for j in range(map_size):
		o.data.append(0)

for i in range(len(region)):
		o2.data.append(0)
		o3.data.append(0)



class Simulator:

	def __init__(self):
		self.s=Mine_Data(map_size)
		self.s_old=Mine_Data(map_size)


	def pose_cb(self,data):
		if data.header.frame_id not in agent_dict:
			agent_dict[data.header.frame_id]=Agent(Mine_Data,map_size)
	 

		agent_dict[data.header.frame_id].x=int(data.pose.position.x)
		agent_dict[data.header.frame_id].y=int(data.pose.position.y)
		agent_dict[data.header.frame_id].battery=int(data.pose.position.z)
		agent_dict[data.header.frame_id].work=int(data.pose.orientation.x)
		agent_dict[data.header.frame_id].time_away_from_network=int(data.pose.orientation.y)

		agent_dict[data.header.frame_id].measure(self.s,False)

	def buoy_cb(self,data):
		if data.header.frame_id not in buoy_dict:
			buoy_dict[data.header.frame_id]=Agent_buoy(Mine_Data,map_size)


		buoy_dict[data.header.frame_id].x=int(data.pose.position.x)
		buoy_dict[data.header.frame_id].y=int(data.pose.position.y)
		buoy_dict[data.header.frame_id].current_action=buoy_dict[data.header.frame_id].policy_set[int(data.pose.orientation.x)]

	def pub(self):
	
		for i in range(map_size):
			for j in range(map_size):
				o.data[i*map_size+j]=self.s.seen[i][j]

		for i in range(map_size):
			for j in range(map_size):
				o.data[i*map_size+j+map_size*map_size]=self.s_old.seen[i][j]

		print self.s.get_reward()-self.s_old.get_reward()

		self.s.imprint(self.s_old)

		o.info.origin.position.x=map_size/2
		o.info.origin.position.y=map_size/2
		o.info.origin.position.z=20

		o.info.origin.orientation.x=self.s.pre_num_unknown_locations
		o.info.origin.orientation.y=self.s_old.pre_num_unknown_locations

		env_pub.publish(o)

		for k,b in buoy_dict.items():
			o.info.origin.position.x=b.x
			o.info.origin.position.y=b.y
			o.info.origin.position.z=20

			env_pub.publish(o)


	def calculate_work_load(self):
	
		for i in range(len(Regions.region)):
			o2.data[i]=0

		for k,a in agent_dict.items():
			if a.work >0 and a.work <26:
				o2.data[a.work]+=1

	
			

	def pub2(self):


	
		#s.calculate_occupied(agent_dict,region,region_size)


		self.calculate_work_load()
		#for i in range(len(region)):
		#		o2.data[i]=s.occupied[i]
		agent_occ.publish(o2)

	def reset_pub(self):
		reset_.data=self.s.get_reward()
		self.s.reset()

		reset_publisher.publish(reset_)
		agent_dict={}

	def pub_to_buoys(self):
		sb.calculate_region_score(agent_dict)
		for i in range(len(region)):
			o3.data[i]=sb.score[i]


		score_pub.publish(o3)
		o4.data=[]
		for k,b in buoy_dict.items():
			o4.data.append(int(b.current_action.index))

		worker_pub.publish(o4)
	


	def run(self):
		start = time.time()
		start2= time.time()
		self.s.reset()
		while not rospy.is_shutdown():
		
			draw.render_once(self.s,agent_dict,map_size,buoy_dict,gd,self.reset_pub)
			#if time.time()-start > 100:
				#s.reset()
			#	start = time.time()

			if time.time()-start > .25:
				self.pub()
				self.pub2()
				self.pub_to_buoys()
				start = time.time()

			if time.time()-start2 > 500:
				self.reset_pub()
				start2=time.time()

###MAIN
def main(args):

	sim=Simulator()
	posesub =rospy.Subscriber('/pose', PoseStamped, sim.pose_cb)#CHANGE TO MATRIX
	mb_sub =rospy.Subscriber('/mobile_buoy', PoseStamped, sim.buoy_cb)#CHANGE TO MATRIX
#	draw.init(s,agent_dict,map_size)
#	draw.start()

	try:
		
		#p = Process(target=root.mainloop, args=())
		#p.start()		
		sim.run()
		rospy.spin()



#
	except KeyboardInterrupt:
		print("Draw: Shutting down")
		


if __name__ == '__main__':
	main(sys.argv)






















