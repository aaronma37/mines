import matplotlib.pyplot as plt
import numpy
import math
import time



data={}
trials={}
N_LIST=[0.0,1.0]

t_values=[.0001,.0003162,.001,.003162,.01,.03162,.1,.3162,1.,3.162]

pd={}
pd[0.0]='t'
pd[1.0]='s'
pd[2.0]=','



n=0.0
data[n]={}
trials[n]={}
for t in t_values:
	try:
		f = open('/home/aaron/mines_temp/single_mcts_'+ str(0.0) +'_' + str(t) +'.txt','r')
	except IOError:
#		print ('results_'+ str(n) +'_' + str(t) +'.txt'), " not found"
		continue	
	c=0
	data[n][t]=[]
	trials[n][t]=[]
	for line in f:
		l = line.split(',')
#		print "length:", len(l)
		if c==0:
			for score in l:
				try:				
					data[n][t].append(float(score))
				except ValueError:
					''' '''
		else:
			for score in l:
				try:				
					trials[n][t].append(float(score))
	#				print score		
				except ValueError:
					''' '''
		c+=1

n=1.0
data[n]={}
trials[n]={}
for t in t_values:
	try:
		f = open('/home/aaron/mines_temp/single_ddr_'+ str(0.0) +'_' + str(t) +'.txt','r')
	except IOError:
#		print ('results_'+ str(n) +'_' + str(t) +'.txt'), " not found"
		continue	
	c=0
	data[n][t]=[]
	trials[n][t]=[]
	for line in f:
		l = line.split(',')
#		print "length:", len(l)
		if c==0:
			for score in l:
				try:				
					data[n][t].append(float(score))
				except ValueError:
					''' '''
		else:
			for score in l:
				try:				
					trials[n][t].append(float(score))
	#				print score		
				except ValueError:
					''' '''
		c+=1


		

Q={}
Q_trials={}

#for n in N_LIST:
#	Q[n]={}
#	#trials[n]={}
#	for t in t_values:
#		try:
#			f = open('/home/aaron/mines_temp/q_'+ str(int(n)) +'_' + str(t) +'.txt','r')
#		except IOError:
#			print ('/home/aaron/mines_temp/q_'+ str(int(n)) +'_' + str(t) +'.txt'), " not found"
#			continue	
#		Q[n][t]={}
#		#Q_trials[n][t]={}
#		for line in f:
#			l = line.split('*')
#			#print l, len(l)
#			if len(l)==4:
#				if Q[n][t].get(l[0]) is None:
#					Q[n][t][l[0]]={}
#					Q[n][t][l[0]][l[1]]=l[2]
#				elif Q[n][t][l[0]].get(l[1]) is None:
#					Q[n][t][l[0]][l[1]]=l[2]
#				else:	
#					Q[n][t][l[0]][l[1]]=l[2]
#					print 'error', n,t,l[0],l[1]




#q_diff={}
#q_diff_list={}
#for n in N_LIST:
#	q_diff[n]={}
#	q_diff_list[n]={}
#	for t in t_values:
#		q_diff[n][t]={}	
#		q_diff_list[n][t]=[]
#		'''
#		for k,v in Q[n][t].items():
#			q_diff[n][t][k]={}
#			
#			for k2,v2 in v.items():
#				q_diff[n][t][k][k2]={}
#				if Q[n][t_values[-1]].get(k) is None:
#					#continue 
#					q_diff[n][t][k][k2]=1
#				elif Q[n][t_values[-1]][k].get(k2) is None:
#					#continue
#					q_diff[n][t][k][k2]=1
#				else:
#					
#					q_diff[n][t][k][k2]=abs(float(v2)-float(Q[n][t_values[-1]][k][k2]))
#				q_diff_list[n][t].append(q_diff[n][t][k][k2])
#	
#		'''
#
#		for k,v in Q[n][t_values[-1]].items():
#			q_diff[n][t][k]={}
#			for k2,v2 in v.items():
#				q_diff[n][t][k][k2]={}
#				if Q[n][t].get(k) is None:
#					#continue
#					q_diff[n][t][k][k2]=1
#				elif Q[n][t][k].get(k2) is None:
#					#continue
#					q_diff[n][t][k][k2]=1
#				else:
#					
#					q_diff[n][t][k][k2]=abs(float(v2)-float(Q[n][t][k][k2]))
#				q_diff_list[n][t].append(q_diff[n][t][k][k2])
		


