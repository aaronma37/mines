#!/usr/bin/env python

from random import randint
from environment_classes import Mine_Data
import time
import math
from sets import Set
from geometry_msgs.msg import PoseStamped
import numpy as np
import Regions




def append_dict(P,h1,h2,h3,r):
	if P.get(h1) is None:
		P[h1]={h2:{h3:r}}
	elif P[h1].get(h2) is None:
		P[h1][h2]={h3:r}
	elif P[h1][h2].get(h3) is None:
		P[h1][h2][h3]=r
	else:
		P[h1][h2][h3]+=r

def append_dict2(P,h1,h2,h3,h4,r):
	if P.get(h1) is None:
		P[h1]={h2:{h3:{h4:r}}}
	if P[h1].get(h2) is None:
		P[h1][h2]={h3:{h4:r}}
	elif P[h1][h2].get(h3) is None:
		P[h1][h2][h3]={h4:r}
	elif P[h1][h2][h3].get(h4) is None:
		P[h1][h2][h3][h4]=r
	else:
		P[h1][h2][h3][h4]+=r


	
class All_Regions():
	def __init__(self):
		self.identification="all_regions"

		self.score=0
		self.hash=self.score

	def update(self,regs):
		self.score=0.
		for i in regs:
			self.score+=i.score
		self.hash=int(self.score/10.)	


class Region():
	def __init__(self,index):
		self.index=index
		self.identification="region_score: " + str(self.index)
		self.hash=0
		self.score=0
		self.region_center=Regions.region[self.index]
		self.region_size=Regions.region_size

	def update(self,s):
		#get output hash
		self.score=s.get_region_score((self.region_center[0]-self.region_size,self.region_center[0]+self.region_size),(self.region_center[1]-self.region_size,self.region_center[1]+self.region_size))

		self.hash=self.score

	def update_with_hash(self,h):
		self.hash=h

	def get_input(self,workload):
		# get input hash
		# input is a combination of other hashes
		# can only depend on other abstractions
		return workload.hash

	def evolve(self,heuristics,workload):
		#the input here will be number of workers
		self.score=heuristics.pull_new_abstraction(self.identification, self.hash,self.get_input(workload))
		self.hash=self.score

		

class Battery():
	def __init__(self):
		self.hash="None"
		self.num=0.

	def update(self,num):
		self.hash=str(int(num/10.))
		self.num=num

	def update_with_hash(self,h):
		self.hash=h

	def get_input(self,s,a):
		print "dont use this"
		return None

	def evolve(self):
		self.num-=1
		if self.num < 0:
			self.num=0

		self.update(self.num)
		

class WorkLoad():
	def __init__(self,index):
		self.index=index
		self.hash="None"
		self.identification="workload"
		self.workload=0.
		self.workforce_number=0.

	def update(self,num_int,workforce_num):
		self.workload=num_int
		self.hash=str(self.workload)
		self.workforce_number=workforce_num

	def update_with_hash(self,h):
		self.hash=h

	def get_input(self,reg):


		if self.workforce_number == 0.:
			return str(int(5.*(self.workload/1.)))+str(":")+str(reg.hash)
		else:
			return str(int(5.*(self.workload/self.workforce_number)))+":"+str(reg.hash)

	def evolve(self,heuristics,reg):
		self.workload=heuristics.pull_new_abstraction(self.identification, self.hash,self.get_input(reg))
		self.hash=str(self.workload)

class Location():
	def __init__(self):
		self.hash="None"
		self.identification="location"

	def update(self,num_int):
		self.hash=str(num_int)
		

	def update_with_hash(self,h):
		self.hash=h

	def get_input(self,goal):
		return str(goal)

	def evolve(self,heuristics,goal):
		self.hash = heuristics.pull_new_abstraction(self.identification, self.hash,self.get_input(goal))

class Abstractions():
	def __init__(self):
		self.regions=[]
		self.work_load=[]
		for i in range(len(Regions.region)):
			self.regions.append(Region(i))
			self.work_load.append(WorkLoad(i))

		self.battery=Battery()
		self.location=Location()
		self.all_regions=All_Regions()

	def imprint(self,a):
		for i in len(self.regions):
			a.regions[i].hash=self.regions[i].hash
			a.regions[i].score=self.regions[i].score

			a.work_load[i].hash=self.work_load[i].hash
			a.work_load[i].workload=self.workload[i].hash
			a.work_load[i].workload_num=self.workload_num[i].hash

		a.battery.num=self.battery.num
		a.battery.hash=self.battery.hash
	

		a.location.hash=self.location.hash






		
	def update_all(self,s,a):
		for r in self.regions:
			r.update(s)
		for wl in self.work_load:
			wl.update(a.work_load[wl.index],sum(a.work_load))

		self.all_regions.update(self.regions)
		self.battery.update(a.battery)
		self.location.update(Regions.get_region(a.x,a.y))

	def evolve_all(self,heuristics,a):

		r= heuristics.pull_from_rewards(a.policy_set.TA.LA.identification,self.get_lower_level_abf(a),a.policy_set.TA.LA.index)
		for i in range(25):
			self.work_load[i].evolve(heuristics,self.regions[i])
			self.regions[i].evolve(heuristics,self.work_load[i])

		self.battery.evolve()

		self.location.evolve(heuristics,a.policy_set.TA.LA.index)
		self.all_regions.update(self.regions)

		return r

	def get_lower_level_abf(self,a):
		if a.policy_set.TA == 0:
			#charge
			return self.get_charge_abf()
		elif a.policy_set.TA == 1:
			#Explore
			return self.get_explore_abf()

	def get_lower_level_trigger(self,a):
		if a.policy_set.TA == 0:
			#charge
			return self.get_charge_trigger()
		elif a.policy_set.TA == 1:
			#Explore
			return self.get_explore_trigger(a.policy_set.TA.LA.index-1)

	def get_charge_trigger(self):
		h="charge trigger:"

		h=h+self.battery.hash

		return h

	def get_explore_trigger(self,index):
		h ="explore trigger:"

		h=h+self.regions[index].hash+":"

		return h

	def get_explore_abf(self):
		h ="explore:"

		for i in self.regions:
			h=h+str(i.hash)+":"

		for i in self.work_load:
			h=h+i.hash+"i"

		h=h+self.location.hash+":"

		return h



	def get_top_level_abf(self):
		h="top:"

		h=h+self.battery.hash + ":"
		h=h+str(self.all_regions.hash)
		return h

	def get_charge_abf(self):
		h="charge:"

		h=h+self.battery.hash

		return h

		






	

		


