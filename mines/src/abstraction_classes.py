#!/usr/bin/env python

from random import randint
from environment_classes import Mine_Data
import time
import math
from sets import Set
from geometry_msgs.msg import PoseStamped
import numpy as np
import Regions


def a2l(a):
	return a-1



class Region():
	def __init__(self,index):
		self.index=index
		self.identification="AR: " + str(Regions.get_region_type(index))
		self.hash=0
		self.score=0
		self.region_center=Regions.region[self.index]
		self.region_size=Regions.region_size

	def update(self,s):
		self.score=int(s.get_region_score((self.region_center[0]-self.region_size,self.region_center[0]+self.region_size),(self.region_center[1]-self.region_size,self.region_center[1]+self.region_size)))
		self.hash=self.score


	def evolve(self,a,workload):
		if a2l(a)==self.index or workload>0:
			self.score-=1
			self.hash-=1
		if self.hash < 0:
			self.hash =0

		

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

	def evolve(self,heuristics,reg):
		return #bandaid


class Battery():
	def __init__(self):
		self.num=0

	def update(self,num):
		self.num=num



class Location():
	def __init__(self):
		self.hash="None"
		self.identification="AL"
		self.region=None

	def update(self,a):
		self.region=Regions.get_region(a.x,a.y)

	def evolve(self,a):
		if a >0 and a < 26:
			self.region=a2l(a)

class mini_ab():
	def __init__(self):
		self.str=""
		self.b=""
		self.base=""

	def allocate(self, stra, b, base):
		self.str=stra
		self.b=b
		self.base=base

	def cull(self,flag):
		s = self.str.split(",")
		self.str=s[:-1]

	def get(self):
		return self.str

	def reward_funct(self,a,s):
		s_ = s.split("~")

		if int(s_[a])==3:
			return 5./(a+1.)
		elif int(s_[a])==2:
			return 2.5/(a+1.)
		elif int(s_[a])==1:
			return 1./(a+1.)
		else:
			return 0./(a+1.)

	def reward_funct_2(self,a,b,base):
		s_ = b.split("~")
		s_2 = base.split("~")
		s_=s_[:-1]
		s_2=s_2[:-1]

		for i in range(len(s_)-1):
			if int(s_[i])==1 and int(s_2[i+1]) == 0:
				return -100
				
			if int(s_[i])==1 and int(s_2[i+1]) == 1 and a==1:  
				return 1000
		
		return 0

		if int(s_[0])==0:
			return 0
		else:
			if int(s_2[0])==1 and a == 0:
				return 100
			elif int(s_2[1])==1 and a == 1:
				return 100
			else:
				print "failure"
				return -100




	def evolve(self,a,s,b,base):
		r=self.reward_funct(a,s)+self.reward_funct_2(a,b,base)
		s_ = s.split("~")
		s_2 = b.split("~")
		s_3 = base.split("~")
		s_=s_[:-1]
		s_2=s_2[:-1]
		s_3=s_3[:-1]

		if a==0:
			s_=s_[:-1]
			if int(s_[0]) > 0:
				s_[0]=str(int(s_[0])-1)
			s_.append("0")
		else:
			s_=s_[1:]
			s_.append("0")

		h=""
		for l in s_:
			h=h+l+"~"






		if s_3[1] == 1:
			for i in s_2:
				i="0"
		else:
			s_2=s_2[1:]
			s_2.append(s_2[-1])

		h2=""
		for l in s_2:
			h2=h2+l+"~"






		if a==0:
			s_3=s_3[:-1]
			s_3.append("0")
		else:
			s_3=s_3[1:]
			s_3.append("0")
		h3=""
		for l in s_3:
			h3=h3+l+"~"










		return h,h2,h3,r		





class Abstractions():
	def __init__(self):
		self.regions=[]
		self.work_load=[]
		for i in range(len(Regions.region)):
			self.regions.append(Region(i))
			self.work_load.append(WorkLoad(i))
		self.location=Location()
		self.battery=Battery()


	def imprint(self,a):
		for i in range(len(self.regions)):
			a.regions[i].hash=self.regions[i].hash
			a.regions[i].score=self.regions[i].score

			a.work_load[i].hash=self.work_load[i].hash
			a.work_load[i].workload=self.work_load[i].workload


		a.location.region=self.location.region
		a.location.hash=self.location.hash
		a.battery.num=self.battery.num

	def update_all(self,s,a):
		for r in self.regions:
			r.update(s)
		for wl in self.work_load:
			wl.update(a.work_load[wl.index],sum(a.work_load))

		self.location.update(a)
		self.battery.num=a.battery

	def get_max_reward_funct(self):
		r=[]
		for i in range(27):
			r.append(self.reward_funct(i))
		return r.index(max(r)),max(r)



	def reward_funct(self,a):
		if a==0 or a==26:
			return 0.
		
		if a2l(a)==self.location.region:
			d=1.
		else:
			d=2.

		if self.regions[a2l(a)].hash==3:
			if self.work_load[a2l(a)].hash>0:
				return 0./d
			else:
				return 5.5/d
		if self.regions[a2l(a)].hash==2:
			if self.work_load[a2l(a)].hash>0:
				return 0./d
			else:
				return 1.5/d
		if self.regions[a2l(a)].hash==1:
			if self.work_load[a2l(a)].hash>0:
				return 0./d
			else:
				return 0./d
		print a,self.regions[a2l(a)].hash
		return 0.




	def evolve_all(self,a):

		r=self.reward_funct(a)

		self.location.evolve(a)
		for i in range(25):
			self.regions[i].evolve(a,self.work_load[i].hash)
		#	self.work_load[i].evolve()


		return r

	def get_discrete_abf(self,i):
		if i==0:
			return str(self.location.region)+"~"
		elif i>0 and i<26:
			return str(self.regions[i-1].hash)+"~"
		elif i>25 and i<51:
			return str(self.work_load[i-26].hash)+"~"


	def get_location_abf(self):
		return "loc:"+str(self.location.region)+"~"


	def get_region_score_abf(self):
		h = "rs:"
		for i in self.regions:
			h=h+str(i.index)+"-"+str(i.hash)+":"
		h = h + "~"
		return h


	def get_work_load_abf(self):
		h= "wl:"
		for i in self.work_load:
			h=h+str(i.index)+"-"+str(i.hash)+":"
		h=h+"~"
		return h


	def get_complete_abf(self):		
		return self.get_location_abf()+self.get_region_score_abf()+self.get_work_load_abf()


	def get_base(self):
		return self.location.region



		






	

		


