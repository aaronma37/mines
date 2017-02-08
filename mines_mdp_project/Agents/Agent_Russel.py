#!/usr/bin/env python

from Action_Definition import get_transition_x
from Action_Definition import get_transition_y
from Environment.Mines import Location
from Environment.Mines import Mine_Data
from random import randint
from Solvers.POMCP_RUSSEL import POMCP_R
import xxhash
import time


import numpy as np

class task:
	def __init__(self,index,primitive):
		self.index=index
		self.primitive=True
		self.message="primitive"

	def check_termination(self,h):
		return True

	def get_index(self):
		return self.index

	def get_primitive(self):
		return self.primitive

	def get_hash(self):
		return xxhash.xxh64("primitive"+str(self.index)).hexdigest()

	def get_hierarchy(self):
		return "primitive"

	def available(self,h):
		return True
	
	def get_message(self):
		return self.index

class Option:
	def __init__(self,init,end,index, st1):
		self.init=init
		self.end=end
		self.index=index
		self.primitive=False
		self.sub_tasks=[]
		self.message=st1

		for i in range(0,9):
			self.sub_tasks.append(task(i,True))

	def get_hierarchy(self):
		return "Option"

	def available(self,h):
		#print h
		#print self.init
		if self.init in h:
			#print "FOUND", self.message, self.out_message
			return True
		else:
			return False

	def get_index(self):
		return self.index

	def check_termination(self, h):
		if self.end in h:
			return True
		return False

	def get_primitive(self):
		return self.primitive

	def get_hash(self):
		return xxhash.xxh64("Option"+str(self.index)).hexdigest() 

	def get_sub_tasks(self):
		return self.sub_tasks

	def get_message(self):
		return self.message

class Abstraction:
	def __init__(self,x_min,x_max,y_min,y_max,index):
		self.state=[]
		self.index=index
		for i in range(x_min,x_max):
			for j in range(y_min,y_max):
				self.state.append((i,j))

	def get_occupancy(self,x,y):
		if (x,y) in self.state:
			return True
		return False

	def get_index(self):
		return self.index

	def get_state(self):
		return self.state



class Abstractions:
	def __init__(self,map_size_):
		self.abstractions=[]
		self.feasible=[]
		self.feasible.append([0,1,3])
		self.feasible.append([0,1,2,4])
		self.feasible.append([1,2,5])
		self.feasible.append([0,3,4,6])
		self.feasible.append([1,3,4,5,7])
		self.feasible.append([2,4,5,8])
		self.feasible.append([3,6,7])
		self.feasible.append([4,6,7,8])
		self.feasible.append([5,7,8])
		for i in range(3):
			for j in range(3):
				self.abstractions.append(Abstraction(i*map_size_/3,(i+1)*map_size_/3,j*map_size_/3,(j+1)*map_size_/3,i+j*3))

	def get_abstraction_index(self,(x,y)):
		for ab in self.abstractions:
			if ab.get_occupancy(x,y) is True:
				return ab.get_index()


	def get_abstraction(self,x,y):
		for ab in self.abstractions:
			if ab.get_occupancy(x,y) is True:
				return ab


	def abf(self,s):
		to_return=str(self.get_abstraction_index(s.get_agent_location()))
		for i in range(9):
			c=0
			for (x,y) in self.abstractions[i].get_state():
				if bool(s.get_seen(x,y)) is False:
					c+=1
				else:
					c-=1
			if c >0:
				to_return+="1"
			else:
				to_return+="0"

		return xxhash.xxh64(to_return).hexdigest()	

	def abf2(self,s,i):
		to_return=str(i)
		for i in range(9):
			c=0
			for (x,y) in self.abstractions[i].get_state():
				if bool(s.get_seen(x,y)) is False:
					c+=1
				else:
					c-=1
			if c < 0:
				to_return+="1"
			else:
				to_return+="0"

		return xxhash.xxh64(to_return).hexdigest()

	def abf3(self,s,j,i):
		to_return=str(i)
		for i in range(9):
			c=0
			for (x,y) in self.abstractions[i].get_state():
				if bool(s.get_seen(x,y)) is False:
					c+=1
				else:
					c-=1
			if c < 0 or i is j:
				to_return+="1"
			else:
				to_return+="0"

		return xxhash.xxh64(to_return).hexdigest()

	def get_sub_tasks(self,s,sub_task_type):
		sub_tasks=[]
		


		if sub_task_type == "Option":
			for k in (self.feasible[self.get_abstraction_index(s.get_agent_location())]):
				sub_tasks.append((self.abf(s),self.abf2(s,k),"Option","Primitive"))
				sub_tasks.append((self.abf(s),self.abf3(s,self.get_abstraction_index(s.get_agent_location()),k),"Option","Primitive"))

		elif sub_task_type == "Primitive":
			for k in range(9):
				sub_tasks.append((str(0),str(k),"Primitive","None"))

		return sub_tasks	

