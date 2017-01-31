#!/usr/bin/env python

from OpenGLContext import testingcontext
#BaseContext = testingcontext.getInteractive()
from drawing import basic_2
from Environment import Mine_Environment
from Agents import Agent_Russel
from multiprocessing import Process, Queue
import multiprocessing
import time

#DIAGNOSTICS
sample_size=100
max_num_steps=5
num_workers=multiprocessing.cpu_count()
time_to_work=600
num_steps=5

#CHOOSE ENVIRONMENT PARAMETERS
map_size=12

#CHOOSE AGENT PARAMETERS
max_depth=10
depth=1
Gamma=.9
upper_confidence_c=1000
action_space_num=9#GET THIS FROM ACTUAL MODEL

class Simulation:

	def __init__(self):
		self.e = Mine_Environment.Environment(map_size)
		self.a = Agent_Russel.Agent(map_size/2,map_size/2,max_depth,depth,Gamma,upper_confidence_c,action_space_num,map_size)
		self.e.mine_data.update_agent_location(self.a.get_x(),self.a.get_y())	
		for o in self.a.root_task.get_sub_tasks():
			o.available(self.a.abstractions.abf(self.e.mine_data))
		self.a_imaginary = Agent_Russel.Agent(map_size/2,map_size/2,max_depth,depth,Gamma,upper_confidence_c,action_space_num,map_size)
		self.count=0
		self.moving_total=[]
		self.total=0
		self.num_steps=10
		self.rounds=0


	def draw(self):
		basic_2.clear()
		for i in range(0, map_size):
			for j in range(0, map_size):
				if bool(self.e.get_mine_data().seen[i][j]) is False:
					basic_2.draw(self.e.get_loc_info(i,j).get_x(),self.e.get_loc_info(i,j).get_y(),self.e.get_loc_info(i,j).get_width(),self.e.get_loc_info(i,j).get_height(),0,self.e.get_mine_data().get_color(i,j)*map_size,0,-.1,map_size/10.)
				

		basic_2.draw(self.e.get_loc_info(self.a.get_x(),self.a.get_y()).get_x(), self.e.get_loc_info(self.a.get_x(),self.a.get_y()).get_y(), self.e.get_loc_info(self.a.get_x(),self.a.get_y()).get_width(), self.e.get_loc_info(self.a.get_x(),self.a.get_y()).get_height(), 1, 1,0,-.1,map_size/10.)
	
		basic_2.draw(self.e.get_loc_info(self.e.mine_data.get_mine_location().get_x(),self.e.mine_data.get_mine_location().get_y()).get_x(), self.e.get_loc_info(self.e.mine_data.get_mine_location().get_x(),self.e.mine_data.get_mine_location().get_y()).get_y(), self.e.get_loc_info(self.e.mine_data.get_mine_location().get_x(),self.e.mine_data.get_mine_location().get_y()).get_width(), self.e.get_loc_info(self.e.mine_data.get_mine_location().get_x(),self.e.mine_data.get_mine_location().get_y()).get_height(), 1, 1,0,-.1,map_size/10.)

		basic_2.end_draw()

	def reset_func(self):
		self.e.mine_data.reset()
		#self.a.reset()
		self.rounds+=1
		self.total+=self.count
		self.count=0
			


	def run(self, to_draw, q,time_to_work,num_steps):
		start = time.time()
		end = time.time()
		while end - start < time_to_work:
			self.a.step(self.e.mine_data,num_steps, self.a_imaginary)
			self.count+=1
			if self.e.mine_data.get_complete() is True:
				self.reset_func()
				end = time.time()
			if self.count>map_size*map_size:
				self.reset_func()
				end = time.time()
				print "max reached"
	
			if to_draw is True:
				self.draw()
		q.put((self.rounds,self.total))

print "Starting threads... Machine limit: ", multiprocessing.cpu_count()

for i in range(0,100):
	num_steps=5+i*25
		
	s=[]
	q=[]
	p=[]
	evaluation=()
	rounds=0
	total=0

	s.append(Simulation())
	q.append(Queue())
	s[0].run(True,q[0],time_to_work,20)

#	for i in range(0,num_workers):
#		s.append(Simulation())
#		q.append(Queue())
#		p.append(Process(target=s[i].run, args=(False,q[i],time_to_work,num_steps)))
#
#	for i in range(0,num_workers):
#		p[i].start()

#	for i in range(0,num_workers):
#		evaluation=(q[i].get())
#		rounds+=evaluation[0]
#		total+=evaluation[1]

#	for i in range(0,num_workers):
#		p[i].join()




	print "#", num_steps," Average: ", total/rounds, " for ", rounds, " rounds"










