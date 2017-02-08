#!/usr/bin/env python

from ActionSpace import ActionSpace
from RewardPair import RewardPair
from Environment import Mines
#from Environment.Mines import Mine_Data
from random import randint
import random
from Agents import Action_Definition
from Supple_Tree import supple_tree
import time
import xxhash
from sets import Set

import math
import numpy as np


class Solver: 


	def __init__(self,max_depth_,depth_,Gamma_,upper_confidence_c_,action_space_num_,E,e_args):

		self.upper_confidence_c=upper_confidence_c_		
		self.action_space_num=action_space_num_
		self.supple_tree=supple_tree()
		self.N = {} #th
		self.Na= {}
		self.Q = {}

		self.Ni= {}
		self.Nai={}
		self.Qi ={}
		self.Q_Guess={}

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
		self.History_Tree=Set([])
		


	def GetGreedyPrimitive(self,t,h,s,abf,sb):

		if t[2] == "Primitive":
			return t
		else:
			a_star= self.arg_max(t,h,s,abf,sb)

			return self.GetGreedyPrimitive(a_star,h,s,abf,sb)

	def GetPrimitive(self,t,h,s,sb):
		if t[2] == "Primitive":
			return t
		else:
			a = random.choice(sb(s,t[3]))
			return self.GetPrimitive(a,h,s,sb)

	
	
	def OnlinePlanning(self,root_task,T,agent_,environment_data_,num_steps_,a_,abstractions,time_to_work):


		start = time.time()
		end = start
		self.counter=0
		while end - start < time_to_work:
			agent_.imprint(a_)
			environment_data_.imprint(self.environment_data)
			self.counter=0
			self.search(a_,root_task,self.environment_data,a_.get_history(),0,T,abstractions.abf,abstractions.get_sub_tasks)
			end = time.time()

		if time_to_work>0: 
			self.Q_Guess=self.supple_tree.step(self.History_Tree,self.Ni,self.Qi,self.Nai)

		a =self.GetGreedyPrimitive(root_task,agent_.get_history(),environment_data_,abstractions.abf,abstractions.get_sub_tasks)
		

		
		return a



	def arg_max(self,t,h,s,abf,sb):
		a_star = 0
		max= -1
		c=0

		for a in sb(s,t[3]):

				
				if self.in_dict(self.Q,(self.h_it(t[0]+t[1]),h,self.h_it(a[0]+a[1]))) == True:
					c+=1

					if self.Q.get(self.h_it(t[0]+t[1])).get(h).get(self.h_it(a[0]+a[1])) > max:
						a_star=a
						max=self.Q.get(self.h_it(t[0]+t[1])).get(h).get(self.h_it(a[0]+a[1]))


		if c == 0:
			for a in sb(s,t[3]):	
				if self.in_dict(self.Q_Guess,(self.h_it(t[0]+t[1]),abf(s),self.h_it(a[0]+a[1]))) == True:
					c+=1
					if self.Q_Guess.get(self.h_it(t[0]+t[1])).get(abf(s)).get(self.h_it(a[0]+a[1])) > max:
						a_star=a
						max=self.Q_Guess.get(self.h_it(t[0]+t[1])).get(abf(s)).get(self.h_it(a[0]+a[1]))

		if c==0:
			a_star=random.choice(sb(s,t[3]))

		return a_star



	def arg_max_ucb(self,t,h,s,abf,sb):
		a_star = 0
		max= -1

		for a in sb(s,t[3]):

			if self.in_N(self.h_it(t[0]+t[1]),h,False) == False:
				return a

			if self.in_Na(self.h_it(t[0]+t[1]),h,self.h_it(a[0]+a[1])) == False:
				return a 

			if self.in_Q(self.h_it(t[0]+t[1]),h,self.h_it(a[0]+a[1])) == False:
				return a

			if self.Q.get(self.h_it(t[0]+t[1])).get(h).get(self.h_it(a[0]+a[1])) + self.c*math.sqrt(math.log(1+self.N.get(self.h_it(t[0]+t[1])).get(h))/(1+self.Na.get(self.h_it(t[0]+t[1])).get(h).get(self.h_it(a[0]+a[1]))))  > max:
				a_star=a
				max=self.Q.get(self.h_it(t[0]+t[1])).get(h).get(self.h_it(a[0]+a[1])) + self.c*math.sqrt(math.log(1+self.N.get(self.h_it(t[0]+t[1])).get(h))/(1+self.Na.get(self.h_it(t[0]+t[1])).get(h).get(self.h_it(a[0]+a[1]))))


		return a_star

	def put_in_N(self,t,h,n):
		if self.N.get(t) is None:
			self.N[t]={h:n}
		elif self.N.get(t).get(h) is None:
			self.N[t][h]=n
		else:
			self.N[t][h]+=n

	def in_N(self,t,h,pr):
		if self.N.get(t) is None:
			return False
		elif self.N.get(t).get(h) is None:
			return False
		return True

	def put_in_Na(self,t,h,a,n):
		if self.Na.get(t) is None:
			self.Na[t]={h:{a:n}}
		elif self.Na.get(t).get(h) is None:
			self.Na[t][h]={a:n}
		elif self.Na.get(t).get(h).get(a) is None:
			self.Na[t][h][a]=n
		else:
			self.Na[t][h][a]+=n 

	def in_Na(self,t,h,a):
		if self.Na.get(t) is None:
			return False
		elif self.Na.get(t).get(h) is None:
			return False
		elif self.Na.get(t).get(h).get(a) is None:
			return False
		return True

	def in_Q(self,t,h,a):
		if self.Q.get(t) is None:
			return False

		elif self.Q.get(t).get(h) is None:
			return False

		elif self.Q.get(t).get(h).get(a) is None:
			return False
		return True

	def put_in_Q(self,t,h,a,r):
		if self.Q.get(t) is None:
			self.Q[t]={h:{a:r}}
		elif self.Q.get(t).get(h) is None:
			self.Q[t][h]={a:r}
		elif self.Q.get(t).get(h).get(a) is None:
			self.Q[t][h][a]=r
		else:
			self.Q[t][h][a] = self.Q.get(t).get(h).get(a) + (r-self.Q.get(t).get(h).get(a))/self.Na.get(t).get(h).get(a)

	def in_dict(self,N,k):
		if len(k) > 1:
			if N.get(k[0]) is None:
				return False
			return self.in_dict(N[k[0]],k[1:])
		else:
			if N.get(k[0]) is None:
				return False
			else:
				return True	
			





			

	def search(self,a_,t,s,h,d,T,abf,sb):

		iteration_index=self.counter
		self.counter+=1
		s.imprint(self.s_[iteration_index][0])



		if t[2] == "Primitive":
			(self.sTemp,r) = a_.simulate(t,self.s_[iteration_index][0])
			self.sTemp.imprint(self.s_[iteration_index][1])
			x = abf(self.s_[iteration_index][1])
			return (r,1,self.h_it(h+self.h_it(t[0]+t[1])+x),self.s_[iteration_index][1])
		else:
			if d>=self.H or t[1] == abf(self.s_[iteration_index][0]):

				if t[1] == abf(self.s_[iteration_index][0]):
					return (0,0,h,self.s_[iteration_index][0])
				return (0,0,h,self.s_[iteration_index][0])
			else:
				self.pre_hash_key= self.h_it(self.h_it(t[0]+t[1])+h) 
				if  self.pre_hash_key not in T:
					T[self.pre_hash_key] = 1
					return self.rollout(a_, t,self.s_[iteration_index][0],h,d,abf,sb)
				else:
					a_star = self.arg_max_ucb(t,h,self.s_[iteration_index][0],abf,sb)

					(r1,n1,h1,self.sTemp)= self.search(a_,a_star,self.s_[iteration_index][0],h,d,T,abf,sb)
					self.sTemp.imprint(self.s_[iteration_index][1])

					(r2,n2,h2,self.sTemp)= self.search(a_,t,self.s_[iteration_index][1],h1,d+n1,T,abf,sb)
					self.sTemp.imprint(self.s_[iteration_index][2])
					


					self.put_in_N(self.h_it(t[0]+t[1]),h,1.)
					self.append_dict(self.Ni,(self.h_it(t[0]+t[1]),abf(self.s_[iteration_index][0])),1.)
					self.put_in_Na(self.h_it(t[0]+t[1]),h,self.h_it(a_star[0]+a_star[1]),1.)
					self.append_dict(self.Nai,(self.h_it(t[0]+t[1]),abf(self.s_[iteration_index][0]),self.h_it(a_star[0]+a_star[1])),1.)
					r= r1+math.pow(self.Gamma,n1)*r2

					self.History_Tree.add((t,h,a_star,abf(self.s_[iteration_index][0])))#{t,h,a,s,next}
					self.append_dict_Q(self.Qi,self.Nai,(self.h_it(t[0]+t[1]),abf(self.s_[iteration_index][0]),self.h_it(a_star[0]+a_star[1])),r)
					self.put_in_Q(self.h_it(t[0]+t[1]),h,self.h_it(a_star[0]+a_star[1]),r) 

					
					return (r,n1+n2,h2,self.s_[iteration_index][2])


	def append_dict(self, N, k,r):
		if len(k) > 1:
			if N.get(k[0]) is None:
				N[k[0]] = {}
			self.append_dict(N[k[0]],k[1:],r)
		else:
			if N.get(k[0]) is None:
				N[k[0]]=r
			else:
				N[k[0]]+=r

	def append_dict_Q(self, N, Na, k,r):
		if len(k) > 1:
			if N.get(k[0]) is None:
				N[k[0]] = {}
			self.append_dict_Q(N[k[0]],Na[k[0]],k[1:],r)
		else:
			if N.get(k[0]) is None:
				N[k[0]]=r
			else:
				N[k[0]]+=(r-N[k[0]])/(Na[k[0]])
			




	def h_it(self,string):
		return xxhash.xxh64(string).hexdigest()

	def rollout(self, a_, t, s, h, d, abf,sb):

		s0 = self.E(self.e_args)
		s1 = self.E(self.e_args)
		s2 = self.E(self.e_args)

		s.imprint(s0)

		if d>= self.H or t[1] is abf(s0):
			return (0,0,h,s0)
		else:
			a = self.GetPrimitive(t,h,s,sb)
			(self.sTemp,r1) = a_.simulate(a,s0)
			self.sTemp.imprint(s1)
			x = abf(s1)
			(r2,n,h2,self.sTemp) = self.rollout(a_,t,s1,self.h_it(h+self.h_it(t[0]+t[1])+x),d+1,abf,sb)
			self.sTemp.imprint(s2)
			r = r1 + self.Gamma * r2
			return (r,n+1,h2,s2)




		for i in range(0, num_steps):
			base_reward = environment_data_.get_reward()
			agent_.simulate(randint(0,agent_.get_action_size()),s)
			self.reward_list.append(environment_data_.get_reward()-base_reward)
			


