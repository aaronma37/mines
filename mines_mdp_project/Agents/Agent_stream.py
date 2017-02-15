#!/usr/bin/env python

from Environment.Mines import Location
from Environment.Mines import Mine_Data
from random import randint
from Solvers.POMCP_RUSSEL import streams
import xxhash
import time
import math

import numpy as np



class Agent: 


	def __init__(self,x_,y_,map_size_,s):

		self.init_x=x_
		self.init_y=y_

		self.solver = streams.Solver(Mine_Data,map_size_)

		self.location = np.ndarray(shape=(1,2), dtype=float)

		self.x=x_
		self.y=y_
		self.map_size=map_size_

		self.measurement_space=[]
		self.alpha=[.7,.3,0]

		self.reset(s)
		self.top_level=1
		self.h_tasks=[]
		for i in range(self.top_level+1):
			self.h_tasks.append(None)
		self.arrows=[]
		self.request_from_level=self.top_level+1
		self.counter=6
		self.action=streams.action(1)
		self.others=[]



	def reset(self,s):
		self.x=self.init_x
		self.y=self.init_y
		self.x=randint(0,self.map_size-1)
		self.y=randint(0,self.map_size-1)
		s.update_agent_location((self.x,self.y))
		self.solver.last_abstraction = None


		#self.search_tree.clear()


	def imprint(self, u):
		u.set_x(self.get_x())
		u.set_y(self.get_y())

	def update_other_agent_loc(self,others,myself):
		self.others=[]
		for i in range(len(others)):
			if i is not myself:
				self.others.append(others[i])
			

	def set_x(self,x_):
		self.x=x_

	def set_y(self,y_):
		self.y=y_

	def get_x(self):
		return self.x
	
	def get_y(self):
		return self.y


	def step(self,environment_data_,num_steps_,a_,time_to_work):
		environment_data_.update_agent_location((self.x,self.y))
	
		self.counter+=1
		if self.counter > 4:
			self.action=self.solver.get_new_macro((self.x,self.y),environment_data_,self.alpha,self.others)
			self.counter=0

		self.execute(self.action.action_string[self.counter],environment_data_)


	def execute(self,action_,environment_data_):
		(x,y) = self.get_transition(action_,self.x,self.y)
		
		if environment_data_.check_boundaries(Location(x,y)) is True:
			(self.x,self.y) = (x,y)

		self.recalculate_measurement_space()
		self.measure(environment_data_,False)
		#self.history = self.abstractions.abf(environment_data_)

		environment_data_.update_agent_location((self.x,self.y))



	def simulate(self,action_,s):
		base_reward= s.get_reward()
		base_reward2= s.get_reward2()
		(x,y) = self.get_transition(action_,self.x,self.y)
		
		if s.check_boundaries(Location(x,y)) is True:
			(self.x,self.y) = (x,y)
			
		s.update_agent_location((self.x,self.y))
		self.recalculate_measurement_space()
		self.measure(s,True)


		return (s,s.get_reward()-base_reward, -s.get_reward2()+base_reward2)


	def recalculate_measurement_space(self):
		self.measurement_space=[]
		for i in range(self.x-1, self.x+2 ):
			for j in range(self.y-1, self.y+2):
				self.measurement_space.append(Location(i,j))

	def measure(self,mine_data_,imaginary):
		for loc in self.measurement_space:
			mine_data_.measure_loc(loc,imaginary)

	def get_transition(self,action,x,y):
		return (x+action[0],y+action[1])



