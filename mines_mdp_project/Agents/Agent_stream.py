#!/usr/bin/env python

from Environment.Mines import Location
from Environment.Mines import Mine_Data
from random import randint
from Solvers.POMCP_RUSSEL import streams
import xxhash
import time
import math
from sets import Set
import numpy as np

zone = (((0,5),(-1,2)),((-4,1),(-1,2)),((-1,2),(-4,1)),((-1,2),(0,5)) )

def abf(x,y,battery,s):

	
	h ="h"

#	for z in zone:
#	
#		for i in range(z[0][0],z[0][1]):
#			score=0.
#			for j in range(z[1][0],z[1][1]):
#				if s.check_boundaries(Location(x+i,y+j)) == True:
#					if bool(s.seen[x+i][y+j]) == False:
#						score+=1.
#		if score/15. > .5:
#			h= h + "1"
#		else:
#			h= h + "0"
#		
	h = h + str(int(battery/5.))

	return h

class policy:
	def __init__(self,index):
		self.index=index


		self.action_string=[(0,0)]
	
		self.num_steps=5

				

		if self.index==2:
			for i in range(5):
				self.action_string.append((1,0))
			self.num_steps=5

		elif self.index==3:
			for i in range(5):
				self.action_string.append((-1,0))
			self.num_steps=5
		elif self.index==4:
			for i in range(5):
				self.action_string.append((0,1))
			self.num_steps=5
		elif self.index==5:
			for i in range(5):
				self.action_string.append((0,-1))
			self.num_steps=5
		elif self.index==6:
			for i in range(5):
				self.action_string.append((-1,-1))
			self.num_steps=5
		elif self.index==7:
			for i in range(5):
				self.action_string.append((1,-1))
			self.num_steps=5
		elif self.index==8:
			for i in range(5):
				self.action_string.append((-1,1))
			self.num_steps=5
		elif self.index==9:
			for i in range(5):
				self.action_string.append((1,1))
			self.num_steps=5


		self.macro_set=self.build_macro_set(self.action_string)


		self.counter=0

	def build_macro_set(self,action_string):

		x=0
		y=0
		macro_set=Set()
		for i in action_string:
			x+=i[0]
			y+=i[1]
			for j in range(-1+x,2+x):
				for k in range(-1+y,2+y):
					macro_set.add((j,k))


		return macro_set
	
	def reset(self):
		self.counter=0
			

	def get_next_action(self,x,y,s):
		next_x=0
		next_y=0
		self.counter+=1
		if self.index==0:
			##RETURN TO SHIP	
			if x < s.middle[0]:
				next_x = 1
			elif x > s.middle[0]:
				next_x = -1

			if y < s.middle[1]:
				next_y= 1
			elif y > s.middle[1]:
				next_y=-1

			if x is s.middle[0] and y is s.middle[1]:
				self.reset()
				return ((0,0),True)

		elif self.index==1:
			#wait
			self.reset()
			return ((0,0),True)

		elif self.index>1 and self.index <10:
			#explore right

			if self.counter < 4:
				return (self.action_string[self.counter],False)
			else:
				self.reset()
				return (self.action_string[4],True)
				



			

		if self.counter < self.num_steps:
			return ((next_x,next_y),False)	
		else:
			return ((next_x,next_y),True)	



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
		self.alpha=[.9,.1,0]

		self.reset(s)
		self.battery=randint(50,100)
		self.counter=6
		self.others=[]
		self.current_action=policy(1)
		
		self.policy_set=[]
		for i in range(10):
			self.policy_set.append(policy(i))
		



	def reset(self,s):
		self.x=self.init_x
		self.y=self.init_y
		self.x=randint(0,self.map_size-1)
		self.y=randint(0,self.map_size-1)
		s.update_agent_location((self.x,self.y))
		self.solver.last_abstraction = None



	def imprint(self, u):
		u.set_x(self.get_x())
		u.set_y(self.get_y())
		u.battery=self.battery


	def set_x(self,x_):
		self.x=x_

	def set_y(self,y_):
		self.y=y_

	def get_x(self):
		return self.x
	
	def get_y(self):
		return self.y


	def step(self,s,num_steps_,a_,time_to_work):	
		self.solver.OnlinePlanning(self,s,a_,time_to_work)		
		action = self.current_action.get_next_action(self.x,self.y,s)
		if action[1] is True:
			self.current_action = policy(self.solver.arg_max(abf(self.x,self.y,self.battery,s)))
			self.current_action.reset()

		self.execute(action[0],s)


	def execute(self,action_,environment_data_):
		(x,y) = self.get_transition(action_,self.x,self.y)
		
		if environment_data_.check_boundaries(Location(x,y)) is True:
			(self.x,self.y) = (x,y)

		self.recalculate_measurement_space()
		self.measure(environment_data_,False)
		if (self.x,self.y) == environment_data_.middle:
			print "charging"
			self.battery+=5
			if self.battery >100:
				self.battery=100
	

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

	def simulate_full(self,policy,s):
		base_reward= s.get_reward()
		base_reward2= s.get_reward2()

		for i in range(policy.num_steps):
			(x,y) = self.get_transition(policy.get_next_action(self.x,self.y,s)[0],self.x,self.y)

			if s.check_boundaries(Location(x,y)) is True:
				(self.x,self.y) = (x,y)
			self.recalculate_measurement_space()
			self.measure(s,True)
			
			if (self.x,self.y) == s.middle:
				self.battery+=1
				if self.battery >100:
					self.battery=100


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
		self.battery-=1
		if self.battery < 0:
			self.battery=0
			return (x,y)
		return (x+action[0],y+action[1])



