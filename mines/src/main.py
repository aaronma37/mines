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

import POMDP_Values as v

L_MAX=v.L_MAX



load_q_flag = rospy.get_param("/load_q")
write_q_flag = rospy.get_param("/write_q")
write_psi_flag = rospy.get_param("/write_psi")
f_path = rospy.get_param("/temp_file_path")

rospy.init_node('main', anonymous=True)
env_pub =rospy.Publisher('/environment_matrix', OccupancyGrid, queue_size=100)#CHANGE TO MATRIX

agent_occ =rospy.Publisher('/work_load', OccupancyGrid, queue_size=100)#CHANGE TO MATRIX
score_pub =rospy.Publisher('/buoy_scores', Int32MultiArray, queue_size=100)#CHANGE TO MATRIX
worker_pub =rospy.Publisher('/buoy_targets', Int32MultiArray, queue_size=100)#CHANGE TO MATRIX
reset_publisher = rospy.Publisher('/reset', Int32, queue_size=100)#CHANGE TO MATRIX
restart_publisher = rospy.Publisher('/restart', Int32, queue_size=100)#CHANGE TO MATRIX


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

restart_=Int32()
restart_.data=0

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

		self.Na_Level=v.Na_Level()
		self.Q_Level=v.Q_Level()
		self.Q=v.Q()
		self.Na=v.Na()
		self.Phi=v.Phi()
		self.Psi=v.Psi()
		self.Pi=v.Pi()
		self.send_to=0
		self.agent_num=0
		self.time_to_wait=0

		if load_q_flag is True:
			self.load_q()

	def load_q(self):
		self.load_file(f_path+"/q_main.txt")


	def load_files(self):
		for k,a in agent_dict.items():
			self.load_file(f_path+k+".txt")

	def load_file(self,fn):
		#Modded for symmetry
		f = open(fn,'r')
		size=0
		for line in f:

			l = line.split(",")
			if l[0]=="Q" and len(l)>4:
				size+=1
				state=l[1]

				try:
					a_i=int(l[2])
				except ValueError:
					print "Value error trying to convert", l[2]					
					return

				try:
					r=float(l[3])
				except ValueError:
					print "Value error trying to convert", l[3]					
					return

				try:
					n=float(l[4])
				except ValueError:
					print "Value error trying to convert", l[4]					
					return

				for rot in range(8):
					rot_state=self.Phi.get_rotated_state(rot,state)
					rot_action=self.Phi.R_action(rot,a_i)
					if rot_action is None:
						print "rot_action is None", rot,a_i
					for L in range(30+1):#MOOOOOOOOOOO
						mod_state=self.Phi.get_from_state(L,rot_state)
						self.Na_Level.append_to_direct(L,mod_state,rot_action,n,self.Phi)
						self.Q_Level.append_to_direct(L,mod_state,rot_action,0.,self.Phi)
						self.Q_Level.append_to_average_direct(L,mod_state,rot_action,r,self.Phi,self.Na_Level)

				self.Na.append_to(state,a_i,n,self.Phi)
				self.Q.append_to(state,a_i,0.,self.Phi)
				self.Q.append_to_average(state,a_i,r,self.Phi,self.Na)

		print "Successfully appended",fn, "with", size, "lines"

	def calculate_policy(self):
		self.time_to_wait=self.Psi.update(self.Pi,self.Phi,self.Q_Level,self.Na_Level)
		
	def write_psi(self):
		if write_q_flag is True:
			self.Q.write_q(f_path+'/q_main.txt',self.Na)
		if write_psi_flag is True:
			self.Psi.write_psi(f_path+'/psi_main.txt')


	def pose_cb(self,data):
		if data.header.frame_id not in agent_dict:
			agent_dict[data.header.frame_id]=Agent(Mine_Data,map_size)
	 

		agent_dict[data.header.frame_id].x=int(data.pose.position.x)
		agent_dict[data.header.frame_id].y=int(data.pose.position.y)
		agent_dict[data.header.frame_id].battery=int(data.pose.position.z)
		agent_dict[data.header.frame_id].work=int(data.pose.orientation.x)
		agent_dict[data.header.frame_id].time_away_from_network=int(data.pose.orientation.y)
		agent_dict[data.header.frame_id].lvl=int(data.pose.orientation.z)
		agent_dict[data.header.frame_id].measure(self.s,False)

	def task_cb(self,data):
		if data.header.frame_id not in agent_dict:
			agent_dict[data.header.frame_id]=Agent(Mine_Data,map_size)

		agent_dict[data.header.frame_id].work=int(data.pose.position.x)

		self.send_to+=1

		if self.send_to + 1 > len(list(agent_dict.values())):
			self.send_to=0
	

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

		#print self.s.get_reward()-self.s_old.get_reward()

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
			#o2.data[Regions.get_region(a.x,a.y)]=o2.data[Regions.get_region(a.x,a.y)]+1
			if  a.work >-1 and a.work <25:
				o2.data[a.work]+=1

	
			

	def pub2(self):


		if self.agent_num > 0:
	
			#s.calculate_occupied(agent_dict,region,region_size)

			o2.header.frame_id=list(agent_dict.keys())[self.send_to]
			agent_dict[o2.header.frame_id].work=26
			self.calculate_work_load()
			o2.header.frame_id=list(agent_dict.keys())[self.send_to]
			agent_occ.publish(o2)

	def reset_pub(self):
		for i in range(25):
			o2.data[i]=0
		reset_.data=self.s.get_reward()
		print self.s.get_reward(), "H"
		self.s.reset()
		reset_publisher.publish(reset_)
		time.sleep(2)

		self.load_files()
		self.calculate_policy()
		self.write_psi()
		self.s.reset()	

		restart_publisher.publish(restart_)
		time.sleep(self.time_to_wait)


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
		asynch_timer=time.time()
		self.s.reset()
		count=0
		while not rospy.is_shutdown():
		
			draw.render_once(self.s,agent_dict,map_size,buoy_dict,gd,self.reset_pub,time.time()-start2)
			#if time.time()-start > 100:
				#s.reset()
			#	start = time.time()
			agents=list(agent_dict.keys())
			self.agent_num = len(agents)
			if self.agent_num > 0:
				if (time.time() - asynch_timer) > (20./self.agent_num):
					asynch_timer=time.time()
					self.pub2()

			if time.time()-start > .025:
				self.pub()
				#self.pub2()
				#self.pub_to_buoys()
				start = time.time()

			if time.time()-start2 > 200:
				count+=1
				if count > 50:
					return
				self.reset_pub()
				start2=time.time()


###MAIN
def main(args):

	sim=Simulator()
	posesub =rospy.Subscriber('/pose', PoseStamped, sim.pose_cb)#CHANGE TO MATRIX
	mb_sub =rospy.Subscriber('/mobile_buoy', PoseStamped, sim.buoy_cb)#CHANGE TO MATRIX
	task_sub =rospy.Subscriber('/task', PoseStamped, sim.task_cb)#CHANGE TO MATRIX
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






















