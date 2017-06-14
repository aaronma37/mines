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
import task_classes
import environment_classes
import MCTS
import Trajectory_Tree_Search

total_agents=16

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
	def __init__(self,max_agents,L,frame_id):
		self.L=L
		self.N=max_agents
		self.claimed_objective_list=beta_msg()#All claimed objectives
		self.owned_objectives=beta_set_msg()# Offerings
		self.owned_objectives.frame_id=frame_id
		self.collective_beta=collective_beta_msg() #everyones beta offerings
		for i in range(self.N+1):
			self.owned_objectives.beta.append(beta_msg())
		self.n_list=[] #naj
		self.effective_claimed_objectives=beta_msg()
		self.beta_hash={}

	def reset(self):
		self.collective_beta=collective_beta_msg() #everyones beta offerings
		for i in range(self.N+1):
			self.owned_objectives.beta.append(beta_msg())

		self.beta_hash={}

	def claimed_objective_list_construction(self,sub_environment,trajectory):
		self.claimed_objective_list=beta_msg()
		for k in range(self.L-1):
			if trajectory.get_task_at_k(k)==False:
				break
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
				continue
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
			self.owned_objectives.beta[i].claimed_objective=[]
			for k in range(self.L-1):
				if i==0:
					try:
						self.owned_objectives.beta[i].claimed_objective.append(self.claimed_objective_list.claimed_objective[k])
					except IndexError:
						''' '''

	def collect_taken_objectives(self,collective_beta_message):
		self.collective_beta=collective_beta_message
		



	def construct_n_list(self,interaction_list):
		self.n_list=[]		
		for a in range(5):
			
			self.n_list.append(0)
			#self.n_list.append(len(interaction_list.others.agent_interaction[a].trajectory_index[interaction_list.interaction_intersection]))



	def construct_effective_claimed_objectives(self,self_id,interaction_list):	
		#print "here"		
		#NOTE need to fix this+need to make sure agents are added onto other agents correctly	
		
		self.beta_hash={}
		#print self.collective_beta
		for a in self.collective_beta.agent_beta:
			self.beta_hash[a.frame_id]={}
			for n in range(len(a.beta)):
				self.beta_hash[a.frame_id][n]=[]
				for claimed_objective in a.beta[n].claimed_objective:
					self.beta_hash[a.frame_id][n].append(claimed_objective)

		#print self.beta_hash

		self.construct_n_list(interaction_list)
		self.effective_claimed_objectives.claimed_objective=[]
		#for a in range(len(self.collective_beta.agent_beta)):
		for a in range(len( self.collective_beta.agent_beta)):
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
		self.trajectory_length=agent_trajectory_length
		self.ON=0
		self.my_action="none"
		self.id=identification
		self.steps=0
		self.available_flag=True
		self.total_steps=0.
		self.reset_flag=False
		self.traj_flag=True

		self.my_action_index="none"		
		self.mcts_flag=True

		self.current_sub_environment=environment_classes.Sub_Environment()
		self.current_trajectory=task_classes.Trajectory(self.current_sub_environment,[],[])

		self.collective_trajectories=collective_trajectories_msg()
		self.current_state='none'
		self.interaction_list=Interaction_List(agent_trajectory_length,self.id)
		self.claimed_objective_sets=Claimed_Objective_Sets(2,agent_trajectory_length,self.id)
		self.expected_reward=0
		self.think_step=0.
                self.max_reward=0.
		self.current_step_time=0.
		self.current_n=0.


	def reset(self,fp,new_param):
                self.max_reward=0.
		self.expected_reward=0
		self.think_step=0.
		self.x=50
		self.y=50
		if self.id=='/a3':
			self.mcts.write(fp,self.current_n,self.current_step_time)
		self.traj_flag=True
		self.mcts_flag=True
		self.steps=0
		self.current_sub_environment=environment_classes.Sub_Environment()
		self.current_trajectory=task_classes.Trajectory(self.current_sub_environment,[],[])
		self.claimed_objective_sets.reset()
		#self.claimed_objective_sets.beta_hash={}
		#print self.total_steps	
		self.total_steps=0.
		self.claimed_objective_sets=Claimed_Objective_Sets(2,self.trajectory_length,self.id)
		self.tts = Trajectory_Tree_Search.TTS(self.trajectory_length,new_param[0])
		self.current_n=new_param[0]




	def restart(self,fp):
		self.steps=0.
		self.solver.reset()
		self.get_psi(fp)
		self.set_aggregate_q(fp)

		self.available_flag=True


	def step(self,complete_environment,time_to_work):
		self.current_step_time=time_to_work
		if self.traj_flag==True:
			self.tts.reset()
			self.traj_flag=False	
		if self.mcts_flag==True:
			self.mcts.reset()
			self.mcts_flag=False
		self.think_step,max_r = self.mcts.execute(self,complete_environment,self.tts,time_to_work)
                if max_r >self.max_reward:
                    self.max_reward=max_r
                
	def test_case_step(self,complete_environment,time_to_work,test_type):
		self.current_step_time=time_to_work
		if test_type=="famine":
			if self.traj_flag==True:
				self.tts.reset()
				self.traj_flag=False	
			if self.mcts_flag==True:
				self.mcts.reset()
				self.mcts_flag=False
			self.think_step,max_r = self.mcts.execute(self,complete_environment,self.tts,time_to_work)
                        if max_r > self.max_reward:
                            self.max_reward=max_r
		else:
			if self.traj_flag==True:
				self.tts.reset()
				self.traj_flag=False	
			if self.mcts_flag==True:
				self.mcts.reset()
				self.mcts_flag=False
			self.think_step = self.mcts.execute(self,complete_environment,self.tts,time_to_work)

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
		sub_environment,trajectory,expected_reward = self.tts.execute((self.x,self.y),complete_environment,time_to_work,self.mcts)
		self.current_trajectory=trajectory
		self.current_sub_environment=sub_environment
		self.expected_reward=int(self.max_reward)
		#print self.id		
		#print self.current_trajectory.task_names
		#print self.current_sub_environment.interaction_set

	def move(self,complete_environment,time_to_work):
		self.steps+=1.
		self.total_steps+=1.
		if self.steps<self.T-5:
			self.tts.reset()
		if self.steps>self.T:
			self.steps=0

			self.choose_trajectory(complete_environment,time_to_work)
		if self.current_trajectory is None:
			return
		self.execute(self.current_trajectory.get_action(self,complete_environment))

	def test_case_move(self,agent_index,total_agents,complete_environment,time_to_work):
		#self.steps+=1.
		#self.total_steps+=1.
		self.choose_trajectory(complete_environment,time_to_work)
		
		#if self.steps>(agent_index+1)*self.T:
		#	self.steps=-10000000
		#	self.choose_trajectory(complete_environment,time_to_work)

		#if self.total_steps>(total_agents)*self.T:
		#	if self.current_trajectory is None:
		#		return
		#	self.execute(self.current_trajectory.get_action(self,complete_environment))	

	def execute(self,action_):
		self.x,self.y = self.get_transition(action_,self.x,self.y)
		


	def execute_objective(self,objective_type,complete_environment):
		complete_environment.execute_objective(objective_type,(self.x,self.y))
	

	def get_transition(self,action,x,y):
		return (x+action[0],y+action[1])



