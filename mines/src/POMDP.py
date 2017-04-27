#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
from abstraction_classes import Abstractions
from Heuristics import heuristic
from sets import Set
import time
import Policies
from random import shuffle
import POMDP_Values as v
import abstraction_classes
import Objective
L_MAX=v.L_MAX

H=5
Gamma=.5

class Solver: 

	def __init__(self,event_time_horizon):
		self.event_time_horizon=event_time_horizon
		self.N=v.N()
		self.Na=v.Na()
		self.Q=v.Q()
		self.Phi=v.Phi(event_time_horizon)
		self.Psi=v.Psi()
		self.Pi=v.Pi()
		self.great=[]
		self.great2=[]
		self.great3=[]
		self.steps=[]
		self.A=Abstractions()

		self.agg_Q=v.Q()
		self.agg_N=v.N()
		self.agg_Na=v.Na()

	def reset(self):
		self.N=v.N()
		self.Na=v.Na()
		self.Q=v.Q()
		self.Phi=v.Phi(self.event_time_horizon)
		self.Psi=v.Psi()
		self.Pi=v.Pi()
		self.H=heuristic()
		self.A=Abstractions()
		self.T={}


	def OnlinePlanning(self,A,time_to_work):
		start = time.time()
		end = start
		while end - start < time_to_work:
			seed=randint(0,999)
			state=self.Phi.get_state(A,seed)
			#self.Phi.set_random_alpha()

			E=self.Phi.get_events(A,seed)

			#print " "

			state= self.Phi.pre_evolve(state,E)
			self.search(state,E,0)
			end = time.time()




	def search(self,state,events,depth):
		if depth>=H:
			return 0.



		E=Objective.Events(0,0)
		events.imprint(E)

		save_state = state
		a = self.arg_max_ucb(save_state)

		self.N.append_to(save_state,1.,self.Phi)
		self.Na.append_to(save_state,a,1.,self.Phi)
		self.Q.append_to(save_state,a,0.,self.Phi)

		self.agg_N.append_to(save_state,1.,self.Phi)
		self.agg_Na.append_to(save_state,a,1.,self.Phi)
		self.agg_Q.append_to(save_state,a,0.,self.Phi)

		
		r = self.Phi.get_reward(state,a)

		E.ammend(a)

		state,E = self.Phi.evolve(state,a,E)


		r += Gamma*self.search(state,E,depth+1)

		self.Q.append_to_average(save_state,a,r,self.Phi,self.Na)
		self.agg_Q.append_to_average(save_state,a,r,self.Phi,self.Na)

		return r	



	def get_action(self,A,next_expected_action,event_time_horizon):

		
		a, b, x_traj,seed = self.Pi.get_and_return_level(A,self.Psi,self.Phi,next_expected_action,event_time_horizon)

		E=self.Phi.get_events(A,seed)
		state=self.Phi.get_state(A,seed)
		self.Phi.print_pre_evolve(state,E)
		print "ree"
		state= self.Phi.pre_evolve(state,E)

		a_traj=[]
		print x_traj
		for i in range(0,len(x_traj)):
			action,l,r=self.Psi.get_with_level(0,state,self.Pi,self.Phi)		
			a_traj.append(action)
			if i== len(x_traj) -1:
				break
			E.ammend(action)
			state,E = self.Phi.evolve(state,action,E)


		E=self.Phi.get_events(A,seed)
		state=self.Phi.get_state(A,seed)

		state= self.Phi.pre_evolve(state,E)
		print state
		return a,b,x_traj,a_traj,state


	def arg_max(self,A):
		return self.Pi.get(L_MAX,A,self.Phi,self.Psi)	

	def rollout(self,A):
		return A.get_max_reward_funct()

	def arg_max_ucb(self,state):

		if self.agg_Q.q.get(state) is None:
			return Policies.action_library[0]

		action_list=Policies.action_library
		shuffle(action_list)

		if self.agg_Q.q[state].get(action_list[0]) is None:
			return action_list[0]

		max_a=action_list[0]
		max_ucb=self.ucb_from_state(self.agg_Q.q[state][max_a],self.agg_N.n[state],self.agg_Na.na[state][max_a])


		for a in action_list:
			if self.agg_Q.q[state].get(a) is None:
				return a

			if self.ucb_from_state(self.agg_Q.q[state][a],self.agg_N.n[state],self.agg_Na.na[state][a])  > max_ucb:
				max_ucb = self.ucb_from_state(self.agg_Q.q[state][a],self.agg_N.n[state],self.agg_Na.na[state][a]) 
				max_a=a

		return max_a
		




	def ucb(self,A,a):
		return self.Q.get(A,self.Phi,a)+100.*math.sqrt(math.log(1+self.N.get(A,self.Phi))/(1+self.Na.get(A,self.Phi,a)))

	def ucb_from_state(self,r,n,na):
		return r+1.94*math.sqrt(math.log(1+n)/(1+na))


	def get_psi(self,filename):
		self.Psi.load(filename)

	def set_aggregate_q(self,filename):
		self.agg_Q.load_file(filename,self.agg_Na,self.agg_N,self.Phi)

	def update_psi(self):
		self.Psi.update(self.Q,self.Na)

	def write_file(self,filename):
		self.Q.write_q(filename,self.Na)

	def write_performance(self,fp,performance,steps,battery):
		self.great.append(performance.exploration)
		self.great2.append(performance.mines)
		self.great3.append(performance.battery)

		file = open(fp+'/performance_exploration.txt','w') 
		for i in range(len(self.great)):
			file.write(str(self.great[i]) +"\n")

		file.close()

		file = open(fp+'/performance_mines.txt','w') 
		for i in range(len(self.great2)):
			file.write(str(self.great2[i]) +"\n")

		file.close()

		file = open(fp+'/performance_battery.txt','w') 
		for i in range(len(self.great3)):
			file.write(str(self.great3[i]) +"\n")

		file.close()

