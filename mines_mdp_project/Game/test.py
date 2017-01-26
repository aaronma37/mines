#!/usr/bin/env python

from OpenGLContext import testingcontext
#BaseContext = testingcontext.getInteractive()
from drawing import basic_2
from Environment import Mine_Environment
from Agents import Agent0
from Solvers.UCT_SOLVER import UCT


import time



map_size=20
max_depth=20*2
depth=20
Gamma=.9
upper_confidence_c=1000
action_space_num=9#GET THIS FROM ACTUAL MODEL

start = time.time()
end = time.time()+10

count=0
moving_total=[]
rounds=0

e = Mine_Environment.Environment(map_size)
solver = UCT.Solver(max_depth,depth,Gamma,upper_confidence_c,action_space_num,map_size)
a = Agent0.Agent(map_size/2,map_size/2,9)

def draw():
	basic_2.clear()
	#basic_2.set_size(map_size)
	for i in range(0, map_size):
		for j in range(0, map_size):
			basic_2.draw(e.get_loc_info(i,j).get_x(),e.get_loc_info(i,j).get_y(),e.get_loc_info(i,j).get_width(),e.get_loc_info(i,j).get_height(),0,e.get_mine_data().get_color(i,j)*map_size,0,-.1,map_size/10.)


	basic_2.draw(e.get_loc_info(a.get_x(),a.get_y()).get_x(), e.get_loc_info(a.get_x(),a.get_y()).get_y(), e.get_loc_info(a.get_x(),a.get_y()).get_width(), e.get_loc_info(a.get_x(),a.get_y()).get_height(), 1, 1,0,-.1,map_size/10.)
	
	basic_2.draw(e.get_loc_info(e.mine_data.get_mine_location().get_x(),e.mine_data.get_mine_location().get_y()).get_x(), e.get_loc_info(e.mine_data.get_mine_location().get_x(),e.mine_data.get_mine_location().get_y()).get_y(), e.get_loc_info(e.mine_data.get_mine_location().get_x(),e.mine_data.get_mine_location().get_y()).get_width(), e.get_loc_info(e.mine_data.get_mine_location().get_x(),e.mine_data.get_mine_location().get_y()).get_height(), 1, 1,0,-.1,map_size/10.)

	basic_2.end_draw()








while 1 is 1:
	#if (end - start)  > 5:


		solver.step(a,e.mine_data,50)
		solver.get_best_action_and_step(a,e.mine_data)
		count+=1
		
		if e.mine_data.get_complete() is True:
			e.mine_data.reset()
			a.reset()
			moving_total.append(count)
			if len(moving_total) > 10:
				moving_total.pop(0)
			print "FINISHED IN: ", count, " AVERAGE IS: ", sum(moving_total)/len(moving_total)
			count=0
	#	start = time.time()
		draw()


	#end = time.time()