class Agent: 


	def __init__(self,x_,y_,max_depth_,depth_,Gamma_,upper_confidence_c_,action_space_num_,map_size_,s):

		self.init_x=x_
		self.init_y=y_

		self.solver = POMCP_R.Solver(max_depth_,depth_,Gamma_,upper_confidence_c_,action_space_num_,Mine_Data,map_size_)


		self.location = np.ndarray(shape=(1,2), dtype=float)
		self.search_tree=dict()
		self.x=x_
		self.y=y_
		self.map_size=map_size_

		self.action_space_num=action_space_num_
		self.measurement_space=[]
		self.local_action=0
		self.abstractions = Abstractions(map_size_)

		#print self.abstractions.abf_init(self.abstractions.get_abstraction_index(5,5),False)
		#time.sleep(5)
		self.reset(s)
	
	def get_action_space_num_(self):
		return self.action_space_num


	def reset(self,s):
		self.x=2
		self.y=2
		#self.x=randint(0,self.map_size-1)
		#self.y=randint(0,self.map_size-1)
		s.update_agent_location((self.x,self.y))
		self.history =  self.abstractions.abf(s)

		#self.search_tree.clear()

	def set_history_from_e(self,e):
		self.history = self.abstractions.abf(e)

	def imprint(self, u):
		u.set_x(self.get_x())
		u.set_y(self.get_y())
		u.set_history(self.get_history())

	def set_history(self,h):
		self.history = h
		

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
		self.history=xxhash.xxh64(xxhash.xxh64(action_[0]+action_[1]).hexdigest()+observation_hash_).hexdigest()

	def step(self,environment_data_,num_steps_,a_,time_to_work):
		self.search_tree.clear()
		environment_data_.update_agent_location((self.x,self.y))
		a = self.solver.OnlinePlanning(("root","False","Root","Option"),self.search_tree, self, environment_data_,num_steps_,a_,self.abstractions,time_to_work)
		self.execute(a,environment_data_)
		self.update_history(a, self.abstractions.abf(environment_data_))

	def execute(self,action_,environment_data_):
		if environment_data_.check_boundaries(Location(self.x+get_transition_x(int(action_[1])),self.y+get_transition_y(int(action_[1])))) is True:
			self.x+=get_transition_x(int(action_[1]))
			self.y+=get_transition_y(int(action_[1]))
		self.recalculate_measurement_space()
		self.measure(environment_data_,False)
		#self.history = self.abstractions.abf(environment_data_)

		environment_data_.update_agent_location((self.x,self.y))



	def simulate(self,action_,s):
		base_reward= s.get_reward()	
		if s.check_boundaries(Location(self.x+get_transition_x(int(action_[1])),self.y+get_transition_y(int(action_[1])))) is True:
			self.x+=get_transition_x(int(action_[1]))
			self.y+=get_transition_y(int(action_[1]))
			
		s.update_agent_location((self.x,self.y))
		self.recalculate_measurement_space()
		self.measure(s,True)
		#print s.get_reward()-base_reward
		return (s,s.get_reward()-base_reward)


	def recalculate_measurement_space(self):
		self.measurement_space=[]
		for i in range(self.x-1, self.x+2 ):
			for j in range(self.y-1, self.y+2):
				self.measurement_space.append(Location(i,j))

	def measure(self,mine_data_,imaginary):
		for loc in self.measurement_space:
			mine_data_.measure_loc(loc,imaginary)



	

	def get_action_size(self):
		return self.action_space_num

