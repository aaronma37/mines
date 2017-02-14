#!/usr/bin/env python


from Mines import Mine_Data
from Mines import Location_Image_Info
from random import randint
import numpy as np


class Environment: 


	def __init__(self, map_size):
		self.map_size=map_size
		self.loc_img_info = np.empty((map_size, map_size), dtype=object)
		self.mine_data = Mine_Data(self.map_size)
		self.add_img_info = np.empty((map_size, map_size), dtype=object)
		for i in range(0, self.map_size):
			for j in range(0, self.map_size):
				self.loc_img_info[i][j] = Location_Image_Info(2.*i/self.map_size-1., 2.*j/self.map_size-1.,1./self.map_size,1./self.map_size)
				#self.loc_img_info[i][j] = Location_Image_Info(i/10.-1.+1./20., j/10.-1.+1./20.,1./20.,1./20.)


	

	def get_mine_data(self):
		return self.mine_data

	def get_norm_size(self):
		return 1./self.map_size

	def get_sqr_loc(self,x):
		return 2.*x/self.map_size-1.

	def get_loc_info(self,x,y):
		return self.loc_img_info[x][y]

	def get_mine_data(self):
		return self.mine_data


					








