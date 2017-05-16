#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
from sets import Set
import time
from random import shuffle
import task_classes

H=5
Gamma=.99

class Solver: 

	def __init__(self,event_time_horizon):
		self.event_time_horizon=event_time_horizon
		self.N={}
		self.Na={}
		self.Q={}

		self.great=[]
		self.great2=[]
		self.great3=[]
		self.steps=[]


	def reset(self):
		self.N={}
		self.Na={}#v.Na()
		self.Q={}#v.Q()



	def execute(self,agent,complete_environment,tts,time_to_work):
		start = time.time()
		end = start
		while end - start < time_to_work:
			sub_environment=tts.get_random_sub_environment(agent,complete_environment)
			#print sub_environment.state
			#print sub_environment.region_list
			self.search(sub_environment,complete_environment,0)
			end = time.time()




	def search(self,sub_environment,complete_environment,depth):

		save_state = sub_environment.state
		objective_type = self.arg_max_ucb(sub_environment,complete_environment)

		self.check_variables_init(save_state,objective_type)

		if objective_type!="wait" and objective_type!="travel":
			r = 1

			t=task_classes.tau(objective_type,sub_environment.get_objective_index(0,complete_environment.objective_map[objective_type]))
			#print sub_environment.get_objective_index(0,complete_environment.objective_map[objective_type]), "G UNIT", t
		else:
			if objective_type!="travel":
				r = 0
				t=100
			else:
				r = 0
				t=11

		
		#state,E = self.Phi.evolve(state,a,E)
		#t=task_classes.tau(objective_type,sub_environment.get_objective_index(0,complete_environment.objective_map[objective_type]))

		if t+depth>50:
			return 0


		evolved_sub_environment=sub_environment.evolve(complete_environment)

		r = math.pow(Gamma,t)*r + self.search(evolved_sub_environment,complete_environment,depth+t)

		self.Q[save_state][objective_type]+=(r-self.Q[save_state][objective_type])/self.Na[save_state][objective_type]
		#print save_state,objective_type,r

		return r

	
	

	def check_variables_init(self,save_state,objective_type):

		if self.N.get(save_state) == None:
			self.N[save_state] = 1.
		else:
			self.N[save_state]+= 1.

		if self.Na.get(save_state)==None:
			self.Na[save_state]={}
			self.Na[save_state][objective_type]=1.
		elif self.Na[save_state].get(objective_type)==None:
			self.Na[save_state][objective_type]=1.
		else:
			self.Na[save_state][objective_type]+=1.

		if self.Q.get(save_state) == None:
			self.Q[save_state]={}
			self.Q[save_state][objective_type]=0.
		elif self.Q[save_state].get(objective_type)==None:
			self.Q[save_state][objective_type]=0.
		


	def arg_max_reward(self,state):
		if self.Q.get(state)==None:
			self.Q[state]={}

		v=list(self.Q[state].values())

		if len(v)==0:
			return 0
		return max(v)

	def arg_max(self,state):
		if self.Q.get(state)==None:
			self.Q[state]={}

		v=list(self.Q[state].values())
		key=list(self.Q[state].keys())
		if len(key)==0:
			return 'wait'
		return key[v.index(max(v))]
			

	def arg_max_ucb(self,sub_environment,complete_environment):

		objective_type_list = task_classes.get_available_objective_types(sub_environment,complete_environment)

		shuffle(objective_type_list)

		if self.Q.get(sub_environment.state) is None:
			return objective_type_list[0]
		if self.Q[sub_environment.state].get(objective_type_list[0]) is None:
			return objective_type_list[0]

		max_a=objective_type_list[0]
		max_ucb=self.ucb_from_state(self.Q[sub_environment.state][max_a],self.N[sub_environment.state],self.Na[sub_environment.state][max_a])


		for a in objective_type_list:
			if self.Q[sub_environment.state].get(a) is None:
				return a

			if self.ucb_from_state(self.Q[sub_environment.state][a],self.N[sub_environment.state],self.Na[sub_environment.state][a])  > max_ucb:
				max_ucb = self.ucb_from_state(self.Q[sub_environment.state][a],self.N[sub_environment.state],self.Na[sub_environment.state][a]) 
				max_a=a

		return max_a


	def ucb_from_state(self,r,n,na):
		return r+1.94*math.sqrt(math.log(1+n)/(1+na))


