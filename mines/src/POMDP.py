#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
from abstraction_classes import Abstractions
from Heuristics import heuristic
from sets import Set
import time
import Policies
from random import shuffle
H=250
gamma=.95

class Solver: 


	def __init__(self,E,e_args):
		self.N={}#{level_type:{state abstraction: num visited}}
		self.Na={}#{level_type:{state abstraction: {policy: num visited}}
		self.Q={}#{state abstraction:{policy:Expected Reward}}
		self.T=Set()
		self.H=heuristic()
		self.A=Abstractions()
		self.environment_data=E(e_args)



	def OnlinePlanning(self,agent_,s,a_,time_to_work):
		#self.print_n()
		#self.H.print_me()
		start = time.time()
		end = start
		agent_.imprint(a_)
		x=agent_.x
		y=agent_.y
		s.imprint(self.environment_data)
		while end - start < time_to_work:
			agent_.imprint(a_)
			s.imprint(self.environment_data)
			self.action_counter=0

			self.A.update_all(self.environment_data,a_)

			self.search_top(a_,self.A,0)
			end = time.time()

#	def rollout_top(self,a_,depth):
#		r1=0.
#		r2=0.
#		while depth<H and a_.battery > 1:
#			policy = a_.policy_set[1]
#			if a_.battery < 1:
#
#			r1+=gamma*r1_
#			r2+=gamma*r2_
#			
#			depth+=n
#
#		return (r1,r2)
#
#	def rollout_bottom(self,a_,depth):
#		r1=0.
#		r2=0.
#		while depth<H and a_.battery > 1:
#			policy = a_.policy_set[1]
#			if a_.battery < 1:
#				policy = a_.policy_set[1]
#
#			(s,r1_,r2_,n) = a_.simulate_full(policy,s)
#			r1+=gamma*r1_
#			r2+=gamma*r2_
#			
#			depth+=n
#
#		return (r1,r2)
	

	def search_top(self,a_,A,depth):
	
		if depth>H:
			return (0,1)

		elif a_.battery < 1:
			return (0,H-depth)
		else:

			abstraction = A.get_top_level_abf()

			if abstraction not in self.T:
				self.T.add(abstraction)#MOD
				self.append_dict(self.N,"root",abstraction,1)
