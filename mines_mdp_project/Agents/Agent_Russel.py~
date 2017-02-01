#!/usr/bin/env python

from Action_Definition import get_transition_x
from Action_Definition import get_transition_y
from Environment.Mines import Location
from Environment.Mines import Mine_Data
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
		return xxhash.xxh64("primitive").hexdigest() + xxhash.xxh64(str(self.index)).hexdigest()

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
		return xxhash.xxh64("Option").hexdigest() + xxhash.xxh64(str(self.index)).hexdigest()

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
		for i in range(3):
			for j in range(3):
				self.abstractions.append(Abstraction(i*map_size_/3,(i+1)*map_size_/3,j*map_size_/3,(j+1)*map_size_/3,i+j*3))

	def get_abstraction_index(self,x,y):
		for ab in self.abstractions:
			if ab.get_occupancy(x,y) is True:
				return ab.get_index()


	def get_abstraction(self,x,y):
		for ab in self.abstractions:
			if ab.get_occupancy(x,y) is True:
				return ab


	def abf(self,s):
		c=0

		for (x,y) in self.get_abstraction(s.get_agent_x(),s.get_agent_y()).get_state():
			if bool(s.get_seen(x,y)) is False:
				c+=1
			else:
				c-=100
	
		if c > -50:
			return xxhash.xxh64(str(self.get_abstraction_index(s.get_agent_x(),s.get_agent_y()))+str(False)).hexdigest()
		else:
			return xxhash.xxh64(str(self.get_abstraction_index(s.get_agent_x(),s.get_agent_y()))+str(True)).hexdigest()


	def abf_init(self,abstraction_index,all_visible):
		return xxhash.xxh64(str(abstraction_index)+str(all_visible)).hexdigest()
		

class RootTask:
	def __init__(self,map_size_):
		self.abstractions=Abstractions(map_size_)
		self.primitive=False
		self.sub_tasks=[]
		self.index=0

		i=0
		j=1
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))

		i=0
		j=3
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))	
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
##
		i=1
		j=0
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		i=1
		j=2
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		i=1
		j=4
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
##

		i=2
		j=1
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		i=2
		j=5
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
##

		i=3
		j=0
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		i=3
		j=4
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		i=3
		j=6
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
##

		i=4
		j=1
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		i=4
		j=3
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		i=4
		j=5
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		i=4
		j=7
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
##

		i=5
		j=2
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		i=5
		j=4
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))

		i=5
		j=8
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
##

		i=6
		j=3
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))


		i=6
		j=7
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
##

		i=7
		j=4
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		i=7
		j=6
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))

		i=7
		j=8
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))

		i=8
		j=7
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))

		i=8
		j=5
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))
		self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,True),len(self.sub_tasks), "section " + str(i)+" to section"+ str(j)))


#		for i in range(9):
#			for j in range(9):
#				if i is not j:
#					self.sub_tasks.append(Option(self.abstractions.abf_init(i,True),self.abstractions.abf_init(j,False),len(self.sub_tasks),"section " + str(i)+ " to section"+ str(j)))

#		for i in range(9):
#					self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(i,True),len(self.sub_tasks),"explore region: " + str(i)))

#		for i in range(9):
#			for j in range(9):
#				if i is not j:
#					self.sub_tasks.append(Option(self.abstractions.abf_init(i,False),self.abstractions.abf_init(j,False),len(self.sub_tasks),"section " + str(i)+ " to section"+ str(j)))

	def check_termination(self,h):
		return False

	def get_primitive(self):
		return self.primitive

	def get_hash(self):
		return xxhash.xxh64("root").hexdigest() + xxhash.xxh64(str(self.index)).hexdigest()

	def get_sub_tasks(self):
		return self.sub_tasks

	def get_index(self):
		return self.index

	def get_hierarchy(self):
		return "root"

	def get_message(self):
		return "root"

class Agent: 


	def __init__(self,x_,y_,max_depth_,depth_,Gamma_,upper_confidence_c_,action_space_num_,map_size_):

		self.init_x=x_
		self.init_y=y_

		self.solver = POMCP_R.Solver(max_depth_,depth_,Gamma_,upper_confidence_c_,action_space_num_,map_size_)


		self.location = np.ndarray(shape=(1,2), dtype=float)
		self.search_tree=dict()
		self.x=x_
		self.y=y_
		self.action_space_num=action_space_num_
		self.measurement_space=[]
		self.local_action=0
		self.root_task=RootTask(map_size_)
		self.abstractions = Abstractions(map_size_)
		self.history =  self.abstractions.abf_init(self.abstractions.get_abstraction_index(self.x,self.y),False)
		self.reset()
	
	def get_action_space_num_(self):
		return self.action_space_num

	def reset(self):
		print len(self.solver.N)
		self.x=self.init_x
		self.y=self.init_y
		self.history =  self.abstractions.abf_init(self.abstractions.get_abstraction_index(self.x,self.y),False)
		#self.search_tree.clear()

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
		self.history=xxhash.xxh64(self.history+action_.get_hash()+observation_hash_).hexdigest()

	def step(self,environment_data_,num_steps_,a_):
		self.search_tree.clear()
		environment_data_.update_agent_location(self.x,self.y)
		a = self.solver.OnlinePlanning(self.root_task,self.search_tree, self, environment_data_,num_steps_,a_,self.abstractions.abf)
		self.execute(a,environment_data_)
		self.update_history(a, self.abstractions.abf(environment_data_))

	def execute(self,action_,environment_data_):
		if environment_data_.check_boundaries(Location(self.x+get_transition_x(action_.get_index()),self.y+get_transition_y(action_.get_index()))) is True:
			self.x+=get_transition_x(action_.get_index())
			self.y+=get_transition_y(action_.get_index())
		self.recalculate_measurement_space()
		self.measure(environment_data_,False)
		#self.history = self.abstractions.abf(environment_data_)

		environment_data_.update_agent_location(self.x,self.y)



	def simulate(self,action_,s):
		base_reward= s.get_reward()	
		if s.check_boundaries(Location(self.x+get_transition_x(action_.get_index()),self.y+get_transition_y(action_.get_index()))) is True:
			self.x+=get_transition_x(action_.get_index())
			self.y+=get_transition_y(action_.get_index())
			
		s.update_agent_location(self.x,self.y)
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

