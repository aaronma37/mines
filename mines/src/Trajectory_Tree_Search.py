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

max_trajectory_size=1000


class TTS: 

	def __init__(self,L,max_interaction_num):
		self.L=L
		self.N={}
		self.Q={}
		self.naive_t=set()
		self.T=set()
		self.T_full=set()
		self.max_interaction_num=max_interaction_num

		self.W=set()
		self.Wp=set()


	def reset(self):
		self.W.clear()
		self.Wp.clear()
		self.N={}
		self.Q={}
		self.T.clear()
		self.T_full.clear()
		self.naive_t.clear()


	def execute(self,agent_loc,complete_environment,time_to_work,mcts):
		start = time.time()
		end = start

		initial_sub_environment=environment_classes.Sub_Environment()

		initial_sub_environment.region_list=[]
		initial_sub_environment.region_list.append(environment_classes.get_region(agent_loc[0],agent_loc[1]))

		initial_sub_environment.update_state(complete_environment)

		self.T.clear()
		self.T.add(initial_sub_environment)
		self.T_full.clear()


		'''
		while end - start < time_to_work:
			best_sub_environment = self.UCB()
		
			
			self.value_update(self.search(complete_environment,best_sub_environment,mcts))
			end = time.time()
		

		env = self.get_max(self.T_full)
		print "choose over", len(self.T_full), "sub-environments and found: ", self.Q[env.state]
		'''
		if self.get_max2(self.naive_t,mcts) == False:
			print "Using random trajectory :("
			env = self.get_random_sub_environment(agent_loc,complete_environment)
		else:
			env = self.get_max2(self.naive_t,mcts)
			#print "choose over", len(self.naive_t), "sub-environments and found: ", mcts.arg_max_reward(env.get_total_state())




		self.naive_t.clear()
		return env,self.get_trajectory(env.get_total_state(),mcts,env,complete_environment),mcts.arg_max_reward(env.get_total_state())

	def search(self,complete_environment,best_sub_environment,mcts):

		start=time.time()

	#	if best_sub_environment is None:
	#		return

		if best_sub_environment.get_k()>0:
			self.T.remove(best_sub_environment)

		start2=time.time()

		if best_sub_environment.get_k()==self.L-1:
			self.T_full.add(best_sub_environment)
		#	print best_sub_environment.state+best_sub_environment.interaction_state, mcts.arg_max_reward(best_sub_environment.state+best_sub_environment.interaction_state)
			return best_sub_environment,mcts.arg_max_reward(best_sub_environment.get_total_state())

		start3=time.time()

		children_sub_environments=self.get_children(mcts,complete_environment,best_sub_environment)
		
		start4=time.time()

		for c in children_sub_environments:
			if c.get_k()<=self.L-1:			
				self.T.add(c)

		start5=time.time()

		


		best_sub_environment = self.get_max(children_sub_environments)

		#print "1", (start2-start)/(time.time()-start), "2", (start3-start2)/(time.time()-start), "3", (start3-start4)/(time.time()-start), "4",(start4-start5)/(time.time()-start), "5",(start5-time.time())/(time.time()-start)

		return self.search(complete_environment,best_sub_environment,mcts)

	def get_children(self,mcts,complete_environment,best_sub_environment):

		children_sub_environments=[]
		for f_region in complete_environment.get_feasible_travel_paths(best_sub_environment.region_list[-1]):
			start=time.time()
			children_sub_environments.append(environment_classes.Sub_Environment())
			for r in best_sub_environment.region_list:
				children_sub_environments[-1].region_list.append(r)
			children_sub_environments[-1].region_list.append(f_region)
			children_sub_environments[-1].update_state(complete_environment)
			#if mcts.pre_Q.get(children_sub_environments[-1].state) is None:
			#	children_sub_environments=children_sub_environments[:-1]
			#	continue
			start2=time.time()
			
			if len(children_sub_environments[-1].interaction_set)<self.max_interaction_num and complete_environment.collective_trajectories_message is not None and complete_environment.cross_trajectory.get(f_region) is not None:
				for agent_id in complete_environment.cross_trajectory[f_region]:
					children_sub_environments.append(environment_classes.Sub_Environment())
					for r in best_sub_environment.region_list:
						children_sub_environments[-1].region_list.append(r)
					children_sub_environments[-1].region_list.append(f_region)
					children_sub_environments[-1].interaction_set.add(agent_id)	
					children_sub_environments[-1].update_state(complete_environment)

			'''
			
			if len(children_sub_environments[-1].interaction_set)<self.max_interaction_num and complete_environment.collective_trajectories_message is not None:
				for agent_trajectory in complete_environment.collective_trajectories_message.agent_trajectory:
					for region in agent_trajectory.region_trajectory:
						if f_region[0]==region.x and f_region[1]==region.y:
							children_sub_environments.append(environment_classes.Sub_Environment())
							for r in best_sub_environment.region_list:
								children_sub_environments[-1].region_list.append(r)
							children_sub_environments[-1].region_list.append(f_region)
							children_sub_environments[-1].interaction_set.add(agent_trajectory.frame_id)	
							children_sub_environments[-1].update_state(complete_environment)


							continue
			
			'''
			#print "1", (start2-start)/(time.time()-start), "2", (time.time()-start2)/(time.time()-start) 

		return children_sub_environments

	def UCB(self):
		return random.choice(tuple(self.T))

	def value_update(self,env_reward_pack):	
		for k in range(0,self.L):
			temp_state=env_reward_pack[0].cull_state_from_back(k)
			self.check_dict(self.N,temp_state,1.)
			self.N[temp_state]+=1
			self.check_dict(self.Q,temp_state,0.)
			self.Q[temp_state]+=(env_reward_pack[1]-self.Q[temp_state])/(self.N[temp_state])

	

	def get_max2(self,T,mcts):
		best_env=None
		max_expected=-1
		if len(T)==0:
			return False

		for sub_env in T:
			##print mcts.arg_max_reward(sub_env.get_total_state())
			if mcts.arg_max_reward(sub_env.get_total_state()) > max_expected:
				best_env=sub_env
				max_expected=mcts.arg_max_reward(sub_env.get_total_state())
	


		return best_env


	def get_max(self,T):
		best_env=None
		max_expected=-1
		if len(T)==0:
			return False

	
		'''
		for sub_env in T:

			self.check_dict(self.Q,sub_env.state,0.)

			if self.Q[sub_env.state] > max_expected:
				best_env=sub_env
				max_expected=self.Q[best_env.state]
		'''

		return best_env

	def check_dict(self,dict_name,state,default):
		if dict_name.get(state) == None:
			dict_name[state] = default

	def empty_environments(self):
		self.naive_t.clear()

	def get_random_sub_environment(self,agent_loc,complete_environment):

		sub_environment=environment_classes.Sub_Environment()
		sub_environment.set_random_region_list(environment_classes.get_region(agent_loc[0],agent_loc[1]),self.L)
		print self.max_interaction_num
		if complete_environment.collective_trajectories_message is not None:
			#print complete_environment.collective_trajectories_message
			for agent_trajectory in complete_environment.collective_trajectories_message.agent_trajectory:
				if len(sub_environment.interaction_set)<self.max_interaction_num:
					for r in sub_environment.region_list:
						for region in agent_trajectory.region_trajectory:
							if r[0]==region.x and r[1]==region.y:
								sub_environment.interaction_set.add(agent_trajectory.frame_id)	
		
						


		sub_environment.update_state(complete_environment)
		self.naive_t.add(sub_environment)
		#self.naive_Q[sub_environment.state]
		return sub_environment

	def SubEnvSearch(self,agent_loc,complete_environment,mcts):
		score=0
		best_sub_env=None		
		for sub_env in self.Wp:
			if mcts.QE[sub_env.get_total_state] > score:
				score=mcts.QE[sub_env.get_total_state]
				best_sub_env=sub_env

		return get_next_best_sub_environment(self,best_sub_env,agent_loc,complete_environment)


	def get_next_best_sub_environment(self,agent_loc,complete_environment):
		return		
		#self.Wp.add(environment_classes.get_valid_partial_environments(complete_environment))
		#get list of sub envs
		#add sub env list to partial set
		#remove current from partial set
		#find best in list of sub envs

		#return if || init sub

		#else repeat
						


		#sub_environment.update_state(complete_environment)
		#self.naive_t.add(sub_environment)
		#self.naive_Q[sub_environment.state]
		#return sub_environment

	def get_trajectory(self,save_state,mcts,env,complete_environment):
		save_state_copy=save_state	
		ordered_objective_type_list=[]	

		for k in range(self.L-1):	
			ordered_objective_type_list.append(mcts.arg_max(save_state_copy))


			interact_string=''
	
			for interact_string_by_agent in save_state_copy.split('|')[2].split('+')[:-1]:
				new_interact_string_by_agent=environment_classes.interact_string_evolve(interact_string_by_agent,ordered_objective_type_list[-1]) #similar to other evolve	
				interact_string=interact_string+new_interact_string_by_agent+'+'

			save_state_copy=environment_classes.string_evolve(save_state_copy,ordered_objective_type_list[-1])			
			save_state_copy=environment_classes.modify_interact_string(save_state_copy,interact_string)


		trajectory=task_classes.Trajectory(env,ordered_objective_type_list,complete_environment)
		return trajectory
			
			





			
				
