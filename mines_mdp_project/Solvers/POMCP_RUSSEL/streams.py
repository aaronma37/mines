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

from drawing import basic_2



def build_macro_sets(action_string):

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
	

def abf(a_string,macro_set,x,y,s, others):
	score=0.
	ms=50
	for (i,j) in macro_set:
		if s.check_boundaries(Location(x+i,y+j)) == True:
			if bool(s.seen[x+i][y+j]) == False:
				score+=1.	


	x,y = get_next(x,y,a_string)

	dist = math.sqrt(math.fabs(x-ms)*math.fabs(x-ms)+math.fabs(y-ms)*math.fabs(y-ms))
	
	dist2= 0
	for (x_,y_) in others:
		if (math.sqrt(math.fabs(x-x_)*math.fabs(x-x_)+math.fabs(y-y_)*math.fabs(y-y_)) < 20):
			dist2=20


	return int(score/float(len(macro_set))*10),(-dist), (-dist2)
		

def hash_(string):
	return xxhash.xxh64(string).hexdigest()




class action:
	def __init__(self,index):
	#direct is direction from higher up action
		self.index=index

		self.action_string=[]

		for i in range(5):
			if self.index==0:
				self.action_string.append((0,1))
			elif self.index==1:
				self.action_string.append((1,0))
			elif self.index==2:
				self.action_string.append((0,-1))
			elif self.index==3:
				self.action_string.append((-1,0))
			elif self.index==4:
				self.action_string.append((1,1))
			elif self.index==5:
				self.action_string.append((-1,1))
			elif self.index==6:
				self.action_string.append((-1,-1))
			elif self.index==7:
				self.action_string.append((1,-1))
			elif self.index==8:
				self.action_string.append((0,0))



		self.macro_set=build_macro_sets(self.action_string)





def get_next(x,y,action):
	for a in action:
		x+=a[0]
		y+=a[1]

	return x,y
