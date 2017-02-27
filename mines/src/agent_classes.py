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

greedy_regions = [(1,1),(-1,1),(-1,-1),(1,-1), (0,1), (1,0), (0,-1), (-1,0)]

policy_set_size=37
H=50
gamma=.95



def abf(a,s):

	h ="h"
	h = h + str(int(a.battery/10.))+":"


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
		h=h+str(s.get_region_score((i[0]-region_size,i[0]+region_size),(i[1]-region_size,i[1]+region_size)))+":"

	for i in range(len(region)):
		h=h+str(s.occupied[i])+":"

	if a.time_away_from_network < 5:
		h=h+str(0)+":"
	elif a.time_away_from_network < 20:
		h=h+str(1)+":"
	elif a.time_away_from_network < 50:
		h=h+str(2)+":"
	else:
		h=h+str(3)+":"

	h=h+str(get_region(a.x,a.y))+":"



	return h

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

class policy:
	def __init__(self,index):
		self.index=index


		self.action_string=[(0,0)]
	
		self.num_steps=1000

				

		if self.index==2:
			for i in range(5):
				self.action_string.append((1,0))
			self.num_steps=5

		elif self.index==3:
			for i in range(5):
				self.action_string.append((-1,0))
			self.num_steps=5
		elif self.index==4:
			for i in range(5):
				self.action_string.append((0,1))
			self.num_steps=5
		elif self.index==5:
			for i in range(5):
				self.action_string.append((0,-1))
			self.num_steps=5
		elif self.index==6:
			for i in range(5):
				self.action_string.append((-1,-1))
			self.num_steps=5
		elif self.index==7:
			for i in range(5):
				self.action_string.append((1,-1))
			self.num_steps=5
		elif self.index==8:
			for i in range(5):
				self.action_string.append((-1,1))
			self.num_steps=5
		elif self.index==9:
			for i in range(5):
				self.action_string.append((1,1))
			self.num_steps=5
	
			


		self.macro_set=self.build_macro_set(self.action_string)


		self.counter=0

	def expected_completion_time(self,x,y,s):
		if self.index > 1 and self.index < 10:
			return 5
		if self.index == 0:
			return max(math.fabs(x-s.middle[0],y-s.middle[1]))
		if self.index >9 and self.index < 35:
			return max(math.fabs(x-region[self.index-10],y-region[self.index-10]))
		else:
			return 1

	def build_macro_set(self,action_string):

		x=0
		y=0
		macro_set=Set()
		for i in action_string:
			x+=i[0]
			y+=i[1]
			for j in range(-1+x,2+x):
				for k in range(-1+y,2+y):
					macro_set.add((j,k))


		return macro_set
	
	def reset(self):
		self.counter=0
			

	def get_next_action(self,a_,x,y,s):
		next_x=0
		next_y=0
		self.counter+=1

		if self.index==0:
			##RETURN TO SHIP	
			if x < s.middle[0]:
				next_x = 1
			elif x > s.middle[0]:
				next_x = -1

			if y < s.middle[1]:
				next_y= 1
			elif y > s.middle[1]:
				next_y=-1

			if x is s.middle[0] and y is s.middle[1]:
				self.reset()
				return ((0,0),True)
			else:	
				return ((next_x,next_y),False)

		elif self.index==1:
			#wait
			if self.counter > 10:
				self.reset()
				return ((0,0),True)
			else:
				return((0,0),False)

		elif self.index>1 and self.index <10:
			#explore right

			if self.counter < 4:
				return (self.action_string[self.counter],False)
			else:
				self.reset()
				return (self.action_string[4],True)
		elif self.index>9 and self.index < 35:
						##RETURN TO SHIP	
			if x < region[self.index-10][0]:
				next_x = 1
			elif x > region[self.index-10][0]:
				next_x = -1

			if y < region[self.index-10][1]:
				next_y= 1
			elif y > region[self.index-10][1]:
				next_y=-1

			if x is region[self.index-10][0] and y is region[self.index-10][1]:
				self.reset()
				return ((0,0),True)
			else:	
				return ((next_x,next_y),False)

		elif self.index==35:				
			##RETURN TO SHIP AND CHARGE
			if x < s.middle[0]:
				next_x = 1
			elif x > s.middle[0]:
				next_x = -1

			if y < s.middle[1]:
				next_y= 1
			elif y > s.middle[1]:
				next_y=-1

			if x is s.middle[0] and y is s.middle[1]:
				if a_.battery > 75:
					self.reset()
					return ((0,0),True)
				else:
					return ((next_x,next_y),False)
			else:	
				return ((next_x,next_y),False)

		elif self.index==36:
			#Spiral!


			direction = (0,0)
			count=0
			while count > -1 and count < 10:
				count+=1
				for i in greedy_regions:
					if s.check_boundaries((x+count*i[0],y+count*i[1])) is True:
						if s.seen[x+count*i[0]][y+count*i[1]] == 0:
							direction=i	
							count =-1
							break
		
			return ((direction),True)




class Solver: 


	def __init__(self,E,e_args):
		self.N={}#{state abstraction: num visited}
		self.Na={}#{state abstraction: {policy: num visited}}
		self.Q={}#{state abstraction:{policy:Expected Reward}}
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
		while depth<H and a_.battery > 1:
			policy = a_.policy_set[1]
			if a_.battery < 1:
				policy = a_.policy_set[1]

			(s,r1_,r2_,n) = a_.simulate_full(policy,s)
			r1+=gamma*r1_
			r2+=gamma*r2_
			
			depth+=n

		return (r1,r2)
	

	def search(self,a_,depth,s):


		if depth>H or a_.battery <1:
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
		self.current_action=policy(1)

		
		self.policy_set=[]
		for i in range(policy_set_size):
			self.policy_set.append(policy(i))
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
		action = self.current_action.get_next_action(self,self.x,self.y,s)
		if action[1] is True:
			self.current_action = policy(self.solver.arg_max(abf(self,s)))
			self.current_action.reset()

		self.execute(action[0],s)
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
