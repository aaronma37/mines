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
			a = self.arg_max_ucb(A)
		else:
			if A.battery.num==0:
				a=26
			else:
				a=0

		state=self.Phi.get_max_level(A)

		self.N.append_to(state,1.,self.Phi)
		self.Na.append_to(state,a,1.,self.Phi)
		self.Q.append_to(state,a,0.,self.Phi)

		
		#print pi_i,a,A.battery.num,A.location.loc

		r = A.evolve_all(self.H,a)
		#if a_.work_load[14]>1 and a == 15:
		#	print r, "ere", A.work_load[14].hash
			#r=.01
		for j in range(20):
			action_step=Policies.get_discrete_action(a_,s_,a)
			a_.execute(action_step,s_)


		r += math.pow(Gamma,depth)*self.search(A,depth+1,a,s_,a_)
		self.Q.append_to_average(state,a,r,self.Phi,self.Na)

		return r	

	def get_action(self,A):
		return self.arg_max(A)	

	def arg_max(self,A):
		return self.Pi.get(L_MAX,A,self.Phi,self.Psi)	

	def arg_max_ucb(self,A):

		pi=self.Pi.get(-1,A,self.Phi,self.Psi)

		for l in range(L_MAX+1):
			if self.Psi.check(l,pi) is False:
				return pi


			cluster = self.Psi.get_cluster(l,pi,A,self.Phi)
			n = cluster.get_total_n()		

			k = range(len(cluster.action_set))
			shuffle(k)
		
			if cluster.n[k[0]] == 0.0:
				return k[0]

			a=k[0]
			max_num = self.ucb_from_state(cluster.r[k[0]],n,cluster.n[k[0]])

			for i in k:
				if cluster.n[i] == 0.0:
					return i

				if self.ucb_from_state(cluster.r[i],n,cluster.n[i]) > max_num:
					max_num=self.ucb_from_state(cluster.r[i],n,cluster.n[i])
					a=i

			pi = a

		return a


	def ucb(self,A,a):
		return self.Q.get(A,self.Phi,a)+100.*math.sqrt(math.log(1+self.N.get(A,self.Phi))/(1+self.Na.get(A,self.Phi,a)))

	def ucb_from_state(self,r,n,na):
		return r+100.*math.sqrt(math.log(1+n)/(1+na))


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

