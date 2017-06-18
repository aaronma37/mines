#!/usr/bin/env python


from random import randint
import random
import copy
import numpy as np
import math
from sets import Set
import time
from random import shuffle
import task_classes
from environment_classes import objective_map	
import environment_classes
Gamma=.98

class Solver: 

	def __init__(self,trajectory_length,time_horizon):
		self.trajectory_length=trajectory_length
		self.time_horizon=time_horizon
		self.N={}
		self.Na={}
		self.Q={}
		self.pre_Q={}
		self.Q_avg={}

		self.great=[]
		self.great2=[]
		self.great3=[]
		self.steps=[]

		self.QE={}
		self.NE={}

		self.temp_Q={}
		self.temp_N={}
		self.temp_Na={}
		


	def reset(self):
		self.N={}
		self.Na={}#v.Na()
		self.Q={}#v.Q()




	def execute_test(self,agent,complete_environment,tts,time_to_work):

		num=0.
		tts.empty_environments()
                self.temp_Q=copy.deepcopy(self.Q)
                self.temp_N=copy.deepcopy(self.N)
                self.temp_Na=copy.deepcopy(self.Na)
		max_r=0
		start = time.time()
		end = start

		while end - start < time_to_work:
			sub_environment=tts.get_random_sub_environment((agent.x,agent.y),complete_environment)
                      #  self.search(sub_environment.get_total_state(),0)
                        r=self.search_test(sub_environment.get_total_state(),0,self.temp_Q,self.temp_N,self.temp_Na)
			if r > max_r:
				max_r=r
			num+=1.
			end = time.time()

			#	self.save_pre_Q(sub_environment)
		# print max_reward
		return num,max_r


	def execute(self,agent,complete_environment,tts,time_to_work):
		start = time.time()
		end = start
		num=0.



		while end - start < time_to_work:
			sub_environment=tts.get_random_sub_environment((agent.x,agent.y),complete_environment)
                        self.search(sub_environment.get_total_state(),0)
			num+=1.
			end = time.time()
			#self.save_pre_Q(sub_environment)


		return num





	def search_test(self,save_state,depth,Q,N,Na):
			print depth, 'df',environment_classes.get_k_from_string(save_state)
			if environment_classes.get_k_from_string(save_state)==0 or depth>100:
				return 0

			#save_state = sub_environment.get_total_state() #sub_environment.state + sub_environment.interaction_state
			objective_type = self.arg_max_ucb(save_state)

			self.check_variables_init_test(Q,N,Na,save_state,objective_type)

			if objective_type!="wait" and objective_type!="travel":
			
				own_reward_flag=True
				r=0
				#need to precalculate tau#

				for interact_string_by_agent in save_state.split('|')[2].split('+')[:-1]:
					interaction_locations=environment_classes.get_interact_intersection(interact_string_by_agent,objective_type)

					if len(interaction_locations)>0:
						own_reward_flag=False
						r=r+self.estimate(depth,interact_string_by_agent,interaction_locations)-self.estimate(depth,interact_string_by_agent,[])
						t=task_classes.coupled_tau(save_state,objective_type)								
			

				if own_reward_flag==True:			
					r = environment_classes.objective_parameter_list[objective_map[objective_type]][3]
					t=task_classes.tau(save_state,objective_type)
				#else:
				#	print "reward diff:", r, environment_classes.objective_parameter_list[objective_map[objective_type]][3]




			else:
				if objective_type!="travel":
					r = 0
					return 0
					t=100
				else:
					r = 0
					t=11

			#if t+depth>10:
			#	return 0.
			interact_string=''
	
			for interact_string_by_agent in save_state.split('|')[2].split('+')[:-1]:
				new_interact_string_by_agent=environment_classes.interact_string_evolve(interact_string_by_agent,objective_type) #similar to other evolve	
				interact_string=interact_string+new_interact_string_by_agent+'+'

			save_state_2=environment_classes.string_evolve(save_state,objective_type)
			save_state_2=environment_classes.modify_interact_string(save_state_2,interact_string)

			r = math.pow(Gamma,t)*(r + self.search_test(save_state_2,depth+t,Q,N,Na))

			Q[save_state][objective_type]+=(r-Q[save_state][objective_type])/Na[save_state][objective_type]


			return r


	def search(self,save_state,depth):

			if environment_classes.get_k_from_string(save_state)==0 or depth>100:
				return 0

			#save_state = sub_environment.get_total_state() #sub_environment.state + sub_environment.interaction_state
			objective_type = self.arg_max_ucb(save_state)

			self.check_variables_init(save_state,objective_type)

			if objective_type!="wait" and objective_type!="travel":
			
				own_reward_flag=True
				r=0
				#need to precalculate tau#

				for interact_string_by_agent in save_state.split('|')[2].split('+')[:-1]:
					interaction_locations=environment_classes.get_interact_intersection(interact_string_by_agent,objective_type)

					if len(interaction_locations)>0:
						own_reward_flag=False
						r=r+self.estimate(depth,interact_string_by_agent,interaction_locations)-self.estimate(depth,interact_string_by_agent,[])
						t=task_classes.coupled_tau(save_state,objective_type)								
			

				if own_reward_flag==True:			
					r = environment_classes.objective_parameter_list[objective_map[objective_type]][3]
					t=task_classes.tau(save_state,objective_type)
				#else:
				#	print "reward diff:", r, environment_classes.objective_parameter_list[objective_map[objective_type]][3]




			else:
				if objective_type!="travel":
					r = 0
					return 0
					t=100
				else:
					r = 0
					t=11

			#if t+depth>10:
			#	return 0.
			interact_string=''
	
			for interact_string_by_agent in save_state.split('|')[2].split('+')[:-1]:
				new_interact_string_by_agent=environment_classes.interact_string_evolve(interact_string_by_agent,objective_type) #similar to other evolve	
				interact_string=interact_string+new_interact_string_by_agent+'+'

			save_state_2=environment_classes.string_evolve(save_state,objective_type)
			save_state_2=environment_classes.modify_interact_string(save_state_2,interact_string)

			r = math.pow(Gamma,t)*(r + self.search(save_state_2,depth+t))

			self.Q[save_state][objective_type]+=(r-self.Q[save_state][objective_type])/self.Na[save_state][objective_type]
			
			#self.updateEValues(save_state,r)


			return r

	def updateEValues(self,save_state,r):
		for s in self.cut_save_states(save_state):
			if self.NE.get(s) is None:
				self.NE[s]=1
			else:
				self.NE[s]+=1
			if self.QE.get(s) is None:
				self.QE[s]=r
			else:
				self.QE[s]+=(r-self.QE[s])/self.NE[s]				

	def cut_save_states(self,save_state):
		s=save_state.split('.')	
		s_list=[]
		ends=str(s[-1]).split(',')
		h=''
		for i in range(len(s)-1):
			h=''

			for j in range(i):
				h=h+str(s[j])+'.'
			h=h+'|'
			
			for j in range(i):

				h=h+str(ends[j+1])+','
			h=h+'|'
			s_list.append(h)
		return s_list


	def estimate(self,initial_t,interact_string_by_agent,interaction_locations):
		t=initial_t
		r=0
		
		per_region_state=interact_string_by_agent.split('@')[0].split('.')[:-1] #list of strings
		task_list = interact_string_by_agent.split('@')[1].split(',')[:-1]
		
		for k in range(len(task_list)):
			if task_list[k]=='wait' or task_list[k]=='travel':
				t+=task_classes.tau_objective("dne",task_list[k])
				r+=0.
			else:
				if k in interaction_locations:
					t+=task_classes.coupled_tau_objective(per_region_state[k].split(',')[environment_classes.objective_map[task_list[k]]],task_list[k])
				else:
					t+=task_classes.tau_objective(per_region_state[k].split(',')[environment_classes.objective_map[task_list[k]]],task_list[k])
			#	if t>10:
			#		r+=0.
			#	else:
				r+=math.pow(Gamma,t)*environment_classes.objective_parameter_list[objective_map[task_list[k]]][3]


		return r		









	def save_pre_Q(self,sub_environment):
		for i in range(sub_environment.get_k()):
			self.pre_Q[sub_environment.cull_state_from_back(i)]=1
		
		
	

	def check_variables_init_test(self,Q,N,Na,save_state,objective_type):

		if N.get(save_state) == None:
			N[save_state] = 1.
		else:
			N[save_state]+= 1.

		if Na.get(save_state)==None:
			Na[save_state]={}
			Na[save_state][objective_type]=1.
		elif Na[save_state].get(objective_type)==None:
			Na[save_state][objective_type]=1.
		else:
			Na[save_state][objective_type]+=1.

		if Q.get(save_state) == None:
			Q[save_state]={}
			Q[save_state][objective_type]=0.
		elif Q[save_state].get(objective_type)==None:
			Q[save_state][objective_type]=0.
		


	def check_variables_init(self,save_state,objective_type):

		if self.N.get(save_state) == None:
			self.N[save_state] = 1.
		else:
			self.N[save_state]+= 1.

		if self.Na.get(save_state)==None:
			self.Na[save_state]={}
			self.Na[save_state][objective_type]=1.
		elif self.Na[save_state].get(objective_type)==None:
			self.Na[save_state][objective_type]=1.
		else:
			self.Na[save_state][objective_type]+=1.

		if self.Q.get(save_state) == None:
			self.Q[save_state]={}
			self.Q[save_state][objective_type]=0.
		elif self.Q[save_state].get(objective_type)==None:
			self.Q[save_state][objective_type]=0.
		


	def arg_max_reward(self,state):
		if self.temp_Q.get(state)==None:
			self.temp_Q[state]={}

		v=list(self.temp_Q[state].values())

		if len(v)==0:
			return 0
		return max(v)

	def arg_max(self,state):
		if self.Q.get(state)==None:
			self.Q[state]={}

		v=list(self.Q[state].values())
		key=list(self.Q[state].keys())
		if len(key)==0:
			return 'wait'

		return key[v.index(max(v))]

	def pq(self):
		for s,q in self.Q.items():
			for k,v in q.items():
				print s,k,v

	def arg_max_ucb(self,save_state):
		#save_state=sub_environment.get_total_state()
		objective_type_list = task_classes.get_available_objective_types(save_state) #CHANGE

		shuffle(objective_type_list)

		if self.Q.get(save_state) is None:
			return objective_type_list[0]
		if self.Q[save_state].get(objective_type_list[0]) is None:
			return objective_type_list[0]

		max_a=objective_type_list[0]
		max_ucb=self.ucb_from_state(self.Q[save_state][max_a],self.N[save_state],self.Na[save_state][max_a])


		for a in objective_type_list:
			if self.Q[save_state].get(a) is None:
				return a

			if self.ucb_from_state(self.Q[save_state][a],self.N[save_state],self.Na[save_state][a])  > max_ucb:
				max_ucb = self.ucb_from_state(self.Q[save_state][a],self.N[save_state],self.Na[save_state][a]) 
				max_a=a

		return max_a



	def ucb_from_state(self,r,n,na):
		return r+0*math.sqrt(math.log(1+n)/(1+na))

	def write(self,fp,a,b):
		if self.Q_avg.get(a) is None:
			self.Q_avg[a]={}
			self.Q_avg[a][b]={}
			
		elif self.Q_avg[a].get(b) is None:
			self.Q_avg[a][b]={}


		file = open(fp+'/single_ddr_q_'+str(a)+'_'+str(b)+'.txt','w')
		for s,q in self.Q.items():
			if self.Q_avg[a][b].get(s) is None:
				self.Q_avg[a][b][s]={}
			for k,v in q.items():
				if self.Q_avg[a][b][s].get(k) is None:
					self.Q_avg[a][b][s][k]=[]
				self.Q_avg[a][b][s][k].append(v)
				file.write(str(s)+"*"+str(k)+"*"+str(sum(self.Q_avg[a][b][s][k])/len(self.Q_avg[a][b][s][k])) +"*\n")

		for s,q in self.Q_avg[a][b].items():
			for k,v in q.items():
				file.write(str(s)+"*"+str(k)+"*"+str(sum(self.Q_avg[a][b][s][k])/len(self.Q_avg[a][b][s][k])) +"*\n")

		file.close()


