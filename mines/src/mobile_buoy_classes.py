#!/usr/bin/env python

from random import randint
from mobile_buoy_environment import Mobile_Buoy_Environment
import time
import math
from sets import Set
from geometry_msgs.msg import PoseStamped
import numpy as np

## To do.  Make reward based on Reward function that is learned heuristically
## To do.  Make transition based on Transition function that is learned heuristically


zone = (((0,5),(-1,2)),((-4,1),(-1,2)),((-1,2),(-4,1)),((-1,2),(0,5)) )
region = [(10,10),(10,30),(10,50),(10,70),(10,90),(30,10),(50,10),(70,10),(90,10),(30,30),(50,30),(70,30),(90,30),(30,50),(50,50),(70,50),(90,50),(30,70),(50,70),(70,70),(90,70),(30,90),(50,90),(70,90),(90,90)]

region_size=10

greedy_regions = [(1,1),(-1,1),(-1,-1),(1,-1), (0,1), (1,0), (0,-1), (-1,0)]

policy_set_size=25
H=50
gamma=.95



def abf(a,s):

	# region scores
	h="h"

	for i in range(len(region)):
		if s.score[i] > 50:
			h=h+str(3)+":"
		elif s.score[i] > 25:
			h=h+str(2)+":"	
		elif s.score[i] > 0:
			h=h+str(1)+":"	
		else:
			h=h+str(0)+":"

	#for i in range(len(region)):
	#	if a.worked[i] > 1:
	#		h=h+str(2)+":"	
	#	elif a.worked[i] > 0:
	#		h=h+str(1)+":"	
	#	else:
	#		h=h+str(0)+":"	


	h=h+str(get_region(a.x,a.y))+":"
	return h

def get_region(x,y):
	for i in range(len(region)):
		if x > region[i][0]-region_size-1 and x < region[i][0] + region_size + 1:
			if y > region[i][1]-region_size-1 and y < region[i][1] + region_size + 1:
				return i

def get_next(x,y,action):
	for a in action:
		x+=a[0]
		y+=a[1]

	return x,y

class policy:
	def __init__(self,index):
		self.index=index

	
		self.num_steps=1000
		self.counter=0
	
	def reset(self):
		self.counter=0
			

	def get_next_action(self,a):
		next_x=0
		next_y=0
		self.counter+=1


		if self.index>0 and self.index < 25:
						##RETURN TO SHIP	
			if a.x < region[self.index][0]:
				next_x = 1
			elif a.x > region[self.index][0]:
				next_x = -1

			if a.y < region[self.index][1]:
				next_y= 1
			elif a.y > region[self.index][1]:
				next_y=-1

			if a.x is region[self.index][0] and a.y is region[self.index][1]:
				self.reset()
				return ((0,0),True)
			else:	
				return ((next_x,next_y),False)
		elif self.index==25:
			return ((0,0),True) 
		else:
			return ((0,0),True) 