'''

data["N=0"]={}
data["N=0"][.001]=[4.43192435858, 4.43192435858, 0.0, 4.43192435858, 0.0, 4.43192435858, 4.30029177321, 4.43192435858, 0.0, 0.0, 0.0, 0.0, 4.43192435858, 0.0, 4.43192435858, 0.0, 4.43192435858, 8.86384871716, 0.0, 0.0, 4.43192435858, 0.0, 0.0, 0.0, 0.0, 8.86384871716, 0.0, 4.43192435858, 0.0, 4.43192435858, 4.43192435858, 0.0, 0.0, 4.43192435858, 0.0, 4.43192435858, 0.0, 0.0, 0.0, 8.73221613179, 0.0, 4.43192435858, 8.73221613179, 4.43192435858, 4.43192435858, 0.0, 8.86384871716, 0.0, 4.43192435858, 0.0, 0.0, 0.0, 0.0, 4.43192435858, 0.0, 0.0, 4.43192435858, 0.0, 4.30029177321, 8.73221613179, 0.0, 4.43192435858, 4.43192435858, 8.73221613179, 0.0, 4.43192435858, 0.0, 4.43192435858, 0.0, 0.0, 4.43192435858, 4.43192435858, 0.0, 4.43192435858, 0.0, 4.43192435858, 8.73221613179, 0.0, 4.43192435858, 0.0, 0.0, 0.0, 4.43192435858, 8.73221613179, 0.0, 0.0, 0.0, 0.0, 4.43192435858, 0.0, 4.43192435858, 0.0, 0.0, 4.43192435858, 13.032507905, 0.0, 13.1641404904, 0.0, 0.0, 0.0]


data["N=0"][.01]=[13.1641404904, 13.1641404904, 0.0, 8.73221613179, 8.73221613179, 4.43192435858, 17.4644322636, 4.43192435858, 8.73221613179, 13.032507905, 4.43192435858, 4.43192435858, 8.73221613179, 8.73221613179, 4.30029177321, 4.43192435858, 4.43192435858, 8.73221613179, 8.73221613179, 4.43192435858, 4.43192435858, 8.73221613179, 13.032507905, 13.032507905, 8.73221613179, 13.1641404904, 8.73221613179, 13.1641404904, 0.0, 8.73221613179, 13.032507905, 8.73221613179, 4.43192435858, 4.43192435858, 10.8823620184, 6.45043765981, 13.1641404904, 8.73221613179, 8.60058354641, 4.43192435858, 8.73221613179, 13.032507905, 13.032507905, 8.73221613179, 4.43192435858, 8.73221613179, 4.43192435858, 13.032507905, 4.30029177321, 4.43192435858, 13.032507905, 8.73221613179, 4.43192435858, 13.1641404904, 8.73221613179, 13.032507905, 4.43192435858, 17.3327996782, 4.43192435858, 4.43192435858, 4.43192435858, 8.73221613179, 13.032507905, 8.73221613179, 13.032507905, 13.032507905, 8.73221613179, 8.86384871716, 8.60058354641, 8.73221613179, 8.73221613179, 8.60058354641, 4.43192435858, 4.30029177321, 4.43192435858, 8.73221613179, 4.30029177321, 4.43192435858, 17.3327996782, 4.43192435858, 13.032507905, 13.032507905, 8.73221613179, 8.73221613179, 13.032507905, 17.4644322636, 8.73221613179, 8.86384871716, 4.30029177321, 4.43192435858, 8.73221613179, 8.73221613179, 4.43192435858, 4.43192435858, 17.3327996782, 17.3327996782, 4.43192435858, 8.73221613179, 13.032507905, 4.43192435858]


data["N=0"][.03162]=[8.73221613179, 8.73221613179, 17.3327996782, 17.3327996782, 13.032507905, 19.6145781502, 21.6330914514, 8.73221613179, 4.43192435858, 8.60058354641, 21.7647240368, 0.0, 8.86384871716, 17.3327996782, 12.9008753196, 26.06501581, 17.4644322636, 17.3327996782, 8.60058354641, 8.73221613179, 17.4644322636, 10.750729433, 8.73221613179, 13.032507905, 17.4644322636, 13.032507905, 8.73221613179, 21.7647240368, 0.0, 13.032507905, 17.4644322636, 13.032507905, 4.43192435858, 17.3327996782, 4.30029177321, 8.73221613179, 13.032507905, 13.1641404904, 4.30029177321, 13.1641404904, 17.3327996782, 0.0, 17.4644322636, 8.73221613179, 12.9008753196, 21.7647240368, 4.30029177321, 21.6330914514, 8.73221613179, 4.43192435858, 21.7647240368, 4.30029177321, 17.3327996782, 8.73221613179, 4.43192435858, 17.3327996782, 4.43192435858, 8.60058354641, 4.43192435858, 17.3327996782, 4.43192435858, 21.7647240368, 4.30029177321, 17.4644322636, 6.45043765981, 13.1641404904, 4.30029177321, 21.7647240368, 13.1641404904, 0.0, 13.032507905, 13.032507905, 4.43192435858, 4.30029177321, 4.43192435858, 21.7647240368, 4.43192435858, 13.032507905, 8.86384871716, 8.73221613179, 4.30029177321, 13.1641404904, 13.032507905, 10.1656467229, 13.032507905, 13.032507905, 13.032507905, 13.032507905, 8.60058354641, 13.1641404904, 4.30029177321, 17.4644322636, 4.30029177321, 13.1641404904, 8.60058354641, 13.1641404904, 13.032507905, 17.3327996782, 13.032507905, 4.30029177321]







data["N=0"][.1]=[21.6330914514, 25.9333832246, 17.3327996782, 8.60058354641, 13.032507905, 11.8038531126, 26.06501581, 21.501458866, 9.44893142732, 13.032507905, 17.3327996782, 21.7647240368, 21.6330914514, 17.4644322636, 12.9008753196, 21.6330914514, 30.3653075832, 21.6330914514, 4.43192435858, 21.6330914514, 13.032507905, 21.7647240368, 13.032507905, 17.3327996782, 13.032507905, 14.1075808483, 21.7647240368, 6.23542307115, 9.80728907509, 21.7647240368, 17.3327996782, 8.60058354641, 13.032507905, 13.1641404904, 17.3327996782, 21.6330914514, 17.4644322636, 26.06501581, 17.3327996782, 13.032507905, 13.032507905, 17.2011670928, 17.3327996782, 14.4659384961, 26.06501581, 21.6330914514, 17.4644322636, 18.3244906182, 9.59227448643, 21.7647240368, 21.6330914514, 13.032507905, 17.3327996782, 17.3327996782, 5.16035012785, 15.1826537916, 17.4644322636, 5.37536471651, 19.4829455648, 17.3327996782, 8.60058354641, 15.1826537916, 13.032507905, 8.73221613179, 17.3327996782, 17.3327996782, 17.3327996782, 13.032507905, 14.5975710814, 8.60058354641, 13.032507905, 26.06501581, 12.9008753196, 17.3327996782, 13.032507905, 13.032507905, 21.501458866, 4.43192435858, 13.032507905, 17.3327996782, 17.3327996782, 17.3327996782, 13.032507905, 17.4644322636, 25.9333832246, 21.7647240368, 12.9008753196, 8.73221613179, 8.60058354641, 25.9333832246, 21.6330914514, 17.4644322636, 18.7662302693, 13.032507905, 13.032507905, 17.3327996782, 21.6330914514, 10.1656467229, 4.43192435858, 22.8397969801, ]


data["N=0"][1.]=[21.7647240368, 25.8017506392, 30.3653075832, 25.9333832246, 26.06501581, 17.2011670928, 21.6330914514, 26.1966483954, 21.6330914514, 26.06501581, 21.6330914514, 21.6330914514, 30.3653075832, 25.9333832246, 21.501458866, 26.06501581, 21.7647240368, 17.3327996782, 26.06501581, 25.9333832246, 12.9008753196, 25.9333832246, 17.2011670928, 25.9333832246, 30.2336749978, 17.2011670928, 17.2011670928, 34.533966771, 21.7647240368, 34.4023341857, 21.501458866, 34.533966771, 21.501458866, 30.3653075832, 21.6330914514, 21.501458866, 17.2011670928, 34.533966771, 25.8017506392, 26.1966483954, 21.6330914514, 25.9333832246, 21.6330914514, 25.9333832246, 21.501458866, 34.6655993564, 8.60058354641, 17.3327996782, 30.2336749978, 17.3327996782, 17.2011670928, 21.6330914514, 21.6330914514, 21.6330914514, 21.7647240368, 21.501458866, 25.9333832246, 30.3653075832, 21.6330914514, 17.3327996782, 39.097523715, 26.3282809807, 21.501458866, 25.9333832246, 21.6330914514, 21.6330914514, 25.9333832246, 21.6330914514, 25.9333832246, 12.9008753196, 34.6655993564, 34.7972319418, 25.9333832246, 25.9333832246, 25.9333832246, 21.501458866, 39.3607888857,25.9333832246, 17.2011670928, 21.6330914514, 25.9333832246, 17.3327996782, 34.533966771, 30.2336749978, 26.06501581, 34.7972319418]

data["N=0"][3.162]=[38.9658911296, 26.1966483954, 25.9333832246, 0.0, 34.7972319418, 30.2336749978, 34.533966771, 8.73221613179, 21.6330914514, 25.9333832246, 38.9658911296, 0.0, 34.6655993564, 26.06501581, 25.9333832246, 13.032507905, 8.73221613179, 34.6655993564, 30.3653075832, 38.9658911296, 0.0, 21.7647240368, 30.2336749978, 26.1966483954, 8.60058354641, 4.30029177321, 30.2336749978, 26.3282809807, 34.6655993564, 0.0, 26.06501581, 38.9658911296]



data["N=0"][10.]=[30.3653075832, 38.9658911296, 34.533966771, 25.9333832246, 25.9333832246, 34.6655993564, 25.9333832246, 26.1966483954, 30.2336749978, 23.5682227493, 25.9333832246, 26.06501581, 25.9333832246, 26.06501581, 30.3653075832, 25.9333832246, 30.3653075832, 25.9333832246, 30.2336749978, 26.06501581, 30.3653075832, 26.06501581, 34.7972319418, 25.9333832246, 30.3653075832, 26.06501581, 26.06501581, 25.9333832246, 23.9787051459, 30.2336749978, 21.9197775696, 30.2336749978, 26.06501581, 30.3653075832, 22.2946748011, 30.2336749978, 25.9333832246, 26.06501581, 34.6655993564, 30.3653075832, 26.1966483954, 25.9333832246, 26.06501581, 25.9333832246, 26.06501581, 26.06501581, 26.06501581, 26.06501581, 30.4969401686, 21.7647240368, 25.9333832246, 21.6330914514, 25.9333832246, 25.9333832246, 25.9333832246, 21.7647240368, 26.06501581, 21.6330914514, 30.4969401686, 25.9333832246, 25.9333832246, 26.06501581, 21.6989077441, 25.9333832246, 30.2336749978, 26.06501581, 30.3653075832, 34.6655993564, 26.06501581, 26.06501581, 26.06501581, 25.9333832246]

data["N=0"][100.]=[39.1633400077]

data["N=1"]={}

data["N=1"][.001]=[0.0, 0.0, 0.0, 0.0, 4.43192435858, 8.86384871716, 0.0, 13.1641404904, 0.0, 0.0, 4.43192435858, 0.0, 4.43192435858, 4.43192435858, 0.0, 4.30029177321, 4.43192435858, 4.43192435858, 0.0, 0.0, 0.0, 4.30029177321, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.43192435858, 4.43192435858, 0.0, 4.43192435858, 4.43192435858, 0.0, 4.43192435858, 0.0, 4.30029177321, 0.0, 0.0, 4.43192435858, 0.0, 0.0, 0.0, 8.86384871716, 0.0, 8.86384871716, 0.0, 8.73221613179, 0.0, 8.73221613179, 0.0, 0.0, 0.0, 8.86384871716, 0.0, 0.0, 8.86384871716, 0.0, 4.43192435858, 0.0, 4.43192435858, 0.0, 0.0, 0.0, 0.0, 4.43192435858, 0.0, 0.0, 0.0, 0.0, 4.43192435858, 4.43192435858, 4.43192435858, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 8.73221613179, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.43192435858, 0.0, 0.0, 0.0, 4.43192435858, 0.0, 4.43192435858, 0.0, 0.0, 0.0, 0.0]
 


data["N=1"][.01]=[8.86384871716, 21.8963566222, 8.73221613179, 13.1641404904, 8.73221613179, 8.86384871716, 13.032507905, 4.43192435858, 4.43192435858, 13.032507905, 8.73221613179, 13.1641404904, 8.73221613179, 4.43192435858, 13.1641404904, 4.43192435858, 8.73221613179, 17.4644322636, 4.30029177321, 13.032507905, 8.86384871716, 0.0, 4.43192435858, 8.73221613179, 8.73221613179, 4.43192435858, 13.032507905, 8.73221613179, 13.032507905, 13.1641404904, 0.0, 8.73221613179, 26.06501581, 4.43192435858, 8.73221613179, 4.43192435858, 13.1641404904, 4.43192435858, 4.43192435858, 13.032507905, 8.86384871716, 0.0, 8.73221613179, 13.032507905, 4.43192435858, 8.73221613179, 8.86384871716, 12.9008753196, 13.032507905, 8.73221613179, 8.73221613179, 4.43192435858, 4.43192435858, 17.3327996782, 13.032507905, 13.1641404904, 4.30029177321, 13.032507905, 8.73221613179, 8.86384871716, 8.73221613179, 8.86384871716, 8.73221613179, 4.43192435858, 4.43192435858, 4.43192435858, 4.43192435858, 4.43192435858, 8.73221613179, 13.032507905, 8.86384871716, 4.30029177321, 4.43192435858, 8.86384871716, 8.73221613179, 8.73221613179, 4.43192435858, 4.43192435858, 17.4644322636, 4.30029177321, 17.3327996782, 8.86384871716, 8.73221613179, 4.43192435858, 8.73221613179, 8.73221613179, 8.73221613179, 4.43192435858, 4.43192435858, 4.30029177321, 13.1641404904, 8.73221613179, 17.3327996782, 13.032507905, 8.86384871716, 0.0, 13.032507905, 8.73221613179, 8.73221613179, 4.43192435858]
 
data["N=1"][.1]=[21.7647240368, 26.06501581, 6.45043765981, 17.4644322636, 17.4644322636, 8.60058354641, 21.6330914514, 17.3327996782, 13.032507905, 4.30029177321, 21.6330914514, 13.032507905, 17.3327996782, 21.7647240368, 13.032507905, 23.1981546278, 13.032507905, 21.7647240368, 13.032507905, 17.4644322636, 12.9008753196, 17.3327996782, 21.7647240368, 21.8963566222, 17.3327996782, 17.3327996782, 26.1966483954, 13.032507905, 17.4644322636, 21.6330914514, 26.06501581, 8.73221613179, 21.7647240368, 17.3327996782, 21.7647240368, 25.8017506392, 26.1966483954, 21.6330914514, 13.032507905, 26.06501581, 17.4644322636, 8.60058354641, 13.032507905, 13.032507905, 13.032507905, 21.8963566222, 21.6330914514, 21.8963566222, 8.60058354641, 11.0139946038, 4.43192435858, 17.4644322636, 21.7647240368, 17.3327996782, 12.9008753196, 25.9333832246, 26.1966483954, 26.06501581, 21.7647240368, 21.6330914514, 25.9333832246, 25.9333832246, 17.4644322636, 13.032507905, 12.9008753196, 21.6330914514, 21.7647240368, 13.032507905, 8.60058354641, 8.73221613179, 26.3282809807, 10.750729433, 13.032507905, 21.8963566222, 21.6330914514, 17.3327996782, 17.3327996782, 26.06501581, 13.032507905, 17.4644322636, 17.3327996782, 21.7647240368, 21.501458866, 18.7662302693, 21.7647240368, 17.2011670928, 8.73221613179, 17.3327996782, 25.9333832246, 21.7647240368, 15.1826537916, 17.3327996782, 13.032507905, 23.9148699234, 8.73221613179, 21.7647240368, 10.1656467229, 26.06501581, 17.4644322636, 13.032507905]


data["N=1"][1.]=[26.06501581, 25.8017506392, 43.5294480736, 17.3327996782, 21.7647240368, 30.2336749978, 21.501458866, 38.9658911296, 34.6655993564, 21.6330914514, 21.501458866, 17.3327996782, 17.2011670928, 17.3327996782, 17.3327996782, 17.3327996782, 17.3327996782, 30.2336749978, 21.501458866, 25.9333832246, 21.501458866, 30.2336749978, 21.6330914514, 30.3653075832, 34.533966771, 17.3327996782, 21.6330914514, 21.501458866, 21.7647240368, 12.9008753196, 17.3327996782, 25.9333832246, 21.6330914514, 25.8017506392, 21.501458866, 25.9333832246, 21.6330914514, 25.8017506392, 30.2336749978, 21.501458866, 12.9008753196, 25.9333832246, 25.8017506392, 21.501458866, 17.2011670928, 21.7647240368, 21.7647240368, 17.3327996782, 21.501458866, 30.3653075832, 30.2336749978, 17.2011670928, 21.501458866, 25.9333832246, 25.9333832246, 21.6330914514, 21.501458866, 26.1966483954, 17.2011670928, 26.06501581, 21.501458866, 30.3653075832, 21.501458866, 25.9333832246, 21.501458866, 21.7647240368, 21.501458866, 26.06501581, 21.501458866, 30.2336749978, 25.9333832246, ]

data["N=1"][10.]=[39.2291563004, 52.13003162, 34.533966771, 47.566474676, 43.3978154882, 30.2336749978, 43.3978154882, 47.566474676, 38.9658911296]

data["N=2"]={}
data["N=2"][.001]=[8.73221613179, 8.73221613179, 4.43192435858, 0.0, 0.0, 4.43192435858, 0.0, 0.0, 0.0, 4.43192435858, 8.73221613179, 8.86384871716, 4.30029177321, 8.86384871716, 4.43192435858, 0.0, 0.0, 8.86384871716, 0.0, 0.0, 0.0, 0.0, 4.43192435858, 0.0, 0.0, 0.0, 4.43192435858, 0.0, 4.43192435858, 0.0, 0.0, 4.43192435858, 0.0, 4.43192435858, 0.0, 4.43192435858, 0.0, 0.0, 8.86384871716, 4.30029177321, 4.43192435858, 4.43192435858, 4.43192435858, 0.0, 4.43192435858, 0.0, 0.0, 8.86384871716, 0.0, 4.30029177321, 4.43192435858, 4.43192435858, 4.43192435858, 0.0, 8.73221613179, 4.43192435858, 0.0, 0.0, 0.0, 0.0, 4.30029177321, 0.0, 4.43192435858, 0.0, 0.0, 0.0, 0.0, 0.0, 4.43192435858, 4.43192435858, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 8.60058354641, 4.43192435858, 4.43192435858, 0.0, 0.0, 0.0, 8.60058354641, 4.43192435858, 0.0, 4.43192435858, 4.43192435858, 0.0, 4.43192435858, 13.032507905, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.43192435858]

data["N=2"][.1]=[17.4644322636, 26.1966483954, 13.032507905, 17.3327996782, 17.4644322636, 13.032507905, 30.4969401686, 25.9333832246, 17.4644322636, 26.06501581, 25.9333832246, 26.06501581, 30.3653075832, 25.9333832246, 21.7647240368, 26.06501581, 13.032507905, 21.8963566222, 30.3653075832, 21.7647240368, 21.6330914514, 21.7647240368, 17.3327996782, 21.7647240368, 21.6330914514, 17.7276974343, 17.3327996782, 26.06501581, 15.1826537916, 13.032507905, 26.06501581, 21.6330914514, 13.1641404904, 17.3327996782, 21.8963566222, 21.6330914514, 21.8963566222, 13.1641404904, 17.3327996782, 26.06501581, 13.032507905, 21.7647240368, 30.3653075832, 17.3327996782, 26.06501581, 17.3327996782, 17.4644322636, 26.1966483954, 17.3327996782, 21.7647240368, 8.73221613179, 26.06501581, 25.9333832246, 21.6330914514, 26.06501581, 13.032507905, 21.7647240368, 8.86384871716, 25.9333832246, 17.4644322636, 13.032507905, 30.3653075832, 21.7647240368, 13.032507905, 26.06501581, 26.06501581, 12.9008753196, 17.3327996782, 12.9008753196, 17.3327996782, 17.4644322636, 21.7647240368, 17.3327996782, 26.1966483954, 39.2291563004, 21.6330914514, 22.0279892075, 21.8963566222, 17.3327996782, 21.7647240368, 34.6655993564, 26.06501581, 17.3327996782, 26.06501581, 17.4644322636, 17.3327996782, 21.7647240368, 26.06501581, 21.7647240368, 26.06501581, 25.9333832246, 26.1966483954, 22.0279892075, 17.3327996782, 21.8963566222, 10.0340141375, 30.7602053393, 17.2011670928, 30.4969401686, 13.032507905]




data["N=2"][1.]=[30.3653075832, 25.9333832246, 34.7972319418, 30.1020424124, 30.3653075832, 21.501458866, 30.4969401686]




data["N=2"][10.]=[38.9658911296, 64.8992743542, 47.6981072614, 56.5619559786, 47.9613724321, 43.1345503174, 47.6981072614, 43.6610806589, 34.7972319418, 39.3607888857, 43.3978154882, 47.4348420906]
'''


