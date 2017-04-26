#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
import Regions


def get_norm_size(s):
	return 1./s

def get_sqr_loc(x,s):
	return 2.*x/s-1.

class Charging_Dock:
	def __init__(self, location):
		self.coordinates=location
		self.size=5.

class Mine:
	def __init__(self, location):
		self.coordinates=location
		self.size=3.
		


class Mine_Data: 

	def __init__(self, map_size,number_of_charging_docks,number_of_mines):
		self.number_of_charging_docks=number_of_charging_docks
		self.number_of_mines=number_of_mines
		self.pre_num_unknown_locations=map_size*map_size
		self.seen = np.ndarray(shape=(map_size,map_size), dtype=int)
		self.temp_seen = np.ndarray(shape=(map_size,map_size), dtype=int)
		self.map_size=map_size

		self.charging_docks=[]
		for i in range(self.number_of_charging_docks):
			self.charging_docks.append(Charging_Dock((50,50)))

		self.mines=[]
		for i in range(number_of_mines):
			self.mines.append(Mine((50,50)))

		self.middle=(self.map_size/2,self.map_size/2)
		self.max_reward=self.map_size*self.map_size
		self.reset()
		self.occupied = []
		self.NOT_SEEN=0
		self.SEEN=1
		self.init_reward

		for i in range(25):
			self.occupied.append(0)

	def reset(self):

		self.pre_num_unknown_locations=self.map_size*self.map_size
		self.seen=np.random.randint(1, size=(self.map_size,self.map_size))
		
		for i in range(25):
			k= random.randint(0, 3)
			if k == 3:
				chance=1.
			elif k==2:
				chance=.66
			elif k==1:
				chance=.33	
			else:
				chance=0.

			for region in Regions.region_list[i]:
				if random.random() < chance:
					self.seen[region[0]][region[1]]=1
				
		
		self.charging_docks=[]
		for i in range(self.number_of_charging_docks):
			self.charging_docks.append(Charging_Dock((random.randint(0, self.map_size),random.randint(0, self.map_size))))	

		self.mines=[]
		for i in range(self.number_of_mines):
			self.mines.append(Mine((random.randint(0, self.map_size),random.randint(0, self.map_size))))	


		self.pre_num_unknown_locations-=self.seen.sum()
		self.init_reward=self.seen.sum()


	def get_region_score(self,x_l,y_l):
		#x_l is of xmin xmax
		score =0.
		size=0.
		for i in range(x_l[0],x_l[1]):
			for j in range(y_l[0],y_l[1]):	
				size+=1.
				if self.seen[i][j] == 0:		
					score+=1.

		return math.ceil(3.*score/size)



	def calculate_occupied(self,agent_dict,region,r_size):
		self.occupied=[]
		for i in range(25):
			self.occupied.append(0)

		for k,a in agent_dict.items():
			for i in range(len(region)):
				if a.x > region[i][0] -r_size and a.x <  region[i][0] +r_size+1:
					if a.y >  region[i][1] -r_size and a.y <  region[i][1] +r_size+1:
						self.occupied[i]=1
						break


	def move(self):
		self.temp_seen=self.seen.copy()
		self.seen[1:][:] = self.temp_seen[:-1][:]

	def update_charging_dock_locations(self,x,y):
		self.charging_docks=[]
		for i in range(len(x)):
			self.charging_docks.append(Charging_Dock((x[i],y[i])))		

	def update_mine_locations(self,x,y):
		self.mines=[]
		for i in range(len(x)):
			self.mines.append(Mine((x[i],y[i])))	

	def imprint(self, a):
		a.seen=self.seen.copy()
		a.pre_num_unknown_locations=self.pre_num_unknown_locations
		a.occupied=self.occupied
		a.charging_docks=self.charging_docks
		a.number_of_charging_docks=self.number_of_charging_docks
		a.mines=self.mines



	def get_reward(self):
		return self.max_reward-self.pre_num_unknown_locations

	def measure_loc(self, loc, imaginary):
		
		if self.check_boundaries(loc) is False:
			return

		if self.seen[loc[0]][loc[1]] == 1:
			return

		self.seen[loc[0]][loc[1]]=1
		self.pre_num_unknown_locations-= 1


	def check_boundaries(self, loc):
		if loc[0]<0 or loc[0] >= self.map_size:
			return False

		if loc[1]<0 or loc[1] >= self.map_size:
			return False

		return True
        	


	
					








