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
top_level=3
top_level_choices=[]
top_level_choices.append(to)
top_level_choices.append(right)
top_level_choices.append(left)
top_level_choices.append(away)

action_space=[]


action_space.append(((to,to,to),len(action_space)))
action_space.append(((away,to,to,to,to),len(action_space)))

action_space.append(((right,to,to,to,left),len(action_space)))
action_space.append(((right,to,left,to,to),len(action_space)))
action_space.append(((right,to,to,left,to),len(action_space)))
action_space.append(((right,left,to,to,to),len(action_space)))
action_space.append(((to,right,to,left,to),len(action_space)))
action_space.append(((to,right,to,to,left),len(action_space)))
action_space.append(((to,to,right,to,left),len(action_space)))
action_space.append(((to,right,left,to,to),len(action_space)))
action_space.append(((to,to,right,left,to),len(action_space)))

action_space.append(((left,to,to,to,right),len(action_space)))
action_space.append(((left,to,right,to,to),len(action_space)))
action_space.append(((left,to,to,right,to),len(action_space)))
action_space.append(((left,right,to,to,to),len(action_space)))
action_space.append(((to,left,to,right,to),len(action_space)))
action_space.append(((to,left,to,to,right),len(action_space)))
action_space.append(((to,to,left,to,right),len(action_space)))
action_space.append(((to,left,right,to,to),len(action_space)))
action_space.append(((to,to,left,right,to),len(action_space)))


def print_seen(s):
	for i in range(s.map_size):
		for j in range(s.map_size):
			if s.seen[i][j] ==True:
			
				print i,j


def abf(direction,x_,y_,s,level):
	#abstraction is a function of %known atm
	score=0.0
	w=int(2*math.pow(3,level-1))
	l=int(math.pow(3,level))
	size=w*l

	if direction == (1,0):
		for x in range(x_,x_+l+1):
			for y in range(y_-w/2,y_+w/2+1):
				if s.check_boundaries(Location(x,y)) == True:
					if bool(s.seen[x][y]) == False:
						score+=1.
	elif direction == (-1,0):

		#print x_,y_, "START"
		for x in range(x_,x_-l-1,-1):
			for y in range(y_-w/2,y_+w/2+1):
				#print x,y,  bool(s.seen[x][y]), s.color[x][y]
				if s.check_boundaries(Location(x,y)) == True:
					if bool(s.seen[x][y]) == False:
						score+=1.
		#print_seen(s)

	elif direction == (0,1):
		for y in range(y_,y_+l+1):
			for x in range(x_-w/2,x_+w/2+1):
				if s.check_boundaries(Location(x,y)) == True:
					if bool(s.seen[x][y]) == False:
						score+=1.
	elif direction == (0,-1):
		#print direction
		for y in range(y_,y_-l-1,-1):
			for x in range(x_-w/2,x_+w/2+1):

				if s.check_boundaries(Location(x,y)) == True:
					if bool(s.seen[x][y]) == False:
						score+=1.

		#print score


	return int(score/float(size)*5)	

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
		self.counter=0.
		self.environment_data=E(e_args)

		self.s_ = np.ndarray(shape=(100,3), dtype=object)
		for i in range(100):
			for j in range(3):
				self.s_[i][j] = E(e_args)



	def GetGreedyPrimitive(self,x,y,direction,s):
		action = [direction]	
		final_dir = direction	
		for i in range(top_level-1,0,-1):
			(a,m) = self.arg_max(x,y,direction,s,i)
			action.append(a)
			direction = get_dir(direction,action[len(action)-1][0][0])
		
		#print "FINAL DIRECTION", direction
		return (action,direction)
	
	def OnlinePlanning(self,agent_,environment_data_,a_,time_to_work):
		level=top_level-1
		start = time.time()
		end = start
		agent_.imprint(a_)
		self.print_n()
		environment_data_.imprint(self.environment_data)
		while end - start < time_to_work:
			agent_.imprint(a_)
			environment_data_.imprint(self.environment_data)
			self.counter=0
			#rint "start"
			self.search(a_,to,level,self.environment_data)
			end = time.time()

		x=agent_.x
		y=agent_.y
		a,b =self.GetGreedyPrimitive(x,y,to,environment_data_)

		print a
		return b

	def search(self,a_,direction,level,s):
		#where t is a policy ((directions), policy num)		
		iteration_index=self.counter
		self.counter+=1
		s.imprint(self.s_[iteration_index][0])

		if level==0:

			(self.sTemp,r) = a_.simulate(direction,self.s_[iteration_index][0])
			self.sTemp.imprint(self.s_[iteration_index][1])	
			#print_dir(direction)			
			#print a_.x,a_.y	
				
			return (r,self.s_[iteration_index][1])
		else:

			sub_task = self.arg_max_ucb(a_,direction,self.s_[iteration_index][0],level)
			self.s_[iteration_index][0].imprint(self.s_[iteration_index][1])
			r1_total=0.
			temp_dir = direction
			for sub_sub_task in sub_task[0]:
				(r1,self.sTemp)= self.search(a_,get_dir(temp_dir,sub_sub_task),level-1,self.s_[iteration_index][1])
				temp_dir=get_dir(temp_dir,sub_sub_task)
				self.sTemp.imprint(self.s_[iteration_index][1])
				r1_total+=r1

			#update N
			abstraction =abf(direction,a_.get_x(),a_.get_y(),self.s_[iteration_index][0],level)
			self.append_dict(self.N,level,abstraction,1)
			#calculate R
			r= r1_total
			#update Q
			self.append_dict(self.Q,level,abstraction,0)
			self.append_dict(self.Q,level,abstraction,(r-self.Q.get(level).get(abstraction))/self.N.get(level).get(abstraction))

			#return 					
			return (r,self.s_[iteration_index][2])



	def append_dict(self,P,level,s,r):
		if P.get(level) is None:
			P[level]={s:r}
		elif P[level].get(s) is None:
			P[level][s]=r
		else:
			P[level][s]+=r



	def arg_max(self,x,y,direction,s,level):
		max=-1

		

		#self.print_seen(s)
		


		if level is top_level:
			for task in top_level_choices:
				if self.Q[task][abf(direction,x,y,level)] > max:
					a = task
					max= self.Q[task][abf(direction,x,y,top_level)]
		elif level is not 0:
			for task in action_space:
				#print "DECIDING", level
				#print_dir(get_dir(direction,task[0][0]))
				#print self.get_score(task,direction,x,y,s,level)

				if self.get_score(task,direction,x,y,s,level) > max:
					a = task
					max=self.get_score(task,direction,x,y,s,level)
		else:
			a = t											

		#print " "
		#time.sleep(3)

	
		return a,max

	def get_score(self,sub_task,direction,x,y,s,level):
		#print "TESTING", level
		#print x,y
		#print abf((0,1),x,y,s,level)
		#print abf((0,-1),x,y,s,level)
		#print abf((-1,0),x,y,s,level)
		#print abf((1,0),x,y,s,level)	

		count=0.0
		score=0.0
		#score=abf(get_dir(direction,sub_task[0][0]),x,y,s,level)
		#print_dir(get_dir(direction,sub_task[0][0]))
		#print score
		for task in sub_task[0]:
			self.append_dict(self.Q,level,abf(get_dir(direction,task),x,y,s,level),0)
			score+=self.Q[level][abf(get_dir(direction,task),x,y,s,level)]
			direction = get_dir(direction,task)
			(x,y)=get_next(x,y,direction,level)
			count+=1.

		#print score
		return score/count



	def arg_max_ucb(self,a_,direction,s,level):
		#max=-1


		x=a_.get_x()
		y=a_.get_y()

		if level is top_level:
			for task in top_level_choices:
				if self.N.get(level) is None:
					return task
				elif self.N.get(level).get(abf(direction,x,y,s,level)) is None:
					return task
			a = random.choice(top_level)
			#max= self.Q[level][abf(t,a_.get_x(),a_.get_y(),top_level)]
		elif level is not 0:
			for task in action_space:
				if self.N.get(level) is None:
					return task
				elif self.N.get(level).get(abf(direction,a_.get_x(),a_.get_y(),s,level)) is None:
					return task

			a = random.choice(action_space)
			#max= self.Q[level][abf(t,x,y,level)]
		else:
			a = t											

		return a



