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


	def reset(self):
                return
		self.N={}
		self.Na={}#v.Na()
		self.Q={}#v.Q()




	def execute_test(self,agent,complete_environment,tts,time_to_work):

		num=0.
                max_reward=0

                Q=copy.deepcopy(self.Q)
                N=copy.deepcopy(self.N)
                Na=copy.deepcopy(self.Na)
		tts.empty_environments()
		start = time.time()
		end = start
		while end - start < time_to_work:
			#sub_environment=tts.get_random_sub_environment((agent.x,agent.y),complete_environment)
			#print sub_environment.get_total_state(), sub_environment.region_list
                        r =  self.search_test(complete_environment.get_full_state(environment_classes.get_region(agent.x,agent.y)),0,environment_classes.get_region(agent.x,agent.y),Q,N,Na)  
                        if r > max_reward:
                            max_reward=r

			num+=1.
			end = time.time()

                        
			#self.save_pre_Q(sub_environment)
		# print max_reward
		return num,max_reward


	def execute(self,agent,complete_environment,tts,time_to_work):
		start = time.time()
		end = start
		num=0.
                max_reward=0
		while end - start < time_to_work:
			#sub_environment=tts.get_random_sub_environment((agent.x,agent.y),complete_environment)
			#print sub_environment.get_total_state(), sub_environment.region_list
                        r =  self.search(complete_environment.get_full_state(environment_classes.get_region(agent.x,agent.y)),0,environment_classes.get_region(agent.x,agent.y))  
                        if r > max_reward:
                            max_reward=r

			num+=1.
			end = time.time()

                        
			#self.save_pre_Q(sub_environment)
		# print max_reward
		return num,max_reward



        def search_test(self,save_state,depth,agent_location,Q,N,Na):

                if depth>100:
			return 0

                action= self.arg_max_ucb_full(save_state)
		self.check_variables_init_test(Q,N,Na,save_state,action)
                action_string=action.split(",")
                objective_type=action_string[2]
                transition_region=(int(action_string[0]),int(action_string[1]))
                if objective_type=='wait':
                    return 0
                elif objective_type=='travel':
                    r=0
                    t=11
                else:
                    # print environment_classes.get_score_at_region(save_state,objective_type,agent_location), "HERE"
                    t=task_classes.tau_objective(environment_classes.get_score_at_region(save_state,objective_type,agent_location),objective_type)
                    r = environment_classes.get_reward_at_region(save_state,objective_type,agent_location)
                objective_region=agent_location
                agent_location=(agent_location[0]+transition_region[0],agent_location[1]+transition_region[1])
                save_state_2=environment_classes.string_evolve_full(save_state,objective_type,objective_region,agent_location)
		r = math.pow(Gamma,t)*(r + self.search_test(save_state_2,depth+t,agent_location,Q,N,Na))
		Q[save_state][action]+=(r-Q[save_state][action])/Na[save_state][action]


		return r








	def search(self,save_state,depth,agent_location):

                if depth>100:
			return 0

		#save_state = sub_environment.get_total_state() #sub_environment.state + sub_environment.interaction_state
		# objective_type = self.arg_max_ucb(save_state)

                action= self.arg_max_ucb_full(save_state)
		self.check_variables_init(save_state,action)
                action_string=action.split(",")
                objective_type=action_string[2]
                transition_region=(int(action_string[0]),int(action_string[1]))
                if objective_type=='wait':
                    return 0
                elif objective_type=='travel':
                    r=0
                    t=11
                else:
                    # print environment_classes.get_score_at_region(save_state,objective_type,agent_location), "HERE"
                    t=task_classes.tau_objective(environment_classes.get_score_at_region(save_state,objective_type,agent_location),objective_type)
                    r = environment_classes.get_reward_at_region(save_state,objective_type,agent_location)
# 		if objective_type!="wait" and objective_type!="travel":
			
# 			own_reward_flag=True
# 			r=0
# 			#need to precalculate tau#

# 			for interact_string_by_agent in save_state.split('|')[2].split('+')[:-1]:
# 				interaction_locations=environment_classes.get_interact_intersection(interact_string_by_agent,objective_type)

# 				if len(interaction_locations)>0:
# 					own_reward_flag=False
# 					r=r+self.estimate(depth,interact_string_by_agent,interaction_locations)-self.estimate(depth,interact_string_by_agent,[])
# 					t=task_classes.coupled_tau(save_state,objective_type)								
			

# 			if own_reward_flag==True:			
# 				r = environment_classes.objective_parameter_list[objective_map[objective_type]][3]
# 				t=task_classes.tau(save_state,objective_type)
# 			#else:
# 			#	print "reward diff:", r, environment_classes.objective_parameter_list[objective_map[objective_type]][3]




# 		else:
# 			if objective_type!="travel":
# 				r = 0
# 				return 0
# 				t=100
# 			else:
# 				r = 0
# 				t=11

# 		#if t+depth>10:
# 		#	return 0.
# 		interact_string=''
	
# 		for interact_string_by_agent in save_state.split('|')[2].split('+')[:-1]:
# 			new_interact_string_by_agent=environment_classes.interact_string_evolve(interact_string_by_agent,objective_type) #similar to other evolve	
# 			interact_string=interact_string+new_interact_string_by_agent+'+'

# 		save_state_2=environment_classes.string_evolve(save_state,objective_type)
# 		save_state_2=environment_classes.modify_interact_string(save_state_2,interact_string)
                objective_region=agent_location
                agent_location=(agent_location[0]+transition_region[0],agent_location[1]+transition_region[1])
                save_state_2=environment_classes.string_evolve_full(save_state,objective_type,objective_region,agent_location)
		r = math.pow(Gamma,t)*(r + self.search(save_state_2,depth+t,agent_location))
                # print save_state,'new', save_state_2
		self.Q[save_state][action]+=(r-self.Q[save_state][action])/self.Na[save_state][action]


		return r

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
		if self.Q.get(state)==None:
			self.Q[state]={}

		v=list(self.Q[state].values())

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

        def arg_max_ucb_full(self,save_state):
                objective_type_list =environment_classes.objective_list 
                action_list=[]
                for i in range(-1,2):
                    for j in range(-1,2):
                        for o in objective_type_list:
                            action_list.append(str(i)+','+str(j)+','+o)

		shuffle(action_list)

		if self.Q.get(save_state) is None:
			return action_list[0]
		if self.Q[save_state].get(action_list[0]) is None:
			return action_list[0]

		max_a=action_list[0]
		max_ucb=self.ucb_from_state(self.Q[save_state][max_a],self.N[save_state],self.Na[save_state][max_a])


		for a in action_list:
			if self.Q[save_state].get(a) is None:
				return a

			if self.ucb_from_state(self.Q[save_state][a],self.N[save_state],self.Na[save_state][a])  > max_ucb:
				max_ucb = self.ucb_from_state(self.Q[save_state][a],self.N[save_state],self.Na[save_state][a]) 
				max_a=a

                return max_a



	def ucb_from_state(self,r,n,na):
		return r+1.94*math.sqrt(math.log(1+n)/(1+na))

	def write(self,fp,a,b):
		if self.Q_avg.get(a) is None:
			self.Q_avg[a]={}
			self.Q_avg[a][b]={}
			
		elif self.Q_avg[a].get(b) is None:
			self.Q_avg[a][b]={}


		file = open(fp+'/q_test_11_'+str(a)+'_'+str(b)+'.txt','w')
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


