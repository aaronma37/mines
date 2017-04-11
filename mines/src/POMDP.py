#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
from abstraction_classes import Abstractions
from Heuristics import heuristic
import Heuristics
from sets import Set
import time
import Policies
from random import shuffle
import POMDP_Values as v
import abstraction_classes
L_MAX=v.L_MAX

H=5
Gamma=.5

class Solver: 

	def __init__(self,E,e_args):
		self.N=v.N()
		self.Na=v.Na()
		self.Q=v.Q()
		self.Phi=v.Phi()
		self.Psi=v.Psi()
		self.Pi=v.Pi()
		self.great=[]
		self.steps=[]
		self.T={}


		self.H=heuristic()
		#Heuristics.load_file(self.H,'testfile_d.txt')
		self.A=Abstractions()
		self.environment_data=E(e_args)
		self.mini_ab=abstraction_classes.mini_ab()
		#self.get_psi('/home/aaron/catkin_ws/src/mines/mines/src/psi_main.txt')

	def reset(self):
		self.N=v.N()
		self.Na=v.Na()
		self.Q=v.Q()
		self.Phi=v.Phi()
		self.Psi=v.Psi()
		self.Pi=v.Pi()
		self.H=heuristic()
		self.A=Abstractions()
		self.T={}


	def OnlinePlanning(self,A,time_to_work):
		start = time.time()
		end = start
		cc=0
		while end - start < time_to_work:
			seed=randint(0,999)
			state=self.Phi.get_state(A,seed)
			self.search(state,0)
			end = time.time()
			cc+=1



	def search(self,state,depth):
		if depth>=H:
			return 0.

		a = self.arg_max_ucb()
		save_state = state
		self.N.append_to(save_state,1.,self.Phi)
		self.Na.append_to(save_state,a,1.,self.Phi)
		self.Q.append_to(save_state,a,0.,self.Phi)

		r = self.Phi.get_reward(state,a)
		state = self.Phi.evolve(state,a)
		r += Gamma*self.search(state,depth+1)

		self.Q.append_to_average(save_state,a,r,self.Phi,self.Na)
		return r	

	def get_action(self,A,next_expected_action):
		return self.Pi.get_and_return_level(A,self.Psi,self.Phi,next_expected_action)

	def arg_max(self,A):
		return self.Pi.get(L_MAX,A,self.Phi,self.Psi)	

	def rollout(self,A):
		return A.get_max_reward_funct()

	def arg_max_ucb(self):
		i = randint(0,1)
		if i == 0:
			return "charge"
		elif i==1:
			return "explore"

	def ucb(self,A,a):
		return self.Q.get(A,self.Phi,a)+100.*math.sqrt(math.log(1+self.N.get(A,self.Phi))/(1+self.Na.get(A,self.Phi,a)))

	def ucb_from_state(self,r,n,na):
		return r+100.*math.sqrt(math.log(1+n)/(1+na))


	def get_psi(self,filename):
		self.Psi.load(filename)

	def update_psi(self):
		self.Psi.update(self.Q,self.Na)

	def write_file(self,filename):
		self.Q.write_q(filename,self.Na)

	def write_performance(self,fp,data,steps):
		self.great.append(data)
		self.steps.append(steps)

		file = open(fp+'/performance.txt','w') 
		for i in range(len(self.great)):
			if self.steps[i] > 0:
				file.write(str(self.great[i]/self.steps[i]) +"\n")
			else:
				file.write(str(0) +"\n")
		file.close()

