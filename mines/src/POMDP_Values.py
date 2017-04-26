#!/usr/bin/env python
from random import shuffle
from sets import Set
from abstraction_classes import Abstractions
import time
import math
import random
import Regions
As=Abstractions()
import Objective
import Policies
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

	def get_and_return_level(self,A,Psi,Phi,last_expected_action,event_time_horizon):
		action = []
		reward = []
		states_=[]
		base=A.get_base()
		#Phi.set_alpha([.5,.5])
	
		for i in range(Phi.num_visions):
			#Phi.set_alpha([.5,.5])
			s=Phi.get_state(A,i)
			E=Phi.get_events(A,i)
			s= Phi.pre_evolve(s,E)

			a,l,r = Psi.get_with_level(0,s,self,Phi)
			if Phi.get_loc_from_vision(Phi.visions[i][0],base) is not None:
				if Phi.get_loc_from_vision(Phi.visions[i][0],base)+1 != last_expected_action:
					r=r/2.	
			else:	
				r=r/2.
			action.append(a)
			reward.append(r)
			states_.append(s)



		best_index=reward.index(max(reward))
		print "chose", states_[best_index],max(reward),action[best_index]
		base=A.get_base()

		x_trajectory=[]

		for i in range(event_time_horizon):
			if Phi.get_loc_from_vision(Phi.visions[best_index][i],base) is None:
				x_trajectory.append(base)
			else:
				x_trajectory.append(Phi.get_loc_from_vision(Phi.visions[best_index][i],base))





		if Phi.get_loc_from_vision(Phi.visions[best_index][0],base) is None:
			return base+1,base+1,x_trajectory,best_index
		else:
			if Phi.get_loc_from_vision(Phi.visions[best_index][1],base) is None:
				return 	Phi.get_loc_from_vision(Phi.visions[best_index][0],base)+1,Phi.get_loc_from_vision(Phi.visions[best_index][0],base)+1,x_trajectory,best_index
			else:
				return 	Phi.get_loc_from_vision(Phi.visions[best_index][0],base)+1,Phi.get_loc_from_vision(Phi.visions[best_index][1],base)+1,x_trajectory,best_index




	def get_and_return_level_2(self,L,s,Phi,Psi):
		if L == -1:
			return self.seed_algorithm(s),L,0
		else:
			s = Phi.get_from_state(L,s)
			return Psi.get_with_level(L,s,self,Phi)

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
	def __init__(self,event_time_horizon):
		'''init'''
		self.state_size=event_time_horizon
		self.num_visions=1000		
		self.visions={}
		self.gen_ord_state()
		self.alpha=[.05,.9,.05]
		self.obj=Objective.Objective_Handler()
		#self.alpha_list=[]
		#self.alpha_list.append((1.,0.))
		#self.alpha_list.append((.5,.5))
		#self.alpha_list.append((.4,.6))
		#self.alpha_list.append((.3,.7))
		#self.alpha_list.append((.2,.8))
		#self.alpha_list.append((.1,.9))
		#self.alpha_list.append((0.,1.))
		#self.alpha_list.append((.6,.4))
		#self.alpha_list.append((.7,.3))
		#self.alpha_list.append((.8,.2))
		#self.alpha_list.append((.9,.1))

	#def set_alpha(self,alpha):
		#self.alpha=alpha

	#def set_random_alpha(self):
	#	i=random.random()
	#	self.alpha[0]=round(i, 1)
	#	self.alpha[1]=1-round(i, 1)
	def print_pre_evolve(self,s,E):
		self.obj.print_pre_evolve(s,self,E)


	def gen_ord_state(self):

		for i in range(self.num_visions):
			prev=(0,0)
			self.visions[i]=[]
			for j in range(self.state_size):
				red_x=0
				red_y=0
				ran_x = random.randint(-1, 1)
				ran_y = random.randint(-1, 1)
				xy=(prev[0]+ran_x,prev[1]+ran_y)
				prev=xy
				self.visions[i].append(xy)
		


	def get_loc_from_vision(self,vision,region):
		if region is None:
			return None
		xy=Regions.region[region]
		x=xy[0]
		y=xy[1]
		reg = Regions.get_region(x+vision[0]*20,y+vision[1]*20)
		return reg

	def get_state(self,A,seed):
		return self.obj.get_state(A,self,seed)

	def get_events(self,A,seed):
		vision = self.visions[seed]
		base=A.get_base()
		trajectory=[] #by dimension and region

		for i in range(self.state_size):
			trajectory.append(self.get_loc_from_vision(vision[i],base))

		return Objective.Events(trajectory,A)

	def get_reward(self,s,a):
		return self.obj.get_reward(s,a)

	def pre_evolve(self,s,E):
		return self.obj.pre_evolve(s,self,E)

	def evolve(self,s,a,E):
		return self.obj.evolve(s,a,E)




