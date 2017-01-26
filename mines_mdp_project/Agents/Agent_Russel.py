#!/usr/bin/env python

from Action_Definition import get_transition_x
from Action_Definition import get_transition_y
from Environment.Mines import Location
from Environment.Mines import Mine_Data

import numpy as np


class Agent: 


	def __init__(self,x_,y_,action_space_num_):

		self.init_x=x_
		self.init_y=y_

		self.history = []
		self.x=x_
		self.y=y_
		self.action_space_num=action_space_num_
		self.measurement_space=[]
		self.local_action=0
		self.search_tree={-1:root_task}

		self.reset()




	def reset(self):
		self.x=self.init_x
		self.y=self.init_y
		self.history = [(0,0)]
		self.search_tree={-1:ActionSpace(upper_confidence_c_,action_space_num_)}

	def imprint(self, u):
		u.set_x(self.get_x())
		u.set_y(self.get_y())
		u.set_history(self.get_history())

	def set_history(self,h):
		self.history = []
	
		for i in range(0, len(h)):
			self.history.append((h[i][0],h[i][1]))

	def get_history(self):
		return self.history

	def set_x(self,x_):
		self.x=x_

	def set_y(self,y_):
		self.y=y_

	def get_x(self):
		return self.x
	
	def get_y(self):
		return self.y

	def update_history(self,action_,observation_hash_):
		self.history.append((action_,observation_hash_))
		if len(self.history) > 10:
			self.history.pop(0)

	def step(self):
		a = OnlinePlanning()
		execute(self,a,mine_data_):
		update_history(self,action_,observation)
		#PARTICLE FILTER

	def execute(self,action_,mine_data_):
		if mine_data_.check_boundaries(Location(self.x+get_transition_x(action_),self.y+get_transition_y(action_))) is True:
			self.x+=get_transition_x(action_)
			self.y+=get_transition_y(action_)
		self.recalculate_measurement_space()
		self.measure(mine_data_,imaginary)

	def simulate(self,action_,mine_data_):
		base_reward= environment_data_.get_reward()	
		if mine_data_.check_boundaries(Location(self.x+get_transition_x(action_),self.y+get_transition_y(action_))) is True:
			self.x+=get_transition_x(action_)
			self.y+=get_transition_y(action_)
		
		self.recalculate_measurement_space()
		self.measure(mine_data_,imaginary)
		return (mine_data_,environment_data_.get_reward()-base_reward)



	def recalculate_measurement_space(self):
		self.measurement_space=[]
		for i in range(self.x-1, self.x+2 ):
			for j in range(self.y-1, self.y+2):
				self.measurement_space.append(Location(i,j))

	def measure(self,mine_data_,imaginary):
		for loc in self.measurement_space:
			mine_data_.measure_loc(loc,imaginary)


	def get_hash(self):
		prime = 31
		result = 11
		result = result*prime + self.x
		result = result*prime + self.y
		return result	

	def get_hash_history(self):
		prime = 31
		result = 11
		for i in range(0,len(self.history)):
			result = result*prime + self.get_single_history_hash(self.history[i][0],self.history[i][1])*i
		return result

	def get_single_history_hash(self,a,o):
		prime=31
		result =11
		result=result*prime + a
		result=result*prime + o
		return result

	

	def get_action_size(self):
		return self.action_space_num
