#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
import Regions
#Tool class
import random
import os

def append_dict_1(P,h1,r):
	if P.get(h1) is None:
		P[h1]=r
	else:
		P[h1]+=r

def append_dict(P,h1,h2,h3,r):
	if P.get(h1) is None:
		P[h1]={h2:{h3:r}}
	elif P[h1].get(h2) is None:
		P[h1][h2]={h3:r}
	elif P[h1][h2].get(h3) is None:
		P[h1][h2][h3]=r
	else:
		P[h1][h2][h3]+=r

def append_dict_if_missing(P,h1,r):
	P[h1]=r

def append_dict2(P,h1,h2,h3,h4,r):
	if P.get(h1) is None:
		P[h1]={h2:{h3:{h4:r}}}
	if P[h1].get(h2) is None:
		P[h1][h2]={h3:{h4:r}}
	elif P[h1][h2].get(h3) is None:
		P[h1][h2][h3]={h4:r}
	elif P[h1][h2][h3].get(h4) is None:
		P[h1][h2][h3][h4]=r
	else:
		P[h1][h2][h3][h4]+=r



class heuristic:
	def __init__(self):
		self.A={} #type,base,input,next abstraction -> number of occasions
		self.N={} #type,base,input - > number of occasions
		self.visits={}
		self.R={} #type,base,input, -> accrued reward
		#classifier,input,output

			

	#def update(self,classifier, base, input_,output_,reward):
	#	append_dict(self.N,classifier, base,input_,1.)
	#	append_dict2(self.A,classifier, base,input_,output_,1.)
#
#		append_dict(self.R,classifier, base,input_,0.)
#		append_dict(self.R,classifier, base,input_,(reward-self.R[classifier][input_])/self.N[classifier][input_])


	def print_N(self):
		for i in range(1,6):
			for k,v in self.A["AR: " + str(i)].items():
				for k2,v2 in self.A["AR: " + str(i)][k].items():
					for k3,v3 in self.A["AR: " + str(i)][k][k2].items():
						print("A" +","+"AR: " + str(i) + "," + str(k) + ","+   str(k2) + "," + str(k3) + "," + str(v3) + "," +  str(self.N["AR: " + str(i)][k][k2]))

		print "end"


	def pull_new_abstraction(self,classifier, base,input_):

		#classifier=str(classifier)
		#base=str(base)
		#input_=str(input_)

		#print classifier,base,input_

		if base is None:
			print "error in abstraction pull"
			return base

		
		if self.N.get(classifier) is None:
			print classifier,base,input_, "class NOT FOUND"
			#self.print_N()
			append_dict(self.N,classifier, base,input_,1.)
			append_dict2(self.A,classifier, base,input_,base,1.)
		if self.N[classifier].get(base) is None:
			print classifier,base,input_ , "base NOT FOUND"
			#self.print_N()
			append_dict(self.N,classifier, base,input_,1.)
			append_dict2(self.A,classifier, base,input_,base,1.)
		if self.N[classifier][base].get(input_) is None:
			print classifier,base,input_ , "intput_NOT FOUND"
			#self.print_N()
			append_dict(self.N,classifier, base,input_,1.)
			append_dict2(self.A,classifier, base,input_,base,1.)


		c=0.
		r=random.random()

		N=self.N[classifier][base][input_]

		if self.A[classifier][base].get(input_) is None:
			return base

		for k,v in self.A[classifier][base][input_].items():
			#print classifier,base,input_,k,v,"b",N
			#print "DIDNT MAKE IT HERE",c,v/N
			if r < c+v/N:
				#print "returning k: ", k, "with: ",v,N
				return k
			c+=v/N

		print "MADE IT TO NONE SHOUJLDNOT HAPPEN",v,N,classifier,base
		return None

	def pull_from_rewards(self,abstraction_function):
		if self.R.get(abstraction_function) is None:
			print abstraction_function, "abstraction_function not found"
			#append_dict_1(self.R,abstraction_function,1.)
			return 0.
		return self.R[abstraction_function]		
		
	def get_inherent_reward(self,c,b,i,num):

		#print "EXPLORE REWARD", b
		#print num
		return num
		
	def check_size(self,H):
		count=0
		for k,v in H.items():
			for k2,v2 in H[k].items():
				for k3,v3 in H[k][k2].items():
					count+=1

		print "size of H is", count

