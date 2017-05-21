#!/usr/bin/env python

from random import randint
import environment_classes

import math
from sets import Set
from geometry_msgs.msg import PoseStamped
import numpy as np
import time
from mines.msg import trajectory
from mines.msg import collective_beta as collective_beta_msg
from mines.msg import beta as beta_msg
from mines.msg import beta_set as beta_set_msg
from mines.msg import claimed_objective as claimed_objective_msg
from mines.msg import collective_interaction as collective_interaction_msg
from mines.msg import collective_trajectories as collective_trajectories_msg
from mines.msg import interaction_list as interaction_list_msg
from mines.msg import interaction_set as interaction_set_msg	
from mines.msg import region as region_msg

import MCTS
import Trajectory_Tree_Search



class Claimed_Objective():
	def __init__(self,state,region,objective_type):
		self.state=state
		self.region=region
		self.objective_type=objective_type

class Interaction_List():
	def __init__(self,L,frame_id):
		self.L=L
		self.interaction_total_set=set()
		self.interaction_list=interaction_list_msg()
		self.interaction_list.frame_id=frame_id
		self.interaction_list.trajectory_index=[]
		self.others=collective_interaction_msg()
		self.interaction_intersection=[]
		for i in range(self.L-1):
			self.interaction_list.trajectory_index.append(interaction_set_msg())
	
	def update(self):
		self.interaction_total_set.clear()
		for k in range(self.L-1):
			self.interaction_list.trajectory_index[k].agent_id=[]

	def update_others(self,collective_interaction_msg):
		self.others=collective_interaction_msg

class Claimed_Objective_Sets():
	def __init__(self,N,L,frame_id):
		self.L=L
		self.N=N
		self.claimed_objective_list=beta_msg()#All claimed objectives
		self.owned_objectives=beta_set_msg()# Offerings
		self.owned_objectives.frame_id=frame_id
		self.collective_beta=collective_beta_msg() #everyones beta offerings
		for i in range(self.N+1):
			self.owned_objectives.beta.append(beta_msg())
		self.n_list=[] #naj
		self.effective_claimed_objectives=beta_msg()
		


	def claimed_objective_list_construction(self,sub_environment,trajectory):
		self.claimed_objective_list=beta_msg()
		for k in range(self.L-1):
			if trajectory.get_task_at_k(k)!="wait" and trajectory.get_task_at_k(k)!="travel":
				region=region_msg()
				region.x=sub_environment.region_list[k][0]
				region.y=sub_environment.region_list[k][1]

				claimed_objective=claimed_objective_msg()
				claimed_objective.state = int(sub_environment.get_objective_index(k,environment_classes.objective_map[trajectory.get_task_at_k(k)]))
				claimed_objective.region=region
				claimed_objective.objective_type=trajectory.get_task_at_k(k)

				self.claimed_objective_list.claimed_objective.append(claimed_objective)
			else:
				region=region_msg()
				region.x=sub_environment.region_list[k][0]
				region.y=sub_environment.region_list[k][1]

				claimed_objective=claimed_objective_msg()
				claimed_objective.state = 0
				claimed_objective.region=region
				claimed_objective.objective_type="None"

				self.claimed_objective_list.claimed_objective.append(claimed_objective)
			
		

	def owned_objective_construction(self,interaction_list):	
		#print len(claimed_objective_list.claimed_objective)

		for i in range(len(self.owned_objectives.beta)):
			for k in range(self.L-1):
				self.owned_objectives.beta[i].claimed_objective=[]
				self.owned_objectives.beta[i].claimed_objective.append(self.claimed_objective_list.claimed_objective[k])


	def collect_taken_objectives(self,collective_beta_message):
		self.collective_beta=collective_beta_message
		



	def construct_n_list(self,interaction_list):
		self.n_list=[]		
		for a in range(len(interaction_list.interaction_total_set)):
			self.n_list.append(0)
			#self.n_list.append(len(interaction_list.others.agent_interaction[a].trajectory_index[interaction_list.interaction_intersection]))



	def construct_effective_claimed_objectives(self,self_id,interaction_list):	
		#print "here"		
		self.construct_n_list(interaction_list)
		self.effective_claimed_objectives.claimed_objective=[]
		for a in range(len(self.n_list)):
			if self.collective_beta.agent_beta[a].frame_id!=self_id:
				for claimed_objective in self.collective_beta.agent_beta[a].beta[self.n_list[a]].claimed_objective:
					self.effective_claimed_objectives.claimed_objective.append(claimed_objective)
			
		



class Agent: 


	def __init__(self,T,identification,agent_trajectory_length,max_interaction_number):

		self.mcts = MCTS.Solver(agent_trajectory_length,T)
		self.tts = Trajectory_Tree_Search.TTS(agent_trajectory_length,max_interaction_number)
		self.x=50
		self.y=50
		self.T=T

		self.ON=0

		self.id=identification
		self.steps=T+1
		self.available_flag=True

		self.reset_flag=False
		self.traj_flag=True
		self.mcts_flag=True
		self.current_trajectory=None
		self.current_sub_environment=None
		self.collective_trajectories=collective_trajectories_msg()

		self.interaction_list=Interaction_List(agent_trajectory_length,self.id)
		self.claimed_objective_sets=Claimed_Objective_Sets(1,agent_trajectory_length,self.id)



	def reset(self,fp):
		self.x=50
		self.y=50
		self.mcts.write(fp)
		self.traj_flag=True
		self.mcts_flag=True
		self.steps=self.T+1
		self.current_trajectory=None
		self.current_sub_environment=None




	def restart(self,fp):
		self.steps=0.
		self.solver.reset()
		self.get_psi(fp)
		self.set_aggregate_q(fp)

		self.available_flag=True


	def step(self,complete_environment,time_to_work):	
		if self.mcts_flag==True:
			self.mcts.reset()
			self.mcts_flag=False
		self.mcts.execute(self,complete_environment,self.tts,time_to_work)

	def update_claimed_objectives(self):
		self.interaction_list.update()
		self.claimed_objective_sets.claimed_objective_list_construction(self.current_sub_environment,self.current_trajectory)

		self.claimed_objective_sets.owned_objective_construction(self.interaction_list)

	def update_collective_trajectories(self,msg):
		self.collective_trajectories=msg
		for agent in self.collective_trajectories.agent_trajectory:	
			if agent.frame_id==self.id:
				self.collective_trajectories.agent_trajectory.remove(agent)
		


	def choose_trajectory(self,complete_environment,time_to_work):	
		sub_environment,trajectory = self.tts.execute((self.x,self.y),complete_environment,time_to_work,self.mcts)
		self.current_trajectory=trajectory
		self.current_sub_environment=sub_environment


	def move(self,complete_environment,time_to_work):
		self.steps+=1.
		if self.steps>self.T:
			self.steps=0
			if self.traj_flag==True:
				self.tts.reset()
				self.traj_flag=False
			self.choose_trajectory(complete_environment,time_to_work)
		self.execute(self.current_trajectory.get_action(self,complete_environment))


	def execute(self,action_):
		self.x,self.y = self.get_transition(action_,self.x,self.y)
		


	def execute_objective(self,objective_type,complete_environment):
		complete_environment.execute_objective(objective_type,(self.x,self.y))
	

	def get_transition(self,action,x,y):
		return (x+action[0],y+action[1])



