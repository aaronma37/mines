#!/usr/bin/env python

from random import randint
import environment_classes

import math
from sets import Set
from geometry_msgs.msg import PoseStamped
import numpy as np
import time
from mines.msg import trajectory
import MCTS
import Trajectory_Tree_Search


class Agent: 


	def __init__(self,T,identification):

		self.mcts = MCTS.Solver(4)
		self.tts = Trajectory_Tree_Search.TTS(4)
		self.x=50
		self.y=50
		self.T=T
		self.ON=0


		self.steps=T+1
		self.available_flag=True

		self.current_trajectory=None
		self.current_sub_environment=None



	def reset(self,s,performance,fp,fn):
		self.x=50
		self.y=50

		self.available_flag=False


	def restart(self,fp):
		self.steps=0.
		self.solver.reset()
		self.get_psi(fp)
		self.set_aggregate_q(fp)

		self.available_flag=True


	def step(self,complete_environment,time_to_work):	
		self.mcts.execute(self,complete_environment,self.tts,time_to_work)
		


	def choose_trajectory(self,complete_environment):	
		sub_environment,trajectory = self.tts.execute((self.x,self.y),complete_environment,.2,self.mcts)
		self.current_trajectory=trajectory
		self.current_sub_environment=sub_environment
		self.current_trajectory.print_data()

	def move(self,complete_environment):
		self.steps+=1.
		if self.steps>40:
			self.steps=0
			self.choose_trajectory(complete_environment)
		#print "start execute"	, self.current_trajectory.get_action(self,complete_environment), self.x,self.y, self.current_trajectory.current_index, self.current_trajectory.sub_environment.region_list
		self.execute(self.current_trajectory.get_action(self,complete_environment))
		#print "end execute", self.x, self.y, complete_environment.print_objective_score("mine")



	def execute(self,action_):
		self.x,self.y = self.get_transition(action_,self.x,self.y)
		


	def execute_objective(self,objective_type,complete_environment):
		complete_environment.execute_objective(objective_type,(self.x,self.y))
	

	def get_transition(self,action,x,y):
		return (x+action[0],y+action[1])



