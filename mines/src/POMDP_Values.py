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
		state=Phi.get(L,A)

		rotated_action=[]
		level=[]
		score=[]
		for rot in range(8):
			rot_state=Phi.get_rotated_state(rot,state)
			a,l,s=self.get_and_return_level_2(L,rot_state,Phi,Psi)
			rotated_action.append(a)
			level.append(l)
			score.append(s)

		ml=-2
		mv=-1
		ind=-1

		for i in range(8):
			if level[i]>ml:
				ind=i
				ml=level[i]
				mv=score[i]
			elif level[i]==ml:
				if score[i]>mv:
					ind=i
					ml=level[i]
					mv=score[i]	

		best_index = ind
		print rotated_action,level,score,best_index
		return Phi.unrotate_action(best_index,rotated_action[best_index]),level[best_index]

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
	def __init__(self):
		'''init'''
		#print "initializing Phi"
		#Phi maps A->A*
		self.forward_rot_vals={}
		self.backward_rot_vals={}
		self.generate_rotations()
		self.state_order={}
		self.loc_order={}
		self.generate_order_state()

	def get_max_level(self,A):
		return self.get(L_MAX,A)

	def get(self,L,A):
		h=""
		base=A.get_base()
		for i in range(L+1):
			h=h+ A.get_discrete_abf(self.state_order[base][i])
		return h

	def generate_order_state(self):

		link={}
		for i in range(25):
			self.state_order[i]={}
			self.loc_order[i]={}
			link[i]=[]


		link[0]=[0,5,1,6,9,2,7,10,13,3,8,11,14,17,4,12,15,18,21,16,19,22,20,23,24]

		link[1]=[1,0,5,9,13,2,6,10,14,18,17,3,7,11,15,19,23,22,21,4,8,12,16,20,24]

		link[5]=[5,6,10,9,1,0,7,11,15,14,13,2,8,12,16,20,19,18,17,3,24,23,22,21,4]

		link[6]=[6,7,11,10,9,5,8,12,16,15,14,13,2,1,0,20,19,18,17,3,24,23,22,21,4]

		link[9]=[9,10,14,13,2,1,0,5,6,7,11,15,19,18,17,3,8,12,16,20,24,23,22,21,4]

		link[10]=[10,11,15,14,13,9,5,6,7,8,12,16,20,19,18,17,3,2,1,0,24,23,22,21,4]

		link[14]=[14,15,19,18,17,13,9,10,11,12,16,20,24,23,22,21,4,3,2,1,0,5,6,7,8]

		# link 2 is 6 with r_index=2 (1 rotation)

		for i in range(25):
			link[2].append(self.R(2,link[6][i]))

		# link 3 is 5 with r_index=2
		for i in range(25):
			link[3].append(self.R(2,link[5][i]))

		# link 4 is 0 with r_index=2
		for i in range(25):
			link[4].append(self.R(2,link[0][i]))

		# link 7 is 1 with r_index=6
		for i in range(25):
			link[7].append(self.R(6,link[1][i]))

		# link 8 is 0 with r_index=6
		for i in range(25):
			link[8].append(self.R(6,link[0][i]))

		# link 11 is 9 with r_index=6
		for i in range(25):
			link[11].append(self.R(6,link[9][i]))

		# link 12 is 5 with r_index=6
		for i in range(25):
			link[12].append(self.R(6,link[5][i]))

		# link 13 is 10 with r_index=2
		for i in range(25):
			link[13].append(self.R(2,link[10][i]))

		# link 15 is 10 with r_index=6
		for i in range(25):
			link[15].append(self.R(6,link[10][i]))

		# link 16 is 6 with r_index=6
		for i in range(25):
			link[16].append(self.R(6,link[6][i]))

		# link 17 is 9 with r_index=2
		for i in range(25):
			link[17].append(self.R(2,link[9][i]))

		# link 18 is 10 with r_index=4
		for i in range(25):
			link[18].append(self.R(4,link[10][i]))

		# link 19 is 9 with r_index=4
		for i in range(25):
			link[19].append(self.R(4,link[9][i]))

		# link 20 is 1 with r_index=4
		for i in range(25):
			link[20].append(self.R(4,link[1][i]))

		# link 21 is 1 with r_index=2
		for i in range(25):
			link[21].append(self.R(2,link[1][i]))

		# link 22 is 6 with r_index=4
		for i in range(25):
			link[22].append(self.R(4,link[6][i]))

		# link 23 is 5 with r_index=4
		for i in range(25):
			link[23].append(self.R(4,link[5][i]))

		# link 24 is 0 with r_index=4
		for i in range(25):
			link[24].append(self.R(4,link[0][i]))

		self.state_order[0][0]=0
		

		for k in range(25):
			self.state_order[k][0]=0
			c=1
			for i in range(L_MAX/2):

				self.state_order[k][c]=link[k][i]+1
				self.loc_order[k][c]=link[k][i]
				c+=1
				self.state_order[k][c]=link[k][i]+26
				self.loc_order[k][c]=link[k][i]
				c+=1


	def get_from_state(self,L,state):

		s=state.split("~")
		h=""
		for i in range(L+1):
			h=h+s[i]+"~"

		return h

	def get_rotated_state(self,r_index,state):
		
		s = state.split("~")
		base=int(s[0])
		h = str(self.R(r_index,int(s[0])))+"~"

		#sort it
		sorted_region={}
		sorted_wl={}
		for i in range(1,51):
			if (i % 2 == 0): #even 
				sorted_wl[self.loc_order[base][i]]=s[i]
			else:
				sorted_region[self.loc_order[base][i]]=s[i]


		for i in range(1,L_MAX+1):
			region_index=self.R(r_index,self.loc_order[base][i])
			if (i % 2 == 0): #even 
				h = h + str(sorted_wl[region_index])+"~"
			else:
				h = h + str(sorted_region[region_index])+"~"

		return h

	def generate_rotations(self):

		for r_index in range(8):
			self.forward_rot_vals[r_index]={}
			self.backward_rot_vals[r_index]={}

			for i in range(25):
				if r_index==0:
					self.forward_rot_vals[r_index][i]=i

				if r_index==1:
					self.forward_rot_vals[r_index][i]=self.get_mirror(i)
				elif r_index==2:
					self.forward_rot_vals[r_index][i]=self.get_rot(i)
				elif r_index==3:
					self.forward_rot_vals[r_index][i]=self.get_mirror(self.get_rot(i))
				elif r_index==4:
					self.forward_rot_vals[r_index][i]=self.get_rot(self.get_rot(i))
				elif r_index==5:
					self.forward_rot_vals[r_index][i]=self.get_mirror(self.get_rot(self.get_rot(i)))
				elif r_index==6:
					self.forward_rot_vals[r_index][i]=self.get_rot(self.get_rot(self.get_rot(i)))
				elif r_index==7:
					self.forward_rot_vals[r_index][i]=self.get_mirror(self.get_rot(self.get_rot(self.get_rot(i))))

				if r_index==0:
					self.backward_rot_vals[r_index][i] = i

				if r_index==1:
					self.backward_rot_vals[r_index][i] = self.get_mirror(i)
				elif r_index==2:
					self.backward_rot_vals[r_index][i] = self.get_rot(self.get_rot(self.get_rot(i)))
				elif r_index==3:
					self.backward_rot_vals[r_index][i] = self.get_rot(self.get_rot(self.get_rot(self.get_mirror(i))))
				elif r_index==4:
					self.backward_rot_vals[r_index][i] = self.get_rot(self.get_rot(i))
				elif r_index==5:
					self.backward_rot_vals[r_index][i] = self.get_rot(self.get_rot(self.get_mirror(i)))
				elif r_index==6:
					self.backward_rot_vals[r_index][i] = self.get_rot(i)
				elif r_index==7:
					self.backward_rot_vals[r_index][i] = self.get_rot(self.get_mirror(i))

	def R(self,r_index,i):
		return self.forward_rot_vals[r_index][i]
		#order none,m,r,rm,rr,rrm,rrr,rrrm
		'''
		if r_index==0:
			return i

		if r_index==1:
			return self.get_mirror(i)
		elif r_index==2:
			return self.get_rot(i)
		elif r_index==3:
			return self.get_mirror(self.get_rot(i))
		elif r_index==4:
			return self.get_rot(self.get_rot(i))
		elif r_index==5:
			return self.get_mirror(self.get_rot(self.get_rot(i)))
		elif r_index==6:
			return self.get_rot(self.get_rot(self.get_rot(i)))
		elif r_index==7:
			return self.get_mirror(self.get_rot(self.get_rot(self.get_rot(i))))
		'''

	def R_backwards(self,r_index,i):
		return self.backward_rot_vals[r_index][i]
		'''
		#order none,m,r,rm,rr,rrm,rrr,rrrm
		if r_index==0:
			return i

		if r_index==1:
			return self.get_mirror(i)
		elif r_index==2:
			return self.get_rot(self.get_rot(self.get_rot(i)))
		elif r_index==3:
			return self.get_rot(self.get_rot(self.get_rot(self.get_mirror(i))))
		elif r_index==4:
			return self.get_rot(self.get_rot(i))
		elif r_index==5:
			return self.get_rot(self.get_rot(self.get_mirror(i)))
		elif r_index==6:
			return self.get_rot(i)
		elif r_index==7:
			return self.get_rot(self.get_mirror(i))
		'''

	def R_action(self,r_index,i):
		if i==0 or i == 26:
			return i
		return self.R(r_index,i-1)+1

	def unrotate_action(self,r_index,i):
		if i==0 or i == 26:
			return i
		return self.R_backwards(r_index,i-1)+1


	def get_rot(self,i):
		if i==0:
			return 4
		if i==1:
			return 21
		if i==2:
			return 22
		if i==3:
			return 23
		if i==4:
			return 24
		if i==5:
			return 3
		if i==6:
			return 2
		if i==7:
			return 1
		if i==8:
			return 0
		if i==9:
			return 17
		if i==10:
			return 13
		if i==11:
			return 9
		if i==12:
			return 5
		if i==13:
			return 18
		if i==14:
			return 14
		if i==15:
			return 10
		if i==16:
			return 6
		if i==17:
			return 19
		if i==18:
			return 15
		if i==19:
			return 11
		if i==20:
			return 7
		if i==21:
			return 20
		if i==22:
			return 16
		if i==23:
			return 12
		if i==24:
			return 8

	def get_mirror(self,i):

		if i==1:
			return 5
		elif i==5:
			return 1
		elif i ==3:
			return 21
		elif i==21:
			return 3
		elif i==23:
			return 20
		elif i==20:
			return 23
		elif i==12:
			return 7
		elif i==7:
			return 12
		else:
			return i





			

	
		

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
		self.score={}

	def update(self,Pi,Phi,Q,Na):
		self.psi={}
		self.point={}
		self.score={}
		print "starting calculate psi"
		start=time.time()

		for l,q_1 in Q.q.items():
			self.point[l]={}
			self.score[l]={}
			for state,q_2 in q_1.items():
				#start1=time.time()
				v=list(q_2.values())
				key=list(q_2.keys())
				#end2=time.time()
				self.point[l][state]=key[v.index(max(v))]
				self.score[l][state]=max(v)

				#print "total", time.time()-start1,"s2",(end2-start1)/(time.time()-start1),"s3",(end3-start3)/(time.time()-start1)


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
			return Pi.get_and_return_level_2(L-1,s,Phi,self)

		if self.point[L].get(s) is None:
			return Pi.get_and_return_level_2(L-1,s,Phi,self)
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
			l = line.split(",")
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
					self.point[L][l[1]]=int(l[2])
					self.score[L][l[1]]=float(l[3])
				except ValueError:
					print "Value error trying to convert", l[2]					
					continue

		print "finished loading psi", time.time()-start




	def write_psi(self, fn):

		file = open(fn,'w') 


		print "writing psi to" , fn

		for l,q1 in self.point.items():
			file.write("L" + "," + str(l) + "," + "\n")
			for state,q2 in q1.items():
				file.write("state," + str(state)+","+ str(q2) + ","+  str(self.score[l][state]) + ","+"\n")



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

	def append_to_average_direct(self,l,s,a,r,Phi,Na):
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

	def append_to_direct(self,l,s,a,r,Phi):
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