#				return self.rollout(a_,depth,s)#MOD
			
			a_.policy_set.TA = a_.policy_set.policy_set[self.arg_max_ucb("root",abstraction,a_.policy_set)]
			a_.policy_set.TA.set_trigger(A)

			a_.policy_set.TA.LA = a_.policy_set.TA.LA=Policies.policy_low_level(self.arg_max_ucb(a_.policy_set.TA.index,abstraction,a_.policy_set.TA))

			a_.policy_set.TA.LA.set_trigger(A,a_)

			#print "UPPER LEVEL CHOSEN: ", a_.policy_set.TA.index

			r1,n = self.search_bottom(a_,A,depth)

			r1_,n2 = self.search_top(a_,A,depth+n)
			r1+=gamma*r1_
			#print r1


			self.append_dict(self.N,"root",abstraction,0.)
			self.append_dict(self.N,"root",abstraction,1.)

			self.append_dict2(self.Na,"root",abstraction,a_.policy_set.TA.index,0.)
			self.append_dict2(self.Na,"root",abstraction,a_.policy_set.TA.index,1.)

			self.append_dict2(self.Q,"root",abstraction,a_.policy_set.TA.index,0.)


			#if a_.policy_set.TA.index==0:
				#print "CHARGE BIG: ", n, a_.policy_set.TA.trigger, a_.policy_set.TA.LA.trigger
			self.append_dict2(self.Q,"root",abstraction,a_.policy_set.TA.index,(r1-(self.Q["root"][abstraction][a_.policy_set.TA.index]))/self.Na["root"][abstraction][a_.policy_set.TA.index])

				
			return r1,n+n2

	def search_bottom(self,a_,A,depth):
	
		if depth>H:
			return (0,1)

		elif a_.battery < 1:
			return (0,H-depth)
		else:

			abstraction =A.get_lower_level_abf(a_)

			if abstraction not in self.T:
				self.T.add(abstraction)#MOD
				self.append_dict(self.N,a_.policy_set.TA.index,abstraction,1)
			#	return self.rollout(a_,depth,s)

			if a_.policy_set.TA.LA.check_trigger(A,a_) is True:
				if a_.policy_set.TA.check_trigger(A) is True:
					return (0,1)
			else:
				a_.policy_set.TA.LA = a_.policy_set.TA.LA=Policies.policy_low_level(self.arg_max_ucb(a_.policy_set.TA.index,abstraction,a_.policy_set.TA))
				a_.policy_set.TA.LA.set_trigger(A,a_)
				#print "LOWER LEVEL CHOSEN: ", a_.policy_set.TA.LA.index


			#print a_.policy_set.TA.LA.trigger,a_.policy_set.TA.LA.index, "low"
			r = A.evolve_all(self.H,a_)
			#print r
			r1,n = self.search_bottom(a_,A,depth+1)

			r+=gamma*r1


			self.append_dict(self.N,a_.policy_set.TA.index,abstraction,0.)
			self.append_dict(self.N,a_.policy_set.TA.index,abstraction,1.)

			self.append_dict2(self.Na,a_.policy_set.TA.index,abstraction,a_.policy_set.TA.LA.index,0.)
			self.append_dict2(self.Na,a_.policy_set.TA.index,abstraction,a_.policy_set.TA.LA.index,1.)

			self.append_dict2(self.Q,a_.policy_set.TA.index,abstraction,a_.policy_set.TA.LA.index,0.)


			self.append_dict2(self.Q,a_.policy_set.TA.index,abstraction,a_.policy_set.TA.LA.index,(r-(self.Q[a_.policy_set.TA.index][abstraction][a_.policy_set.TA.LA.index]))/self.Na[a_.policy_set.TA.index][abstraction][a_.policy_set.TA.LA.index])
			print a_.policy_set.TA.index,abstraction,a_.policy_set.TA.LA.index,self.Na[a_.policy_set.TA.index][abstraction][a_.policy_set.TA.LA.index]

				
			return r,n+1.



	def append_dict(self,P,ab_action,hash1,r):
		if P.get(ab_action) is None:
			P[ab_action]={hash1:r}
		elif P[ab_action].get(hash1) is None:
			P[ab_action][hash1]=r
		else:
			P[ab_action][hash1]+=r

	def append_dict2(self,P,ab_action,hash1,hash2,r):
		if P.get(ab_action) is None:
			P[ab_action]={hash1:{hash2:r}}	
		elif P[ab_action].get(hash1) is None:
			P[ab_action][hash1]={hash2:r}
		elif P[ab_action][hash1].get(hash2) is None:
			P[ab_action][hash1][hash2]=r
		else:
			P[ab_action][hash1][hash2]+=r



	def arg_max(self,identification,abstraction):

		# returns index of best policy		
		if self.Q.get(identification) is not None:
			if self.Q[identification].get(abstraction) is not None:
				v = list(self.Q[identification][abstraction].values())
				k = list(self.Q[identification][abstraction].keys())
				#print "chose: ", k[v.index(max(v))], " with : :", max(v)
     				return k[v.index(max(v))]
			else:
				"ERROR"
				return 0
		else:
			"ERROR"
			return 0

	def explore_ucb(self,identification,abstraction,P):
		max=-1000
		policy_index = None
		total=0.
		


		if self.H.visits.get(identification) is not None:
			if self.H.visits[identification].get(abstraction) is not None:


				for k,v in self.H.visits[identification][abstraction].items():
					total+=v

				k = range(P.bottom,P.top)
				shuffle(k)
				for kz in k:
					if self.H.visits[identification][abstraction].get(kz) is None:
						#self.append_dict2(self.Q,identification,abstraction,kz,0.)
						#self.append_dict2(self.Na,identification,abstraction,kz,0.)
						#print "DID NOT FIND", identification, abstraction, kz
						print "ex: action", abstraction,kz
						return kz
					#else:
						#print "FOUND: ", kz-P.bottom
					if self.ucb(total,0,self.H.visits[identification][abstraction][kz]+1.) > max:
						max=self.ucb(total,0,self.H.visits[identification][abstraction][kz]+1.)
						policy_index = kz
			else:
				print "ex: abstraction", abstraction
				return 0
		else:
			print "ex: Identification", identification
			return 0

		return policy_index

	def arg_max_ucb(self,identification,abstraction,P):
		max=-1000
		policy_index = None

		


		if self.Q.get(identification) is not None:
			if self.Q[identification].get(abstraction) is not None:
				k = range(P.bottom,P.top)
				shuffle(k)
				for kz in k:
					if self.Q[identification][abstraction].get(kz) is None:
						self.append_dict2(self.Q,identification,abstraction,kz,0.)
						self.append_dict2(self.Na,identification,abstraction,kz,0.)
						#print "DID NOT FIND", identification, abstraction, kz
						return kz
					#else:
						#print "FOUND: ", kz-P.bottom
					if self.ucb(self.N[identification][abstraction],self.Q[identification][abstraction][kz],self.Na[identification][abstraction][kz]+1.) > max:
						max=self.ucb(self.N[identification][abstraction],self.Q[identification][abstraction][kz],self.Na[identification][abstraction][kz]+1.)
						policy_index = kz
			else:
				#print "RETURN DOUBLE EARLY"
				return 0
		else:
			#print "RETURN EARLY"
			return 0

		return policy_index



	def ucb(self,N,Q,Na):
		return Q+1000000.*math.sqrt(math.log(1+N)/(1+Na))





	def print_n(self):
		if self.Q.get(1) is not None:
			for ele in self.Q[1]:
				for ele2,v in self.Q[1][ele].items():
					print ele,ele2,v,self.N[1][ele]


