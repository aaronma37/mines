#!/usr/bin/env python

from random import randint
from environment_classes import Mine_Data
import time
import math
from sets import Set
from geometry_msgs.msg import PoseStamped
import numpy as np
import Regions

def get_next_action(loc,i):
	next_x=0
	next_y=0
	target = Regions.region[i]

	if loc[0] < target[0]:
		next_x = 1
	elif loc[0] > target[0]:
		next_x = -1

	if loc[1] <target[1]:
		next_y= 1
	elif loc[1] > target[1]:
		next_y=-1

	if loc[0] is target[0] and loc[1] is target[1]:
		return (0,0)
	else:	
		return (next_x,next_y)


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
		self.identification="AAR"

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
		self.identification="AR: " + str(Regions.get_region_type(index))
		self.hash=0
		self.score=0
		self.region_center=Regions.region[self.index]
		self.region_size=Regions.region_size

	def update(self,s):
		#get output hash


		self.score=int(s.get_region_score((self.region_center[0]-self.region_size,self.region_center[0]+self.region_size),(self.region_center[1]-self.region_size,self.region_center[1]+self.region_size)))
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
	
		#print heuristics.pull_new_abstraction(self.identification, self.hash,self.get_input(workload))
		#indent=A1.regions[i].identification
		#base=A1.regions[i].hash
		#input_=A1.regions[i].get_input(A1.work_load[i])

		self.score=int(heuristics.pull_new_abstraction(self.identification, str(self.hash),str(self.get_input(workload))))#BANDAID
		#print self.score, "SCORE"
		self.hash=self.score

		

class Battery():
	def __init__(self):
		self.hash="None"
		self.num=0.
		self.val=0.

	def update(self,num):
		self.val=num
		self.hash=str(int(num/10.))
		self.num=num

	def update_with_hash(self,h):
		self.hash=h

	def get_input(self,s,a):
		print "dont use this"
		return None

	def evolve(self,base):

		if base is True:
			self.val+=5.
			if self.val > 100:
				self.val=100

			self.update(self.val)
		
		else:
			self.val-=.25
			if self.val < 0:
				self.val=0

			self.update(self.val)

		

class WorkLoad():
	def __init__(self,index):
		self.index=index
		self.hash="DEFAULT"
		self.identification="AW"
		self.workload=0.
		self.workforce_number=0.

	def update(self,num_int,workforce_num):
		self.workload=num_int
		if self.workload > 1:
			self.hash=1
		else:
			self.hash=0		
		self.workforce_number=workforce_num

	def update_with_hash(self,h):
		self.hash=h

	def get_input(self,reg):
		if self.workforce_number == 0.:
			return str(int(5.*(self.workload/1.)))+":"+str(reg.hash)
		else:
			return str(int(5.*(self.workload/self.workforce_number)))+":"+str(reg.hash)

	def evolve(self,heuristics,reg):
		return #bandaid
		#self.workload=int(heuristics.pull_new_abstraction(self.identification, self.hash,self.get_input(reg)))
		#self.hash=str(self.workload)

