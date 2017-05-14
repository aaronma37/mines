#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
import Regions

Objective_Types

def get_available_objective_types(sub_environment):
	aot=[]
	aot.append("wait")
	aot.append("travel")
	
	for o in Objective_Types:
		if sub_environment.get_objective_index(0,o) > 0:
			aot.append(o)

	return aot
	

	


def tau(objective_type,region_i,region_f):
	if objective_type=="wait":
		return 1000
	return 15


class Task:
	def __init__(self,objective_type,state_i,region_i,region_f):
		self.complete=False
		self.objectives=[(objective_type,region_i),("travel",region_f)]
		self.state_i=state_i
		self.current_objective=self.objectives[0]
		if objective_type!="wait" and objective_type!="travel":
			self.reward=1
		else:
			self.reward=0

	def get_distance(self,x,y,x2,y2):
		return max(math.fabs(x-x2),math.fabs(y-y2))

	def get_target(self,objective_type,a,r,complete_state):

		sub_objectives = complete_state.get_sub_objectives_in_region(objective_type,r)

		min_dist=1000
		min_next=(a.x,a.y)

		for sub_objective in sub_objectives:
			if self.get_distance(a.x,a.y,sub_objective.x,sub_objective.y) < min_dist:
				min_dist=self.get_distance(a.x,a.y,sub_objective.x,sub_objective.y)
				min_next=(sub_objective.x,sub_objective.y)

		return min_next
				
	def check_completion(self,agent,complete_state):
		self.current_objective=self.objectives[0]
		if complete_state.get_region_objective_state(self.current_objective[0],region_i) == self.state_i:
			self.current_objective = self.objectives[1]
		if complete_state.get_region(agent.x,agent.y) == region_f:
			return True
		return False
		
	def get_next_action(self,agent,complete_state):
		next_x=0
		next_y=0

		target = self.get_target(self.current_objective[0],agent,self.current_objective[1],complete_state)
	
		if a.x < target[0]:
			next_x = 1
		elif a.x > target[0]:
			next_x = -1

		if a.y <target[1]:
			next_y= 1
		elif a.y > target[1]:
			next_y=-1

		if a.x is target[0] and a.y is target[1]:
			return (0,0)
		else:	
			return (next_x,next_y)

	def tau(self):
		return 15

	




class Trajectory:
	def __init__(self,sub_environment,ordered_objective_type_list):
		self.task_list=[]
		for i in range(len(ordered_objective_type_list)):
			self.task_list.append(Task(ordered_objective_type_list[i]),sub_environment.get_objective_index(i,ordered_objective_type_list[i]),sub_environment.region_list[i],sub_environment.region_list[i+1])
		#self.sub_environment=sub_environment
		self.current_index=0

	def update_completion(self,agent,complete_state):
		for i in range(self.current_index,len(self.action_list)):
			if self.action_list[i].check_complete(agent,complete_state) == False:
				self.current_index=i
				break

	def get_action(self,agent,complete_state):
		self.update_completion(self,agent,complete_state)
		return self.task_list[self.current_index].get_next_action(agent,complete_state)
















