#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
import Regions

class Regions:
	def __init__(self,size):
		self.size=size
		
	def get_region(self,x,y):
		return (math.floor((math.abs(x)-self.size/2)/self.size),math.floor((math.abs(y)-self.size/2)/self.size))

	def get_region_parts(self,r):
		region_list=[]
		for x in range(self.size*r(0)-self.size/2,self.size*r(0)+self.size/2)
			for y in range(self.size*r(1)-self.size/2,self.size*r(1)+self.size/2)		
				region_list.append(x,y)
		return region_list

	def is_feasible_travel_path(self,r1,r2):
		if math.abs(r1(0)-r2(0))<2 and math.abs(r1(1)-r2(1))<2:
			return True
		return False

class Sub_Objective():
	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.region=Regions.get_region(x,y)


class Objective():
	def __init__(self,objective_parameters):
		self.sub_objectives=[]
		self.distribute(objective_parameters[0])
		self.granularity=objective_parameters[1]
		
		
	def distribute(self,distribution_type):
		if distribution_type=="All":
			for x in range(100):
				for y in range(100):
					self.sub_objectives.append(Sub_Objective(x,y))
		

class Sub_Environment:
	def __init__(self):
		self.region_list=None
		self.state=None
		self.interaction_set=None
		 
	def set_region_list(self,region_list):
		self.region_list=region_list
	
	def set_random_region_list(self,r):
		self.region_list=[]
		self.region_list.append(r)
		for k in range(L):
			self.region_list.append((self.region_list[-1][0]+random.randint(-1, 1),self.region_list[-1][1]+random.randint(-1, 1)))



	def get_sub_sub_environment(self,k):
		return Sub_Environment(self.region_list[0:k],self.state[0:k],self.interaction_set[0:k])

	def cull_state_from_back(self,k):
		s=self.state.split(".")

		h=""
		for i in range(0,len(s)-k):
			h=h+"."+s[i]

		return h
		

	def cull_state_from_front(self,k):
		s=self.state.split(".")
		h=""
		for i in range(k,len(s)):
			h=h+"."+s[i]

		return h

	def get_state_index(self,k):
		return self.state.split(".")[k]

	def get_objective_index(self,k,objective_type):
		o_index=objective_set.index(objective_type)
		return self.get_state_index(k).split(",")[o_index]

		
		
	def update_state(self,complete_environment):
		self.state=""
		for r in self.region_list:
			self.state=self.state+"."
			for o in objectives:
				self.state=self.state+str(complete_environment.get_region_objective_state(o,r))

	def get_region_objective_state(self,k,objective_type):
		



class Complete_Environment:
	def __init__(self,region_size,objective_parameter_list):
		self.regions=Regions(region_size) 
		self.objective_parameter_list=objective_parameter_list
		self.objective_set=[]
		for objective_parameters in objective_parameter_list:
			self.objective_set.append(Objective(objective_parameters))
		self.agent_locations=[]

	def reset(self):
		self.objective_set=[]
		for objective_parameters in objective_parameter_list:
				self.objective_set.append(Objective(objective_parameters))

	def update(self,agent_locations):
		self.agent_locations=agent_locations

	def get_sub_objectives_in_region(self,objective_type,r):
		sub_objectives=[]
		for sub_objective in self.objective_set[objective_type]:
			if sub_objective.region==r:
				sub_objectives.append(sub_objective)
		return sub_objectives

	def get_region(self,x,y):
		return self.regions.get_region(x,y)

	
	def get_feasible_travel_paths(self,r):
		regions=[]
		for p in range(r(0)-1,r(0)+2):
			for q in range(r(1)-1,r(1)+2):
				regions.append(p,q)		

		return regions

	def get_region_objective_state(self,objective_type,r):
		c=0
		for sub_objective in self.objective_set[objective_type]:
			if sub_objective.region == r:
				c+=sub_objective.granularity
		
		return math.ceil(c/(self.region.size*self.region.size))	
		






	
					








