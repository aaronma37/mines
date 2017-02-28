#!/usr/bin/env python

from random import randint
from environment_classes import Mine_Data
import time
import math
from sets import Set
from geometry_msgs.msg import PoseStamped
import numpy as np

zone = (((0,5),(-1,2)),((-4,1),(-1,2)),((-1,2),(-4,1)),((-1,2),(0,5)) )
region = [(10,10),(10,30),(10,50),(10,70),(10,90),(30,10),(50,10),(70,10),(90,10),(30,30),(50,30),(70,30),(90,30),(30,50),(50,50),(70,50),(90,50),(30,70),(50,70),(70,70),(90,70),(30,90),(50,90),(70,90),(90,90)]

region_size=10

region_set=[]

for i in range(25):
	region_set.append([])
	for j in range(region[i][0]-region_size,region[i][0]+region_size):
		for k in range(region[i][1]-region_size,region[i][1]+region_size):	
			region_set[i].append((j,k))


greedy_regions = [(1,1),(-1,1),(-1,-1),(1,-1), (0,1), (1,0), (0,-1), (-1,0)]

policy_set_size=37
H=50
gamma=.95

def abf_battery(a):
	return  str(int(a.battery/10.))



def abf_general_explored(s):
	return str(int(s.get_reward()/s.max_reward*10.))

def abf_top_level(a,s):
	return ":" + str(int(a.battery/10.)) + ":" + str(int(s.get_reward()/s.max_reward*10.))

def abf_explore(a,s):

	h ="h"

	if max(math.fabs(a.x-s.middle[0]),math.fabs(a.y-s.middle[1])) > 30:
		h=h+"4:"
	elif max(math.fabs(a.x-s.middle[0]),math.fabs(a.y-s.middle[1])) > 20:
		h=h+"3:"
	elif max(math.fabs(a.x-s.middle[0]),math.fabs(a.y-s.middle[1])) > 10:
		h=h+"2:"
	elif max(math.fabs(a.x-s.middle[0]),math.fabs(a.y-s.middle[1])) > 0:
		h=h+"1:"
	else:
		h=h+"0:"


	for i in region:
		h=h+abf_region(s,i)+":"

	#rework this to be number of agents working on it
	for i in range(len(region)):
		h=h+str(a.others_explore_num[i])+":"
	h=h+str(get_region(a.x,a.y))+":"
	return h

def abstracted_regions(s):
	region_abstractions=[]
	for i in regions:
		region_abstractions.append(abf_region(s,i))
	return region_abstractions


def abf_region(s,i):
	return str(s.get_region_score((i[0]-region_size,i[0]+region_size),(i[1]-region_size,i[1]+region_size)))

def get_region(x,y):
	for i in range(len(region)):
		if x > region[i][0]-region_size and x < region[i][0] + region_size:
			if y > region[i][1]-region_size and y < region[i][1] + region_size:
				return i

def get_next(x,y,action):
	for a in action:
		x+=a[0]
		y+=a[1]

	return x,y


class policy_top_level:
	def __init__(self,index,trigger):
		self.index=index
		#index=0 is to go charge
		#index 1 is to go explore
		self.trigger=trigger
		self.low_level_policy_set=[]
		if self.index==0:
			self.low_level_policy_set.append(policy_low_level(0))
		elif self.index==1:
			for i in range(1,26):
				self.low_level_policy_set.append(policy_low_level(i,"Not set"))

		self.LA=(policy_low_level(0,"Not set"))

	def check_trigger(self,a,s):
		if self.trigger is not self.get_trigger_definition(a,s):
			return True
		return False

	def get_trigger_definition(self,a,s):
		return abf_top_level(a,s)

	def set_trigger(self,a,s):
		self.trigger=self.get_trigger_definition(a,s)
	
	def get_abstraction(self,a,s):
		return abf_top_level(a,s)