mean={}
std={}
x={}
mean_list={}
error_list={}
ucb_list={}


trial_mean={}
trial_error={}

mean_q_error={}


for n, q in data.items():
	mean[n]={}
	std[n]={}
	x[n]=[]
	mean_list[n]=[]
	error_list[n]=[]
	ucb_list[n]=[]

	trial_mean[n]=[]
	trial_error[n]=[]

	mean_q_error[n]=[]

	for t in t_values:
		if q.get(t) is not None:
			if len(q[t])>0:
				x[n].append(t)
				arr = numpy.array(q[t])
				mean[n][t]=sum(q[t])/len(q[t])
				mean_list[n].append(mean[n][t])
				std[n][t]=numpy.std(arr, axis=0)
				error_list[n].append(std[n][t])
				ucb_list[n].append(1.96*std[n][t]/math.sqrt(len(q[t])))
				trial_mean[n].append(sum(trials[n][t])/len(trials[n][t]))
#				mean_q_error[n].append(sum(q_diff_list[n][t])/len(q_diff_list[n][t]))

font = {'family' : 'normal',
                'weight' : 'bold',
                        'size'   : 15}

plt.rc('font', **font)

yerr=error_list[n]
fig = plt.figure(figsize=(7,6))
#fig2 = plt.figure(figsize=(7,6))
#fig3 = plt.figure(figsize=(7,6))

