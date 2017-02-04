#!/usr/bin/env python

from Action_Definition import get_transition_x
from Action_Definition import get_transition_y
from Environment.Mines import Location
from Environment.Mines import Mine_Data
from random import randint
from Solvers.POMCP_RUSSEL import POMCP_R
import xxhash
import math
import time


import numpy as np



class Agent: 


	def __init__(self):
		self.nodes=[]
		self.connections=[]
		self.node_count=0
		self.T_list=[]
		self.N={}
		self.Na={{}}
		self.Q={{}}
		self.threshold=100
	
	def run(self,T,D):
		self.nodes=[]
		self.connections={}
		self.node_count=0
		self.T_list=[]

		#T is a set nodes, A: has h~ history hash, x ~ state, c ~ children
		#c is {a:(h,X)}
		#D ~ Learned data, N(h), Na(h,a), Q(h,a))

		for A in T:
			self.connections.append(0)
		for A in T:
			for B in T:
				if self.check_similarity(A,B) is True:
						self.add_connection(A,B)

	def check_similarity(self,A,B):
		if A[1] is not B[1]:
			return False
		
		for a in actions:
			if A[2].get(a) is not None and B[2].get(a) is not None:
				if math.abs(Q[A[0][a] - Q[A[0]][a]) >= threshold or check_similarity(T[A[2][a][0]], T[B[2]][a][0]) is False:
					return False

		return True
					

	def add_connection(self,A,B):
		if self.connections.get(A.h) is not None:
			self.connections[B.h] = self.connections.get(A.h)
			self.merge(self.T_list[self.connections.get(A.h)],B)
		else:
			self.T_list.append(self.node_init(len(self.T_list),A.x))
			self.connections[A.h] = len(self.T_list)-1
			self.merge(self.T_list[self.T_list-1],A)
			self.connections[B.h] = len(self.T_list)-1
			self.merge(self.T_list[self.T_list-1],B)
			
	
	def node_init(self, h, x):
		n= (h,x,{})
		if self.N.get(h) is None:
			self.N.get(h) = 0	
		return n

	
	def merge(self, n, A):
		self.N(n[0])+=N[A[0]]

		for k,v in A[2]:
			if n[2].get(k) is None:
				child=node_init(self,self.h_it(n[0]+k+v[1]),v[1])
				n[2][k]=(self.h_it(n[0]+k+v[1]),v[1])
			else:
				child=n[2].get(k)

			if Na[A[0]].get(k) is not None:
				if self.Na[n[0]][k] is None:
					self.Na[n[0]][k]=0.	
		
				self.Na[n[0]][k]+=Na[A[0]][k]

			if Q[A[0]].get(k) is not None:
				if self.Q[n[0]][k] is None:
					self.Q[n[0]][k]=0.

				self.Q[n[0]][k]+=(Q[A[0]][k]self.Q[n[0]][k])/self.Na[n[0]][k]

			self.merge(child,T[v[0]])				

		
		