class policy_low_level:
	def __init__(self,index,trigger):
		self.index=index
		self.trigger=trigger
		# index = 0 is go to base and charge

		# index 1: 25 is go to region (region -1 ) 

	def abstraction_function()

	def check_trigger(self,a,s):
		if self.trigger is not self.get_trigger_definition(a,s):
			return True
		return False

	def get_distance(self,x,y,x2,y2):
		return max(math.fabs(x-x2),math.fabs(y-y2))

	def get_trigger_definition(self,a,s):
		if self.index==0:
			return abf_battery(a)
		elif self.index <26:
			return abf_region(s,self.index-1)

	def set_trigger(self,a,s):
		self.trigger=self.get_trigger_definition(a,s)


	def get_abstraction(self,a,s):
		if self.index==0:
			return abf_battery(a)
		elif self.index <26:
			return abf_region(s,self.index-1)

	def get_target(self,a,s):
		if self.index==0:
			return (s.middle[0],s.middle[1])
		elif self.index <26:
			m=1000
			loc=(0,0)
			for i in region_set[self.index-1]:
				if s.seen[i[0]][i[1]]==s.NOT_SEEN:
					if get_distance(a.x,a.y,i[0],i[1]) < m:
						m=get_distance(a.x,a.y,i[0],i[1])
						loc = i
			if loc==(0,0):
				print "none found"
			return loc
						
				
			

	def get_next_action(self,a,s):
		next_x=0
		next_y=0
		target = self.get_target(a,s)
	
		if a.x < target[0]:
			next_x = 1
		elif a.x > target[0]:
			next_x = -1

		if a.y <target[1]:
			next_y= 1
		elif a.y > target[1]:
			next_y=-1

		if a.x is target[0] and a.y is target[1]:
			self.reset()
			return (0,0)
		else:	
			return (next_x,next_y)



def append_dict(P,h1,h2,r):
	if P.get(h1) is None:
		P[h1]={h2:r}
	elif P[h1].get(h2) is None:
		P[h1][h2]=r
	else:
		P[h1][h2]+=r

def append_dict2(P,h1,h2,h3,r):
	if P.get(h1) is None:
		P[h1]={h2:{h3:r}}
	if P[h1].get(h2) is None:
		P[h1][h2]={h3:r}
	elif P[h1][h2].get(h3) is None:
		P[h1][h2][h3]=r
	else:
		P[h1][h2][h3]+=r


class heuristics:
	def __init__(self):
		self.A={} #type,input,next abstraction -> number of occasions
		self.N={} #type,input - > number of occasions
		self.R={} #type,input, -> accrued reward
		#classifier,input,output

			

	def update(self,classifier,input_,output_,reward):
		append_dict(self.N,classifier,input_,1)
		append_dict2(self.A,classifier,input_,output_,1)

		append_dict(self.R,classifier,input_,0.)
		append_dict(self.R,classifier,input_,(reward-self.R[classifier][input_])/self.N[classifier][input_])


	def pull_new_abstraction(self,classifier,input_):

		#Returns from particle

		c=0.
		r=rand.rand()

		if self.R[classifier].get(input_) is None:
			return None

		N=self.N[classifier][input_]
		for k,v in self.A[classifier][input_].items() 
			if r < c+self.A[classifier][input][k]/N:
				return v
			c+=v/N

		return None

	def pull_from_rewards(self,classifier,input_):
		
		if self.R.get(classifier) is None:
			append_dict(self.R,classifier,input_,0.)
	
		if self.R[classifier].get(input_) is None:
			append_dict(self.R,classifier,input_,0.)

		return self.R[classifier][input_]
				