ax = fig.add_subplot(1, 1, 1)
#ax2 = fig2.add_subplot(1, 1, 1)
#ax3 = fig3.add_subplot(1, 1, 1)
ax.set_xscale('log')
ax.set_ylabel('Discounted reward')
ax.set_xlabel('Time per action(s)')
#ax.set_title('Expected reward vs time')
ax.set_ylim(0,1)
ax.grid(True)


#ax2.set_xscale('log')
#ax2.set_ylabel('Discounted reward')
#ax2.set_xlabel('Simulations')
#ax2.set_title('Expected reward vs # trials')
# ax2.set_ylim(0,1)
#ax2.grid(True)

#ax3.set_xscale('log')
#ax3.set_ylabel('Q ratio')
#ax3.set_xlabel('Trials')
#ax3.set_title('Q convergence')
# ax2.set_ylim(0,1)
#ax3.grid(True)

line_colors=['r','c','b']
plotter_symbols=['o','s','p']
label1={}
label1[N_LIST[0]]='MCTS'
label1[N_LIST[1]]='DDRP'
#label1[N_LIST[2]]='N=2'
ccc=0
for n,q in data.items():

	#plt.plot(x[n], trial_mean[n])
	#ax.errorbar(x[n], mean_list[n], yerr=error_list[n], fmt='o')
	ax.errorbar(x[n], mean_list[n], yerr=ucb_list[n], fmt='o')
	ax.plot(x[n],  mean_list[n],label=label1[n],linewidth=2.0, marker=plotter_symbols[ccc],markersize=7,color=line_colors[ccc])
#	ax2.plot(trial_mean[n],  mean_list[n],label=label1[n],linewidth=2.0, marker=plotter_symbols[ccc],markersize=8,color=line_colors[ccc])
	#ax3.plot(x[n],  mean_q_error[n],label=label1[n],linewidth=2.0, marker=plotter_symbols[ccc],markersize=8,color=line_colors[ccc])
        ccc+=1


legend = ax.legend(loc='upper left', shadow=True, fontsize='x-large',frameon=False)
# legend.get_frame().set_facecolor('#00FFCC')

#legend2 = ax2.legend(loc='lower right', shadow=True, fontsize='x-large',frameon=False)
# legend2.get_frame().set_facecolor('#00FFCC')


#legend3 = ax3.legend(loc='lower right', shadow=True, fontsize='x-large',frameon=False)
# legend3.get_frame().set_facecolor('#00FFCC')

plt.show()


