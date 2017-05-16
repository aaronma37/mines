#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
from sets import Set
import time
from random import shuffle
import environment_classes
import task_classes

H=5
Gamma=.5

class TTS: 

	def __init__(self,L):
		self.L=L
		self.N={}
		self.Q={}
		self.T=[]
		self.T_full=[]


	def reset(self):
		self.N={}
		self.Q={}
		self.T=[]
		self.T_full=[]


	def execute(self,agent_loc,complete_environment,time_to_work,mcts):
		start = time.time()
		end = start

		initial_sub_environment=environment_classes.Sub_Environment()

		initial_sub_environment.region_list=[]
		initial_sub_environment.region_list.append(environment_classes.get_region(agent_loc[0],agent_loc[1]))

		initial_sub_environment.update_state(complete_environment)

		self.T=[] #Tree\
		self.T.append(initial_sub_environment)
		self.T_full=[]


		while end - start < time_to_work:
			best_sub_environment = self.UCB()
						
			
			self.value_update(self.search(complete_environment,best_sub_environment,mcts))
			end = time.time()

		return self.get_max(self.T_full),self.get_trajectory(self.get_max(self.T_full),mcts,complete_environment)

	def search(self,complete_environment,best_sub_environment,mcts):
		children_sub_environments=self.get_children(complete_environment,best_sub_environment)
		for c in children_sub_environments:
			self.T.append(c)

		self.T.remove(best_sub_environment)
		
		


		best_sub_environment = self.get_max(children_sub_environments)

		if best_sub_environment.get_k()>=self.L:
			self.T_full.append(best_sub_environment)
			return best_sub_environment,mcts.arg_max_reward(best_sub_environment.state)

		return self.search(complete_environment,best_sub_environment,mcts)

	def get_children(self,complete_environment,best_sub_environment):
		children_sub_environments=[]
		for f_region in complete_environment.get_feasible_travel_paths(best_sub_environment.region_list[-1]):
			children_sub_environments.append(environment_classes.Sub_Environment())
			children_sub_environments[-1].region_list=best_sub_environment.region_list
			children_sub_environments[-1].region_list.append(f_region)
			children_sub_environments[-1].update_state(complete_environment)
		return children_sub_environments

	def UCB(self):
		return self.T[0]

	def value_update(self,env_reward_pack):	
		for k in range(0,self.L):
			temp_state=env_reward_pack[0].cull_state_from_back(k)
			self.check_dict(self.N,temp_state,1.)
			self.N[temp_state]+=1
			self.check_dict(self.Q,temp_state,0.)
			self.Q[temp_state]+=(env_reward_pack[1]-self.Q[temp_state])/(self.N[temp_state])

	

	def get_max(self,T):
		best_env=None
		max_expected=-1
		print self.T_full		

		for sub_env in T:

			self.check_dict(self.Q,sub_env.state,0.)

			if self.Q[sub_env.state] > max_expected:
				best_env=sub_env
				max_expected=self.Q[best_env.state]

		return best_env

	def check_dict(self,dict_name,state,default):
		if dict_name.get(state) == None:
			dict_name[state] = default

	def get_random_sub_environment(self,agent,complete_environment):
		sub_environment=environment_classes.Sub_Environment()
		sub_environment.set_random_region_list(environment_classes.get_region(agent.x,agent.y),self.L)
		sub_environment.update_state(complete_environment)
		return sub_environment

	def get_trajectory(self,sub_environment,mcts,complete_environment):
		ordered_objective_type_list=[]				
		for k in range(self.L-1):	
			ordered_objective_type_list.append(mcts.arg_max(sub_environment.cull_state_from_back(k))) # an objective_type - string

		return task_classes.Trajectory(sub_environment,ordered_objective_type_list,complete_environment)
			
			





			
				