#	def in_dict(self,N,k):
#		if len(k) > 1:
#			if N.get(k[0]) is None:
#				return False
#			return self.in_dict(N[k[0]],k[1:])
#		else:
#			if N.get(k[0]) is None:
#				return False
#			else:
#				return True	
			





			




#	def append_dict(self, N, k,r):
#		if len(k) > 1:
#			if N.get(k[0]) is None:
#				N[k[0]] = {}
#			self.append_dict(N[k[0]],k[1:],r)
#		else:
#			if N.get(k[0]) is None:
#				N[k[0]]=r
#			else:
#				N[k[0]]+=r
#
#	def append_dict_Q(self, N, Na, k,r):
#		if len(k) > 1:
#			if N.get(k[0]) is None:
#				N[k[0]] = {}
#			self.append_dict_Q(N[k[0]],Na[k[0]],k[1:],r)
#		else:
#			if N.get(k[0]) is None:
#				N[k[0]]=r
#			else:
#				N[k[0]]+=(r-N[k[0]])/(Na[k[0]])
			


	def print_n(self):
		for ele in self.N:

			for ele2 in self.N[ele]:
				print ele,ele2,self.N[ele][ele2]
				print ele,ele2,self.Q[ele][ele2], "\n"

#	def rollout(self, a_, t, s, h, d, abf,sb):
#
#		s0 = self.E(self.e_args)
#		s1 = self.E(self.e_args)
#		s2 = self.E(self.e_args)
#
#		s.imprint(s0)
#
#		if d>= self.H or t[1] is abf(s0):
#			return (0,0,h,s0)
#		else:
#			a = self.GetPrimitive(t,h,s,sb)
#			(self.sTemp,r1) = a_.simulate(a,s0)
#			self.sTemp.imprint(s1)
#			x = abf(s1)
#			(r2,n,h2,self.sTemp) = self.rollout(a_,t,s1,self.h_it(h+self.h_it(t[0]+t[1])+x),d+1,abf,sb)
#			self.sTemp.imprint(s2)
#			r = r1 + self.Gamma * r2
#			return (r,n+1,h2,s2)




#		for i in range(0, num_steps):
#			base_reward = environment_data_.get_reward()
#			agent_.simulate(randint(0,agent_.get_action_size()),s)
#			self.reward_list.append(environment_data_.get_reward()-base_reward)
			


