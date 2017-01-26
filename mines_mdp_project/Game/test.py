#!/usr/bin/env python

from OpenGLContext import testingcontext
#BaseContext = testingcontext.getInteractive()
from drawing import basic_2
from Environment import Mine_Environment
from Agents import Agent0

import time

#DIAGNOSTICS


#CHOOSE ENVIRONMENT PARAMETERS
map_size=50

#CHOOSE AGENT PARAMETERS
max_depth=map_size*2
depth=map_size
Gamma=.9
upper_confidence_c=1000
action_space_num=9#GET THIS FROM ACTUAL MODEL

class Simulation:

	def __init__(self):
		self.e = Mine_Environment.Environment(map_size)
		self.a = Agent0.Agent(map_size/2,map_size/2,max_depth,depth,Gamma,upper_confidence_c,action_space_num,map_size)
		self.a_imaginary = Agent0.Agent(map_size/2,map_size/2,max_depth,depth,Gamma,upper_confidence_c,action_space_num,map_size)
		self.count=0
		self.moving_total=[]

	def draw(self):
		basic_2.clear()
		for i in range(0, map_size):
			for j in range(0, map_size):
				basic_2.draw(self.e.get_loc_info(i,j).get_x(),self.e.get_loc_info(i,j).get_y(),self.e.get_loc_info(i,j).get_width(),self.e.get_loc_info(i,j).get_height(),0,self.e.get_mine_data().get_color(i,j)*map_size,0,-.1,map_size/10.)


		basic_2.draw(self.e.get_loc_info(self.a.get_x(),self.a.get_y()).get_x(), self.e.get_loc_info(self.a.get_x(),self.a.get_y()).get_y(), self.e.get_loc_info(self.a.get_x(),self.a.get_y()).get_width(), self.e.get_loc_info(self.a.get_x(),self.a.get_y()).get_height(), 1, 1,0,-.1,map_size/10.)
	
		basic_2.draw(self.e.get_loc_info(self.e.mine_data.get_mine_location().get_x(),self.e.mine_data.get_mine_location().get_y()).get_x(), self.e.get_loc_info(self.e.mine_data.get_mine_location().get_x(),self.e.mine_data.get_mine_location().get_y()).get_y(), self.e.get_loc_info(self.e.mine_data.get_mine_location().get_x(),self.e.mine_data.get_mine_location().get_y()).get_width(), self.e.get_loc_info(self.e.mine_data.get_mine_location().get_x(),self.e.mine_data.get_mine_location().get_y()).get_height(), 1, 1,0,-.1,map_size/10.)

		basic_2.end_draw()

	def reset_func(self):
		self.e.mine_data.reset()
		self.a.reset()
		self.moving_total.append(self.count)
		if len(self.moving_total) > 10:
			self.moving_total.pop(0)
		print "FINISHED IN: ", self.count, " AVERAGE IS: ", sum(self.moving_total)/len(self.moving_total)
		self.count=0

	def run(self):
		while 1 is 1:
			self.a.step(self.e.mine_data,50, self.a_imaginary)
			self.count+=1
			if self.e.mine_data.get_complete() is True:
				self.reset_func()	

			self.draw()

s = Simulation()
s.run()









