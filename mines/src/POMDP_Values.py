#!/usr/bin/env python
from random import shuffle
class Pi:
	def __init__(self):
		print "initializing Pi"

	def seed_algorithm(self,A):
		k = range(26)
		shuffle(k)
		return 0

	def get(self,L,A,Phi,Psi):
		if L == 0:
			return self.seed_algorithm(A)
		else:
			Psi.get(L-1,A,self,Phi.get(L,A))

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

	def check(self,L,A,pi,phi,psi):
		if self.q.get(L) is None:
			return False
			#self.q[L]={pi.get(L,A,phi,psi):{phi.get(L,A):{a:r}}}	
		elif self.q[L].get(pi.get(L,A,phi,psi)) is None:
			return False
		elif self.q[L][pi.get(L,A,phi,psi)].get(phi.get(L,A)) is None:
			return False
		return True
	
	def vals(self,L,A,pi,phi,psi):
		return list(self.q[L][pi.get(L,A,phi,psi)][phi.get(L,A)].values())

	def keys_(self,L,A,pi,phi,psi):
		return list(self.q[L][pi.get(L,A,phi,psi)][phi.get(L,A)].keys())

	def append_to(self,L,A,pi,phi,psi,a,r):
		if self.q.get(L) is None:
			self.q[L]={pi.get(L,A,phi,psi):{phi.get(L,A):{a:r}}}	
		elif self.q[L].get(pi.get(L,A,phi,psi)) is None:
			self.q[L][pi.get(L,A,phi,psi)]={phi.get(L,A):{a:r}}	
		elif self.q[L][pi.get(L,A,phi,psi)].get(phi.get(L,A)) is None:
			self.q[L][pi.get(L,A,phi,psi)][phi.get(L,A)]={a:r}
		elif self.q[L][pi.get(L,A,phi,psi)][phi.get(L,A)].get(a) is None:
			self.q[L][pi.get(L,A,phi,psi)][phi.get(L,A)][a]=r	
		else:
			self.q[L][pi.get(L,A,phi,psi)][phi.get(L,A)][a]+=r	



class N:
	def __init__(self):
		print "initializing N"
		self.n={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)]->n

	def get(self,L,A,pi,phi,psi):
		return self.n[L][pi.get(L,A,phi,psi)][phi.get(L,A)]

	def append_to(self,L,A,pi,phi,psi,r):
		if self.n.get(L) is None:
			self.n[L]={pi.get(L,A,phi,psi):{phi.get(L,A):r}}	
		elif self.n[L].get(pi.get(L,A,phi,psi)) is None:
			self.n[L][pi.get(L,A,phi,psi)]={phi.get(L,A):r}	
		elif self.n[L][pi.get(L,A,phi,psi)].get(phi.get(L,A)) is None:
			self.n[L][pi.get(L,A,phi,psi)][phi.get(L,A)]=r	
		else:
			self.n[L][pi.get(L,A,phi,psi)][phi.get(L,A)]+=r

class Na:
	def __init__(self):
		print "initializing Na"
		self.na={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)][a]->n

	def get(self,L,A,pi,phi,psi,a):
		return self.na[L][pi.get(L,A,phi,psi)][phi.get(L,A)][a]

	def check(self,L,A,pi,phi,psi,i):
		if self.na.get(L) is None:
			return False
			#self.q[L]={pi.get(L,A,phi,psi):{phi.get(L,A):{a:r}}}	
		elif self.na[L].get(pi.get(L,A,phi,psi)) is None:
			return False
		elif self.na[L][pi.get(L,A,phi,psi)].get(phi.get(L,A)) is None:
			return False
		elif self.na[L][pi.get(L,A,phi,psi)][phi.get(L,A)].get(i) is None:
			return False
		return True

	def append_to(self,L,A,pi,phi,psi,a,r):
		if self.na.get(L) is None:
			self.na[L]={pi.get(L,A,phi,psi):{phi.get(L,A):{a:r}}}	
		elif self.na[L].get(pi.get(L,A,phi,psi)) is None:
			self.na[L][pi.get(L,A,phi,psi)]={phi.get(L,A):{a:r}}	
		elif self.na[L][pi.get(L,A,phi,psi)].get(phi.get(L,A)) is None:
			self.na[L][pi.get(L,A,phi,psi)][phi.get(L,A)]={a:r}
		elif self.na[L][pi.get(L,A,phi,psi)][phi.get(L,A)].get(a) is None:
			self.na[L][pi.get(L,A,phi,psi)][phi.get(L,A)][a]=r	
		else:
			self.na[L][pi.get(L,A,phi,psi)][phi.get(L,A)][a]+=r

