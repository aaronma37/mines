#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math


region = [(10,10),(10,30),(10,50),(10,70),(10,90),(30,10),(50,10),(70,10),(90,10),(30,30),(50,30),(70,30),(90,30),(30,50),(50,50),(70,50),(90,50),(30,70),(50,70),(70,70),(90,70),(30,90),(50,90),(70,90),(90,90)]
region_size=10


class Mobile_Buoy_Environment: 

	def __init__(self, map_size):
		self.map_size=map_size
		self.score = []
		for i in range(len(region)):
			self.score.append(0)

	def calculate_region_score(self, agent_dict):
		for i in range(len(self.score)):
			self.score[i]=0.

		for k,a in agent_dict.items():
			self.score[self.get_region(a.x,a.y)]+=a.time_away_from_network

	def get_region(self,x,y):
		for i in range(len(region)):
			if x > region[i][0] -region_size and x <  region[i][0] +region_size:
				if y >  region[i][1] -region_size and y <  region[i][1] +region_size:
					return i

		return 0

	def reset(self):
		self.seen.fill(0)
		self.pre_num_unknown_locations=self.map_size*self.map_size



	def imprint(self, a):
		a.score = self.score



	def get_reward(self):
		return -sum(self.score)

	def measure_loc(self, region_index, imaginary):
		self.score[region_index]=0.

	def check_boundaries(self, loc):
		if loc[0]<0 or loc[0] >= self.map_size:
			return False

		if loc[1]<0 or loc[1] >= self.map_size:
			return False

		return True
        	


	
					








