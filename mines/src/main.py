#!/usr/bin/env python


import math
#from OpenGLContext import testingcontext
import draw
from sets import Set
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid
from agent_classes import Agent
from environment_classes import get_sqr_loc
from environment_classes import get_norm_size
from environment_classes import Mine_Data
import rospy
import sys
import time

'''Main, keeps track of all agents, and environment data, draws''' 


map_size=100
s=Mine_Data(map_size)
agent_dict = {}# {Agent Identity:Agent}
o = OccupancyGrid()
for i in range(map_size):
	for j in range(map_size):
		o.data.append(s.seen[i][j])


rospy.init_node('main', anonymous=True)

env_pub =rospy.Publisher('/environment_matrix', OccupancyGrid, queue_size=100)#CHANGE TO MATRIX

def draw_():
		draw.clear()
		draw.begin_basic()

		for i in range(map_size):
			for j in range(map_size):
				if s.seen[i][j] == 0:
					 draw.draw_basic(get_sqr_loc(i,map_size),get_sqr_loc(j,map_size),get_norm_size(map_size),get_norm_size(map_size),-.1)
				

		for k,a in agent_dict.items():
			draw.draw(get_sqr_loc(a.x,map_size), get_sqr_loc(a.y,map_size), get_norm_size(map_size),get_norm_size(map_size),1, 1,0,-.1,map_size/10.)

		draw.end_draw()



def pose_cb(data):
	# IDENTIFY AND ADD		

	if data.header.frame_id not in agent_dict:
		agent_dict[data.header.frame_id]=Agent(Mine_Data,map_size)
	 

	agent_dict[data.header.frame_id].x=int(data.pose.position.x)
	agent_dict[data.header.frame_id].y=int(data.pose.position.y)
	agent_dict[data.header.frame_id].measure(s,False)


def run():
	while not rospy.is_shutdown():

		#publish data
		env_pub.publish(o)

		#draw
		draw_()

		#wait
		#time.sleep(.05)
		




###MAIN
def main(args):

	pose_pub = rospy.Subscriber('/pose',PoseStamped, pose_cb)
	try:
		run()
		rospy.spin()

	except KeyboardInterrupt:
		print("Draw: Shutting down")



if __name__ == '__main__':
	main(sys.argv)






















