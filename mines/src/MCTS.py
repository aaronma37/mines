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
import POMDP_Values as v
import abstraction_classes
import Objective
L_MAX=v.L_MAX

H=5
Gamma=.5

class Solver: 

	def __init__(self,event_time_horizon):
		self.event_time_horizon=event_time_horizon
		self.N=v.N()
		self.Na=v.Na()
		self.Q=v.Q()
		self.Phi=v.Phi(event_time_horizon)
		self.Psi=v.Psi()
		self.Pi=v.Pi()
		self.great=[]
		self.great2=[]
		self.great3=[]
		self.steps=[]
		self.A=Abstractions()

		self.agg_Q=v.Q()
		self.agg_N=v.N()
		self.agg_Na=v.Na()

	def reset(self):
		self.N=v.N()
		self.Na=v.Na()
		self.Q=v.Q()
		self.Phi=v.Phi(self.event_time_horizon)
		self.Psi=v.Psi()
		self.Pi=v.Pi()
		self.H=heuristic()
		self.A=Abstractions()
		self.T={}


	def execute(self,agent,complete_state,tts,time_to_work):
		start = time.time()
		end = start
		while end - start < time_to_work:
			sub_environment=tts.get_random_sub_environment(agent,complete_state)
			self.search(sub_environment,0)
			end = time.time()




	def search(self,sub_environment,depth):

		save_state = sub_environment.state
		objective_type = self.arg_max_ucb(save_state)

		self.check_variables_init(save_state)

		if objective_type!="wait" and objective_type!="travel":
			r = 1
		else:
			r = 0

		#state,E = self.Phi.evolve(state,a,E)
		t=task_classes.tau(objective_type,sub_environment.region_list[0],sub_environment.region_list[1])

		if t+depth>H:
			return 0

		r = math.pow(Gamma,t)*r + self.search(state,E,depth+t)

		self.Q.append_to_average(save_state,objective_type,r,self.Phi,self.Na)


		return r

	

	def check_variables_init(self,save_state,objective_type):
		self.N.append_to(save_state,1.,self.Phi)
		self.Na.append_to(save_state,objective_type,1.,self.Phi)
		self.Q.append_to(save_state,objective_type,0.,self.Phi)	


	def arg_max(self,state):
		v=list(self.Q.q[state].values())
		key=list(self.Q.q[state].keys())
		return key[v.index(max(v))]
			

	def arg_max_ucb(self,sub_environment):

		objective_type_list = task_classes.get_available_objective_types(sub_environment)

		shuffle(objective_type_list)

		if self.Q.q[sub_environment.state].get(objective_type_list[0]) is None:
			return objective_type_list[0]

		max_a=objective_type_list[0]
		max_ucb=self.ucb_from_state(self.agg_Q.q[sub_environment.state][max_a],self.agg_N.n[sub_environment.state],self.agg_Na.na[sub_environment.state][max_a])


		for a in objective_type_list:
			if self.agg_Q.q[sub_environment.state].get(a) is None:
				return a

			if self.ucb_from_state(self.agg_Q.q[sub_environment.state][a],self.agg_N.n[sub_environment.state],self.agg_Na.na[sub_environment.state][a])  > max_ucb:
				max_ucb = self.ucb_from_state(self.agg_Q.q[sub_environment.state][a],self.agg_N.n[sub_environment.state],self.agg_Na.na[sub_environment.state][a]) 
				max_a=a

		return max_a


	def ucb_from_state(self,r,n,na):
		return r+1.94*math.sqrt(math.log(1+n)/(1+na))


