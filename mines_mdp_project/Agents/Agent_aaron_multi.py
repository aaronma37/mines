#!/usr/bin/env python

from Environment.Mines import Location
from Environment.Mines import Mine_Data
from random import randint
from Solvers.POMCP_RUSSEL import hierarchy_policy_multi
import xxhash
import time
import math

import numpy as np

away=(0,-1)
to=(0,1)
right=(1,0)
left=(-1,0)
## CURRENT ERROR, DOESNT MAKE TO END OF CHAIN, CAUSES INFINITE LOOPS
def print_dir(direction):
	if direction == to:
		print "TO"
	elif direction == away:
		print "AWAY"
	elif direction == left:
		print "LEFT"
	else:
		print "RIGHT"

def get_next(x,y,direction,level):
	dist=int(math.pow(3,level))

	x+=dist*direction[0]
	y+=dist*direction[1]
	return (x,y)

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

	print t,"AGENT"


class Agent: 


	def __init__(self,x_,y_,map_size_,s):

		self.init_x=x_
		self.init_y=y_

		self.solver = hierarchy_policy_multi.Solver(Mine_Data,map_size_)

		self.location = np.ndarray(shape=(1,2), dtype=float)

		self.x=x_
		self.y=y_
		self.map_size=map_size_

		self.measurement_space=[]
		self.alpha=[1,0]

		self.reset(s)
		self.top_level=1
		self.h_tasks=[]
		for i in range(self.top_level+1):
			self.h_tasks.append(None)
		self.arrows=[]
		self.request_from_level=self.top_level+1
		self.current_counter=0

	def make_arrows(self):
		self.arrows=[]

		loc = ( self.x,self.y)


		for t in self.h_tasks:
			#bloc=t.starting_loc
			for a_ in t.a[1:]:
				bloc = get_next(loc[0],loc[1],get_dir(t.direction,a_),t.level)
				bloc = ((loc[0]+bloc[0])/2, (loc[1]+bloc[1])/2)
				self.arrows.append((bloc,get_dir(t.direction,a_),math.pow(3,t.level)))
				loc= get_next(loc[0],loc[1],get_dir(t.direction,a_),t.level)

		immediate_direction = get_dir(self.h_tasks[0].direction,self.h_tasks[0].a[0])

		for t in self.h_tasks:
			self.request_from_level=t.level
			if t.remove_action() is False:
				break
			elif self.request_from_level==self.top_level:
				self.request_from_level+=1
							
		return immediate_direction	

	def iterate_for_dir(self,s,end):
		if len(s[0]) is 0:
			return to
		direction = to		
		for i in range(len(s)-end):
			direction = get_dir(direction,s[i][0])
		return direction

	def get_action_space_num_(self):
		return self.action_space_num

	def remove_from_action_space(self, s,i):
		if i < 0:
			return len(s)-1-i
		print s[i]
		del s[i][1]
		print s[i]
		s[i] = s[i][0]+s[i][2:]
		if len(s[i]) == 1:
			return self.remove_from_action_space(s,i-1)

		return len(s)-1-i

	def reset(self,s):
		self.x=self.init_x
		self.y=self.init_y
		#self.x=randint(0,self.map_size-1)
		#self.y=randint(0,self.map_size-1)
		s.update_agent_location((self.x,self.y))
		self.solver.last_abstraction = None


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


		#  while level requested > 0
			#calculate lower level
			# append to h.
	
		if self.current_counter > math.pow(3,self.top_level+1):
			self.request_from_level=self.top_level+1
			self.current_counter=0
		if self.request_from_level > self.top_level:
			self.h_tasks[self.top_level] = self.solver.get_new_macro(self.x,self.y,environment_data_,self.top_level,self.alpha)
			self.request_from_level = self.top_level

		self.solver.OnlinePlanning(self, environment_data_,a_,time_to_work,self.top_level)

		while self.request_from_level > 0:
			direction = get_dir(self.h_tasks[self.request_from_level].direction,self.h_tasks[self.request_from_level].a[0])
			self.request_from_level-=1
			self.h_tasks[self.request_from_level]=self.solver.GetGreedyPrimitive(self.x,self.y,direction,environment_data_,self.request_from_level,self.alpha)
		  	
		#for t in self.h_tasks:
		#	t.print_data()
		self.current_counter+=1



		direction = self.make_arrows()
		self.execute(direction,environment_data_)


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



