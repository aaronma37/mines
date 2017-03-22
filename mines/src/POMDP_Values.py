#!/usr/bin/env python
from random import shuffle
from sets import Set

class Pi:
	def __init__(self):
		print "initializing Pi"

	def seed_algorithm(self,A):
		rewards=[]
		for i in range(27):
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

class Cluster:
	def __init__(self,a,default):
		self.a=a #a is static
		self.action_set=[]
		self.r=[]
		self.n=[]
		for i in range(27):
			self.action_set.append(i)
			self.r.append(0.)
			self.n.append(0.)

		self.default=default

		self.states=Set([])

	def update(self,action,r,n,state):
		self.states.add(state)
		self.n[action]+=n
		self.r[action]+=(r-self.r[action])/self.n[action]
		if action==0:
			print self.n[0],self.r[0]

class Psi:
	def __init__(self):
		print "initializing Psi"
		self.psi={}#[L][pi(L-1,A,Phi,Psi)]-> cluster

	def update(self,Q,Na):
		self.psi={}

		for l,v in Q.q.items():
			for pi,v2 in Q.q[l].items():
				self.check_and_append(l,pi)
				for state, v3 in Q.q[l][pi].items():
					
					v = Q.q[l][pi][state].values()
					key = Q.q[l][pi][state].keys()
					k = self.splitter(self.psi[l][pi],key[v.index(max(v))])
					#print key[v.index(max(v))], v.index(max(v)),v
					for action,v4 in Q.q[l][pi][state].items():
						if l==0 and pi ==0 and action ==0:
							print v4, Na.na[l][pi][state][action], k
						self.psi[l][pi][k].update(action,v4,Na.na[l][pi][state][action],state)

	def splitter(self, cluster_list, m):
		if cluster_list[0].a==m:
			return 0

		for i in cluster_list:
			if i.default is False:
				if i.a == m:
					return cluster_list.index(i)


		cluster_list.append(Cluster(m,False))

		return len(cluster_list)-1

	def check(self,L,pi):
		if self.psi.get(L) is None:
			return False
		if self.psi[L].get(pi) is None:
			return False
		return True

	def check_and_append(self,l,pi):
		if self.psi.get(l) is None:
			self.psi[l]={pi:[]}
			self.psi[l][pi].append(Cluster(pi,True))
		elif self.psi[l].get(pi) is None:
			self.psi[l][pi]=[]
			self.psi[l][pi].append(Cluster(pi,True))


	def get(self,L,A,pi,phi):
		PSI = self.psi[L][pi.get(L,A,phi,psi)]
		for p in PSI:
			if p.default is False:
				if phi(L,A) in p.states:
					return p
			else:
				i=p

		return i
	
	def get_from_state(self,cluster_list,phi):
		for i in cluster_list:
			if phi in i.states:
				return i
		#state not found yet
		return cluster_list[0]

	
	def get_max(self,L,pi,phi):
		return self.get_from_state(self.psi[L][pi],phi).a

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

