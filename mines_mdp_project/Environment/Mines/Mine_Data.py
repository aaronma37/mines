#!/usr/bin/env python


from Location import Location
from random import randint
import xxhash
import random
import numpy as np


class Mine_Data: 

	def __init__(self, map_size):
		self.h = xxhash.xxh64
		self.pre_num_unknown_locations=map_size*map_size
		self.pre_prime=13
		self.pre_result=1

		self.PFS = np.ndarray(shape=(map_size,map_size), dtype=float)
		self.color = np.ndarray(shape=(map_size,map_size), dtype=float)
		self.seen = np.ndarray(shape=(map_size,map_size), dtype=bool)

		self.map_size=map_size
		self.mine_location = Location(randint(0,self.map_size-1),randint(0,self.map_size-1))
		self.complete=True
		self.max_reward=self.map_size*self.map_size
		self.reset()

	def get_mine_location(self):
		return self.mine_location

	def reset(self):

		self.PFS = np.ndarray(shape=(self.map_size,self.map_size), dtype=float)
		self.PFS.fill(1.0/(self.map_size*self.map_size))
		self.color.fill(1.0)
		self.seen.fill(False)


		self.mine_location = Location(randint(0,self.map_size-1),randint(0,self.map_size-1))
		self.complete=False
		self.pre_num_unknown_locations=self.map_size*self.map_size


	def update_probabilities(self):
		self.PFS.fill(1./self.pre_num_unknown_locations)

	def get_hash(self):

		return xxhash.xxh64(self.seen).hexdigest()

#		self.pre_result=1
#		for i in range(0, self.map_size):	
#			for j in range(0, self.map_size):	
#				if self.seen[i][j] is False:
#					self.pre_result = self.pre_prime*self.pre_result+1
#				else:
#					self.pre_result = self.pre_prime*self.pre_result+2
#
		#return self.pre_result

	def set_complete(self, complete_):
		self.complete=complete_

	def get_complete(self):
		return self.complete

	def set_pre_unknown(self, num):
		self.pre_num_unknown_locations = num

	def imprint(self, a):
		a.set_complete(self.complete)
		a.mine_location.set_x(self.mine_location.get_x())
		a.mine_location.set_y(self.mine_location.get_y())
		a.max_reward = self.max_reward
		a.PFS=self.PFS.copy()
		a.seen=self.seen.copy()


		#for i in range(0, self.map_size):	
		#	for j in range(0, self.map_size):
		#		a.PFS[i][j] =  self.PFS[i][j]
		#		a.seen[i][j]= self.seen[i][j]

		a.set_pre_unknown(self.pre_num_unknown_locations)


	def get_reward(self):
		if self.complete is True:
			return self.max_reward
		return self.max_reward-self.pre_num_unknown_locations




	def measure_loc(self, loc, imaginary):
		
		if self.check_boundaries(loc) is False:
			return

		if bool(self.seen[loc.get_x()][loc.get_y()]) is True:
			return


		self.seen[loc.get_x()][loc.get_y()]=True


		if imaginary is False:
			if self.complete is True:
				return
			if self.mine_location.get_x() is loc.get_x() and self.mine_location.get_y() is loc.get_y():

				self.PFS.fill(0.0)
				self.color.fill(0.0)

				self.PFS[loc.get_x()][loc.get_y()] = 1.0
				self.color[loc.get_x()][loc.get_y()] = 1.0

	
				self.complete = True
				self.pre_num_unknown_locations=1
			
			else:	
				self.PFS[loc.get_x()][loc.get_y()]=0.0
				self.color[loc.get_x()][loc.get_y()]=0.0
				self.pre_num_unknown_locations-= 1
				self.update_probabilities()

		else:
			if self.complete is True:
				return
			if self.PFS[loc.get_x()][loc.get_y()] > random.random():
				self.PFS.fill(0.0)
				self.color.fill(0.0)

				self.PFS[loc.get_x()][loc.get_y()] = 1.0
				self.color[loc.get_x()][loc.get_y()] = 1.0

	
				self.complete = True
				self.pre_num_unknown_locations=1

        		else:
        			self.PFS[loc.get_x()][loc.get_y()]=0.0
    				self.color[loc.get_x()][loc.get_y()]=0.0
				self.pre_num_unknown_locations-=1
        			self.update_probabilities()

	def check_boundaries(self, loc):
		if loc.get_x()<0 or loc.get_x() >= self.map_size:
			return False

		if loc.get_y()<0 or loc.get_y() >= self.map_size:
			return False

		return True
        	
    	

	def print_mine_location(self):
		print self.mine_location.get_x()
		print self.mine_location.get_y()
		print(self.PFS)

	def get_color(self,x_,y_):
		return self.PFS[x_][y_]



	
					