class Solver: 


	def __init__(self,E,e_args):
		self.N={}#{state abstraction: num visited}
		self.Na={}#{state abstraction: {policy: num visited}}
		self.Q={}#{state abstraction:{policy:Expected Reward}}
		self.T=Set()
		self.H=heuristics()
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
		while depth<H and a_.battery > 1:
			policy = a_.policy_set[1]
			if a_.battery < 1:
				policy = a_.policy_set[1]

			(s,r1_,r2_,n) = a_.simulate_full(policy,s)
			r1+=gamma*r1_
			r2+=gamma*r2_
			
			depth+=n

		return (r1,r2)
	

	def search(self,a_,depth,s,level):


		# start at top level
		# use a recursive under part

		# if top level:
		if level==1:	
			if depth>H or a_.battery <1:
				return 0,H-depth
			else:

				abstraction =abf_top_level(a_,s)#*
				if abstraction not in self.T:
					self.T.add(abstraction)
					self.append_dict(self.N,abstraction,1)
					return self.rollout(a_,depth,s)
				else:
					a_.TA = a_.policy_set[self.arg_max_ucb("root",abstraction)]
					r1,n = self.search(a_,depth,s,0)
					r1_,n2 = self.search(a_,depth+n,s,1)
					r1+=gamma*r1_
				


				self.append_dict(self.N,"root",abstraction,0)
				self.append_dict(self.N,"root",abstraction,1)

				self.append_dict2(self.Na,"root",abstraction,policy.index,0)
				self.append_dict2(self.Na,"root",abstraction,policy.index,1)

				self.append_dict2(self.Q,"root",abstraction,policy.index,0.)
				self.append_dict2(self.Q,"root",abstraction,policy.index,(r1/n-(self.Q[abstraction][policy.index]))/self.Na[abstraction][policy.index])

					
				return r1,n2


			# if lower level
		elif level==0:
			if depth>H or a_.battery <1:
				return (0,0)
			else:

				abstraction =abf(a_,s)#*
				if abstraction not in self.T:
					self.T.add(abstraction)
					self.append_dict(self.N,abstraction,1)
					return self.rollout(a_,depth,s)
				else:
					if a_.TA.LA.check_trigger(a_,s) is True:
						a_.TA.LA = a_.TA.policy_set[self.arg_max_ucb(a_.TA.index,abstraction)]
						a_.TA.LA.set_trigger(a_,s)

					#for the abstractions we care about
					#pull abstractions
					#pull R


					(s,r,a)
					# for all regions, input, etc
					Some abstraction = self.H.pull_from_abstractions(region,)

					r = self.H.pull_from_rewards(an abstraction,input_)

					#(s,r1,n) = a_.simulate_full(policy,s)
					r1,n1 = self.search(a_,depth+1,s)
					r+=gamma*r1



				self.append_dict(self.N,a_.TA.index,abstraction,0)
				self.append_dict(self.N,a_.TA.index,abstraction,1)

				self.append_dict2(self.Na,a_.TA.index,abstraction,policy.index,0)
				self.append_dict2(self.Na,a_.TA.index,abstraction,policy.index,1)

				self.append_dict2(self.Q,a_.TA.index,abstraction,policy.index,0.)
				self.append_dict2(self.Q,a_.TA.index,abstraction,policy.index,(r1/n-(self.Q[abstraction][policy.index]))/self.Na[abstraction][policy.index])

					
				return r1,n



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



	def arg_max(self,abstraction):

		# returns index of best policy		
		if self.Q.get(abstraction) is not None:
			v = list(self.Q[abstraction].values())
			k = list(self.Q[abstraction].keys())

     			return k[v.index(max(v))]
		else:
			"ERROR"
			return 0

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

class Agent: 


	def __init__(self,Mine_Data,map_size_):

		self.solver = Solver(Mine_Data,map_size_) # get rid of
		self.x=0
		self.y=0
		self.map_size=map_size_
		self.ON=0
		self.measurement_space=[]
		self.alpha=[.9,.1,0]
		self.reset()
		self.battery=50
		self.TA=policy(1)
		
		self.policy_set=[]
		for i in range(2):
			self.policy_set.append(policy_top_level(i,"Not set"))
		self.time_away_from_network=0
		



	def reset(self):
		self.x=self.map_size/2
		self.y=self.map_size/2


	def death(self):
		self.x=randint(0,self.map_size-1)
		self.y=randint(0,self.map_size-1)
		self.battery=75


	def imprint(self, u):
		u.x=self.x
		u.y=self.y
		u.battery=self.battery
		u.time_away_from_network=self.time_away_from_network



	def step(self,s,a_,time_to_work):	
		self.solver.OnlinePlanning(self,s,a_,time_to_work)

	def decide(self,s,a_):	
		#DO WE NEED A_ HERE


		if self.TA.LA.check_trigger(a_,s):
			if self.TA.check_trigger(a_,s):
				self.TA=self.policy_set(self.solver.arg_max("Root",abf(self,s)))
				self.TA.set_trigger(a_,s)	
				self.TA.LA=self.TA.policy_set(self.solver.arg_max(self.TA.index,abf(self,s)))
				self.TA.LA.set_trigger(a_,s)	
			else:
				self.TA.LA=self.TA.policy_set(self.solver.arg_max(self.TA.index,abf(self,s)))
				self.TA.LA.set_trigger(a_,s)				
		
		action = self.TA.LA.get_next_action(self,s)

		self.execute(action,s)
		# return s?		
		return s


	def execute(self,action_,environment_data_):
		(x,y) = self.get_transition(action_,self.x,self.y,environment_data_.middle)
		
		if environment_data_.check_boundaries((x,y)) is True:
			(self.x,self.y) = (x,y)

		self.measure(environment_data_,False)

		if self.battery < 1:
			print time.time(), "Dead"
			self.death()

	

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
