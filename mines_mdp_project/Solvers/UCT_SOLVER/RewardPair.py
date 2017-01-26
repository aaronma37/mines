#!/usr/bin/env python

import numpy as np


class RewardPair: 


	def __init__(self,action_index_):
		self.reward=0.
		self.visited=0.
		self.action_index=action_index_
		self.last_reward=0

	
	def visit(self, reward_):
		#self.visited+=1
		self.reward+=reward_
		self.last_reward=reward_

	def get_estimated_reward(self):
		if self.visited > 0:
			return self.reward/self.visited
		else:
			return 0

	def get_last_reward(self):
		return last_reward

	def clear_RP(self):
		self.reward=0
		self.visited=0
		self.last_reward=0


	def get_action_index(self):
		return self.action_index

	def get_visited(self):
		return self.visited
	
	def add_visit(self):
		self.visited+=1