class Location():
	def __init__(self):
		self.hash="None"
		self.identification="AL"
		self.distance=0
		self.inside_region = False

		self.goto=0
		self.loc=(0,0)

	def update(self,a):
		self.loc=(a.x,a.y)
		if a.current_action.index > 0 and a.current_action.index <26:
			self.goto=a.current_action.index-1
			self.distance=Regions.get_distance(self.loc[0],self.loc[1],Regions.region[a.current_action.index-1][0],Regions.region[a.current_action.index-1][1])#regions get distance between goal and 
		else:
			self.goto=14
			self.distance=Regions.get_distance(self.loc[0],self.loc[1],Regions.region[14][0],Regions.region[14][1])
			#print self.distance
		self.check_inside(a.current_action.index)
		self.hash=str(self.distance)


	def check_inside(self,a):
		if a!=0:
			if self.distance < 10: 
				self.inside_region =True
			else:
				self.inside_region =False
		else:
			if self.distance < 2: 

				self.inside_region =True
			else:
				self.inside_region =False
		

	def update_with_hash(self,h):
		self.hash=h

	def get_input(self,goal):
		return str(goal)

	def evolve(self,heuristics,goal):
		if goal==0:
			if self.goto==14:
				ev=get_next_action(self.loc,self.goto)

				self.loc= (self.loc[0]+ev[0], self.loc[1]+ev[1])

				self.distance-=1
				#print self.goto,goal,self.distance,self.inside_region,self.loc	
				self.check_inside(goal)
				#self.hash = heuristics.pull_new_abstraction(self.identification, self.hash,self.get_input(goal))
			else:
				self.update_action(goal)
		elif goal<26:
		
			if goal-1==self.goto:
				ev=get_next_action(self.loc,self.goto)

				self.loc= (self.loc[0]+ev[0], self.loc[1]+ev[1])

				self.distance-=1
				#print self.goto,goal,self.distance,self.inside_region,self.loc	
				self.check_inside(goal)
				#self.hash = heuristics.pull_new_abstraction(self.identification, self.hash,self.get_input(goal))
			else:
				self.update_action(goal)
			

	def update_action(self,action):
		self.inside_region =False
		if action > 0 and action < 26:
			self.goto=action-1
			self.distance=Regions.get_distance(self.loc[0],self.loc[1],Regions.region[action-1][0],Regions.region[action-1][1])#regions get distance between goal and 
		elif action==0:
			self.goto=14
			self.distance=Regions.get_distance(self.loc[0],self.loc[1],Regions.region[14][0],Regions.region[14][1])
			self.check_inside(action)
			self.hash=str(self.distance)
		
			#print "GOING TO MIDDLE", self.inside_region
			

	


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

	def battery_charge(self):
		self.battery.num=95
		self.battery.update(self.battery.num)
		self.location.reg=14





		
	def update_all(self,s,a):
		for r in self.regions:
			r.update(s)
		for wl in self.work_load:
			wl.update(a.work_load[wl.index],sum(a.work_load))

		self.all_regions.update(self.regions)
		self.battery.update(a.battery)
		self.location.update(a)
		#print self.location.hash, "loc"

	def get_reward_abf(self,region_num):
		if region_num== 0:
			return "charging"
		elif region_num==26:
			return "charging"
		else:
			h ="reward_abf_explore:"
			#h = h + str(Regions.get_region_type(region_num-1)) + ":"
			h = h + str(self.regions[region_num-1].hash) + ":"

			#if self.work_load[region_num-1].hash==0:
			h = h + str(self.work_load[region_num-1].hash)+":"
				#h = h + str(1)+ ":"
			#else:
			#	h = h + str(self.work_load[region_num-1].hash)+ ":"
			if self.location.inside_region is True:
				h=h+"search"
			else:
				h=h+"travel"
			
		return h

	def get_inherent_reward_func(self,a):
		#r if exploring
		#r = score/distance-(100-battery)*distance

		# if charging
		# r is static

		if self.battery.num==0:
			if a==26:
				return 100000.
			else:
				return 0.



		if a!=0 and a < 26:
			distance1=Regions.get_distance(Regions.region[Regions.get_region(self.location.loc[0],self.location.loc[1])][0],Regions.region[Regions.get_region(self.location.loc[0],self.location.loc[1])][1],Regions.region[a-1][0],Regions.region[a-1][1])/10.#regions get distance between goal and
			distance2=Regions.get_distance(Regions.region[14][0],Regions.region[14][1],Regions.region[a-1][0],Regions.region[a-1][1])/10.#regions get distance between goal and
		elif a==0:
			#print a,1
			return 0.
		elif a==26:
			distance1=Regions.get_distance(Regions.region[Regions.get_region(self.location.loc[0],self.location.loc[1])][0],Regions.region[Regions.get_region(self.location.loc[0],self.location.loc[1])][1],Regions.region[14][0],Regions.region[14][1])#regions get distance between goal and
			if distance1/3.9 > self.battery.num:
				return 10000000000	
			else:
				return -100000


		if distance1<1:
			distance1=1
		if distance2<1:
			distance2=1
		
		if self.battery.num<20:
			return -1

		#print a,5*(self.regions[a-1].score/distance1-(100.-self.battery.val)*(100.-self.battery.val)*distance2/10000.),self.battery.val
		return 5*(self.regions[a-1].score/distance1-(100.-self.battery.val)*(100.-self.battery.val)*distance2/10000.)

	def get_inherent_reward_func2(self,a):
		if a!=0 and a < 26:
			distance1=Regions.get_distance(Regions.region[Regions.get_region(self.location.loc[0],self.location.loc[1])][0],Regions.region[Regions.get_region(self.location.loc[0],self.location.loc[1])][1],Regions.region[a-1][0],Regions.region[a-1][1])/10.#regions get distance between goal and
			distance2=Regions.get_distance(Regions.region[14][0],Regions.region[14][1],Regions.region[a-1][0],Regions.region[a-1][1])/10.#regions get distance between goal and
		elif a==0:
			#print a,1
			return 0.
		elif a==26:
			return 0.


		if distance1<1:
			distance1=1
		if distance2<1:
			distance2=1
		
		if self.battery.num<20:
			return -1

		#print a,5*(self.regions[a-1].score/distance1-(100.-self.battery.val)*(100.-self.battery.val)*distance2/10000.),self.battery.val
		return self.regions[a-1].score/distance1


	def new_action(self, action):
		self.location.update_action(action)

	def reward_func(self,region_num):

		if region_num== 0:
			return 0.
		elif region_num==26:
			return 0.
		else:
			if self.location.inside_region is True:
				r=1.
				r=r*self.regions[region_num-1].hash


				if self.work_load[region_num-1].hash > 0:
					r=r/100.#(self.work_load[region_num-1].hash*self.work_load[region_num-1].hash*self.work_load[region_num-1].hash)
					#print r, region_num-1, "HERE"
			else:
				r=0.


			
		return r

	def evolve_all(self,heuristics,action):
		r=0

		for j in range(5):

				
			#for i in range(25):
			#	self.work_load[i].evolve(heuristics,self.regions[i])
			#	self.regions[i].evolve(heuristics,self.work_load[i])

			if action==0 and self.location.inside_region is True:
				self.battery.evolve(True)
			elif action < 26:
				self.battery.evolve(False)

		

			if self.battery.num>0:
				self.location.evolve(heuristics,action)
			else:
				return -1000.


			if self.location.inside_region is False:
				r+=0.
			else:
				#r += heuristics.pull_from_rewards(self.get_reward_abf(action))
				r += self.reward_func(action)

			self.all_regions.update(self.regions)
			

		return r



	def get_lower_level_abf(self,a):
		if a.current_action.index == 0:
			#charge
			return self.get_charge_abf()
		elif a.current_action.index == 1:
			#Explore
			#return self.get_explore_abf()+str(a.policy_set.TA.LA.index)+":"+str(self.regions[a.policy_set.TA.LA.index-1].hash)+"end"
			return self.get_explore_abf()+"end"

	def get_lower_level_trigger(self,a):
		if a.current_action.index == 0:
			#charge
			return self.get_charge_trigger()
		elif a.current_action.index == 1:
			#Explore
			return self.get_explore_trigger(a.current_action.index-1)
		print "MISSED"

	def get_charge_trigger(self):
		h="charge trigger:"

		h=h+self.battery.hash

		return h

	def get_explore_trigger(self,index):
		h ="explore trigger:"

		h=h+str(self.regions[index].hash)+":"

		return h

	def get_explore_abf(self):
		h ="explore:"

		for i in self.regions:
			h=h+str(i.hash)+":"

		for i in self.work_load:
			h=h+str(i.hash)+":"

		h=h+str(Regions.get_region(self.location.loc[0],self.location.loc[1]))+":"
		#h=h+str(self.battery.hash)+":"

		


		return h


		
		



	def get_top_level_abf(self):
		h="top:"

		h=h+self.battery.hash + ":"
		h=h+str(self.all_regions.hash)+":"
		h=h+str(Regions.get_region_type(self.location.reg))
		return h

	def get_charge_abf(self):
		h="charge:"

		h=h+self.battery.hash

		return h

		






	

		


