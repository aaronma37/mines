#!/usr/bin/env python

from ActionSpace import ActionSpace
from RewardPair import RewardPair
from Environment import Mines
#from Environment.Mines import Mine_Data
from random import randint
import random
from Agents import Action_Definition

import time
import xxhash

import math
import numpy as np


class supple_tree:

	def __init__(self):
		self.N={}#t,h
		self.Q={}#t,h,a
		self.Na={} #t,h,a

		self.Ni={}#{t,s}
		self.Qi={}#{t,s,a}
		self.Nai={}#{t,s,a}

	def step(self,T,N,Q,Na):
		#T : {t,h,a,s,next}	
		self.Ni={}#{t,s}
		self.Qi={}#{t,s,a}
		self.Nai={}#{t,s,a}	

		for node in T:
			self.add_to_init(node,N,Q,Na)
	
		return self.Qi

	def add_to_init(self,n,N,Q,Na):
		self.append_dict(self.Ni,(self.h_it(n[0][0]+n[0][1]),n[3]))		
		self.append_dict(self.Nai,(self.h_it(n[0][0]+n[0][1]),n[3],self.h_it(n[2][0]+n[2][1])))		
		self.append_dict(self.Qi,(self.h_it(n[0][0]+n[0][1]),n[3],self.h_it(n[2][0]+n[2][1])))		

		self.Ni[self.h_it(n[0][0]+n[0][1])][n[3]]+=N[self.h_it(n[0][0]+n[0][1])][n[3]]
		self.Nai[self.h_it(n[0][0]+n[0][1])][n[3]][self.h_it(n[2][0]+n[2][1])]+=Na[self.h_it(n[0][0]+n[0][1])][n[3]][self.h_it(n[2][0]+n[2][1])]

		self.Qi[self.h_it(n[0][0]+n[0][1])][n[3]][self.h_it(n[2][0]+n[2][1])]+=(Q[self.h_it(n[0][0]+n[0][1])][n[3]][self.h_it(n[2][0]+n[2][1])]*Na[self.h_it(n[0][0]+n[0][1])][n[3]][self.h_it(n[2][0]+n[2][1])]-self.Qi[self.h_it(n[0][0]+n[0][1])][n[3]][self.h_it(n[2][0]+n[2][1])])/(self.Nai[self.h_it(n[0][0]+n[0][1])][n[3]][self.h_it(n[2][0]+n[2][1])])



	def append_dict(self, N, k):
		if len(k) > 1:
			if N.get(k[0]) is None:
				N[k[0]] = {}
			self.append_dict(N[k[0]],k[1:])
		else:
			if N.get(k[0]) is None:
				N[k[0]]=0.0
			



	def h_it(self,string):
		return xxhash.xxh64(string).hexdigest()

	
