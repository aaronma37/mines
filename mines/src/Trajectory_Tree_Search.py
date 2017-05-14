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

class TTS: 

	def __init__(self,event_time_horizon):
		self.event_time_horizon=event_time_horizon
		self.N={}
		self.Q={}
		self.T=[]
		self.T_full=[]


	def reset(self):
		self.N={}
		self.Q={}
		self.T=[]
		self.T_full=[]


	def execute(self,complete_state,time_to_work):
		start = time.time()
		end = start

		self.T=[] #Tree
		self.T_full=[]


		while end - start < time_to_work:
			best_sub_environment = #UCB
						
			
			self.value_update(self.search(complete_state,best_sub_environment))

		return self.get_max_full(self.T_full),self.get_trajectory()

	def search(self,complete_state,best_sub_environment,T):
		children_sub_environments=self.get_children(complete_state,best_sub_environment)
		for c in children_sub_environments:
			self.T.append(c)

		self.T.remove(best_sub_environment)
	
		best_sub_environment = get_max(children_sub_environments)

		if best_sub_environment.get_k()>=L:
			return best_sub_environment,get_score(best_sub_environment)

		return self.search(complete_state,best_sub_environment)

	def get_children(self,complete_state,best_sub_environment):

	def UCB(self):
		return self.T[0]

	def value_update(self,best_sub_environment,r):
		for k in range(0,L):
			self.N[best_sub_environment.state[0:k]]+=1
			self.Q[best_sub_environment.state[0:k]]+=(r-self.Q[best_sub_environment.state[0:k]])/(self.N[best_sub_environment.state[0:k]])

	def get_max_full(self,T):\
		best_env=None
		max_expected=0
		
		for sub_env in T:
			if self.Q[sub_env] > max_expected:
				best_env=sub_env
				max_expected=self.Q[best_env]

		return best_env

	def get_random_sub_environment(self,agent,complete_state):
		sub_environment=environment_classes.Sub_Environment()
		sub_environment.set_random_region_list((agent.x,agent.y))
		sub_environment.update_state(complete_state)
		return sub_environment

	def get_trajectory(self,sub_environment,mcts):
		ordered_objective_type_list=[]				
		for k in range(L-1):	
			ordered_objective_type_list.append(mcts.arg_max(sub_environment.cull_state_from_front(k))) # an objective_type - string

		return task_classes.Trajectory(sub_environment,ordered_objective_type_list)
			
			





			
				
