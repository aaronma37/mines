#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
import Regions

from random import shuffle

class policy_root:
	def __init__(self):
		self.identification="root"

		self.policy_set=[]
		self.policy_set.append(policy_top_level(0))
		self.policy_set.append(policy_top_level(1))
		self.TA=policy_top_level(policy_top_level(0))
		self.bottom=0
		self.top=2

class policy_top_level:
	def __init__(self,index):
		self.index=index
		self.identification="Not set"
		#index=0 is to go charge
		#index 1 is to go explore
		self.trigger="Not set"
		self.policy_set=[]
		self.bottom=0
		self.top=0
		if self.index==0:
			self.bottom=0
			self.identification="Charge"
			self.policy_set.append(policy_low_level(0))
			self.top=1
		else:
			self.bottom=1
			self.identification="Explore"
			self.top=26
			for i in range(1,self.top):
				self.policy_set.append(policy_low_level(i))

		self.LA=(policy_low_level(0))

	def check_trigger(self,A):

		if self.trigger != self.get_trigger_definition(A):
			return True

		if A.battery.num>90 and self.index==0:
			return True

		return False

	def get_trigger_definition(self,A):
		return A.get_top_level_abf()

	def set_trigger(self,A):
		self.trigger=self.get_trigger_definition(A)
	




class policy_low_level:
	def __init__(self,index):
		self.index=index
		self.trigger="Not set"
		if self.index==0:
			self.identification="Charge"
		else:
			self.identification="Explore " + str(self.index) 
		# index = 0 is go to base and charge

		# index 1: 25 is go to region (region -1 ) 

	def check_trigger(self,A,a):
		if self.trigger != self.get_trigger_definition(A,a):
			return True

		if A.battery.num>90 and self.index==0:
			return True

		if self.index > 0 and A.regions[self.index-1].score<1: #bandaid
			return True

		return False

	def get_distance(self,x,y,x2,y2):
		return max(math.fabs(x-x2),math.fabs(y-y2))

	def get_trigger_definition(self,A,a):
		return A.get_lower_level_trigger(a)

	def set_trigger(self,A,a):
		self.trigger=self.get_trigger_definition(A,a)


	#def get_abstraction(self,A):
	#	if self.index==0:
	#		return abf_battery(a)
	#	elif self.index <26:
	#		return abf_region(s,self.index-1)

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

