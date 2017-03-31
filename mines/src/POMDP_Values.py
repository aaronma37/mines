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
			if Psi.check(L,self.get_from_state(L-1,Phi.get_from_state(L-1,state),Phi,Psi)) is True:
				return Psi.get_from_state(Psi.psi[L][self.get_from_state(L-1,Phi.get_from_state(L-1,state),Phi,Psi)],state,self.get_from_state(L-1,Phi.get_from_state(L-1,state),Phi,Psi))
			else:
				return self.get_from_state(L-1,Phi.get_from_state(L-1,state),Phi,Psi)

class Phi:
	def __init__(self):
		'''init'''
		#print "initializing Phi"
		#Phi maps A->A*

	def get_max_level(self,A):
		return A.get_complete_abf()
	
	def get(self,L,A):
		if L==0:
			return A.get_location_abf()
		elif L==1:
			return A.get_location_abf()+A.get_region_score_abf()
		elif L==2:
			return A.get_complete_abf()


		return A.get_complete_abf()

	'''

	def get(self,L,A):
		if L==0:
			return A.get_complete_abf()



		return A.get_complete_abf()
	'''
	def get_from_state(self,L,state):
		s=state.split("~")
		if L==0:
			return s[0]+"~"
		elif L==1:
			return s[0]+"~"+s[1]+"~"
		elif L==2:
			return s[0]+"~"+s[1]+"~"+s[2]+"~"
	'''

	def get_from_state(self,L,state):
		s=state.split("~")
		if L==0:
			return s[0]+"~"+s[1]+"~"+s[2]+"~"
	'''
				
		

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

	def get_total_n(self):
		n=0.0
		for i in self.n:
			n+=i
		return n	
			

class Psi:
	def __init__(self):
		#print "initializing Psi"
		self.psi={}#[L][pi(L-1,A,Phi,Psi)]-> cluster

	def update(self,Pi,Phi,Q,Na):
		self.psi={}

		for l,irrelevant in Q.q.items():
			for state,v in Q.q[l].items():
				pi=Pi.get_from_state(l-1,state,Phi,self)
				self.check_and_append(l,pi)
				v=list(Q.q[l][state].values())
				key=list(Q.q[l][state].keys())
				k = self.splitter(self.psi[l][pi],key[v.index(max(v))],pi)
				for action,v2 in Q.q[l][state].items():
					self.psi[l][pi][k].update(action,v2,Na.na[l][state][action],Phi.get_from_state(l,state))

	def splitter(self, cluster_list, m, pi):
		for i in cluster_list:
			if int(i.a) == int(m):
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

	def check_and_append_k(self,l,pi,k):
		for p in self.psi[l][pi]:
			if p.a == k:
				return self.psi[l][pi].index(p)

		self.psi[l][pi].append(Cluster(k,False))
		return len(self.psi[l][pi])-1

	def get_cluster(self,L,pi,A,Phi):
		for p in self.psi[L][pi]:
			if Phi.get(L,A) in p.states:
				return p

		return self.psi[L][pi][0]



	def get(self,L,A,Pi,Phi):
		if self.check(L,Pi.get(L-1,A,Phi,self)) is False:
			return Pi.get(L-1,A,Phi,self)

		PSI = self.psi[L][Pi.get(L-1,A,Phi,self)]
		if len(PSI) < 1:
			print "missing psi?"
		for p in PSI:
			if Phi.get(L,A) in p.states:
				return p.a

			#else:
				#if L==2:
					#print "states",p.states
					#print "this one",L,Phi.get(L,A)
	

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

				self.check_and_append(L,pi_i)
			elif l[0]=="k":
				try:
					k=int(l[1])
				except ValueError:
					print "Value error trying to convert", l[1]					
					continue

				index = self.check_and_append_k(L,pi_i,k)
			elif l[0]=="action":

				try:
					self.psi[L][pi_i][index].r[int(l[1])]=float(l[2])
				except ValueError:
					print "Value error trying to convert", l[2]					
					continue

				try:
					self.psi[L][pi_i][index].n[int(l[1])]=float(l[3])
				except ValueError:
					print "Value error trying to convert", l[2]					
					continue




			elif l[0]=="state":
				self.psi[L][pi_i][index].states.add(l[1])

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

	def get(self,L,A,phi,a):
		return self.q[L][phi.get(L_MAX,A)][a]

	def check(self,L,phi):
		if self.q.get(L) is None:
			return False
		if self.q[L].get(phi) is None:
			return False
		return True
	
	def vals(self,L,A,phi):
		return list(self.q[L][phi.get(L_MAX,A)].values())

	def keys_(self,L,A,phi):
		return list(self.q[L][phi.get(L_MAX,A)].keys())

	def append_to_average(self,state,a,r,Phi,Na):
		for l in range(L_MAX+1):
			s = Phi.get_from_state(l,state)
			self.q[l][s][a]+=(r-self.q[l][s][a])/Na.na[l][s][a]

	def append_to_average_direct(self,l,state,a,r,Phi,Na):
		s = Phi.get_from_state(l,state)
		self.q[l][s][a]+=(r-self.q[l][s][a])/Na.na[l][s][a]

	def append_to(self,state,a,r,Phi):
		for l in range(L_MAX+1):
			s = Phi.get_from_state(l,state)
			if self.q.get(l) is None:
				self.q[l]={s:{a:r}}
			elif self.q[l].get(s) is None:
				self.q[l][s]={a:r}
			elif self.q[l][s].get(a) is None:
				self.q[l][s][a]=r
			else:
				self.q[l][s][a]+=r

	def append_to_direct(self,l,state,a,r,Phi):
		s = Phi.get_from_state(l,state)
		if self.q.get(l) is None:
			self.q[l]={s:{a:r}}	
		elif self.q[l].get(s) is None:
			self.q[l][s]={a:r}	
		elif self.q[l][s].get(a) is None:
			self.q[l][s][a]=r		
		else:
			self.q[l][s][a]+=r
	

	def get_direct(self,L,phi,a):
		return self.q[L][phi][a]


	def write_q(self,filename,Na):
		file = open(filename,'w') 
		for k,v in self.q.items():
			file.write("\n")
			for k2,v2 in self.q[k].items():
				file.write("\n")
				for k3,v3 in self.q[k][k2].items():
					file.write("Q"+","+str(k) + "," +  str(k2)  + "," +  str(k3) +","+ str(v3) + "," + str(Na.na[k][k2][k3]) + "," +  "\n")

		file.close()



