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



away=(0,-1)
to=(0,1)
right=(1,0)
left=(-1,0)

top_level_choices=[]
top_level_choices.append((to))
top_level_choices.append((right))
top_level_choices.append((left))
top_level_choices.append((away))

action_space=[]


action_space.append((to,to,to))
#action_space.append((away,to,to,to,to))

action_space.append((right,to,to,to,left))
action_space.append((right,to,left,to,to))
action_space.append((right,to,to,left,to))
#action_space.append((right,left,to,to,to))
action_space.append((to,right,to,left,to))
action_space.append((to,right,to,to,left))
action_space.append((to,to,right,to,left))
#action_space.append((to,right,left,to,to))
#action_space.append((to,to,right,left,to))

action_space.append((left,to,to,to,right))
action_space.append((left,to,right,to,to))
action_space.append((left,to,to,right,to))
#action_space.append((left,right,to,to,to))
action_space.append((to,left,to,right,to))
action_space.append((to,left,to,to,right))
action_space.append((to,to,left,to,right))
#action_space.append((to,left,right,to,to))
#action_space.append((to,to,left,right,to))


class task:
	def __init__(self,a,direction,level,loc):
	#direct is direction from higher up action
		self.direction=direction
		self.a=a
		self.level=level
		self.starting_loc=loc
	

	def remove_action(self):
		self.a = self.a[1:]

		if len(self.a) == 0:
			return True

		return False

	def print_data(self):
		print "Level: ", self.level, ", Direction: ", self.direction
		print self.a






def print_seen(s):
	for i in range(s.map_size):
		for j in range(s.map_size):
			if s.seen[i][j] ==True:
			
				print i,j


def abf(direction,x_,y_,s,level):
	#abstraction is a function of %known atm
	score=0.0
	ms=0
	#2*
	w=int(2*math.pow(3,level)+1)
	#l=int(math.pow(3,level+1))
	l=int(math.pow(3,level+1)+1)

	size=w*l

	if direction == (1,0):
		for x in range(x_,x_+l+1):
			for y in range(y_-w/2,y_+w/2+1):
				if s.check_boundaries(Location(x,y)) == True:
					if bool(s.seen[x][y]) == False:
						score+=1.
		dist = math.sqrt(math.fabs(l*direction[0]/2+x_-ms)*math.fabs(l*direction[0]/2+x_-ms)+math.fabs(y_-ms)*math.fabs(y_-ms))
	elif direction == (-1,0):

		#print x_,y_, "START"
		for x in range(x_,x_-l-1,-1):
			for y in range(y_-w/2,y_+w/2+1):
				#print x,y,  bool(s.seen[x][y]), s.color[x][y]
				if s.check_boundaries(Location(x,y)) == True:
					if bool(s.seen[x][y]) == False:
						score+=1.
		#print_seen(s)
		dist = math.sqrt(math.fabs(l*direction[0]/2+x_-ms)*math.fabs(l*direction[0]/2+x_-ms)+math.fabs(y_-ms)*math.fabs(y_-ms))

	elif direction == (0,1):
		for y in range(y_,y_+l+1):
			for x in range(x_-w/2,x_+w/2+1):
				if s.check_boundaries(Location(x,y)) == True:
					if bool(s.seen[x][y]) == False:
						score+=1.	

		dist = math.sqrt(math.fabs(l*direction[1]/2+y_-ms)*math.fabs(l*direction[1]/2+y_-ms)+math.fabs(x_-ms)*math.fabs(x_-ms))

	elif direction == (0,-1):
		#print direction
		for y in range(y_,y_-l-1,-1):
			for x in range(x_-w/2,x_+w/2+1):

				if s.check_boundaries(Location(x,y)) == True:
					if bool(s.seen[x][y]) == False:
						score+=1.

		dist = math.sqrt(math.fabs(l*direction[1]/2+y_-ms)*math.fabs(l*direction[1]/2+y_-ms)+math.fabs(x_-ms)*math.fabs(x_-ms))

		
	return str(int(score/float(size)*10))+":"+str(int(dist)/10)	