class Solver: 


	def __init__(self,E,e_args):
		self.N={}#{state abstraction: num visited}
		self.Na={}#{state abstraction: {policy: num visited}}
		self.Q={}#{state abstraction:{policy:Expected Reward}}
		self.Tr={}#{state abstraction:{policy:{state abstraction: probability}}
		self.NTr={}#{state abstraction:{policy:{state abstraction: number of times}
		self.R={}#{state abstraction:{policy:{Immediate 1 step Reward}}
		self.NR={}#{state abstraction:{policy:Number of times}

		# in order to calculate these, we need to save the last abstraction/policy

		self.T=Set()
		self.environment_data=E(e_args)

	def OnlinePlanning(self,agent_,s,a_,time_to_work):
		
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
			self.search(a_,0,self.environment_data)
			end = time.time()

	def rollout(self,a_,depth,s):
		r1=0.
		r2=0.
		while depth<H:
			policy = a_.policy_set[24]

			(s,r1_,r2_,n) = a_.simulate_full(policy,s)
			r1+=gamma*r1_
			r2+=gamma*r2_
			
			depth+=n

		return (r1,r2)
	

	def search(self,a_,depth,s):


		if depth>H:
			return (0,0)
		else:

			abstraction =abf(a_,s)#*
			if abstraction not in self.T:
				self.T.add(abstraction)
				self.append_dict(self.N,abstraction,1)
				return self.rollout(a_,depth,s)
			else:
				policy = a_.policy_set[self.arg_max_ucb(abstraction)]

				(s,r1,r2,n) = a_.simulate_full(policy,s)
				r1_,r2_ = self.search(a_,depth+n,s)
				r1+=gamma*r1_
				r2+=gamma*r2_


			self.append_dict(self.N,abstraction,0)
			self.append_dict(self.N,abstraction,1)

			self.append_dict2(self.Na,abstraction,policy.index,0)
			self.append_dict2(self.Na,abstraction,policy.index,1)

			self.append_dict2(self.Q,abstraction,policy.index,0.)
			self.append_dict2(self.Q,abstraction,policy.index,(r1/n-(self.Q[abstraction][policy.index]))/self.Na[abstraction][policy.index])

					
			return (r1,r2)



	def append_dict(self,P,hash1,r):
		if P.get(hash1) is None:
			P[hash1]=r
		else:
			P[hash1]+=r

	def append_dict2(self,P,hash1,hash2,r):
		if P.get(hash1) is None:
			P[hash1]={hash2:r}
		elif P[hash1].get(hash2) is None:
			P[hash1][hash2]=r
		else:
			P[hash1][hash2]+=r



	def arg_max(self,abstraction):

		# returns index of best policy		
		if self.Q.get(abstraction) is not None:
			v = list(self.Q[abstraction].values())
			k = list(self.Q[abstraction].keys())

     			return k[v.index(max(v))]
		else:
			"ERROR"
			return 0

	def append_dict_tr(self,P,P2,ab2,ab1,policy_index):
		if P.get(ab1) is None:
			P[ab1]={}
			P[ab1][policy_index]={}
			P[ab1][policy_index][ab2]=1.
			P2[ab1]={}
			P2[ab1][policy_index]=1.
		elif P.get(ab1).get(policy_index) is None:
			P[ab1][policy_index]={}
			P[ab1][policy_index][ab2]=1.
			P2[ab1][policy_index]=1.
		elif P.get(ab1).get(policy_index).get(ab2) is None:
			P[ab1][policy_index][ab2]=1.
			P2[ab1][policy_index]+=1.
		else:
			P2[ab1][policy_index]+=1.
			P[ab1][policy_index][ab2]+=1.

	def append_dict_R(self,P,P2,ab1,policy_index,r):
		if P.get(ab1) is None:
			P[ab1]={}
			P[ab1][policy_index]=r
			P2[ab1]={}
			P2[ab1][policy_index]=1.
		elif P.get(ab1).get(policy_index) is None:
			P[ab1][policy_index]=1.
			P2[ab1][policy_index]=r
		else:
			P2[ab1][policy_index]+=1.
			P[ab1][policy_index]+=(r-P[ab1][policy_index])/(P2[ab1][policy_index])



	def update_transition_and_reward_functions(self,s,a):
		# add probabilities to Tr and R		
		abstraction = abf(a,s)

		self.append_dict_tr(self.Tr,self.NTr,abstraction,a.last_abstraction,a.current_action.index)
		self.append_dict_R(self.R,self.NR,a.last_abstraction,a.current_action.index,a.last_reward)

	def arg_max_ucb(self,abstraction):
		max=-1000
		policy_index = None

		if self.Q.get(abstraction) is not None:
			k = range(policy_set_size)


			for kz in k:
				if self.Q[abstraction].get(kz) is None:
					return kz
				if self.ucb(self.N[abstraction],self.Q[abstraction][kz],self.Na[abstraction][kz]) > max:
					max=self.ucb(self.N[abstraction],self.Q[abstraction][kz],self.Na[abstraction][kz])
					policy_index = kz
		else:
			return 0

		return policy_index

	def ucb(self,N,Q,Na):
		return Q+1000.*math.sqrt(math.log(1+N)/(1+Na))





	def print_n(self):
		for ele in self.N:
			print ele,self.N

		for ele in self.Na:
			for ele2 in self.Na[ele]:
				print ele,ele2,self.Na[ele][ele2]
				print ele,ele2,self.Q[ele][ele2]

	def print_pr(self):
		
		summ=0.
		for ab in self.Tr:#ab,polic,ab2
 			for pol in self.Tr[ab]:
				summ +=self.NTr[ab][pol]
				for ab2 in self.Tr[ab][pol]:
					print "starting",self.Tr[ab][pol][ab2],self.NTr[ab][pol],self.Tr[ab][pol][ab2]/self.NTr[ab][pol] 
					print "expected R", self.R[ab][pol]
					
					if self.Q.get(ab) is not None:
						if self.Q.get(ab).get(pol) is not None:					
							print "Q",self.Q[ab][pol]

		print summ


