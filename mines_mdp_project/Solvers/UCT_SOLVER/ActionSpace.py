#!/usr/bin/env python

from RewardPair import RewardPair

import math

class ActionSpace: 


	def __init__(self,c_,action_space_num):
		self.reward_pair_dict={0:RewardPair(0)}
		self.visited=0
		self.c=c_
		
		for i in range(1, action_space_num):
			self.reward_pair_dict[i]=RewardPair(i)



	def get_best_action(self):
		best_action=self.reward_pair_dict.get(0)
		max = best_action.get_estimated_reward()

		for k,ap in self.reward_pair_dict.items():
			if ap.get_estimated_reward()>max:
				best_action=ap
				max=best_action.get_estimated_reward()

		self.visited +=1
		return best_action
		

	def get_ucb(self):
		self.visited+=1
		best_action=self.reward_pair_dict.get(0)
		max = -10 #best_action.get_estimated_reward()+self.c*math.sqrt(math.log(self.visited)/best_action.visited)

		for k,ap in self.reward_pair_dict.items():
			if int(ap.get_visited()) is 0:
				best_action=ap
				best_action.add_visit()
				return best_action


			if ap.get_estimated_reward()+self.c*math.sqrt(math.log(self.visited)/ap.get_visited())>max:
				best_action=ap
				max=best_action.get_estimated_reward()+self.c*math.sqrt(math.log(self.visited)/ap.get_visited())

		best_action.add_visit()
		return best_action

	def get_action_reward(self, i):
		return self.reward_pair_dict.get(i).get_estimated_reward()

	def visit(self, ap, reward):
		ap.visit(reward)

	def get_reward_pairs(self):
		return self.reward_pair_dict

		
