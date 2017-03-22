#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
import Regions

from random import shuffle

action_index_max=27
action_list=[]


for i in range(action_index_max):
	action_list.append(i)

class Policy:
	def __init__(self,index):
		self.index=index
		self.time=10

	def check_trigger(self):
		if self.time > 0:
			return False
		return True
	
	def get_distance(self,x,y,x2,y2):
		return max(math.fabs(x-x2),math.fabs(y-y2))

	def set_trigger(self,A,a):
		#depreciated
		self.trigger=self.get_trigger_definition(A,a)

	def get_target(self,a,s):
		if self.index==0:
			return (s.middle[0],s.middle[1])
		elif self.index <26:
			m=1000
			loc=(0,0)
			l = Regions.region_list[self.index-1]
			shuffle(l)
			for i in l:
				if s.seen[i[0]][i[1]]==s.NOT_SEEN:
					if self.get_distance(a.x,a.y,i[0],i[1]) < m:
						m=self.get_distance(a.x,a.y,i[0],i[1])
						loc = i
			if loc==(0,0):
				print "none found"
			return loc
						
	def get_next_action(self,a,s):
		next_x=0
		next_y=0
		self.time-=1

		if self.index==26:
			return (0,0)


		target = self.get_target(a,s)
	
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

