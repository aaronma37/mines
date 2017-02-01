#!/usr/bin/env python

from ActionSpace import ActionSpace
from RewardPair import RewardPair
from Environment import Mines
from Environment.Mines import Mine_Data
from random import randint
import random
from Agents import Action_Definition

import time
import xxhash

import math
import numpy as np


class Solver: 


	def __init__(self,max_depth_,depth_,Gamma_,upper_confidence_c_,action_space_num_,map_size_):

		self.upper_confidence_c=upper_confidence_c_		
		self.action_space_num=action_space_num_

		self.N = {}
		self.Na= {}
		self.Q = {}


		self.max_depth=max_depth_
		self.reward_list=[]
		self.environment_data =Mine_Data(map_size_)#
		self.Gamma=Gamma_
		self.H=20
		self.c=15.
		self.history_length=32

	def GetGreedyPrimitive(self,t,h,s,abf):
		if t.get_primitive() is True:
			return t
		else:
			a_star= self.arg_max(t,h,s,abf)
			return self.GetGreedyPrimitive(a_star,h,s,abf)

	def GetPrimitive(self,t,h):
		if t.get_primitive() is True:
			return t
		else:
			a = random.choice(t.get_sub_tasks())
			return self.GetPrimitive(a,h)

	
	
	def OnlinePlanning(self,root_task,T,agent_,environment_data_,num_steps_,a_,abf):

		#print "SEEN", self.N.get(self.hash_generator_1(root_task,agent_.get_history()))
		#print agent_.get_history()
		for i in range(0, num_steps_):
			agent_.imprint(a_)
			environment_data_.imprint(self.environment_data)

			self.search(a_,root_task,self.environment_data,a_.get_history(),0,T,abf)

		a =self.GetGreedyPrimitive(root_task,agent_.get_history(),environment_data_,abf)
		
		return a



	def arg_max(self,t,h,s,abf):
		a_star = t.get_sub_tasks()[0]
		max= -1
		c=0
		#print "finding best choice in" , t.get_message()

		for a in t.get_sub_tasks():



			if a.available(abf(s)) is True:
				c+=1
 
				if self.hash_generator_2(t,h,a) not in self.Q.keys():
					self.Q[self.hash_generator_2(t,h,a)]=0.

				if self.Q.get(self.hash_generator_2(t,h,a)) > max:
					a_star=a
					max=self.Q.get(self.hash_generator_2(t,h,a)) 


		if c is 0:
			print "NO OPTIONS"
		return a_star

	def arg_max_ucb(self,t,h,s,abf):
		a_star = t.get_sub_tasks()[0]

		if self.hash_generator_1(t,h) not in self.N.keys():
			self.N[self.hash_generator_1(t,h)]=0.

		if self.hash_generator_2(t,h,a_star) not in self.Q.keys():
			self.Q[self.hash_generator_2(t,h,a_star)]=0.

		if self.hash_generator_2(t,h,a_star) not in self.Na.keys():
			self.Na[self.hash_generator_2(t,h,a_star)]=0.



		max= -1

		


		for a in t.get_sub_tasks():

			if a.available(abf(s)) is True:
				if self.hash_generator_2(t,h,a) not in self.Q.keys():
					self.Q[self.hash_generator_2(t,h,a)]=0.

				if self.hash_generator_2(t,h,a) not in self.Na.keys():
					self.Na[self.hash_generator_2(t,h,a)]=0.

				if self.Na[self.hash_generator_2(t,h,a)] is 0.:
					return a

			
				if self.Q.get(self.hash_generator_2(t,h,a)) + self.c*math.sqrt(math.log(1+self.N.get(self.hash_generator_1(t,h)))/(1+self.Na.get(self.hash_generator_2(t,h,a))))  > max:
					a_star=a
					max=self.Q.get(self.hash_generator_2(t,h,a)) + self.c*math.sqrt(math.log(1+self.N.get(self.hash_generator_1(t,h)))/(1+self.Na.get(self.hash_generator_2(t,h,a))))



		#print self.N.get(self.hash_generator_1(t,h)), t.get_hierarchy(),self.hash_generator_1(t,h)
		return a_star



			

	def search(self,a_,t,s,h,d,T,abf):
		s0 = Mine_Data(s.map_size)
		s1 = Mine_Data(s.map_size)
		s2 = Mine_Data(s.map_size)


		s.imprint(s0)

		if t.get_primitive() is True:
			(sTemp,r) = a_.simulate(t,s0)
			sTemp.imprint(s1)
			x = abf(s1)
			return (r,1,xxhash.xxh64(h+t.get_hash()+x).hexdigest(),s1)
		else:
			if d>=self.H or t.check_termination(abf(s)) is True:

				if t.check_termination(abf(s)) is True:
					#print t.get_message(), " completed"
					return (0,0,h,s0)
				return (0,0,h,s0)
			else:
				self.pre_hash_key= self.hash_generator_1(t,h)
				if  self.pre_hash_key not in T:
					T[self.pre_hash_key] = 1
					return self.rollout(a_, t,s0,h,d,abf)
				else:
					a_star = self.arg_max_ucb(t,h,s0,abf)
					(r1,n1,h1,sTemp)= self.search(a_,a_star,s0,h,d,T,abf)
					sTemp.imprint(s1)
					#print "h",h
					if len(h)>25:
						print t.get_message()
						print a_.get_history()
						print d
					#print "h1",h1
					(r2,n2,h2,sTemp2)= self.search(a_,t,s1,h1,d+n1,T,abf)
					sTemp2.imprint(s2)
					


					if self.hash_generator_1(t,h) in self.N:
						self.N[self.hash_generator_1(t,h)] +=1.0
					else:
						self.N[self.hash_generator_1(t,h)] = 1.0


					if self.hash_generator_2(t,h,a_star) in self.Na:
						self.Na[self.hash_generator_2(t,h,a_star)] +=1.0
					else:
						self.Na[self.hash_generator_2(t,h,a_star)] = 1.0

					
					#print self.Na[self.hash_generator_2(t,abf(s),a_star)]

					r= r1+math.pow(self.Gamma,n1)*r2

					if self.hash_generator_2(t,h,a_star) in self.Q:
               					self.Q[self.hash_generator_2(t,h,a_star)] = self.Q[self.hash_generator_2(t,h,a_star)] + (r-self.Q[self.hash_generator_2(t,h,a_star)])/self.Na[self.hash_generator_2(t,h,a_star)]
					else:
						self.Q[self.hash_generator_2(t,h,a_star)] = r

					
					return (r,n1+n2,h2,s2)




	def rollout(self, a_, t, s, h, d, abf):

		s0 = Mine_Data(s.map_size)
		s1 = Mine_Data(s.map_size)
		s2 = Mine_Data(s.map_size)

		s.imprint(s0)

		if d>= self.H or t.check_termination(abf(s0)) is True:
			return (0,0,h,s0)
		else:
			a = self.GetPrimitive(t,h)
			(sTemp1,r1) = a_.simulate(a,s0)
			sTemp1.imprint(s1)
			x = abf(s1)
			(r2,n,h2,sTemp2) = self.rollout(a_,t,s1,xxhash.xxh64(h+a.get_hash()+x).hexdigest(),d+1,abf)
			sTemp2.imprint(s2)
			r = r1 + self.Gamma * r2
			return (r,n+1,h2,s2)




		for i in range(0, num_steps):
			base_reward = environment_data_.get_reward()
			agent_.simulate(randint(0,agent_.get_action_size()),s)
			self.reward_list.append(environment_data_.get_reward()-base_reward)
			
	

	def hash_generator_1(self,t,h):
		return t.get_hash()+h

	def hash_generator_2(self,t,h,a):
		return t.get_hash()+h+a.get_hash()


	#def hash_generator(self, agent_, environment_data_):	
		#self.pre_result = 1
		
		#self.pre_result = self.pre_result*self.pre_prime + environment_data_.get_hash()
		#self.pre_result = self.pre_result*self.pre_prime + agent_.get_hash()
		#self.pre_result = self.pre_result*self.pre_prime + agent_.get_hash_history()
		
		#return environment_data_.get_hash()+agent_.get_hash()+ agent_.get_hash_history()

	def hash_generator_without_history(self, agent_, environment_data_):	
		#self.pre_result = 1
		
		#self.pre_result = self.pre_result*self.pre_prime + environment_data_.get_hash()
		#self.pre_result = self.pre_result*self.pre_prime + agent_.get_hash()

		return environment_data_.get_hash()+agent_.get_hash()


