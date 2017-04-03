#!/usr/bin/env python
from random import shuffle
from sets import Set
from abstraction_classes import Abstractions
import time
As=Abstractions()

L_MAX=50


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

	def get_and_return_level(self,L,A,Phi,Psi):
		if L == -1:
			return self.seed_algorithm(A),L
		else:
			return Psi.get_with_level(L,A,self,Phi)	

	def get(self,L,A,Phi,Psi):
		if L == -1:
			return self.seed_algorithm(A)
		else:
			return Psi.get(L,A,self,Phi)

	def get_from_state(self,L,state,Phi,Psi):
		if L<0:
			return self.seed_algorithm_from_state(state)
		else:	
			return Psi.get_from_state(L,state,self,Phi)


	def get_from_state_pure(self,L,state,Phi,Psi):
		if L<0:
			return self.seed_algorithm_from_state(state)
		else:	
			return Psi.get_from_state_pure(L,state,self,Phi)

class Phi:
	def __init__(self):
		'''init'''
		#print "initializing Phi"
		#Phi maps A->A*

	def get_max_level(self,A):
		return self.get(L_MAX,A)

	def get(self,L,A):
		h=""
		for i in range(L+1):
			h=h+ A.get_discrete_abf(i)
		return h

	def get_from_state(self,L,state):

		s=state.split("~")
		h=""
		for i in range(L+1):
			h=h+s[i]+"~"

		return h
	

	'''
	def get(self,L,A):
		if L==0:
			return A.get_location_abf()
		elif L==1:
			return A.get_location_abf()+A.get_region_score_abf()
		elif L==2:
			return A.get_complete_abf()


		return A.get_complete_abf()

	'''

	'''

	def get(self,L,A):
		if L==0:
			return A.get_complete_abf()



		return A.get_complete_abf()
	'''

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
		#Get rid of dependence on Pi
		self.psi={}#[L][pi(L-1,A,Phi,Psi)]-> cluster
		self.point={}

	def update(self,Pi,Phi,Q,Na):
		self.psi={}
		self.point={}
		print "starting calculate psi"
		start=time.time()
		for l,q_1 in Q.q.items():
			self.point[l]={}
			for state,q_2 in q_1.items():
				start1=time.time()
				#pi=Pi.get_from_state_pure(l-1,state,Phi,self)
				end1=time.time()
				start2=time.time()
				#self.check_and_append(l,pi)
				v=list(q_2.values())
				key=list(q_2.keys())
				end2=time.time()
				start3=time.time()
				#k = self.splitter(self.psi[l][pi],key[v.index(max(v))],pi)
				self.point[l][state]=key[v.index(max(v))]
				end3=time.time()
				start4=time.time()
				#for action,v2 in q_2.items():
				#	self.psi[l][pi][k].update(action,v2,Na.na[l][state][action],state)
				end4=time.time()
				#print "total", time.time()-start1,"s1",(end1-start1)/(time.time()-start1),"s2",(end2-start2)/(time.time()-start1),"s3",(end3-start3)/(time.time()-start1),"s4",(end4-start4)/(time.time()-start1)


		print "finished calculated psi",time.time()-start

	def splitter(self, cluster_list, m, pi):
		for i in cluster_list:
			if int(i.a) == int(m):
				return cluster_list.index(i)


		cluster_list.append(Cluster(m,False))

		return len(cluster_list)-1

	def check(self,L,pi):
		if self.point.get(L) is None:
			#print "L NOT FOUND", L
			return False
		if self.point[L].get(pi) is None:
			#print "PI NOT FOUND", pi			
			return False
		return True

	def check_state(self,L,state):
		if self.psi.get(L) is None:
			return False

		for p in self.psi[L].values():
			for i in p:
				for s in i.states:
					if state == s:
						return True

		return False		


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
		if self.point.get(L) is None:
			return Pi.get(L-1,A,Phi,self)

		if self.point[L].get(Phi.get(L,A)) is None:
			return Pi.get(L-1,A,Phi,self)
		else:
			return self.point[L][Phi.get(L,A)]

		#list_of_pis = self.psi[L].values()

		#for cluster_list in list_of_pis:
		#	for cluster in cluster_list:
		#		if Phi.get(L,A) in cluster.states:
		#			return cluster.a


		return Pi.get(L-1,A,Phi,self)

	def get_with_level(self,L,A,Pi,Phi):
		if self.point.get(L) is None:
			return Pi.get_and_return_level(L-1,A,Phi,self)

		if self.point[L].get(Phi.get(L,A)) is None:
			return Pi.get_and_return_level(L-1,A,Phi,self)
		else:
			return self.point[L][Phi.get(L,A)],L

		#list_of_pis = self.psi[L].values()

		#for cluster_list in list_of_pis:
		#	for cluster in cluster_list:
		#		if Phi.get(L,A) in cluster.states:
		#			return cluster.a,L

		return Pi.get_and_return_level(L-1,A,Phi,self)
	
	def get_from_state(self,L,state,Pi,Phi):

		if self.point.get(L) is None:
			return Pi.get_from_state(L-1,A,Phi,self)

		if self.point[L].get(state) is None:
			return Pi.get_from_state_pure(L-1,state,Phi,self)
		else:
			return self.point[L][state]

		#list_of_pis = self.psi[L].values()
		#for cluster_list in list_of_pis:
		#	for cluster in cluster_list:
		#		if Phi.get_from_state(L,state) in cluster.states:
		#			return cluster.a

		return Pi.get_from_state(L-1,state,Phi,self)

	def get_from_state_pure(self,L,state,Pi,Phi):

		if self.point.get(L) is None:
			return Pi.get_from_state_pure(L-1,state,Phi,self)

		if self.point[L].get(state) is None:
			return Pi.get_from_state_pure(L-1,state,Phi,self)
		else:
			return self.point[L][state]

		#list_of_pis = self.psi[L].values()
		#for cluster_list in list_of_pis:
		#	for cluster in cluster_list:
		#		if state in cluster.states:
		#			return cluster.a

		return Pi.get_from_state_pure(L-1,state,Phi,self)

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

				self.point[L]={}
			elif l[0]=="state":
				try:
					self.point[L][l[1]]=int(l[2])
				except ValueError:
					print "Value error trying to convert", l[2]					
					continue




	def write_psi(self, fn):

		file = open(fn,'w') 


		print "writing psi to" , fn

		for l,q1 in self.point.items():
			file.write("L" + "," + str(l) + "," + "\n")
			for state,q2 in q1.items():
				file.write("state," + str(state)+","+ str(q2) + ","+ "\n")



		'''
		for l,v in self.point.items():
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
		'''

		file.close()
		print "finished writing psi to" ,fn

