#!/usr/bin/env python

from random import randint
from environment_classes import Mine_Data

import math
from sets import Set
from geometry_msgs.msg import PoseStamped
import numpy as np
from Policies import policy_root
from abstraction_classes import Abstractions
from Heuristics import update_H
import Regions
from POMDP import Solver
import time
import Policies
class Agent: 


	def __init__(self,Mine_Data,map_size_):

		self.solver = Solver(Mine_Data,map_size_) # get rid of

		self.map_size=map_size_
		self.x=self.map_size/2
		self.y=self.map_size/2		
		self.ON=0
		self.measurement_space=[]
		self.alpha=[.9,.1,0]
		#self.reset()
		self.battery=50
		self.work_load=[]
		self.work=0
		self.last_reward=0.
		for i in range(len(Regions.region)):
			self.work_load.append(0)

		self.old_A=Abstractions()
		self.new_A=Abstractions()


		self.policy_set=policy_root()
		self.time_away_from_network=0
		
	def update_heuristics(self,old_s,new_s):
		self.old_A.update_all(old_s,self)
		self.new_A.update_all(new_s,self)	
#
		#print "cc: ", self.new_A.get_lower_level_abf(self)
		#print new_s.get_reward()-old_s.get_reward(), "reward",new_s.get_reward(),old_s.get_reward()
		update_H(self.solver.H,self.old_A,self.new_A,self,self.last_reward)#THIS R IS A BANDAID
		#print self.solver.H.R[self.policy_set.TA.identification][self.old_A.get_lower_level_abf(self)][self.policy_set.TA.LA.index], self.solver.H.N[self.policy_set.TA.identification][self.old_A.get_lower_level_abf(self)][self.policy_set.TA.LA.index]




	def predict_A(self):
		self.new_A.evolve_all(self.solver.H,self)

	def reset(self,s,val):
		self.x=self.map_size/2
		self.y=self.map_size/2
		self.policy_set=policy_root()
		self.old_A=Abstractions()
		self.new_A=Abstractions()
		self.battery=50
		self.old_A.update_all(s,self)
		self.new_A.update_all(s,self)
		#self.solver.write_file(self.solver.Q,self.solver.N,self.solver.Na,val)




	def death(self):
		print "dead"
		#self.x=randint(0,self.map_size-1)
		#self.y=randint(0,self.map_size-1)
		#self.battery=75


	def imprint(self, u):
		u.x=self.x
		u.y=self.y
		u.battery=self.battery
		u.time_away_from_network=self.time_away_from_network
		for i in range(len(Regions.region)):
			u.work_load[i]=self.work_load[i]



	def step(self,s,a_,time_to_work):	
		''''''		
		#self.solver.OnlinePlanning(self,s,a_,time_to_work)


	def check_trigger_high_level(self,s): 
		self.policy_set.TA.index=1
		if self.policy_set.TA.LA.check_trigger(self.new_A,self) is True:
			self.policy_set.TA.index==1
			self.policy_set.TA.LA=Policies.policy_low_level(self.solver.step(s,self)+1)

			self.policy_set.TA.LA.set_trigger(self.new_A,self)
			#print self.policy_set.TA.LA.trigger, "set"

			





	def decide(self,s):	
		self.new_A.update_all(s,self)
		#self.solver.step(s,self)
		self.check_trigger_high_level(s)
				
		
		action = self.policy_set.TA.LA.get_next_action(self,s)
		#print self.policy_set.TA.LA.index


		#self.work=self.policy_set.TA.LA.index-1
		self.execute(action,s)#NEED TO RESOLVE s


	def execute(self,action_,environment_data_):
		(x,y) = self.get_transition(action_,self.x,self.y,environment_data_.middle)
		
		base_r = environment_data_.get_reward()

		if environment_data_.check_boundaries((x,y)) is True:
			(self.x,self.y) = (x,y)

		self.measure(environment_data_,False)

		if self.battery < 1:
			self.death()

		self.last_reward= environment_data_.get_reward()- base_r

	

	def simulate_full(self,policy,s):
		base_reward= s.get_reward()
		r1=0
		complete=False
		count=0.

		while complete is False and self.battery >0:
			count+=1.
			action = policy.get_next_action(self,self.x,self.y,s)
			complete=action[1]
			(x,y) = self.get_transition(action[0],self.x,self.y,s.middle)

			if s.check_boundaries((x,y)) is True:
				(self.x,self.y) = (x,y)
			base_reward= s.get_reward()
			self.measure(s,True)

			r1+=math.pow(gamma,count-1)*(s.get_reward()-base_reward)
			base_reward=s.get_reward()

		if self.battery < 25:
			return (s,0,0,count)
		else:
			return (s,r1,0,count)

	def measure(self,mine_data_,imaginary):
		for i in range(-1,2):
			for j in range(-1,2):
				if self.work == Regions.get_region(self.x+i,self.y+j):
					mine_data_.measure_loc((self.x+i,self.y+j),imaginary)

	def get_transition(self,action,x,y,middle):
		self.time_away_from_network+=1		
		if self.x > self.map_size/2 - 10 and self.x < self.map_size/2 + 11:
			if self.y > self.map_size/2 - 10 and self.y < self.map_size/2 + 11:
				self.time_away_from_network=0
		


		if action != (0,0):
			self.add_battery(-.25)
			if self.battery <1:
				return (x,y)
		else:
			if (x,y)==middle:
				self.add_battery(5)
			#else:
				#self.add_battery(1)	


		return (x+action[0],y+action[1])


	def add_battery(self,num):
		self.battery+=num

		if self.battery <0:
			self.battery=0
		elif self.battery >100:
			self.battery=100