def update_H(H,A1,A2,a,R):
	#STUFF HEURISTICS HERE
	#REW	self.get_lower_level_abf(a)
	#append_dict(H.NN,a.policy_set.TA.identification,A1.get_lower_level_abf(a),1.) 
	#LOWER LEVEL REWARD
	#print "adding", H.R[a.policy_set.identification][A1.get_top_level_abf()][a.policy_set.TA.index],a.policy_set.identification,A1.get_top_level_abf(),a.policy_set.TA.index
	#print "adding",A1.get_reward_abf(a.current_action.index)
	append_dict_1(H.N,A1.get_reward_abf(a.current_action.index),0.)
	append_dict_1(H.N,A1.get_reward_abf(a.current_action.index),1.)
	append_dict_1(H.R,A1.get_reward_abf(a.current_action.index),0.)
	append_dict_1(H.R,A1.get_reward_abf(a.current_action.index),(R-H.R[A1.get_reward_abf(a.current_action.index)])/H.N[A1.get_reward_abf(a.current_action.index)])
	
	append_dict_1(H.visits,A1.get_reward_abf(a.current_action.index),1.)

	#print "adding", H.R[a.policy_set.TA.identification][A1.get_reward_abf(a,a.policy_set.TA.LA.index)]["empty"], a.policy_set.TA.identification,A1.get_reward_abf(a,a.policy_set.TA.LA.index),a.policy_set.TA.LA.index,H.N[a.policy_set.TA.identification][A1.get_reward_abf(a,a.policy_set.TA.LA.index)]["empty"]

	#A
	#for i in range(len(A1.regions)):

	#	indent=A1.regions[i].identification
	#	base=str(A1.regions[i].hash)
	#	input_=str(A1.regions[i].get_input(A1.work_load[i]))
		
	#	output=str(A2.regions[i].hash)
	#	append_dict(H.N,indent,base,input_,1.)
	#	append_dict2(H.A,indent,base,input_,output,1.)


	#for i in range(len(A1.work_load)):

	#	indent=A1.work_load[i].identification
	#	base=str(A1.work_load[i].hash)
	#	input_=str(A1.work_load[i].get_input(A1.regions[i]))
	##	output=str(A2.work_load[i].hash)
		
	#	append_dict(H.N,indent,base,input_,1.)
	#	append_dict2(H.A,indent,base,input_,output,1.)

	#print_region_transitions(H,A1)

	#indent=A1.location.identification
	#base=A1.location.hash
	#input_=A1.location.get_input(a.policy_set.TA.LA.index)
	#output=A2.location.hash

	#print_location_transitions(H,A1)

	#append_dict(H.N,indent,base,input_,1.)
	#append_dict2(H.A,indent,base,input_,output,1.)

def print_region_transitions(H,A):
	print "begin"
	for i in range(1,6):
		for k,v in H.A["AR: " + str(i)].items():
			for k2,v2 in H.A["AR: " + str(i)][k].items():
				for k3,v3 in H.A["AR: " + str(i)][k][k2].items():
					print i,k,k2,k3,v3/H.N["AR: " + str(i)][k][k2]
					
def print_location_transitions(H,A):
	print "begin"

	if H.A.get("AL") is not None:
		for k,v in H.A["AL"].items():
			for k2,v2 in H.A["AL"][k].items():
				for k3,v3 in H.A["AL"][k][k2].items():
					print k,k2,k3,v3/H.N["AL"][k][k2]




def write_file(H,filename):
	file = open('testfile_d_temp_mult.txt','w') 
	print "writing file: testfile_d.txt"
	 

	for k,v in H.R.items():
		print H.R[k]
		print k
		print H.N[k],"g"
		file.write("R"+","+str(k) + "," + str(v) + "," +  str(H.N[k]) + "\n")

	#for i in range(1,6):
	#	for k,v in H.A["AR: " + str(i)].items():
	#		for k2,v2 in H.A["AR: " + str(i)][k].items():
	#			for k3,v3 in H.A["AR: " + str(i)][k][k2].items():
	#				file.write("A" +","+"AR: " + str(i) + "," + str(k) + ","+   str(k2) + "," + str(k3) + "," + str(v3) + "," +  str(H.N["AR: " + str(i)][k][k2]) + "\n")



	 
	file.close()

def load_file(H,filename):

	f = open(filename,'r')
	for line in f:
		l = line.split(",")
		append_dict_if_missing(H.N,l[1],float(l[3].strip('\n')))
		append_dict_1(H.R,l[1],float(l[2]))

	print "FILES LOADED"

		
				





	

