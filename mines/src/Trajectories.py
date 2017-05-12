#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
import Regions

traj_length=1

class Trajectory:
	def __init__(self,action_list):
		self.action_list=action_list
		self.current_index=0

	def update_completion(self,a,s):
		self.current_index=0
		for i in range(len(self.action_list)):
			if self.action_list[i].check_complete(a,s) == False:
				self.current_index=i
				break

	def get_action(self,a,s):
		self.update_completion(self,a,s)
		return self.action_list[self.current_index].get_next_action(a,s)
		


class Sub_Environment:
	def __init__(self,region_list,state_list,interaction_set):
		self.region_list=region_list
		self.state_list=state_list
		self.interaction_set=interaction_set 



	
					








