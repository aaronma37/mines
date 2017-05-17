#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math

def get_available_objective_types(sub_environment,complete_environment):
	aot=[]
	aot.append("wait")
	aot.append("travel")
	

	for obj_type in complete_environment.objective_map.keys():
		if sub_environment.get_objective_index(0,complete_environment.objective_map[obj_type]) > 0:
			aot.append(obj_type)

	return aot
	

	


def tau(objective_type,score):

	try:	
         	int(score)
    	except ValueError:
        	print("Oops!  That was no valid number.  Try again...")
		return 1000

	if objective_type=="wait":
		return 1000
	if objective_type=="travel":
		return 10
	if int(score)==0:
		return 1000
	elif int(score)==1:
		return 25
	elif int(score)==2:
		return 16
	else:
		return 12


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

		if objective_type=="wait":
			return (a.x,a.y)
		elif objective_type=="travel":
			target_locations = complete_state.get_sub_objectives_in_region(objective_type,r)

			min_dist=1000
			min_next=(a.x,a.y)

			for loc in target_locations:
				if self.get_distance(a.x,a.y,loc[0],loc[1]) < min_dist:
					min_dist=self.get_distance(a.x,a.y,loc[0],loc[1])
					min_next=(loc[0],loc[1])

			#print min_dist, "distance", objective_type
			#if min_dist==0:
			#	print self.current_objective[1],complete_state.get_region(a.x,a.y)
			return min_next

		sub_objectives = complete_state.get_sub_objectives_in_region(objective_type,r)

		min_dist=1000
		min_next=(a.x,a.y)

		for sub_objective in sub_objectives:
			if self.get_distance(a.x,a.y,sub_objective.x,sub_objective.y) < min_dist:
				min_dist=self.get_distance(a.x,a.y,sub_objective.x,sub_objective.y)
				min_next=(sub_objective.x,sub_objective.y)

		return min_next
				
	def check_completion(self,agent,complete_environment):
		self.current_objective=self.objectives[0]
		if self.current_objective[0]=="wait":
			return False
		if self.current_objective[0]=="travel":
			if complete_environment.get_region(agent.x,agent.y) == self.current_objective[1]:
				return True
		elif int(complete_environment.get_region_objective_state(self.current_objective[0],self.current_objective[1])) != int(self.state_i):
			#print int(self.state_i)==int(complete_environment.get_region_objective_state(self.current_objective[0],self.current_objective[1])), self.current_objective[0]
			self.current_objective = self.objectives[1]
			if complete_environment.get_region(agent.x,agent.y) == self.current_objective[1]:
				return True
		return False
		
	def get_next_action(self,agent,complete_state):
		next_x=0
		next_y=0

		target = self.get_target(self.current_objective[0],agent,self.current_objective[1],complete_state)
	
		if agent.x < target[0]:
			next_x = 1
		elif agent.x > target[0]:
			next_x = -1

		if agent.y <target[1]:
			next_y= 1
		elif agent.y > target[1]:
			next_y=-1

		if agent.x is target[0] and agent.y is target[1]:
			return (0,0)
		else:	
			return (next_x,next_y)

	def tau(self,score):
		return 15

	




class Trajectory:
	def __init__(self,sub_environment,ordered_objective_type_list,complete_environment):
		self.task_list=[]
		for i in range(len(ordered_objective_type_list)):
			if ordered_objective_type_list[i] == "wait" or ordered_objective_type_list[i] == "travel":
				self.task_list.append(Task(ordered_objective_type_list[i],0,sub_environment.region_list[i],sub_environment.region_list[i+1]))
			else:
				self.task_list.append(Task(ordered_objective_type_list[i],sub_environment.get_objective_index(i,complete_environment.objective_map[ordered_objective_type_list[i]]),sub_environment.region_list[i],sub_environment.region_list[i+1]))
		self.sub_environment=sub_environment
		self.current_index=0

	def update_completion(self,agent,complete_state):
		for i in range(self.current_index,len(self.task_list)):
			if self.task_list[i].check_completion(agent,complete_state) == False:
				if i!= self.current_index:
					print "updated trajectory", self.current_index, i, self.task_list[i].objectives[0][0], self.task_list[i].state_i
				self.current_index=i
				break

	def get_action(self,agent,complete_state):
		self.update_completion(agent,complete_state)
		return self.task_list[self.current_index].get_next_action(agent,complete_state)

	def print_data(self):
		for t in self.task_list:
			print t.current_objective[0]
