class Psi:
	def __init__(self):
		#print "initializing Psi"
		#Get rid of dependence on Pi
		self.psi={}#[L][pi(L-1,A,Phi,Psi)]-> cluster
		self.point={}
		self.score={}
		self.Q={}
		self.N={}
		self.Na={}

	def update(self,Pi,Phi,Q,Na):
		self.psi={}
		self.point={}
		self.score={}

		print "starting calculate psi"
		start=time.time()

		l=0

		self.point[l]={}
		self.score[l]={}



		for state,q_2 in Q.q.items():
			v=list(q_2.values())
			key=list(q_2.keys())

			self.point[l][state]=key[v.index(max(v))]
			self.score[l][state]=max(v)


		print "finished calculated psi",time.time()-start
		return time.time()-start

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

	def get_with_level(self,L,s,Pi,Phi):
		if self.point.get(L) is None:
			return "explore",L,-1000.

		if self.point[L].get(s) is None:
			return "explore",L,-1000.
		else:
			return self.point[L][s],L,self.score[L][s]

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
		start=time.time()
		f = open(filename,'r')

		for line in f:
			l = line.split(">")
			if l[0]=="L":
				try:
					L=int(l[1])
				except ValueError:
					print "Value error trying to convert", l[1]					
					continue

				self.point[L]={}
				self.score[L]={}
			elif l[0]=="state":
				try:
					self.point[L][l[1]]=l[2]
					self.score[L][l[1]]=float(l[3])
				except ValueError:
					print "Value error trying to convert", l[2]					
					continue

		print "finished loading psi", time.time()-start




	def write_psi(self, fn):

		file = open(fn,'w') 


		print "writing psi to" , fn

		for l,q1 in self.point.items():
			file.write("L" + ">" + str(l) + ">" + "\n")
			for state,q2 in q1.items():
				file.write("state>" + str(state)+">"+ str(q2) + ">"+  str(self.score[l][state]) + ">"+"\n")



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

	def get_bypass(self,state,a):
		if self.q[state].get(a) is None:
			return 0.
		else:
			return self.q[state][a]

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

	def load_file(self,fn,Na,N,Phi):
		#ONLY FOR AGGREGATE!

		self.q={}
		Na.na={}
		N.n={}

		f = open(fn,'r')
		size=0
		for line in f:

			l = line.split(">")
			if l[0]=="Q" and len(l)>4:
				size+=1
				state=l[1]

				try:
					a_i=l[2]
				except ValueError:
					print "Value error trying to convert", l[2]					
					return

				try:
					r=float(l[3])
				except ValueError:
					print "Value error trying to convert", l[3]					
					return

				try:
					n=float(l[4])
				except ValueError:
					print "Value error trying to convert", l[4]					
					return


				Na.append_to(state,a_i,n,Phi)
				N.append_to(state,n,Phi)
				self.append_to(state,a_i,0.,Phi)
				self.append_to_average(state,a_i,r,Phi,Na)


		f.close()
		print "Successfully appended",fn, "with", size, "lines"




	def get_direct(self,phi,a):
		return self.q[phi][a]


	def write_q(self,filename,Na):
		file = open(filename,'w') 
		start=time.time()
		count=0
		for k,q_1 in self.q.items():
			file.write("\n")
			for k2,v in self.q[k].items():	
				file.write("Q"+">"+str(k) + ">" +  str(k2)  +">"+ str(v) + ">" + str(Na.na[k][k2]) + ">" +  "\n")
				count+=1
		file.close()
		print "Completed writing Q",time.time()-start,count

class Q_Level:
	def __init__(self):
		#print "initializing Q"
		self.q={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)][a]->r
		self.var={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)][a]->r
		self.lcb={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)][a]->r
		self.ldb={}#[L][pi(L-1,A,Phi,Psi)][Phi(L,A)][a]->r

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

	def append_to_average_direct(self,l,s,a,r,Phi,Na):
		N=Na.na[l][s][a]
		om=self.q[l][s][a]
		self.q[l][s][a]+=(r-om)/N
		if N>1:
			self.var[l][s][a]=((N-2)*self.var[l][s][a]+(r-self.q[l][s][a])*(r-om))/(N-1)
			self.lcb[l][s][a]=self.q[l][s][a]-1.96*self.var[l][s][a]/math.sqrt(N)
			self.ldb[l][s][a]=self.q[l][s][a]-self.var[l][s][a]

		else:
			self.var[l][s][a]=0.
			self.lcb[l][s][a]=self.q[l][s][a]
			self.ldb[l][s][a]=self.q[l][s][a]

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

	def append_to_direct(self,l,s,a,r,Phi):



		if self.q.get(l) is None:
			self.q[l]={s:{a:r}}	
			self.var[l]={s:{a:0.}}
			self.lcb[l]={s:{a:0.}}	
			self.ldb[l]={s:{a:0.}}			
		elif self.q[l].get(s) is None:
			self.q[l][s]={a:r}
			self.var[l][s]={a:0.}	
			self.lcb[l][s]={a:0.}
			self.ldb[l][s]={a:0.}

		elif self.q[l][s].get(a) is None:
			self.q[l][s][a]=r	
			self.var[l][s][a]=0.
			self.lcb[l][s][a]=0.
			self.ldb[l][s][a]=0.										
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
		return self.n[phi.get(L_MAX,A)]

	def append_to(self,s,r,Phi):

			if self.n.get(s) is None:
				self.n[s]=r	
			else:
				self.n[s]+=r

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

	def append_to_direct(self,l,s,a,r,Phi):
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