class Agent_buoy: 


	def __init__(self,Mobile_Buoy_Environment,map_size_):

		self.solver = Solver(Mobile_Buoy_Environment,map_size_) # get rid of
		self.x=0
		self.y=0
		self.map_size=map_size_
		self.alpha=[.9,.1,0]
		self.reset()
		self.counter=0
		self.current_action=policy(24)
		self.worked=[]


		self.last_abstraction="h"
		self.last_reward=0.
		
		self.policy_set=[]
		for i in range(policy_set_size):
			self.policy_set.append(policy(i))
			self.worked.append(0)

	def update_worked(self,list_of_workers_tasks):
		for i in range(len(region)):
			self.worked[i]=0

		for i in list_of_workers_tasks:
			self.worked[i]+=1
			
		self.worked[self.current_action.index]-=1


	def reset(self):
		self.x=self.map_size/2
		self.y=self.map_size/2


	def imprint(self, u):
		u.x=self.x
		u.y=self.y
		u.worked=self.worked



	def step(self,s,a_,time_to_work):	
		self.solver.OnlinePlanning(self,s,a_,time_to_work)

	def decide(self,s,a_):	
		action = self.current_action.get_next_action(self)
		self.counter+=1
		if action[1] is True or self.counter > 10:
			self.current_action = policy(self.solver.arg_max(abf(self,s)))
			self.current_action.reset()
			self.counter=0

		self.execute(action[0],s)



	def execute(self,action_,s):
		self.last_abstraction=abf(self,s)
		base_reward= s.get_reward()
		(x,y) = self.get_transition(action_,self.x,self.y)
		
		if s.check_boundaries((x,y)) is True:
			(self.x,self.y) = (x,y)

		self.measure(s,False)

		r= s.get_reward()-base_reward
		self.last_reward=r

		
		self.solver.print_pr()

	

	def simulate_full(self,policy,s):
		base_reward= s.get_reward()
		r1=0
		complete=False
		count=0.

		while complete is False:
			count+=1.
			action = policy.get_next_action(self)
			complete=action[1]
			(x,y) = self.get_transition(action[0],self.x,self.y)

			if s.check_boundaries((x,y)) is True:
				(self.x,self.y) = (x,y)

			base_reward= s.get_reward()
			self.measure(s,True)

			r1+=math.pow(gamma,count-1)*(s.get_reward()-base_reward)
			base_reward=s.get_reward()

			return (s,r1,0,count)

	def measure(self,s,imaginary):
		for r in region:
			if (self.x,self.y) == r:
				s.measure_loc(s.get_region(self.x,self.y),imaginary)

	def get_transition(self,action,x,y):
		return (x+action[0],y+action[1])



