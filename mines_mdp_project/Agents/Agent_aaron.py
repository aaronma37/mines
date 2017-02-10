#!/usr/bin/env python

from Environment.Mines import Location
from Environment.Mines import Mine_Data
from random import randint
from Solvers.POMCP_RUSSEL import hierarchy_policy
import xxhash
import time


import numpy as np

away=(0,-1)
to=(0,1)
right=(1,0)
left=(-1,0)

def print_dir(direction):
	if direction == to:
		print "TO"
	elif direction == away:
		print "AWAY"
	elif direction == left:
		print "LEFT"
	else:
		print "RIGHT"

def get_dir(direction,t):

	if t == to:
		return direction
	elif t == away:
		if direction == (0,1):
			return (0,-1)
		elif direction == (0,-1):
			return (0,1)
		elif direction == (1,0):
			return (-1,0)
		else:
			return (1,0)
	elif t == left:
		if direction == (0,1):
			return (-1,0)
		elif direction == (0,-1):
			return (1,0)
		elif direction == (1,0):
			return (0,1)
		else:
			return (0,-1)
	elif t == right:
		if direction == (0,1):
			return (1,0)
		elif direction == (0,-1):
			return (-1,0)
		elif direction == (1,0):
			return (0,-1)
		else:
			return (0,1)

	print t,"WARNING NOT FOUND"


class Agent: 


	def __init__(self,x_,y_,map_size_,s):

		self.init_x=x_
		self.init_y=y_

		self.solver = hierarchy_policy.Solver(Mine_Data,map_size_)

		self.location = np.ndarray(shape=(1,2), dtype=float)

		self.x=x_
		self.y=y_
		self.map_size=map_size_

		self.measurement_space=[]

		self.reset(s)
	
	def get_action_space_num_(self):
		return self.action_space_num


	def reset(self,s):
		self.x=self.init_x
		self.y=self.init_y
		#self.x=randint(0,self.map_size-1)
		#self.y=randint(0,self.map_size-1)
		s.update_agent_location((self.x,self.y))


		#self.search_tree.clear()


	def imprint(self, u):
		u.set_x(self.get_x())
		u.set_y(self.get_y())


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
		a = self.solver.OnlinePlanning(self, environment_data_,a_,time_to_work)

		#print "CHOSE: UP"
		#print_dir(a[len(a)-3][0][0])
		#print_dir(a[len(a)-2][0][0])
		#print_dir(a[len(a)-1][0][0])

		self.execute(a,environment_data_)


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
		(x,y) = self.get_transition(action_,self.x,self.y)
		
		if s.check_boundaries(Location(x,y)) is True:
			(self.x,self.y) = (x,y)
			
		s.update_agent_location((self.x,self.y))
		self.recalculate_measurement_space()
		self.measure(s,True)


		return (s,s.get_reward()-base_reward)


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



