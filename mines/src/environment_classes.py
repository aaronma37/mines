#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
from mines.msg import subobjective as subobjective_msg
from mines.msg import objective as objective_msg
from mines.msg import environment as environment_msg

size=10

objective_parameter_list=[]
objective_map={}
objective_parameter_list.append(('All',2,"mine"))
objective_map["mine"]=0



def get_region(x,y):
	return (int(math.floor(x/size)),int(math.floor(y/size)))

def get_region_parts(r):
	region_list=[]
	for x in range(r[0]*size,(r[0]+1)*size):
		for y in range(r[1]*size,(r[1]+1)*size):		
			region_list.append((x,y))
	return region_list

def is_feasible_travel_path(r1,r2):
	if abs(r1(0)-r2(0))<2 and abs(r1(1)-r2(1))<2:
		return True
	return False



class Sub_Objective():
	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.region=get_region(x,y)


class Objective():
	def __init__(self,objective_parameters):
		self.sub_objectives=[]
		self.distribution_type=objective_parameters[0]
		self.granularity=objective_parameters[1]
		self.frame_id=objective_parameters[2]
		
		
	def distribute(self,distribution_type):
		if distribution_type=="All":
			for x in range(100):
				for y in range(100):
					self.sub_objectives.append(Sub_Objective(x,y))

	def repopulate(self):
		if self.distribution_type=="All":
			for x in range(25,75):
				for y in range(25,75):
					self.sub_objectives.append(Sub_Objective(x,y))		
		

class Sub_Environment:
	def __init__(self):
		self.region_list=[]
		self.state=None
		self.interaction_set=None
		 
	def set_region_list(self,region_list):
		self.region_list=region_list
	
	def set_random_region_list(self,r,L):
		self.region_list=[]
		self.region_list.append(r)
		for k in range(L-1):
			self.region_list.append((self.region_list[-1][0]+random.randint(-1, 1),self.region_list[-1][1]+random.randint(-1, 1)))



	def get_sub_sub_environment(self,k):
		return Sub_Environment(self.region_list[0:k],self.state[0:k],self.interaction_set[0:k])

	def append_region(self,r):
		self.region_list.append(r)

	def cull_state_from_back(self,k):
		s=self.state.split(".")

		h=""
		for i in range(0,len(s)-k-1):
			h=h+s[i]+"."

		return h


		

	def cull_state_from_front(self,k):
		s=self.state.split(".")
		h=""
		for i in range(k,len(s)-1):
			h=h+s[i]+"."

		return h

	def get_state_index(self,k):
		return self.state.split(".")[k]

	def get_objective_index(self,k,o_index):
		return self.get_state_index(k).split(",")[o_index]

	def get_k(self):
		return len(self.region_list)-1

		
		
	def update_state(self,complete_environment):
		self.state=""

		for r in self.region_list:
			self.state=self.state
			for obj_type in complete_environment.objective_map.keys():
				self.state=self.state+str(complete_environment.get_region_objective_state(obj_type,r))+","

			self.state=self.state+"."

	def evolve(self,complete_environment):
		evolved_environment=Sub_Environment()
		evolved_environment.region_list=self.region_list[1:]
		evolved_environment.update_state(complete_environment)
		return evolved_environment

		



class Complete_Environment:
	def __init__(self):

		self.objective_parameter_list=objective_parameter_list
		self.objective_list=[]
		self.objective_map={}
		for objective_parameters in self.objective_parameter_list:
			self.objective_list.append(Objective(objective_parameters))
			self.objective_map[objective_parameters[2]]=len(self.objective_list)-1
		self.agent_locations=[]
		self.repopulate()

	def reset(self):
		self.objective_list=[]
		self.objective_map={}
		for objective_parameters in self.objective_parameter_list:
			self.objective_list.append(Objective(objective_parameters))
			self.objective_map[objective_parameters[2]]=len(self.objective_list)-1
		self.repopulate()

	def repopulate(self):
		for o in self.objective_list:
			o.repopulate()

	def update(self,agent_locations):
		self.agent_locations=agent_locations

	def get_sub_objectives_in_region(self,objective_type,r):
		sub_objectives=[]
		if objective_type == "wait":
			return sub_objectives
		elif objective_type=="travel":
			return 	get_region_parts(r)	




		for sub_objective in self.objective_list[self.objective_map[objective_type]].sub_objectives:
			if sub_objective.region==r:
				sub_objectives.append(sub_objective)
		return sub_objectives

	def get_region(self,x,y):
		return get_region(x,y)

	
	def get_feasible_travel_paths(self,r):
		regions=[]
		
		for p in range((int(r[0])-1),(int(r[0])+2)):
			for q in range((int(r[1])-1),(int(r[1])+2)):
				regions.append((p,q))		

		return regions

	def get_region_objective_state(self,objective_type,r):
		if objective_type=="wait" or objective_type=="travel":
			return 0

		c=0
		obj=self.objective_list[self.objective_map[objective_type]]
		for sub_objective in obj.sub_objectives:
			if sub_objective.region == r:
				c+=obj.granularity
		
		return int(math.ceil(c/float(size*size)))	

	def execute_objective(self, objective_type, location):
		obj=self.objective_list[self.objective_map[objective_type]]

		for i in xrange(len(obj.sub_objectives)-1,-1,-1):
			if abs(obj.sub_objectives[i].x-location[0])<2 and abs(obj.sub_objectives[i].y-location[1])<2:
				del obj.sub_objectives[i]



#
		#for sub_objective in list(obj.sub_objectives):
		#	if abs(sub_objective.x-location[0])<2 and abs(sub_objective.y-location[1])<2:
		#		obj.sub_objectives.delete(sub_objective)





	def generate_environment_msg(self):
		env_msg=environment_msg()
		env_msg.frame_id="default"
		
		env_msg.objective=[]

		for o in self.objective_list:
			env_msg.objective.append(objective_msg())
			env_msg.objective[-1].frame_id=o.frame_id
			env_msg.objective[-1].param1=o.distribution_type
			env_msg.objective[-1].param2=o.granularity

			for so in o.sub_objectives:
				env_msg.objective[-1].subobjective.append(subobjective_msg())
				env_msg.objective[-1].subobjective[-1].x=so.x
				env_msg.objective[-1].subobjective[-1].y=so.y
				env_msg.objective[-1].subobjective[-1].rx=so.region[0]
				env_msg.objective[-1].subobjective[-1].ry=so.region[1]

		return env_msg

	def update(self,env_msg):
		self.objective_list=[]
		self.objective_map={}

		for o in env_msg.objective:
			self.objective_list.append(Objective([o.param1,o.param2,o.frame_id]))
			self.objective_map[o.frame_id]=len(self.objective_list)-1
			for so in list(o.subobjective):
				self.objective_list[-1].sub_objectives.append(Sub_Objective(so.x,so.y))


	def print_objective_score(self,objective_type):
		obj=self.objective_list[self.objective_map[objective_type]]
		#print "score", objective_type, len(obj.sub_objectives)
			

	def modify(self,effective_beta):
		for o in self.objective_list:
			#print "lena", len(o.sub_objectives), len(effective_beta.claimed_objective)
			for claimed_objective in effective_beta.claimed_objective:
				if claimed_objective.objective_type!=o.frame_id:
					continue
				for i in xrange(len(o.sub_objectives)-1,-1,-1):
					if o.sub_objectives[i].region == (claimed_objective.region.x,claimed_objective.region.y):
						o.sub_objectives.remove(o.sub_objectives[i])
			#print "lenb", len(o.sub_objectives)





	
					