class N:
	def __init__(self):
		#print "initializing N"
		self.n={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)]->n

	def get(self,L,A,phi):
		return self.n[L][phi.get(L_MAX,A)]

	def append_to(self,state,r,Phi):
		for l in range(L_MAX+1):
			s = Phi.get_from_state(l,state)
			if self.n.get(l) is None:
				self.n[l]={s:r}	
			if self.n[l].get(s) is None:
				self.n[l][s]=r	
			else:
				self.n[l][s]+=r

class Na:
	def __init__(self):
		#print "initializing Na"
		self.na={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)][a]->n

	def get(self,L,A,phi,a):
		return self.na[L][phi.get(L_MAX,A)][a]

	def check(self,L,phi,i):
		if self.na.get(L) is None:
			return False
		if self.na[L].get(phi) is None:
			return False
		elif self.na[L][phi].get(i) is None:
			return False
		return True

	def append_to(self,state,a,r,Phi):
		for l in range(L_MAX+1):
			s = Phi.get_from_state(l,state)
			if self.na.get(l) is None:
				self.na[l]={s:{a:r}}	
			elif self.na[l].get(s) is None:
				self.na[l][s]={a:r}	
			elif self.na[l][s].get(a) is None:
				self.na[l][s][a]=r		
			else:
				self.na[l][s][a]+=r

	def append_to_direct(self,l,state,a,r,Phi):
		s = Phi.get_from_state(l,state)
		if self.na.get(l) is None:
			self.na[l]={s:{a:r}}	
		elif self.na[l].get(s) is None:
			self.na[l][s]={a:r}	
		elif self.na[l][s].get(a) is None:
			self.na[l][s][a]=r		
		else:
			self.na[l][s][a]+=r

	def get_direct(self,L,phi,a):
		return self.na[L][phi][a]

