#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math



def get_norm_size(s):
	return 1./s

def get_sqr_loc(x,s):
	return 2.*x/s-1.



class Mine_Data: 

	def __init__(self, map_size):
		self.pre_num_unknown_locations=map_size*map_size
		self.seen = np.ndarray(shape=(map_size,map_size), dtype=int)
		self.temp_seen = np.ndarray(shape=(map_size,map_size), dtype=int)
		self.map_size=map_size

		self.middle=(self.map_size/2,self.map_size/2)
		self.max_reward=self.map_size*self.map_size
		self.reset()

	def reset(self):
		self.seen.fill(0)
		self.pre_num_unknown_locations=self.map_size*self.map_size


	def move(self):
		self.temp_seen=self.seen.copy()
		self.seen[1:][:] = self.temp_seen[:-1][:]


	def imprint(self, a):
		a.seen=self.seen.copy()
		a.pre_num_unknown_locations=self.pre_num_unknown_locations



	def get_reward(self):
		return self.max_reward-self.pre_num_unknown_locations

	def measure_loc(self, loc, imaginary):
		
		if self.check_boundaries(loc) is False:
			return

		if self.seen[loc[0]][loc[1]] is 1:
			return

		self.seen[loc[0]][loc[1]]=1
		self.pre_num_unknown_locations-= 1

	def check_boundaries(self, loc):
		if loc[0]<0 or loc[0] >= self.map_size:
			return False

		if loc[1]<0 or loc[1] >= self.map_size:
			return False

		return True
        	


	
					








