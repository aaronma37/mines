#!/usr/bin/env python

from Action_Definition import get_transition_x
from Action_Definition import get_transition_y
from Environment.Mines import Location
from Environment.Mines import Mine_Data
from Solvers.UCT_SOLVER import UCT



import numpy as np



class Agent: 


	def __init__(self,x_,y_,max_depth_,depth_,Gamma_,upper_confidence_c_,action_space_num_,map_size_):

		self.init_x=x_
		self.init_y=y_

		self.solver = UCT.Solver(max_depth_,depth_,Gamma_,upper_confidence_c_,action_space_num_,map_size_)

		self.history = [0,0]
		#self.search_tree=manager.dict()
		self.search_tree=dict()
		self.x=x_
		self.y=y_
		self.action_space_num=action_space_num_
		self.measurement_space=[]
		self.local_action=0

		self.reset()

	def reset(self):
		self.x=self.init_x
		self.y=self.init_y
		self.history = [(0,0)]
		self.search_tree.clear()

	def imprint(self, u):
		u.set_x(self.get_x())
		u.set_y(self.get_y())
		u.set_history(self.get_history())

	def set_history(self,h):
		self.history = []
	
		for i in range(0, len(h)):
			self.history.append((h[i][0],h[i][1]))

	def get_history(self):
		return self.history

	def set_x(self,x_):
		self.x=x_

	def set_y(self,y_):
		self.y=y_

	def get_x(self):
		return self.x
	
	def get_y(self):
		return self.y

	def update_history(self,action_,observation_hash_):
		self.history.append((action_,observation_hash_))
		if len(self.history) > 10:
			self.history.pop(0)

	def step(self,environment_data_,num_steps_,a_):

	      #  p1 = Process(target=self.solver.OnlinePlanning, args=(self.search_tree, self, environment_data_,num_steps_,a_,))
	    #p2 = Process(target=f, args=(d,))
	       # p1.start()
	    #p2 .start()
	      # p1.join()
	    #p2.join()


		self.solver.OnlinePlanning(self.search_tree, self, environment_data_,num_steps_,a_)



		a = self.solver.get_best_action(self.search_tree,self,environment_data_)
		self.execute(a,environment_data_)
		self.update_history(a,self.solver.hash_generator_without_history(self,environment_data_))

	def execute(self,action_,environment_data_):
		if environment_data_.check_boundaries(Location(self.x+get_transition_x(action_),self.y+get_transition_y(action_))) is True:
			self.x+=get_transition_x(action_)
			self.y+=get_transition_y(action_)
		self.recalculate_measurement_space()
		self.measure(environment_data_,False)

	def simulate(self,action_,environment_data_):
		base_reward= environment_data_.get_reward()	
		if environment_data_.check_boundaries(Location(self.x+get_transition_x(action_),self.y+get_transition_y(action_))) is True:
			self.x+=get_transition_x(action_)
			self.y+=get_transition_y(action_)
		
		self.recalculate_measurement_space()
		self.measure(environment_data_,True)
		return (environment_data_,environment_data_.get_reward()-base_reward)


	def recalculate_measurement_space(self):
		self.measurement_space=[]
		for i in range(self.x-1, self.x+2 ):
			for j in range(self.y-1, self.y+2):
				self.measurement_space.append(Location(i,j))

	def measure(self,mine_data_,imaginary):
		for loc in self.measurement_space:
			mine_data_.measure_loc(loc,imaginary)


	def get_hash(self):
		prime = 31
		result = 11
		result = result*prime + self.x
		result = result*prime + self.y
		return result	

	def get_hash_history(self):
		prime = 31
		result = 11
		for i in range(0,len(self.history)):
			result = result*prime + self.get_single_history_hash(self.history[i][0],self.history[i][1])*i
		return result

	def get_single_history_hash(self,a,o):
		prime=31
		result =11
		result=result*prime + a
		result=result*prime + o
		return result

	

	def get_action_size(self):
		return self.action_space_num

