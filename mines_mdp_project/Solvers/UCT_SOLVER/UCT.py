#!/usr/bin/env python

from ActionSpace import ActionSpace
from RewardPair import RewardPair
from Agents import Agent0
from Environment import Mines
from Environment.Mines import Mine_Data
from random import randint
from Agents import Action_Definition

import math
import numpy as np


class Solver: 


	def __init__(self,max_depth_,depth_,Gamma_,upper_confidence_c_,action_space_num_,map_size_):

		self.upper_confidence_c=upper_confidence_c_		
		self.action_space_num=action_space_num_



		self.pre_prime=31
		self.pre_result=11
		self.pre_hash_key=0

		self.hash = {-1:ActionSpace(upper_confidence_c_,action_space_num_)}
		self.max_depth=max_depth_
		self.depth=depth_
		self.reward_list=[]
		self.agent = Agent0.Agent(0,0,action_space_num_)#
		self.environment_data =Mine_Data(map_size_)#
		self.Gamma=Gamma_
		

	def get_best_action(self, agent_, environment_data_):
		
		self.pre_hash_key=self.hash_generator(agent_,environment_data_)
		if self.pre_hash_key in self.hash:
			return self.hash.get(self.pre_hash_key).get_best_action().get_action_index()
		else:
			print "Missing Hash"
			
			#print hash_key


		#uuv set location action


	def p_info(self, action_space_):
		print "printing rewards"
		for k,rp in action_space_.get_reward_pairs().items():
			print "action: ", Action_Definition.action_to_string(rp.get_action_index())
			print "visited: ", rp.get_visited(), "reward: ", rp.get_estimated_reward()
			print ""

	def get_best_action_and_step(self, agent_, environment_data_):
		
		self.pre_hash_key=self.hash_generator(agent_,environment_data_)
		if self.pre_hash_key in self.hash:
			agent_.step(self.hash.get(self.pre_hash_key).get_best_action().get_action_index(),environment_data_,False)
			agent_.update_history(self.hash.get(self.pre_hash_key).get_best_action().get_action_index(),self.hash_generator_without_history(agent_,environment_data_))
			#print self.p_info(self.hash.get(self.pre_hash_key))
		else:
			print "Missing Hash"
			print len(self.hash)
			for k,v in self.hash.items():
				print self.pre_hash_key
				print k
				print v



	def step(self, agent_, environment_data_,num_steps):

		#if self.hash_generator(agent_,environment_data_) in  self.hash:
		#print len(agent_.get_history())

		for i in range(0, num_steps):
			agent_.imprint(self.agent)
			environment_data_.imprint(self.environment_data)
			self.reward_list=[]
			self.execute(self.agent,self.environment_data,self.depth,0)

	def rollout(self, agent_, environment_data_,num_steps):
		for i in range(0, num_steps):
			base_reward = environment_data_.get_reward()
			agent_.step(randint(0,agent_.get_action_size()),environment_data_,True)
			self.reward_list.append(environment_data_.get_reward()-base_reward)
			
	
	def explore(self, ARP, agent_,environment_data_):
			base_reward = environment_data_.get_reward()
			agent_.step(ARP.get_action_index(),environment_data_,True)
			self.reward_list.append(environment_data_.get_reward()-base_reward)
			agent_.update_history(ARP.get_action_index(),self.hash_generator_without_history(agent_,environment_data_))

	def execute(self, agent_, environment_data_, depth_, iteration_):
		self.pre_hash_key=self.hash_generator(agent_,environment_data_)
		if self.pre_hash_key not in self.hash:
			self.hash[self.pre_hash_key] = ActionSpace(self.upper_confidence_c,self.action_space_num)

		cummulated_reward=0.

		ARP = self.hash.get(self.pre_hash_key).get_ucb()
		self.explore(ARP,agent_,environment_data_)

		if ARP.get_visited() > 1:
			if iteration_ < self.max_depth+depth_:
				self.execute(agent_,environment_data_,depth_,iteration_+1)
		else:
			self.rollout(agent_,environment_data_,depth_)

		if iteration_< self.max_depth:
			for i in range(iteration_, iteration_+depth_):
				cummulated_reward+=math.pow(self.Gamma,(i-iteration_))*self.reward_list[i]

		self.hash.get(self.pre_hash_key).visit(ARP,cummulated_reward)


	def hash_generator(self, agent_, environment_data_):	
		self.pre_result = 11
		
		self.pre_result = self.pre_result*self.pre_prime + environment_data_.get_hash()
		self.pre_result = self.pre_result*self.pre_prime + agent_.get_hash()
		self.pre_result = self.pre_result*self.pre_prime + agent_.get_hash_history()

		return self.pre_result

	def hash_generator_without_history(self, agent_, environment_data_):	
		self.pre_result = 11
		
		self.pre_result = self.pre_result*self.pre_prime + environment_data_.get_hash()
		self.pre_result = self.pre_result*self.pre_prime + agent_.get_hash()

		return self.pre_result


