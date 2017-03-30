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



		self.H=heuristic()
		#Heuristics.load_file(self.H,'testfile_d.txt')
		self.A=Abstractions()
		self.environment_data=E(e_args)
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


	def OnlinePlanning(self,agent_,s,a_,time_to_work):
		start = time.time()
		end = start
		agent_.imprint(a_)
		x=agent_.x
		y=agent_.y
		s.imprint(self.environment_data)
		
		while end - start < time_to_work:
			agent_.imprint(a_)
			s.imprint(self.environment_data)
			self.action_counter=0
			#print "start"
			self.A.update_all(self.environment_data,a_)
			#print self.A.get_explore_abf()
			self.search(self.A,0,26,self.environment_data,a_)
			end = time.time()


	def search(self,A,depth,last_action,s_,a_):

		A.update_all(s_,a_)

		if depth>H:
			return 0.
		
		if last_action!=0 or A.battery.num>90:
			a,roll = self.arg_max_ucb(A)
		else:
			if A.battery.num==0:
				a=26
			else:
				a=0


		#pi_i=self.Pi.get(L,A,self.Phi,self.Psi)
		phi_i=self.Phi.get_max_level(A)

		self.N.append_to(phi_i,1.)
		self.Na.append_to(phi_i,a,1.)
		self.Q.append_to(phi_i,a,0.)

		
		#print pi_i,a,A.battery.num,A.location.loc

		r = A.evolve_all(self.H,a)
		#if a_.work_load[14]>1 and a == 15:
		#	print r, "ere", A.work_load[14].hash
			#r=.01
		for j in range(20):
			action_step=Policies.get_discrete_action(a_,s_,a)
			a_.execute(action_step,s_)


		r += math.pow(Gamma,depth)*self.search(A,depth+1,a,s_,a_)

		self.Q.append_to(phi_i,a,(r-self.Q.get_direct(phi_i,a))/self.Na.get_direct(phi_i,a))

		return r	

	def get_action(self,A):
		return self.arg_max(A)	

	def arg_max(self,A):
		return self.Pi.get(L_MAX,A,self.Phi,self.Psi)	

	def arg_max_ucb(self,A):

		#NOTE: MAKE THIS REFLECT LEVELS (UCB FROM BOTTOM UP)
	
		if self.Q.check(self.Phi.get_max_level(A)) is False:
			return self.Pi.get(L_MAX,A,self.Phi,self.Psi),False

		k=range(Policies.action_index_max)	
		shuffle(k)
		#return k[0]

		if self.Na.check(self.Phi.get(L_MAX,A),k[0]) is False:

			return k[0],False

		a=k[0]
		max_num=self.ucb(A,k[0])

		for i in k:
			if self.Na.check(self.Phi.get(L_MAX,A),i) is False:
				return i,False
			if self.ucb(A,i)>max_num:

				max_num=self.ucb(A,i)
				a = i
		return a,True

	def ucb(self,A,a):
		return self.Q.get(A,self.Phi,a)+100.*math.sqrt(math.log(1+self.N.get(A,self.Phi))/(1+self.Na.get(A,self.Phi,a)))


	def get_psi(self,filename):
		self.Psi.load(filename)

	def update_psi(self):
		self.Psi.update(self.Q,self.Na)

	def write_file(self,data,steps,filename):
		self.write_performance(data,steps)
		self.Q.write_q(filename,self.Na)

	def write_performance(self,data,steps):
		self.great.append(data)
		self.steps.append(steps)

		file = open("/home/aaron/catkin_ws/src/mines/mines/src/performance.txt",'w') 

		for i in range(len(self.great)):
			file.write(str(self.great[i]) + ", " + str(self.steps[i])+ ", " + str(self.great[i]/self.steps[i]) +"\n")

		file.close()