class Solver: 


	def __init__(self,E,e_args):
		self.N={}#{level of hierarchy:{ab():num visited}}
		self.Q={}#{level_of_hierarchy:{ab():Expected Reward}}
		self.N2={}#{level of hierarchy:{ab():num visited}}
		self.Q2={}#{level_of_hierarchy:{ab():Expected Reward}}
		self.counter=0
		self.environment_data=E(e_args)
		self.last_reward=0
		self.last_reward2=0
		self.action_counter=0
		self.s_ = np.ndarray(shape=(1000,3), dtype=object)
		for i in range(1000):
			for j in range(3):
				self.s_[i][j] = E(e_args)
		self.actual_Q={}
		self.actual_N={}
		self.actual_Q2={}
		self.actual_N2={}
		self.last_abstraction=None
		self.actions=[]
		
		for i in range(9):
			self.actions.append(action(i))



	def GetGreedyPrimitive(self,x,y,direction,s,lvl,alpha):
		(a,m) = self.arg_max(x,y,direction,s,lvl, alpha)
		t = task(a,direction,lvl,(x,y))
		return t






	def get_new_macro(self,loc,s,alpha, others):
		max=-1000
		x=loc[0]
		y=loc[1]
		for a_1 in self.actions:
			x=loc[0]
			y=loc[1]
			r1,r2,r3=abf(a_1.action_string,a_1.macro_set,x,y,s,others)
			r=r1*alpha[0] + r2*alpha[1]+ r3*alpha[2]
			x,y=get_next(x,y,a_1.action_string)
			for a_2 in self.actions:
				r1,r2,r3=abf(a_2.action_string,a_2.macro_set,x,y,s,others)
				r+=.3*(r1*alpha[0] + r2*alpha[1] + r3*alpha[2])
				x,y=get_next(x,y,a_2.action_string)
				for a_3 in self.actions:
					r1,r2,r3=abf(a_3.action_string,a_3.macro_set,x,y,s,others)
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



	

	def search(self,a_,direction,level,s):
		#where t is a policy ((directions), policy num)		
		iteration_index=self.counter
		self.counter+=1
		#s.imprint(self.s_[iteration_index][0])


		if level==-1:

			(s,r1,r2) = a_.simulate(direction,s)
			#self.sTemp.imprint(self.s_[iteration_index][1])	
			#print "tiny r", r
			self.action_counter+=1
			return (r1,r2,s)
		else:
			abstraction =abf(direction,a_.get_x(),a_.get_y(),s,level)
			sub_task = self.arg_max_ucb(a_,direction,s,level)
			#self.s_[iteration_index][0].imprint(self.s_[iteration_index][1])
			r1_total=0.
			r2_total=0.
			counter2=0
			for sub_sub_task in sub_task:
				(r1,r2,s)= self.search(a_,get_dir(direction,sub_sub_task),level-1,s)
				#temp_dir=get_dir(temp_dir,sub_sub_task)
				#self.sTemp.imprint(self.s_[iteration_index][1])
				r1_total+=math.pow(.95,counter2)*r1
				r2_total+=math.pow(.95,counter2)*r2
				counter2+=1

			#update N

			self.append_dict(self.N,level,abstraction,1)

			self.append_dict(self.Q,level,abstraction,0)
			self.append_dict(self.Q,level,abstraction,(r1_total-self.Q.get(level).get(abstraction))/self.N.get(level).get(abstraction))

			self.append_dict(self.Q2,level,abstraction,0)
			self.append_dict(self.Q2,level,abstraction,(r2_total-self.Q2.get(level).get(abstraction))/self.N.get(level).get(abstraction))
					
			return (r1_total,r2_total,s)



	def append_dict(self,P,level,s,r):
		if P.get(level) is None:
			P[level]={s:r}
		elif P[level].get(s) is None:
			P[level][s]=r
		else:
			P[level][s]+=r



	def arg_max(self,x,y,direction,s,level, alpha):
		max=-1000


		for task in action_space:

			if self.get_score(task,direction,x,y,s,level,alpha,0) + self.get_score(task,direction,x,y,s,level,alpha,1) > max:
				a = task
				max=self.get_score(task,direction,x,y,s,level,alpha,0) + self.get_score(task,direction,x,y,s,level,alpha,1)
										

	
		return a,max

	def get_score(self,sub_task,direction,x,y,s,level, alpha, alpha_index):
	

		count=0.0
		score=0.0

		if alpha_index==0:
	
			for task in sub_task:
				self.append_dict(self.Q,level,abf(get_dir(direction,task),x,y,s,level),0)
				score+=math.pow(.95,count)*self.Q[level][abf(get_dir(direction,task),x,y,s,level)]#abf(get_dir(direction,task),x,y,s,level)#
				(x,y)=get_next(x,y,get_dir(direction,task),level)
				count+=1.

		else:
			for task in sub_task:
				self.append_dict(self.Q2,level,abf(get_dir(direction,task),x,y,s,level),0)
				score+=math.pow(.95,count)*self.Q2[level][abf(get_dir(direction,task),x,y,s,level)]#abf(get_dir(direction,task),x,y,s,level)#
				(x,y)=get_next(x,y,get_dir(direction,task),level)
				count+=1.
			
		return score/count*alpha[alpha_index]



	def arg_max_ucb(self,a_,direction,s,level):
		#max=-1


		x=a_.get_x()
		y=a_.get_y()


		for task in action_space:
			if self.N.get(level) is None:
				return task
			elif self.N.get(level).get(abf(direction,a_.get_x(),a_.get_y(),s,level)) is None:
				return task

		a = random.choice(action_space)
										

		return a



	def print_n(self):
		for ele in self.N:

			for ele2 in self.N[ele]:
				print ele,ele2,self.N[ele][ele2]
				print ele,ele2,self.Q[ele][ele2]
				print ele,ele2,self.Q2[ele][ele2]

	


