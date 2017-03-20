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



		self.H=heuristic()
		Heuristics.load_file(self.H,'testfile.txt')
		self.A=Abstractions()
		self.environment_data=E(e_args)



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

			self.A.update_all(self.environment_data,a_)

			self.search(0,self.A)
			end = time.time()


	def search(self,L,A):


		a = self.arg_max_ucb(L,A)
		r = A.evolve_all(self.H,a)
		if a!=0:
			r += math.pow(Gamma,self.search(L,A))

		self.N.append_to(L,A,self.Pi,self.Phi,self.Psi,1.)
		self.Na.append_to(L,A,self.Pi,self.Phi,self.Psi,a,1.)
		self.Q.append_to(L,A,self.Pi,self.Phi,self.Psi,a,0.)
		self.Q.append_to(L,A,self.Pi,self.Phi,self.Psi,a,(r-self.Q.get(L,A,self.Pi,self.Phi,self.Psi,a))/self.Na.get(L,A,self.Pi,self.Phi,self.Psi,a))

		return r	

	def get_action(self,L,A):
		return self.arg_max(L,A)	

	def arg_max(self,L,A):
		return self.Pi.get(L,A,self.Phi,self.Psi)

		if self.Q.check(L,A,self.Pi,self.Phi,self.Psi) is False:
			return self.Pi.get(L,A,self.Phi,self.Psi)


		v = self.Q.vals(L,A,self.Pi,self.Phi,self.Psi)
		k = self.Q.keys_(L,A,self.Pi,self.Phi,self.Psi)


		return k[v.index(max(v))]




	def arg_max_ucb(self,L,A):	
		if self.Q.check(L,A,self.Pi,self.Phi,self.Psi) is False:
			return self.Pi.get(L,A,self.Phi,self.Psi)

		k=range(Policies.action_index_max)	
		shuffle(k)
		return k[0]
		if self.Na.check(L,A,self.Pi,self.Phi,self.Psi,k[0]) is False:
			return k[0]

		a=k[0]
		max_num=self.ucb(L,A,k[0])

		for i in k:
			if self.Na.check(L,A,self.Pi,self.Phi,self.Psi,i) is False:
				return i
			if self.ucb(L,A,i)>max_num:

				max_num=self.ucb(L,A,i)
				a = i
		return a

	def ucb(self,L,A,a):
		return self.Q.get(L,A,self.Pi,self.Phi,self.Psi,a)+1000000.*math.sqrt(math.log(1+self.N.get(L,A,self.Pi,self.Phi,self.Psi))/(1+self.Na.get(L,A,self.Pi,self.Phi,self.Psi,a)))


	def write_file(self,Q,N,Na,val):

		self.great.append(val)

		file = open('Q.txt','w') 

		for i in self.great:
			file.write(str(i) + "\n")

		for k,v in Q.items():
			for k2,v2 in Q[k].items():
				for k3,v3 in Q[k][k2].items():
					file.write("Q"+","+str(k) + "," +  str(k2) + "," + str(k3) + "," + str(v3) + "," +  str(Na[k][k2][k3]) + "\n")

		for k,v in Q.items():
			for k2,v2 in Q[k].items():
				file.write("N"+","+str(k) + "," +  str(k2) + ","  + str(v3) + "," +  str(N[k][k2]) + "\n")


		 
		file.close()

