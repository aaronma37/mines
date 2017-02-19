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
from agent_classes import Agent

import sys
from pynput import mouse

rospy.init_node('main', anonymous=True)
env_pub =rospy.Publisher('/environment_matrix', OccupancyGrid, queue_size=100)#CHANGE TO MATRIX








map_size=100
s=Mine_Data(map_size)
agent_dict = {}# {Agent Identity:Agent}
o = OccupancyGrid()

for i in range(map_size):
	for j in range(map_size):
		o.data.append(s.seen[i][j])




def pose_cb(data):
	if data.header.frame_id not in agent_dict:
		agent_dict[data.header.frame_id]=Agent(Mine_Data,map_size)
 

	agent_dict[data.header.frame_id].x=int(data.pose.position.x)
	agent_dict[data.header.frame_id].y=int(data.pose.position.y)
	agent_dict[data.header.frame_id].battery=int(data.pose.position.z)
	agent_dict[data.header.frame_id].current_action=agent_dict[data.header.frame_id].policy_set[int(data.pose.orientation.x)]
	agent_dict[data.header.frame_id].measure(s,False)


def pub():
	for i in range(map_size):
		for j in range(map_size):
			o.data[i*map_size+j]=s.seen[i][j]

def run():
	start = time.time()
	s.reset()
	while not rospy.is_shutdown():
		draw.draw_all(s,agent_dict,map_size)
		if time.time()-start > 100:
			s.reset()
			start = time.time()

###MAIN
def main(args):

	posesub =rospy.Subscriber('/pose', PoseStamped, pose_cb)#CHANGE TO MATRIX
#	draw.init(s,agent_dict,map_size)
#	draw.start()

	try:
		run()
		rospy.spin()
#
	except KeyboardInterrupt:
		print("Draw: Shutting down")
		


if __name__ == '__main__':
	main(sys.argv)






















