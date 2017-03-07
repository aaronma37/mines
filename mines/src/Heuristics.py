#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
import Regions
#Tool class
import random
import os


def append_dict(P,h1,h2,h3,r):
	if P.get(h1) is None:
		P[h1]={h2:{h3:r}}
	elif P[h1].get(h2) is None:
		P[h1][h2]={h3:r}
	elif P[h1][h2].get(h3) is None:
		P[h1][h2][h3]=r
	else:
		P[h1][h2][h3]+=r

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



	def pull_new_abstraction(self,classifier, base,input_):

		if base is None:
			print "error in abstraction pull"
			return base


		if self.N.get(classifier) is None:
			append_dict(self.N,classifier, base,input_,1.)
			append_dict2(self.A,classifier, base,input_,base,1.)
		if self.N[classifier].get(base) is None:
			append_dict(self.N,classifier, base,input_,1.)
			append_dict2(self.A,classifier, base,input_,base,1.)
		if self.N[classifier][base].get(input_) is None:
			append_dict(self.N,classifier, base,input_,1.)
			append_dict2(self.A,classifier, base,input_,base,1.)


		c=0.
		r=random.random()

		N=self.N[classifier][base][input_]

		if self.A[classifier][base].get(input_) is None:
			return base

		for k,v in self.A[classifier][base][input_].items():
			#print k,v,"b",N
			#print "DIDNT MAKE IT HERE",c,v/N
			if r < c+v/N:
				return k
			c+=v/N

		print "MADE IT TO NONE SHOUJLDNOT HAPPEN",c,N
		return None

	def pull_from_rewards(self,classifier,base,input_):
		
		#if classifier=="Explore" and num==0:
			#return 0.
			

		if self.R.get(classifier) is None:
			#if classifier=="Explore":
			#	return self.get_inherent_reward(classifier,base,input_,num)
			if input_ == 0:
				append_dict(self.R,classifier, base,input_,1.)
			else:
				append_dict(self.R,classifier, base,input_,1.)

		if self.R[classifier].get(base) is None:
			#if classifier=="Explore":
			#	return self.get_inherent_reward(classifier,base,input_,num)
			if input_ == 0:
				append_dict(self.R,classifier, base,input_,1.)
			else:
				append_dict(self.R,classifier, base,input_,1.)

		if self.R[classifier][base].get(input_) is None:
			#if classifier=="Explore":
			#	return self.get_inherent_reward(classifier,base,input_,num)
			if input_ == 0:
				append_dict(self.R,classifier, base,input_,1.)
			else:
				append_dict(self.R,classifier, base,input_,1.)

		#print self.R[classifier][base][input_]
		#if self.N.get(classifier)is not None:
		#	print self.N[classifier][base][input_]
		#print classifier,base,input_
		return self.R[classifier][base][input_]		
		
	def get_inherent_reward(self,c,b,i,num):

		#print "EXPLORE REWARD", b
		#print num
		return num
		


def update_H(H,A1,A2,a,R):
	#STUFF HEURISTICS HERE
	#REW	self.get_lower_level_abf(a)
	#append_dict(H.NN,a.policy_set.TA.identification,A1.get_lower_level_abf(a),1.) 

	#HIGHER LEVEL REWARD
	append_dict(H.N,a.policy_set.identification,A1.get_top_level_abf(),a.policy_set.TA.index,1.)

	append_dict(H.R,a.policy_set.identification,A1.get_top_level_abf(),a.policy_set.TA.index,0.)
	append_dict(H.R,a.policy_set.identification,A1.get_top_level_abf(),a.policy_set.TA.index,(R-H.R[a.policy_set.identification][A1.get_top_level_abf()][a.policy_set.TA.index])/H.N[a.policy_set.identification][A1.get_top_level_abf()][a.policy_set.TA.index])


	append_dict(H.visits,a.policy_set.identification,A1.get_top_level_abf(),a.policy_set.TA.index,1.)
	#LOWER LEVEL REWARD
	#print "adding", H.R[a.policy_set.identification][A1.get_top_level_abf()][a.policy_set.TA.index],a.policy_set.identification,A1.get_top_level_abf(),a.policy_set.TA.index

	append_dict(H.N,a.policy_set.TA.identification,A1.get_reward_abf(a,a.policy_set.TA.LA.index),"empty",1.)
	append_dict(H.R,a.policy_set.TA.identification,A1.get_reward_abf(a,a.policy_set.TA.LA.index),"empty",0.)
	append_dict(H.R,a.policy_set.TA.identification,A1.get_reward_abf(a,a.policy_set.TA.LA.index),"empty",(R-H.R[a.policy_set.TA.identification][A1.get_reward_abf(a,a.policy_set.TA.LA.index)]["empty"])/H.N[a.policy_set.TA.identification][A1.get_reward_abf(a,a.policy_set.TA.LA.index)]["empty"])
	
	append_dict(H.visits,a.policy_set.TA.identification,A1.get_lower_level_abf(a),a.policy_set.TA.LA.index,1.)

	print "adding", H.R[a.policy_set.TA.identification][A1.get_reward_abf(a,a.policy_set.TA.LA.index)]["empty"], a.policy_set.TA.identification,A1.get_reward_abf(a,a.policy_set.TA.LA.index),a.policy_set.TA.LA.index,H.N[a.policy_set.TA.identification][A1.get_reward_abf(a,a.policy_set.TA.LA.index)]["empty"]

	#A
	for i in range(len(A1.regions)):

		indent=A1.regions[i].identification
		base=A1.regions[i].hash
		input_=A1.regions[i].get_input(A1.work_load[i])
		
		output=A2.regions[i].hash
		append_dict(H.N,indent,base,input_,1.)
		append_dict2(H.A,indent,base,input_,output,1.)


	for i in range(len(A1.work_load)):

		indent=A1.work_load[i].identification
		base=A1.work_load[i].hash
		input_=A1.work_load[i].get_input(A1.regions[i])
		output=A2.work_load[i].hash
		
		append_dict(H.N,indent,base,input_,1.)
		append_dict2(H.A,indent,base,input_,output,1.)

	#print_region_transitions(H,A1)

	indent=A1.location.identification
	base=A1.location.hash
	input_=A1.location.get_input(a.policy_set.TA.LA.index)
	output=A2.location.hash

	#print_location_transitions(H,A1)

	append_dict(H.N,indent,base,input_,1.)
	append_dict2(H.A,indent,base,input_,output,1.)

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

def load_file(H,filename):

	f = open('filename','r')
	print f.read() 

def write_file(H,filename):
	file = open('testfile.txt','w') 

	 

	for k,v in H.R.items():
		for k2,v2 in H.R[k].items():
			for k3,v3 in H.R[k][k2].items():
				file.write("R"+","+str(k) + "," +  str(k2) + "," + str(k3) + "," + str(v3) + "," +  str(H.N[k][k2][k3]) + "\n")

	for i in range(1,6):
		for k,v in H.A["AR: " + str(i)].items():
			for k2,v2 in H.A["AR: " + str(i)][k].items():
				for k3,v3 in H.A["AR: " + str(i)][k][k2].items():
					file.write("A" +","+"AR: " + str(i) + "," + str(k) + ","+   str(k2) + "," + str(k3) + "," + str(v3) + "," +  str(H.N["AR: " + str(i)][k][k2]) + "\n")


	 
	file.close()
		
				





	