class Q:
	def __init__(self):
		#print "initializing Q"
		self.q={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)][a]->r

	def get(self,A,phi,a):
		return self.q[L][phi.get(L_MAX,A)][a]

	def check(self,phi):
		if self.q.get(phi) is None:
			return False
		return True
	
	def vals(self,A,phi):
		return list(self.q[phi.get(L_MAX,A)].values())

	def keys_(self,A,phi):
		return list(self.q[phi.get(L_MAX,A)].keys())

	def append_to_average(self,s,a,r,Phi,Na):
			self.q[s][a]+=(r-self.q[s][a])/Na.na[s][a]

	def append_to_average_direct(self,s,a,r,Phi,Na):
		self.q[s][a]+=(r-self.q[s][a])/Na.na[s][a]

	def append_to(self,s,a,r,Phi):
			if self.q.get(s) is None:
				self.q[s]={a:r}
			elif self.q[s].get(a) is None:
				self.q[s][a]=r
			else:
				self.q[s][a]+=r

	def append_to_direct(self,s,a,r,Phi):
		if self.q.get(s) is None:
			self.q[s]={a:r}	
		elif self.q[s].get(a) is None:
			self.q[s][a]=r		
		else:
			self.q[s][a]+=r
	

	def get_direct(self,phi,a):
		return self.q[phi][a]


	def write_q(self,filename,Na):
		file = open(filename,'w') 
		start=time.time()
		count=0
		for k,q_1 in self.q.items():
			file.write("\n")
			for k2,v in self.q[k].items():	
				file.write("Q"+","+str(k) + "," +  str(k2)  +","+ str(v) + "," + str(Na.na[k][k2]) + "," +  "\n")
				count+=1
		file.close()
		print "Completed writing Q",time.time()-start,count

class Q_Level:
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
		print "Writing Q to", filename
		start=time.time()
		for k,v in self.q.items():
			file.write("\n")
			for k2,v2 in self.q[k].items():
				file.write("\n")
				for k3,v3 in self.q[k][k2].items():
					file.write("Q"+","+str(k) + "," +  str(k2)  + "," +  str(k3) +","+ str(v3) + "," + str(Na.na[k][k2][k3]) + "," +  "\n")

		file.close()
		print "Completed writing Q",time.time()-start
		



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
		self.na={}#[pi(L-1,A,Phi,Psi)][Phi(L,A)][a]->n

	def get(self,A,phi,a):
		return self.na[phi.get(L_MAX,A)][a]

	def check(self,phi,i):
		if self.na.get(phi) is None:
			return False
		elif self.na[phi].get(i) is None:
			return False
		return True

	def append_to(self,s,a,r,Phi):
			if self.na.get(s) is None:
				self.na[s]={a:r}	
			elif self.na[s].get(a) is None:
				self.na[s][a]=r		
			else:
				self.na[s][a]+=r

	def append_to_direct(self,state,a,r,Phi):
		if self.na.get(s) is None:
			self.na[s]={a:r}	
		elif self.na[s].get(a) is None:
			self.na[s][a]=r		
		else:
			self.na[s][a]+=r

	def get_direct(self,phi,a):
		return self.na[phi][a]

class Na_Level:
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

