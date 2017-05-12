#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
import Regions

from random import shuffle

action_index_max=27
action_list=[]

action_library=[]

action_library.append('explore')
action_library.append('charge')
action_library.append('mine')



for i in range(action_index_max):
	action_list.append(i)

def get_distance(x,y,x2,y2):
	return max(math.fabs(x-x2),math.fabs(y-y2))

def get_discrete_target(a,s,action):
	if action==0:
		return (s.middle[0],s.middle[1])
	elif action <26:
		m=1000
		loc=(0,0)
		l = Regions.region_list[action-1]
		shuffle(l)
		for i in l:
			if s.seen[i[0]][i[1]]==s.NOT_SEEN:
				if get_distance(a.x,a.y,i[0],i[1]) < m:
					m=get_distance(a.x,a.y,i[0],i[1])
					loc = i
		#if loc==(50,50):
			#print "none found"
		return loc




def get_discrete_action(a,s,action):
	next_x=0
	next_y=0

	if action==26:
		return (0,0)


	target = get_discrete_target(a,s,action)

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

class Policy:
	def __init__(self,objective_type,state_i,state_f,region_i,region_f):
		self.complete=False
		self.objectives=[(objective_type,region_i),("travel",region_f)]

		self.state_i=state_i
		self.state_f=state_f


	def get_distance(self,x,y,x2,y2):
		return max(math.fabs(x-x2),math.fabs(y-y2))

	def get_target(self,o,a,s):
		#returns closest in o in region
		o_list = s.get_objective_locations(o)

		min_dist=1000
		min_next=(a.x,a.y)

		for loc_o in o_list:
			if self.get_distance(a.x,a.y,loc_o(0),loc_o(1)) < min_dist:
				min_dist=self.get_distance(a.x,a.y,loc_o(0),loc_o(1))
				min_next=loc_o

		return min_next
				
	def check_completion(self,a,s):
		self.current_objective=self.objectives[0]
		if s.check_state(a,o,self.state_i) == True:
			self.current_objective = self.objectives[1]
		if s.check_state(a,o,"default") == True:
			return True
		else:
			return False
		
	def get_next_action(self,a,s):
		next_x=0
		next_y=0

		target = self.get_target(self.current_objective,a,s)
	
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

