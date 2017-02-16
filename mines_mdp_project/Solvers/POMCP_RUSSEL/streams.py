#!/usr/bin/env python

from ActionSpace import ActionSpace
from RewardPair import RewardPair
from Environment import Mines
from Environment.Mines import Location
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


def abf(policy,x,y,battery,s):
	score=0.
	ms=50
	for (i,j) in policy.macro_set:
		if s.check_boundaries(Location(x+i,y+j)) == True:
			if bool(s.seen[x+i][y+j]) == False:
				score+=1.	


	x,y = get_next(x,y,policy.action_string)

	if policy.index ==1 and (x,y) == s.middle:
		battery+=policy.num_steps*5
		if battery > 100:
			battery =100

	if policy.index != 1:
		battery-=policy.num_steps

	dist = math.sqrt(math.fabs(x-ms)*math.fabs(x-ms)+math.fabs(y-ms)*math.fabs(y-ms))
	
	#dist2= 0
	#for (x_,y_) in others:
	#	if (math.sqrt(math.fabs(x-x_)*math.fabs(x-x_)+math.fabs(y-y_)*math.fabs(y-y_)) < 20):
	#		dist2=20

	if battery < 10:
		score =0.

	print score, policy.index
	return int(score/float(policy.num_steps)),(-dist), 0
		

def hash_(string):
	return xxhash.xxh64(string).hexdigest()


def get_next(x,y,action):
	for a in action:
		x+=a[0]
		y+=a[1]

	return x,y



class Solver: 


	def __init__(self,E,e_args):
		self.N={}#{state abstraction: num visited}
		self.Na={}#{state abstraction: {policy: num visited}}
		self.Q={}#{state abstraction:{policy:Expected Reward}}
		self.T=Set()

		self.counter=0
		self.environment_data=E(e_args)
		self.last_reward=0
		self.last_reward2=0
		self.action_counter=0

	def GetGreedyPrimitive(self,x,y,direction,s,lvl,alpha):
		(a,m) = self.arg_max(x,y,direction,s,lvl, alpha)
		t = task(a,direction,lvl,(x,y))
		return t






	def get_new_macro(self,loc,s,alpha,battery,policy_set):
		max=-1000
		x=loc[0]
		y=loc[1]
		for a_1 in policy_set:
			x=loc[0]
			y=loc[1]
			r1,r2,r3=abf(a_1,x,y,battery,s)
			r=r1*alpha[0] + r2*alpha[1]+ r3*alpha[2]
			x,y=get_next(x,y,a_1.action_string)
			for a_2 in policy_set:
				r1,r2,r3=abf(a_2,x,y,battery,s)
				r+=.3*(r1*alpha[0] + r2*alpha[1] + r3*alpha[2])
				x,y=get_next(x,y,a_2.action_string)
				for a_3 in policy_set:
					r1,r2,r3=abf(a_3,x,y,battery,s)
					r+=.09*(r1*alpha[0] + r2*alpha[1] + r3*alpha[2])

					if r > max:
						a_=a_1
						max=r

		return a_
	
	def OnlinePlanning(self,agent_,environment_data_,a_,time_to_work, top):
		level=top
		start = time.time()
		end = start
		agent_.imprint(a_)
		#self.print_n()
		x=agent_.x
		y=agent_.y
		environment_data_.imprint(self.environment_data)
		while end - start < time_to_work:
			agent_.imprint(a_)
			environment_data_.imprint(self.environment_data)
			self.counter=0
			#rint "start"
			self.action_counter=0
			self.search(a_,random.choice(top_level_choices),level,self.environment_data)
			end = time.time()



	

	def search(self,a_,depth,s):


		if depth>20:
			return (0,0)
		else:

			abstraction =abf(direction,a_.get_x(),a_.get_y(),s,level)#*
			if abstraction not in self.T:
				self.T.add(abstraction)
				self.append_dict(self.N,level,abstraction,1)
				return self.rollout(a_,depth,s)
			else:
				policy = self.arg_max_ucb(abstraction,a_.policy_set)
				(s,r1,r2) = a_.simulate_full(policy,s)
				r1_,r2_ = self.search(a_,depth+policy.num_steps,s)
				r1+=.95*r1_
				r2+=.95*r2_


			self.append_dict(self.N,abstraction,0)
			self.append_dict(self.N,abstraction,1)

			self.append_dict2(self.Na,abstraction,policy.index,0)
			self.append_dict2(self.Na,abstraction,policy.index,1)

			self.append_dict2(self.Q,abstraction,policy.index,0)
			self.append_dict2(self.Q,abstraction,policy.index,(r1-self.Q[abstraction][policy.index])/self.Na[abstraction][policy.index])

					
			return (r1,r2)



	def append_dict(self,P,hash1,r):
		if P.get(hash1) is None:
			P[hash1]=r
		else:
			P[hash1]+=r

	def append_dict_2(self,P,hash1,hash2,r):
		if P.get(hash1) is None:
			P[hash1]={hash2:r}
		elif P[hash1].get(s) is None:
			P[hash1][hash2]=r
		else:
			P[hash1][hash2]+=r



	def arg_max(self,abstraction):

		# returns index of best policy		
		if self.Q[abstraction] is not None:
			v = list(self.Q[abstraction].values())
			k = list(self.Q[abstraction].keys())

     			return k[v.index(max(v))]
		else:
			"ERROR"

	def arg_max_ucb(self,abstraction):
		max=-1000
		policy_index = None

		if self.Q[abstraction] is not None:
			v = list(self.Q[abstraction].values())
			k = list(self.Q[abstraction].keys())

			for kz in k:
				if self.ucb(self.N[abstraction],self.Q[Abstraction][kz],self.Na[abstraction][kz]) > max:
					max=self.ucb(self.N[abstraction],self.Q[Abstraction][kz],self.Na[abstraction][kz])
					policy_index = kz

		return policy_index

	def ucb(self,N,Q,Na):
		return Q+100.*math.sqrt(math.log(1+N)/(1+Na))





	def print_n(self):
		for ele in self.N:

			for ele2 in self.N[ele]:
				print ele,ele2,self.N[ele][ele2]
				print ele,ele2,self.Q[ele][ele2]
				print ele,ele2,self.Q2[ele][ele2]

	


