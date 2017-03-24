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


H=5
Gamma=.95

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
			self.search(0,self.A,0,26,self.environment_data,a_)
			end = time.time()


	def search(self,L,A,depth,last_action,s_,a_):

		A.update_all(s_,a_)

		if depth>H:
			return 0.
		
		if last_action!=0 or A.battery.num>90:
			a,roll = self.arg_max_ucb(L,A)
		else:
			if A.battery.num==0:
				a=26
			else:
				a=0


		pi_i=self.Pi.get(L,A,self.Phi,self.Psi)
		phi_i=self.Phi.get(L,A)

		self.N.append_to(L,pi_i,phi_i,1.)
		self.Na.append_to(L,pi_i,phi_i,a,1.)
		self.Q.append_to(L,pi_i,phi_i,a,0.)

		
		#print pi_i,a,A.battery.num,A.location.loc

		r = A.evolve_all(self.H,a)
		
		action_step=Policies.get_discrete_action(a_,s_,a)

		a_.execute(action_step,s_)


		r += math.pow(Gamma,depth)*self.search(L,A,depth+1,a,s_,a_)


		self.Q.append_to(L,pi_i,phi_i,a,(r-self.Q.get_direct(L,pi_i,phi_i,a))/self.Na.get_direct(L,pi_i,phi_i,a))

		return r	

	def get_action(self,L,A):
		return self.arg_max(L,A)	

	def arg_max(self,L,A):	
		#return self.Pi.get(L,A,self.Phi,self.Psi)

		if self.Psi.check(L,self.Pi.get(L,A,self.Phi,self.Psi)) is False:
			
			print "Did not find cluster", L, self.Pi.get(L,A,self.Phi,self.Psi)
			return self.Pi.get(L,A,self.Phi,self.Psi)

		if self.Q.check(L,self.Pi.get(L,A,self.Phi,self.Psi),self.Phi.get(L,A)) is False:
			print "Missing Q"	
			return self.Pi.get(L,A,self.Phi,self.Psi)


		
		v = self.Q.vals(L,A,self.Pi,self.Phi,self.Psi)
		k = self.Q.keys_(L,A,self.Pi,self.Phi,self.Psi)

		return self.Psi.get_max(L,self.Pi.get(L,A,self.Phi,self.Psi),self.Phi.get(L,A))




	def rollout(self,L,A,a,depth):
		r=0
		for i in range(depth,H):
			r+=math.pow(Gamma,depth)*A.evolve_all(self.H,a)
		print r
		return r

	def arg_max_ucb(self,L,A):	
		if self.Q.check(L,self.Pi.get(L,A,self.Phi,self.Psi),self.Phi.get(L,A)) is False:

			return self.Pi.get(L,A,self.Phi,self.Psi),False

		k=range(Policies.action_index_max)	
		shuffle(k)
		#return k[0]

		if self.Na.check(L,self.Pi.get(L,A,self.Phi,self.Psi),self.Phi.get(L,A),k[0]) is False:

			return k[0],False

		a=k[0]
		max_num=self.ucb(L,A,k[0])

		for i in k:
			if self.Na.check(L,self.Pi.get(L,A,self.Phi,self.Psi),self.Phi.get(L,A),i) is False:
				return i,False
			if self.ucb(L,A,i)>max_num:

				max_num=self.ucb(L,A,i)
				a = i

		return a,True

	def ucb(self,L,A,a):
		return self.Q.get(L,A,self.Pi,self.Phi,self.Psi,a)+100.*math.sqrt(math.log(1+self.N.get(L,A,self.Pi,self.Phi,self.Psi))/(1+self.Na.get(L,A,self.Pi,self.Phi,self.Psi,a)))


	def explore_ucb(self,L,A):
		k=range(26)
		shuffle(k)
		v=[]
		v.append(k[0])
		v.append(self.Pi.get(L,A,self.Phi,self.Psi))
		shuffle(v)
		return v[0]

	def get_psi(self,filename):
		self.Psi.load(filename)

	def update_psi(self):
		self.Psi.update(self.Q,self.Na)

	def write_file(self,data,steps,filename):

		self.write_performance(data,steps)
		file = open(filename,'w') 
		for k,v in self.Q.q.items():
			file.write("\n")
			for k2,v2 in self.Q.q[k].items():
				file.write("\n")
				for k3,v3 in self.Q.q[k][k2].items():
					file.write("\n")
					for k4,v4 in self.Q.q[k][k2][k3].items():
						file.write("Q"+","+str(k) + "," +  str(k2) + "," + str(k3) + "," + str(k4) + "," + str(v4) + "," + str(self.Na.na[k][k2][k3][k4]) + "," +  "\n")

	def write_performance(self,data,steps):
		self.great.append(data)
		self.steps.append(steps)

		file = open("/home/aaron/catkin_ws/src/mines/mines/src/performance.txt",'w') 

		for i in range(len(self.great)):
			file.write(str(self.great[i]) + ", " + str(self.steps[i])+ ", " + str(self.great[i]/self.steps[i]) +"\n")







		 
		file.close()