def hash_(string):
	return xxhash.xxh64(string).hexdigest()

def get_dir(direction,t):

	if t == to:
		return direction
	elif t == away:
		if direction == (0,1):
			return (0,-1)
		elif direction == (0,-1):
			return (0,1)
		elif direction == (1,0):
			return (-1,0)
		else:
			return (1,0)
	elif t == left:
		if direction == (0,1):
			return (-1,0)
		elif direction == (0,-1):
			return (1,0)
		elif direction == (1,0):
			return (0,1)
		else:
			return (0,-1)
	elif t == right:
		if direction == (0,1):
			return (1,0)
		elif direction == (0,-1):
			return (-1,0)
		elif direction == (1,0):
			return (0,-1)
		else:
			return (0,1)

	print t,"WARNING NOT FOUND"


def print_dir(direction):
	if direction == to:
		print "TO"
	elif direction == away:
		print "AWAY"
	elif direction == left:
		print "LEFT"
	else:
		print "RIGHT"

def get_next(x,y,direction,level):
	dist=int(math.pow(3,level))

	x+=dist*direction[0]
	y+=dist*direction[1]
	return (x,y)


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



	def GetGreedyPrimitive(self,x,y,direction,s,lvl,alpha):
		(a,m) = self.arg_max(x,y,direction,s,lvl, alpha)
		t = task(a,direction,lvl,(x,y))
		return t






	def get_new_macro(self,x,y,s,level,alpha):
		max=-1000
		
		for i in top_level_choices:
			self.append_dict(self.Q,level,abf(i,x,y,s,level),0.)
			self.append_dict(self.Q2,level,abf(i,x,y,s,level),0.)
			#if abf(i,x,y,s,level)>max:#self.Q[level][abf(i,x,y,s,level)] > max:
			if self.Q[level][abf(i,x,y,s,level)]*alpha[0] + self.Q2[level][abf(i,x,y,s,level)]*alpha[1] > max:
				a = i
				max= self.Q[level][abf(i,x,y,s,level)]*alpha[0] + self.Q2[level][abf(i,x,y,s,level)]*alpha[1]
				#max= abf(i,x,y,s,level)#self.Q[level][abf(i,x,y,s,level)]
		t = self.GetGreedyPrimitive(x,y,a,s,level,alpha)

		r=s.get_reward()-self.last_reward
		r2=-s.get_reward2()
		self.append_dict(self.actual_Q,level,self.last_abstraction,0.)
		self.append_dict(self.actual_Q2,level,self.last_abstraction,0.)
		self.append_dict(self.actual_N,level,self.last_abstraction,0.)
		print "Expected gain: ", self.actual_Q.get(level).get(self.last_abstraction),self.actual_Q2.get(level).get(self.last_abstraction), ", State: ", self.last_abstraction, ", Number of visits: ", self.actual_N.get(level).get(self.last_abstraction)
		print "actual gain: ", r
		print "actual gain: ", r2


		self.last_reward=s.get_reward()	

		if self.last_abstraction is not None:
			self.append_dict(self.actual_Q,level,self.last_abstraction,0.)
			self.append_dict(self.actual_Q2,level,self.last_abstraction,0.)
			self.append_dict(self.actual_N,level,self.last_abstraction,1.)
			self.append_dict(self.actual_Q,level,self.last_abstraction,(r-self.actual_Q.get(level).get(self.last_abstraction))/self.actual_N.get(level).get(self.last_abstraction))
			self.append_dict(self.actual_Q2,level,self.last_abstraction,(r-self.actual_Q2.get(level).get(self.last_abstraction))/self.actual_N.get(level).get(self.last_abstraction))

		self.last_abstraction= abf(t.direction,x,y,s,level)
		
		return t
	
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

	


