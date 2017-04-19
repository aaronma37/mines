#!/usr/bin/env python

from random import randint
from environment_classes import Mine_Data

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


class Agent: 


	def __init__(self,agent_poll_time,event_time_horizon,identification):

		self.solver = Solver() # get rid of
		self.lvl=0

		self.x=50
		self.y=50
	
		self.ON=0
		self.measurement_space=[]

		self.battery=100
		self.work_load=[]
		self.work=0

		self.last_reward=0.
		self.poll_time=agent_poll_time

		self.current_action=Policies.Policy(0,0,self.poll_time,0,(50,50))
		self.display_action="None"
		self.steps=0.
		self.available_flag=True
		self.trajectory=trajectory()
		self.trajectory.frame_id=identification
		self.event_time_horizon=event_time_horizon
		self.Exploration_Event=Events.Event("Exploration",event_time_horizon)

		for i in range(len(Regions.region)):
			self.work_load.append(0)

		self.old_A=Abstractions()
		self.new_A=Abstractions()

		self.time_away_from_network=0

	def clear_trajectory(self):
		self.trajectory.region_trajectory=[]
		self.trajectory.action_trajectory=[]

	def clear_events(self):
		self.Exploration_Event.clear()
		
	def update_events(self,e):
		self.Exploration_Event.update(e)

		
	def update_heuristics(self,old_s,new_s):
		self.old_A.update_all(old_s,self)
		self.new_A.update_all(new_s,self)	
		#update_H(self.solver.H,self.old_A,self.new_A,self,self.last_reward)#THIS R IS A BANDAID





	def predict_A(self):
		self.new_A.evolve_all(self.solver.H,self)

	def reset(self,s,data,fp,fn):
		self.x=50
		self.y=50
		self.current_action=Policies.Policy(0,0,self.poll_time,0,(50,50))
		self.old_A=Abstractions()
		self.new_A=Abstractions()
		self.battery=100
		self.old_A.update_all(s,self)
		self.new_A.update_all(s,self)
		self.solver.write_file(fp+fn+".txt")
		self.solver.write_performance(fp,data,self.steps)
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



	def step(self,s,time_to_work):	
		self.calculate_A(s)
		self.solver.OnlinePlanning(self.new_A,time_to_work)

	def calculate_A(self,s):
		self.new_A.update_all(s,self)

	def decide(self,s):	

		a,an,x_traj,a_traj  = self.solver.get_action(self.new_A,self.current_action.next,self.event_time_horizon)	
		self.trajectory.region_trajectory=x_traj
		self.trajectory.action_trajectory=a_traj
					
		self.display_action=a_traj[0]
		if a == 26:
			print "ERROR",26

		if a_traj[0]=="charge":
			try:
				charge_index=self.new_A.charging_docks.regions.index(x_traj[0])
				coordinates = self.new_A.charging_docks.coordinates[charge_index]
			except ValueError:
				try:
					charge_index=self.new_A.charging_docks.regions.index(x_traj[1])
					coordinates = self.new_A.charging_docks.coordinates[charge_index]
				except ValueError:
					charge_index=None
					coordinates = Regions.region[x_traj[0]]
				



			print charge_index,coordinates
			self.current_action=Policies.Policy(x_traj[0]+1,x_traj[1]+1,self.poll_time,a_traj[0],coordinates)
		elif a_traj[0]=="mine":
			try:
				charge_index=self.new_A.mines.regions.index(x_traj[0])
				coordinates = self.new_A.mines.coordinates[charge_index]
			except ValueError:
				try:
					charge_index=self.new_A.mines.regions.index(x_traj[1])
					coordinates = self.new_A.mines.coordinates[charge_index]
				except ValueError:
					charge_index=None
					coordinates = Regions.region[x_traj[0]]
				



			print charge_index,coordinates
			self.current_action=Policies.Policy(x_traj[0]+1,x_traj[1]+1,self.poll_time,a_traj[0],coordinates)

		else:
			self.current_action=Policies.Policy(x_traj[0]+1,x_traj[1]+1,self.poll_time,a_traj[0],Regions.region[x_traj[0]])

		if self.current_action.index < 26 and self.current_action.index > 0:
			self.work=self.current_action.index-1
		else:
			self.work=-1
		#action = self.current_action.get_next_action(self,s)
		#self.execute(action,s)#NEED TO RESOLVE s
		self.lvl=0

	def move(self,s):
		self.steps+=1.
		if self.battery  > 1:
			action = self.current_action.get_next_action(self,s)
			self.execute(action,s)#NEED TO RESOLVE s
		self.battery-=.25
		self.check_docking()

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
				if self.work == Regions.get_region(self.x+i,self.y+j):
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
