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
from std_msgs.msg import Bool
from agent_classes import Agent

import sys
from pynput import mouse
from multiprocessing import Process
from draw import gui_data
from mobile_buoy_classes import Agent_buoy
from mobile_buoy_environment import Mobile_Buoy_Environment




rospy.init_node('main', anonymous=True)
env_pub =rospy.Publisher('/environment_matrix', OccupancyGrid, queue_size=100)#CHANGE TO MATRIX
agent_occ =rospy.Publisher('/environment_occupied', OccupancyGrid, queue_size=100)#CHANGE TO MATRIX
score_pub =rospy.Publisher('/buoy_scores', Int32MultiArray, queue_size=100)#CHANGE TO MATRIX
worker_pub =rospy.Publisher('/buoy_targets', Int32MultiArray, queue_size=100)#CHANGE TO MATRIX
reset_publisher = rospy.Publisher('/reset', Bool, queue_size=100)#CHANGE TO MATRIX


region = [(10,10),(10,30),(10,50),(10,70),(10,90),(30,10),(50,10),(70,10),(90,10),(30,30),(50,30),(70,30),(90,30),(30,50),(50,50),(70,50),(90,50),(30,70),(50,70),(70,70),(90,70),(30,90),(50,90),(70,90),(90,90)]

region_size=10


gd=gui_data()

map_size=100
s=Mine_Data(map_size)
sb=Mobile_Buoy_Environment(map_size)
agent_dict = {}# {Agent Identity:Agent}
buoy_dict = {}
o = OccupancyGrid()
o2= OccupancyGrid()
o3= Int32MultiArray()
o4= Int32MultiArray()
reset_ = Bool()
reset_.data = True

networks = OccupancyGrid()

for i in range(map_size):
	for j in range(map_size):
		o.data.append(s.seen[i][j])

for i in range(len(region)):
		o2.data.append(0)
		o3.data.append(0)

def pose_cb(data):
	if data.header.frame_id not in agent_dict:
		agent_dict[data.header.frame_id]=Agent(Mine_Data,map_size)
 

	agent_dict[data.header.frame_id].x=int(data.pose.position.x)
	agent_dict[data.header.frame_id].y=int(data.pose.position.y)
	agent_dict[data.header.frame_id].battery=int(data.pose.position.z)
	agent_dict[data.header.frame_id].current_action=agent_dict[data.header.frame_id].policy_set[int(data.pose.orientation.x)]
	agent_dict[data.header.frame_id].time_away_from_network=int(data.pose.orientation.y)
	agent_dict[data.header.frame_id].measure(s,False)

def buoy_cb(data):
	if data.header.frame_id not in buoy_dict:
		buoy_dict[data.header.frame_id]=Agent_buoy(Mine_Data,map_size)


	buoy_dict[data.header.frame_id].x=int(data.pose.position.x)
	buoy_dict[data.header.frame_id].y=int(data.pose.position.y)
	buoy_dict[data.header.frame_id].current_action=buoy_dict[data.header.frame_id].policy_set[int(data.pose.orientation.x)]

def pub():
	
	for i in range(map_size):
		for j in range(map_size):
			o.data[i*map_size+j]=s.seen[i][j]

	o.info.origin.position.x=map_size/2
	o.info.origin.position.y=map_size/2
	o.info.origin.position.z=20

	env_pub.publish(o)

	for k,b in buoy_dict.items():
		o.info.origin.position.x=b.x
		o.info.origin.position.y=b.y
		o.info.origin.position.z=20

		env_pub.publish(o)


def pub2():
	
	s.calculate_occupied(agent_dict,region,region_size)

	for i in range(len(region)):
			o2.data[i]=s.occupied[i]
	agent_occ.publish(o2)

def reset_pub():
	reset_publisher.publish(reset_)

def pub_to_buoys():
	sb.calculate_region_score(agent_dict)
	for i in range(len(region)):
		o3.data[i]=sb.score[i]
	score_pub.publish(o3)
	o4.data=[]
	for k,b in buoy_dict.items():
		o4.data.append(b.current_action.index)

	worker_pub.publish(o4)
	


def run():
	start = time.time()
	s.reset()
	while not rospy.is_shutdown():
		
		draw.render_once(s,agent_dict,map_size,buoy_dict,gd,reset_pub)
		#if time.time()-start > 100:
			#s.reset()
		#	start = time.time()
		pub()
		pub2()
		pub_to_buoys()

###MAIN
def main(args):

	posesub =rospy.Subscriber('/pose', PoseStamped, pose_cb)#CHANGE TO MATRIX
	mb_sub =rospy.Subscriber('/mobile_buoy', PoseStamped, buoy_cb)#CHANGE TO MATRIX
#	draw.init(s,agent_dict,map_size)
#	draw.start()

	try:
		
		#p = Process(target=root.mainloop, args=())
		#p.start()		
		run()
		rospy.spin()



#
	except KeyboardInterrupt:
		print("Draw: Shutting down")
		


if __name__ == '__main__':
	main(sys.argv)






















