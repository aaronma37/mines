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
	def __init__(self,index,next,agent_poll_time,index_type,point):
		self.index=index
		self.index_type=index_type #explore, go to point, etc.#
		self.point=point
		self.next=next
		self.time=agent_poll_time
		self.max_time=agent_poll_time
		self.last_motion=(0,0)
	
	def get_distance(self,x,y,x2,y2):
		return max(math.fabs(x-x2),math.fabs(y-y2))

	def get_target(self,a,s):
		if self.index_type=="charge" or self.index_type=="mine":
			if self.point is not None:
				return self.point
			else:
				return Regions.region[next]

		if self.index==0:
			return (s.middle[0],s.middle[1])
		elif self.index <26:
			
			m=1000
			if self.index==15:
				loc=(50,50)
			else:
				loc=(a.x,a.y)

			l = Regions.region_list[self.index-1]
			l2 = Regions.region_list[self.next-1]
			shuffle(l)
			shuffle(l2)


			short_next=(a.x,a.y)
			m2=1000
		

			for i in l2:
				if s.seen[i[0]][i[1]]==s.NOT_SEEN:
					if self.get_distance(a.x,a.y,i[0],i[1]) < m2:
						m2=self.get_distance(a.x,a.y,i[0],i[1])
						short_next = i

			for i in l:
				if s.seen[i[0]][i[1]]==s.NOT_SEEN:
					if self.time < 5.:
						if 10*self.get_distance(a.x,a.y,i[0],i[1])*self.time/self.max_time + 0*self.get_distance(short_next[0],short_next[1],i[0],i[1])*(self.max_time-self.time)/self.max_time < m and self.allowable_motions(self.last_motion,(a.x-i[0],a.y-i[1])) is True:	
							m=self.get_distance(a.x,a.y,i[0],i[1])
							loc = i
					else:
						if self.get_distance(a.x,a.y,i[0],i[1])*self.time/self.max_time < m and self.allowable_motions(self.last_motion,(a.x-i[0],a.y-i[1])) is True:	
							m=self.get_distance(a.x,a.y,i[0],i[1])
							loc = i

			self.last_motion = a.x-loc[0],a.y-loc[1]

			return loc

	def allowable_motions(self,prev,motion):
		return True
		if prev == (0,0):
			return True
		if prev[0] == -1:
			if motion[0] == 1:
				return False
		elif prev[0] == 1:
			if motion[0] == -1:
				return False
		if prev[1] == -1:
			if motion[1] == 1:
				return False
		elif prev[1] == 1:
			if motion[1] == -1:
				return False
		return True

						
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

