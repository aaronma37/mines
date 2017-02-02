#!/usr/bin/env python

from ActionSpace import ActionSpace
from RewardPair import RewardPair
from Environment import Mines
#from Environment.Mines import Mine_Data
from random import randint
import random
from Agents import Action_Definition

import time
import xxhash

import math
import numpy as np


class Solver: 


	def __init__(self,max_depth_,depth_,Gamma_,upper_confidence_c_,action_space_num_,E,e_args):

		self.upper_confidence_c=upper_confidence_c_		
		self.action_space_num=action_space_num_

		self.N = {} #th
		self.Na= {}
		self.Q = {}

		self.s_ = np.ndarray(shape=(100,3), dtype=object)
		for i in range(100):
			for j in range(3):
				self.s_[i][j] = E(e_args)
			
		self.sTemp= E(e_args)

		self.max_depth=max_depth_
		self.reward_list=[]
		self.environment_data =E(e_args)
		self.Gamma=Gamma_
		self.H=20
		self.c=15.
		self.E=E
		self.e_args=e_args
		self.counter=0


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

	
	
	def OnlinePlanning(self,root_task,T,agent_,environment_data_,num_steps_,a_,abf,time_to_work):


		start = time.time()
		end = start
		self.counter=0
		while end - start < time_to_work:
			agent_.imprint(a_)
			environment_data_.imprint(self.environment_data)
			self.counter=0
			self.search(a_,root_task,self.environment_data,a_.get_history(),0,T,abf)
			end = time.time()

		#time.sleep(1)
		if self.in_N(root_task,agent_.get_history(),True) is True:
			print self.in_N(root_task,agent_.get_history(),True)
			print "visited ", self.N.get(root_task.get_hash()).get(agent_.get_history())
			

		
		a =self.GetGreedyPrimitive(root_task,agent_.get_history(),environment_data_,abf)
		print a.get_message()
				

		return a



	def arg_max(self,t,h,s,abf):
		a_star = t.get_sub_tasks()[0]
		max= -1
		c=0
		#print "finding best choice in" , t.get_message()

		for a in t.get_sub_tasks():

			if a.available(abf(s)) is True:
				c+=1

				if self.in_Q(t,h,a) is True:


					if self.Q.get(t.get_hash()).get(h).get(a.get_hash()) > max:
						a_star=a
						max=self.Q.get(t.get_hash()).get(h).get(a.get_hash())


		if c is 0:
			print "NO OPTIONS"

		
		return a_star



	def arg_max_ucb(self,t,h,s,abf):
		a_star = t.get_sub_tasks()[0]

		#self.put_in_N(t,h,self.N,0.)
		#self.put_in_Na(t,h,a_star,self.Na,0.)

		max= -1

		for a in t.get_sub_tasks():

			if a.available(abf(s)) is True:

				#self.put_in_Na(t,h,a,self.Na,0.)

				if self.in_N(t,h,False) is False:
					return a

				if self.in_Na(t,h,a) is False:
					return a 

				if self.in_Q(t,h,a) is False:
					return a

				if self.Q.get(t.get_hash()).get(h).get(a.get_hash()) + self.c*math.sqrt(math.log(1+self.N.get(t.get_hash()).get(h))/(1+self.Na.get(t.get_hash()).get(h).get(a.get_hash())))  > max:
					a_star=a
					max=self.Q.get(t.get_hash()).get(h).get(a.get_hash()) + self.c*math.sqrt(math.log(1+self.N.get(t.get_hash()).get(h))/(1+self.Na.get(t.get_hash()).get(h).get(a.get_hash())))


		return a_star

	def put_in_N(self,t,h,n):
		if self.N.get(t.get_hash()) is None:
			self.N[t.get_hash()]={h:n}
		elif self.N.get(t.get_hash()).get(h) is None:
			self.N[t.get_hash()][h]=n
		else:
			self.N[t.get_hash()][h]+=n

	def in_N(self,t,h,pr):
		if self.N.get(t.get_hash()) is None:
			return False
		elif self.N.get(t.get_hash()).get(h) is None:
			return False
		return True

	def put_in_Na(self,t,h,a,n):
		if self.Na.get(t.get_hash()) is None:
			self.Na[t.get_hash()]={h:{a.get_hash():n}}
		elif self.Na.get(t.get_hash()).get(h) is None:
			self.Na[t.get_hash()][h]={a.get_hash():n}
		elif self.Na.get(t.get_hash()).get(h).get(a.get_hash()) is None:
			self.Na[t.get_hash()][h][a.get_hash()]=n
		else:
			self.Na[t.get_hash()][h][a.get_hash()]+=n 

	def in_Na(self,t,h,a):
		if self.Na.get(t.get_hash()) is None:
			return False
		elif self.Na.get(t.get_hash()).get(h) is None:
			return False
		elif self.Na.get(t.get_hash()).get(h).get(a.get_hash()) is None:
			return False
		return True

	def in_Q(self,t,h,a):
		if self.Q.get(t.get_hash()) is None:
			return False

		elif self.Q.get(t.get_hash()).get(h) is None:
			return False

		elif self.Q.get(t.get_hash()).get(h).get(a.get_hash()) is None:
			return False
		return True

	def put_in_Q(self,t,h,a,r):
		if self.Q.get(t.get_hash()) is None:
			self.Q[t.get_hash()]={h:{a.get_hash():r}}
		elif self.Q.get(t.get_hash()).get(h) is None:
			self.Q[t.get_hash()][h]={a.get_hash():r}
		elif self.Q.get(t.get_hash()).get(h).get(a.get_hash()) is None:
			self.Q[t.get_hash()][h][a.get_hash()]=r
		else:
			self.Q[t.get_hash()][h][a.get_hash()] = self.Q.get(t.get_hash()).get(h).get(a.get_hash()) + (r-self.Q.get(t.get_hash()).get(h).get(a.get_hash()))/self.Na.get(t.get_hash()).get(h).get(a.get_hash())
			





			

	def search(self,a_,t,s,h,d,T,abf):


		iteration_index=self.counter
		self.counter+=1



		s.imprint(self.s_[iteration_index][0])
		#s.imprint(self.s_[iteration_index][1])
		#s.imprint(self.s_[iteration_index][2])


		if t.get_primitive() is True:
			(self.sTemp,r) = a_.simulate(t,self.s_[iteration_index][0])
			self.sTemp.imprint(self.s_[iteration_index][1])
			x = abf(self.s_[iteration_index][1])
			return (r,1,xxhash.xxh64(h+t.get_hash()+x).hexdigest(),self.s_[iteration_index][1])
		else:
			if d>=self.H or t.check_termination(abf(self.s_[iteration_index][0])) is True:

				if t.check_termination(abf(self.s_[iteration_index][0])) is True:
					return (0,0,h,self.s_[iteration_index][0])
				return (0,0,h,self.s_[iteration_index][0])
			else:
				self.pre_hash_key= self.hash_generator_1(t,h)
				if  self.pre_hash_key not in T:
					T[self.pre_hash_key] = 1
					return self.rollout(a_, t,self.s_[iteration_index][0],h,d,abf)
				else:
					a_star = self.arg_max_ucb(t,h,self.s_[iteration_index][0],abf)

					(r1,n1,h1,self.sTemp)= self.search(a_,a_star,self.s_[iteration_index][0],h,d,T,abf)
					self.sTemp.imprint(self.s_[iteration_index][1])

					(r2,n2,h2,self.sTemp)= self.search(a_,t,self.s_[iteration_index][1],h1,d+n1,T,abf)
					self.sTemp.imprint(self.s_[iteration_index][2])
					


					self.put_in_N(t,h,1.)
					self.put_in_Na(t,h,a_star,1.)

					r= r1+math.pow(self.Gamma,n1)*r2

					self.put_in_Q(t,h,a_star,r) 

					
					return (r,n1+n2,h2,self.s_[iteration_index][2])




	def rollout(self, a_, t, s, h, d, abf):

		s0 = self.E(self.e_args)
		s1 = self.E(self.e_args)
		s2 = self.E(self.e_args)

		s.imprint(s0)

		if d>= self.H or t.check_termination(abf(s0)) is True:
			return (0,0,h,s0)
		else:
			a = self.GetPrimitive(t,h)
			(self.sTemp,r1) = a_.simulate(a,s0)
			self.sTemp.imprint(s1)
			x = abf(s1)
			(r2,n,h2,self.sTemp) = self.rollout(a_,t,s1,xxhash.xxh64(h+a.get_hash()+x).hexdigest(),d+1,abf)
			self.sTemp.imprint(s2)
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


