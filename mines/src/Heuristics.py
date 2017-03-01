#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
import Regions
#Tool class
import random



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
		self.R={} #type,base,input, -> accrued reward
		#classifier,input,output

			

	def update(self,classifier, base, input_,output_,reward):
		append_dict(self.N,classifier, base,input_,1.)
		append_dict2(self.A,classifier, base,input_,output_,1.)

		append_dict(self.R,classifier, base,input_,0.)
		append_dict(self.R,classifier, base,input_,(reward-self.R[classifier][input_])/self.N[classifier][input_])


	def pull_new_abstraction(self,classifier, base,input_):

		#Returns from particle

		if self.N.get(classifier) is None:
			append_dict(self.N,classifier, base,input_,1.)
			append_dict2(self.A,classifier, base,input_,input_,1.)
		if self.N[classifier].get(base) is None:
			append_dict(self.N,classifier, base,input_,1.)
			append_dict2(self.A,classifier, base,input_,input_,1.)
		if self.N[classifier][base].get(input_) is None:
			append_dict(self.N,classifier, base,input_,1.)
			append_dict2(self.A,classifier, base,input_,input_,1.)


		c=0.
		r=random.random()

		N=self.N[classifier][base][input_]

		if self.A[classifier][base].get(input_) is None:
			return input_

		for k,v in self.A[classifier][base][input_].items():
			#print "DIDNT MAKE IT HERE",c,v/N
			if r < c+v/N:
				return v
			c+=v/N

		#print "MADE IT TO NONE SHOUJLDNOT HAPPEN",c,N
		return None

	def pull_from_rewards(self,classifier,base,input_):
		
		if self.R.get(classifier) is None:

			if input_ == 0:
				append_dict(self.R,classifier, base,input_,0.)
			else:
				append_dict(self.R,classifier, base,input_,1.)

		if self.R[classifier].get(base) is None:
			if input_ == 0:
				append_dict(self.R,classifier, base,input_,0.)
			else:
				append_dict(self.R,classifier, base,input_,1.)

		if self.R[classifier][base].get(input_) is None:
			if input_ == 0:
				append_dict(self.R,classifier, base,input_,0.)
			else:
				append_dict(self.R,classifier, base,input_,1.)

		#print self.R[classifier][base][input_]
		#if self.N.get(classifier)is not None:
		#	print self.N[classifier][base][input_]
		return self.R[classifier][base][input_]

def update_H(H,A1,A2,a,R):
	#STUFF HEURISTICS HERE
	#REW	self.get_lower_level_abf(a)
	append_dict(H.N,a.policy_set.TA.LA.identification,A1.get_lower_level_abf(a),a.policy_set.TA.LA.index,1.)
	append_dict(H.R,a.policy_set.TA.LA.identification,A1.get_lower_level_abf(a),a.policy_set.TA.LA.index,(R-H.R[a.policy_set.TA.LA.identification][A1.get_lower_level_abf(a)][a.policy_set.TA.LA.index])/H.N[a.policy_set.TA.LA.identification][A1.get_lower_level_abf(a)][a.policy_set.TA.LA.index])

	#A
	for i in range(len(A1.regions)):

		indent=A1.regions[i].identification
		base=A1.regions[i].hash
		input_=A1.regions[i].get_input(A1.work_load[i])
		output=A2.regions[i]
		
		append_dict(H.N,indent,base,input_,1.)
		append_dict2(H.A,indent,base,input_,output,1.)

	for i in range(len(A1.work_load)):

		indent=A1.work_load[i].identification
		base=A1.work_load[i].hash
		input_=A1.work_load[i].get_input(A1.regions[i])
		output=A2.work_load[i]
		
		append_dict(H.N,indent,base,input_,1.)
		append_dict2(H.A,indent,base,input_,output,1.)

	indent=A1.location.identification
	base=A1.location.hash
	input_=A1.location.get_input(a.policy_set.TA.LA.index)
	output=A2.location.hash

	append_dict(H.N,indent,base,input_,1.)
	append_dict2(H.A,indent,base,input_,output,1.)






	

