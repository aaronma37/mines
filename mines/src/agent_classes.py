#!/usr/bin/env python

from random import randint
import environment_classes

import math
from sets import Set
from geometry_msgs.msg import PoseStamped
import numpy as np
from abstraction_classes import Abstractions
import Regions
from POMDP import Solver
import time
import Policies
import Events
from mines.msg import trajectory
import MTCS
import Trajectory_Tree_Search


class Agent: 


	def __init__(self,complete_state,event_time_horizon,identification,policy_steps):

		self.mtcs = MTCS.Solver(event_time_horizon)
		self.tts = Trajectory_Tree_Search.TTS()
		self.x=50
		self.y=50
		self.event_time_horizon
		self.ON=0
		self.measurement_space=[] #make with objectives
		self.battery=100

		self.work=0
		self.current_event=0
		self.current_state="None"

		self.last_reward=0.
		self.poll_time=agent_poll_time
		self.decide_counter=10

		self.display_action="None"
		self.steps=0.
		self.available_flag=True
		self.complete_state=complete_state


	def reset(self,s,performance,fp,fn):
		self.x=50
		self.y=50
		self.current_action=Policies.Policy(0,0,self.poll_time,0,(50,50))
		self.old_A=Abstractions()
		self.new_A=Abstractions()

		self.old_A.update_all(s,self)
		self.new_A.update_all(s,self)
		self.solver.write_file(fp+fn+".txt")
		self.solver.write_performance(fp,performance,self.steps,self.battery)
		self.battery=100
		self.available_flag=False
		self.lvl=0

	def restart(self,fp):
		self.steps=0.
		self.solver.reset()
		self.get_psi(fp)
		self.set_aggregate_q(fp)

		self.available_flag=True
		
	def set_aggregate_q(self,fp):
		self.solver.set_aggregate_q(fp+'/q_main.txt')

	def get_psi(self,fp):
		self.solver.get_psi(fp+'/psi_main.txt')

	def death(self):
		print "dead"

	def imprint(self, u):
		u.x=self.x
		u.y=self.y
		u.battery=self.battery
		u.time_away_from_network=self.time_away_from_network
		for i in range(len(Regions.region)):
			u.work_load[i]=self.work_load[i]

	def step(self,complete_state,time_to_work):	
		self.solver.execute(self,self.complete_state,time_to_work)


	def choose_trajectory(self,complete_state):	
		sub_environment,trajectory = self.tts.execute(.2)


	def move(self,s):
		self.steps+=1.
		action = self.current_trajectory.get_action(self,s)
		self.execute(action,s)


	def check_docking(self):
		if self.current_action.index_type=="charge" and Regions.get_region(self.x,self.y) in self.new_A.charging_docks.regions:
			self.battery=100
	

	def execute(self,action_,environment_data_):
		(x,y) = self.get_transition(action_,self.x,self.y,environment_data_.middle)
		
		base_r = environment_data_.get_reward()

		if environment_data_.check_boundaries((x,y)) is True:
			(self.x,self.y) = (x,y)

		self.measure(environment_data_,False)

		if self.battery < 1:
			self.death()


		self.last_reward= environment_data_.get_reward()- base_r


	

	def simulate_full(self,policy,s):
		base_reward= s.get_reward()
		r1=0
		complete=False
		count=0.

		while complete is False and self.battery >0:
			count+=1.
			action = policy.get_next_action(self,self.x,self.y,s)
			complete=action[1]
			(x,y) = self.get_transition(action[0],self.x,self.y,s.middle)

			if s.check_boundaries((x,y)) is True:
				(self.x,self.y) = (x,y)
			base_reward= s.get_reward()
			self.measure(s,True)

			r1+=math.pow(gamma,count-1)*(s.get_reward()-base_reward)
			base_reward=s.get_reward()

		if self.battery < 25:
			return (s,0,0,count)
		else:
			return (s,r1,0,count)

	def measure(self,mine_data_,imaginary):
		for i in range(-1,2):
			for j in range(-1,2):
				if Regions.in_bounds(self.x+i,self.y+j) is True:
					#if self.work == Regions.get_region(self.x+i,self.y+j):
					mine_data_.measure_loc((self.x+i,self.y+j),imaginary)

	def mine(self,e,imaginary):
		if self.display_action == "mine":
			for mine in e.mines:
				if self.x==mine.coordinates[0] and self.y==mine.coordinates[1]:
					e.mines.remove(mine)
					return

	def get_transition(self,action,x,y,middle):
		self.time_away_from_network+=1		
		return (x+action[0],y+action[1])


	def add_battery(self,num):
		self.battery+=num

		if self.battery <0:
			self.battery=0
		elif self.battery >100:
			self.battery=100
