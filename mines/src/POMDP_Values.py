#!/usr/bin/env python
from random import shuffle
from sets import Set

class Pi:
	def __init__(self):
		'''init'''		
		#print "initializing Pi"

	def seed_algorithm(self,A):
		rewards=[]
		for i in range(27):
			rewards.append(A.get_inherent_reward_func2(i))

		#print  rewards.index(max(rewards)), max(rewards)
		return rewards.index(max(rewards))

	def get(self,L,A,Phi,Psi):
		if L == 0:
			#print self.seed_algorithm(A), A.get_explore_abf(), A.battery.val
			#return 26
			return self.seed_algorithm(A)
		else:
			return Psi.get(L-1,A,self,Phi.get(L,A))

class Phi:
	def __init__(self):
		'''init'''
		#print "initializing Phi"
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
		#if action==0:
			#print self.n[0],self.r[0]

class Psi:
	def __init__(self):
		#print "initializing Psi"
		self.psi={}#[L][pi(L-1,A,Phi,Psi)]-> cluster

	def update(self,Q,Na):
		self.psi={}

		for l,v in Q.q.items():
			for pi,v2 in Q.q[l].items():
				self.check_and_append(l,pi)
				for state, v3 in Q.q[l][pi].items():
					
					v = list(Q.q[l][pi][state].values())
					key = list(Q.q[l][pi][state].keys())
					k = self.splitter(self.psi[l][pi],key[v.index(max(v))],pi)
					#if len(v) == 25:
						#print key[v.index(max(v))], v.index(max(v)),v
						#if self.psi[l][pi][k].a != key[v.index(max(v))]:
						#	print "broken match",self.psi[l][pi][k].a,key[v.index(max(v))]
					for action,v4 in Q.q[l][pi][state].items():
						self.psi[l][pi][k].update(action,v4,Na.na[l][pi][state][action],state)

	def splitter(self, cluster_list, m, pi):
		if pi==m:
			return 0

		for i in cluster_list:
			if i.a == m:
				return cluster_list.index(i)


		cluster_list.append(Cluster(m,False))

		return len(cluster_list)-1

	def check(self,L,pi):
		if self.psi.get(L) is None:
			#print "L NOT FOUND", L
			return False
		if self.psi[L].get(pi) is None:
			#print "PI NOT FOUND", pi			
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
		print "finding"
		PSI = self.psi[L][pi.get(L,A,phi,psi)]
		if len(PSI) < 1:
			print "missing psi?"
		for p in PSI:
			if phi(L,A) in p.states:
				return p
	
		print "New state in psi", 
		return pi.get(L,A,phi,psi), phi(L,A)
	
	def get_from_state(self,cluster_list,phi,pi):
		for i in cluster_list:
			if phi in i.states:
				return i.a
		#print "state not found yet", phi
		return pi

	
	def get_max(self,L,pi,phi):
		return self.get_from_state(self.psi[L][pi],phi,pi)

	def load(self,filename):
		print "loading psi"
		self.psi={}
		f = open(filename,'r')
		for line in f:
			l = line.split(",")
			if l[0]=="L":
				try:
					L=int(l[1])
				except ValueError:
					print "Value error trying to convert", l[1]					
					continue

				self.psi[L]={}
			elif l[0]=="pi":
				try:
					pi_i=int(l[1])
				except ValueError:
					print "Value error trying to convert", l[1]					
					continue

				self.psi[L][pi_i]=[]
				self.psi[L][pi_i].append(Cluster(pi_i,True))
			elif l[0]=="k":
				try:
					k=int(l[1])
				except ValueError:
					print "Value error trying to convert", l[1]					
					continue

				if len(self.psi[L][pi_i]):
					self.psi[L][pi_i].append(Cluster(k,False))
			elif l[0]=="action":

				try:
					self.psi[L][pi_i][len(self.psi[L][pi_i])-1].r[int(l[1])]=float(l[2])
				except ValueError:
					print "Value error trying to convert", l[2]					
					continue

				try:
					self.psi[L][pi_i][len(self.psi[L][pi_i])-1].n[int(l[1])]=float(l[3])
				except ValueError:
					print "Value error trying to convert", l[2]					
					continue




			elif l[0]=="state":
				self.psi[L][pi_i][len(self.psi[L][pi_i])-1].states.add(l[1])

		self.write_psi("/home/aaron/catkin_ws/src/mines/mines/src/checkpsi.txt")


	def write_psi(self, fn):

		file = open(fn,'w') 


		print "writing psi to" , fn
		for l,v in self.psi.items():
			file.write("L" + "," + str(l) + "," + "\n")
			for pi,v2 in self.psi[l].items():
				file.write("pi," + str(pi) + ","+ "\n")
				for k in range(len(self.psi[l][pi])):
					file.write("k," + str(self.psi[l][pi][k].a) + ","+ "\n")
					for a in range(27):
						file.write("action,"+str(a) + ", " +str(self.psi[l][pi][k].r[a]) + ", " + str(self.psi[l][pi][k].n[a]) + ","+ "\n")
					for s in self.psi[l][pi][k].states:
						file.write("state," + str(s) + "," + "\n")
					file.write("\n")
		print "finished writing psi to" ,fn

class Q:
	def __init__(self):
		#print "initializing Q"
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

	def write_q(self,filename,Na):

		file = open(filename,'w') 
		for k,v in self.q.items():
			file.write("\n")
			for k2,v2 in self.q[k].items():
				file.write("\n")
				for k3,v3 in self.q[k][k2].items():
					file.write("\n")
					for k4,v4 in self.q[k][k2][k3].items():
						file.write("Q"+","+str(k) + "," +  str(k2) + "," + str(k3) + "," + str(k4) + "," + str(v4) + "," + str(Na.na[k][k2][k3][k4]) + "," +  "\n")



class N:
	def __init__(self):
		#print "initializing N"
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
		#print "initializing Na"
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

