#!/usr/bin/env python
from random import shuffle
class Pi:
	def __init__(self):
		print "initializing Pi"

	def seed_algorithm(self,A):
		rewards=[]
		for i in range(26):
			rewards.append(A.get_inherent_reward_func(i))

		#print  rewards.index(max(rewards)), max(rewards)
		return rewards.index(max(rewards))

	def get(self,L,A,Phi,Psi):
		if L == 0:
			#print self.seed_algorithm(A), A.get_explore_abf(), A.battery.val
			return self.seed_algorithm(A)
		else:
			return Psi.get(L-1,A,self,Phi.get(L,A))

class Phi:
	def __init__(self):
		print "initializing Phi"
		#Phi maps A->A*

	def get(self,L,A):
		return A.get_explore_abf()

class Psi:
	def __init__(self):
		print "initializing Psi"
		self.psi={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)]->a

	def get(self,L,A,pi,phi):
		return self.psi[L][pi.get(L,A,phi,psi)][phi.get(L,A)]

class Q:
	def __init__(self):
		print "initializing Q"
		self.q={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)][a]->r

	def get(self,L,A,pi,phi,psi,a):
		return self.q[L][pi.get(L,A,phi,psi)][phi.get(L,A)][a]

	def check(self,L,pi,phi):
		if self.q.get(L) is None:
			return False
			#self.q[L]={pi.get(L,A,phi,psi):{phi.get(L,A):{a:r}}}	
		elif self.q[L].get(pi) is None:
			return False
		elif self.q[L][pi].get(phi) is None:
			return False
		return True
	
	def vals(self,L,A,pi,phi,psi):
		return list(self.q[L][pi.get(L,A,phi,psi)][phi.get(L,A)].values())

	def keys_(self,L,A,pi,phi,psi):
		return list(self.q[L][pi.get(L,A,phi,psi)][phi.get(L,A)].keys())

	def append_to(self,L,pi,phi,a,r):
		#print "pi",a,pi,L,phi
		if self.q.get(L) is None:
			self.q[L]={pi:{phi:{a:r}}}	
		elif self.q[L].get(pi) is None:
			self.q[L][pi]={phi:{a:r}}	
		elif self.q[L][pi].get(phi) is None:
			self.q[L][pi][phi]={a:r}
		elif self.q[L][pi][phi].get(a) is None:
			self.q[L][pi][phi][a]=r	
		else:
			self.q[L][pi][phi][a]+=r	

	def get_direct(self,L,pi,phi,a):
		return self.q[L][pi][phi][a]



class N:
	def __init__(self):
		print "initializing N"
		self.n={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)]->n

	def get(self,L,A,pi,phi,psi):
		return self.n[L][pi.get(L,A,phi,psi)][phi.get(L,A)]

	def append_to(self,L,pi,phi,r):
		if self.n.get(L) is None:
			self.n[L]={pi:{phi:r}}	
		elif self.n[L].get(pi) is None:
			self.n[L][pi]={phi:r}	
		elif self.n[L][pi].get(phi) is None:
			self.n[L][pi][phi]=r	
		else:
			self.n[L][pi][phi]+=r

class Na:
	def __init__(self):
		print "initializing Na"
		self.na={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)][a]->n

	def get(self,L,A,pi,phi,psi,a):
		return self.na[L][pi.get(L,A,phi,psi)][phi.get(L,A)][a]

	def check(self,L,pi,phi,i):
		if self.na.get(L) is None:
			return False
			#self.q[L]={pi.get(L,A,phi,psi):{phi.get(L,A):{a:r}}}	
		elif self.na[L].get(pi) is None:
			return False
		elif self.na[L][pi].get(phi) is None:
			return False
		elif self.na[L][pi][phi].get(i) is None:
			return False
		return True

	def append_to(self,L,pi,phi,a,r):
		if self.na.get(L) is None:
			self.na[L]={pi:{phi:{a:r}}}	
		elif self.na[L].get(pi) is None:
			self.na[L][pi]={phi:{a:r}}	
		elif self.na[L][pi].get(phi) is None:
			self.na[L][pi][phi]={a:r}
		elif self.na[L][pi][phi].get(a) is None:
			self.na[L][pi][phi][a]=r	
		else:
			self.na[L][pi][phi][a]+=r

	def get_direct(self,L,pi,phi,a):
		return self.na[L][pi][phi][a]

