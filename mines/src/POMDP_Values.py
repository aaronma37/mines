#!/usr/bin/env python
from random import shuffle
from sets import Set
from abstraction_classes import Abstractions

As=Abstractions()

L_MAX=2


class Pi:
	def __init__(self):
		'''init'''		
		#print "initializing Pi"

	def seed_algorithm(self,A):
		return 26
		rewards=[]
		for i in range(27):
			rewards.append(A.get_inherent_reward_func2(i))

		#print  rewards.index(max(rewards)), max(rewards)
		return rewards.index(max(rewards))

	def seed_algorithm_from_state(self,state):
		return 26

	def get(self,L,A,Phi,Psi):
		if L == -1:
			return self.seed_algorithm(A)
		else:
			return Psi.get(L,A,self,Phi)

	def get_from_state(self,L,state,Phi,Psi):
		if L==-1:
			return self.seed_algorithm_from_state(state)
		else:
			return Psi.get_from_state(Psi.psi[L][self.get_from_state(L-1,Phi.get_from_state(L-1,state),Phi,Psi)],state,self.get_from_state(L-1,Phi.get_from_state(L-1,state),Phi,Psi))

class Phi:
	def __init__(self):
		'''init'''
		#print "initializing Phi"
		#Phi maps A->A*
	
	def length_of_abstraction(self,L):
		if L==0:
			return As.location_abf_length()+As.battery_abf_length()
		elif L==1:
			return As.location_abf_length()+As.battery_abf_length()+As.region_score_abf_length()
		elif L==2:
			return As.complete_abf_length()

	def get_max_level(self,A):
		return A.get_complete_abf()

	def get(self,L,A):
		if L==0:
			return A.get_location_abf()+A.get_battery_abf()
		elif L==1:
			return A.get_location_abf()+A.get_battery_abf()+A.get_region_score_abf()
		elif L==2:
			return A.get_location_abf()+A.get_battery_abf()+A.get_region_score_abf()+A.get_work_load_abf()

		return A.get_complete_abf()
	
	def get_from_state(self,L,state):
		if L==0:
			#stop state when it is beginning of L1
		return state[:self.length_of_abstraction(L)]
		

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

	def update(self,Pi,Phi,Q,Na):
		self.psi={}

		for l in range(L_MAX):
			for state,v in Q.q.items():
				pi=Pi.get_from_state(l-1,state,Phi,self)
				self.check_and_append(l,pi)
				v=list(Q.q[state].values())
				key=list(Q.q[state].keys())
				k = self.splitter(self.psi[l][pi],key[v.index(max(v))],pi)
				for action,v2 in Q.q[state].items():
					self.psi[l][pi][k].update(action,v2,Na.na[state][action],Phi.get_from_state(l,state))

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


	def get(self,L,A,Pi,Phi):
		if self.check(L,Pi.get(L-1,A,Phi,self)) is False:
			return Pi.get(L-1,A,Phi,self)

		PSI = self.psi[L][Pi.get(L-1,A,Phi,self)]
		if len(PSI) < 1:
			print "missing psi?"
		for p in PSI:
			if Phi.get(L,A) in p.states:
				return p

			else:
				print "states",p.states
				print "this one",L,Phi.get(L,A)
	

		return Pi.get(L-1,A,Phi,self)
	
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

		file.close()
		print "finished writing psi to" ,fn

class Q:
	def __init__(self):
		#print "initializing Q"
		self.q={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)][a]->r

	def get(self,A,phi,a):
		return self.q[phi.get(L_MAX,A)][a]

	def check(self,phi):
		if self.q.get(phi) is None:
			return False
		return True
	
	def vals(self,A,phi):
		return list(self.q[phi.get(L_MAX,A)].values())

	def keys_(self,A,phi):
		return list(self.q[phi.get(L_MAX,A)].keys())

	def append_to(self,phi,a,r):
		if self.q.get(phi) is None:
			self.q[phi]={a:r}	
		elif self.q[phi].get(a) is None:
			self.q[phi][a]=r	
		else:
			self.q[phi][a]+=r	

	def get_direct(self,phi,a):
		return self.q[phi][a]

	def write_q(self,filename,Na):
		file = open(filename,'w') 
		for k,v in self.q.items():
			file.write("\n")
			for k2,v2 in self.q[k].items():
				file.write("Q"+","+str(k) + "," +  str(k2)  + "," + str(v2) + "," + str(Na.na[k][k2]) + "," +  "\n")

		file.close()



class N:
	def __init__(self):
		#print "initializing N"
		self.n={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)]->n

	def get(self,A,phi):
		return self.n[phi.get(L_MAX,A)]

	def append_to(self,phi,r):
		if self.n.get(phi) is None:
			self.n[phi]=r	
		else:
			self.n[phi]+=r

class Na:
	def __init__(self):
		#print "initializing Na"
		self.na={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)][a]->n

	def get(self,A,phi,a):
		return self.na[phi.get(L_MAX,A)][a]

	def check(self,phi,i):
		if self.na.get(phi) is None:
			return False
		elif self.na[phi].get(i) is None:
			return False
		return True

	def append_to(self,phi,a,r):
		if self.na.get(phi) is None:
			self.na[phi]={a:r}	
		elif self.na[phi].get(a) is None:
			self.na[phi][a]=r		
		else:
			self.na[phi][a]+=r

	def get_direct(self,phi,a):
		return self.na[phi][a]

