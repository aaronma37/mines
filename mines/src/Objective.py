#!/usr/bin/env python
from random import shuffle
from sets import Set
from abstraction_classes import Abstractions
import time
import math
import random
import Regions
As=Abstractions()

class Battery():
	def __init__(self):
		'''nothing'''
	
	def get_state(self,A,Phi,seed):
		n=A.battery.num
		h=""
		for i in range(Phi.state_size):
			if n>50:			
				h=h+str(0)+"~"
			else:
				h=h+str(1)+"~"
			n-=5


		h=h+';'

		vision=Phi.visions[seed]
		base=A.get_base()
		
		for i in range(Phi.state_size):
			if base is None:
				h=h+str(0)+"~"
			elif Phi.get_loc_from_vision(vision[i],base) is None:
				h=h+str(0)+"~"
			else:
				if Phi.get_loc_from_vision(vision[i],base) == 14: 
					h=h+str(1)+"~"
				else:
					h=h+str(0)+"~"
		return h
		
	def evolve(self,state_string,a):

		s_ = state_string.split(";")

		battery_string = s_[0].split("~")
		charger_string = s_[1].split("~")

		battery_string=battery_string[:-1]
		charger_string=charger_string[:-1]



		if a is "charge" and charger_string[0] == 1:
			for i in battery_string:
				i="0"
		else:
			battery_string=battery_string[1:]
			battery_string.append(battery_string[-1])
		
		
		charger_string=charger_string[1:]
		charger_string.append("-1")

		h=''
		for l in battery_string:
			h=h+l+"~"
		h=h+';'
		for l in charger_string:
			h=h+l+"~"
		

		return h

	def get_reward(self,state_string,a):
		s_ = state_string.split(";")

		battery_string = s_[0].split("~")
		charger_string = s_[1].split("~")

		battery_string=battery_string[:-1]
		charger_string=charger_string[:-1]

		if int(battery_string[0])==1 and int(charger_string[0]) == 1 and a is "charge":  
			return 1000
		
		return 0


class Exploration():
	def __init__(self):
		'''nothing'''
	
	def get_state(self,A,Phi,seed):
		vision=Phi.visions[seed]
		h=""
		base=A.get_base()

		for i in range(Phi.state_size):
			if Phi.get_loc_from_vision(vision[i],base) is None:
				h=h+str(0)+"~"
			else:
				h=h+str(A.regions[Phi.get_loc_from_vision(vision[i],base)].hash)+"~"
		return h
		
	def evolve(self,state_string,a):
		exploration_string = state_string.split("~")
		exploration_string=exploration_string[:-1]

		exploration_string=exploration_string[1:]
		exploration_string.append("-1")

		h=""
		for l in exploration_string:
			h=h+l+"~"

		return h

	def get_reward(self,state_string,a):
		exploration_string = state_string.split("~")
		exploration_string=exploration_string[:-1]

		ex=int(exploration_string[0])

		if a is "explore":
			if ex==3:
				return 5.
			elif ex==2:
				return 4.5
			elif ex==1:
				return 1.
			else:
				return 0.
		else:
			return 0.

class Objective_Handler():
	def __init__(self):
		self.objectives=[]
		self.objectives.append(Battery())
		self.objectives.append(Exploration())

	def get_state(self,A,Phi,seed):
		h=''
		for i in Phi.alpha:
			h=h+str(i)+"~"

		h=h+','

		for i in range(len(self.objectives)):
			h=h+self.objectives[i].get_state(A,Phi,seed)+','

		return h

	def evolve(self,state_string,a):
		objective_string = state_string.split(",")
		alpha_string = objective_string[0]
		alpha_string = alpha_string.split("~")
		alpha_string = alpha_string[:-1]
		objective_string=objective_string[1:]
		objective_string=objective_string[:-1]

		h=''
		for i in alpha_string:
			h=h+i+"~"

		h=h+","


		for i in range(len(self.objectives)):
			objective_string[i]=self.objectives[i].evolve(objective_string[i],a)

		for l in objective_string:		
			h=h+l+","

		return h

	def get_reward(self,s,a):
		state_string = s.split(",")
		state_string=state_string[:-1]
		alpha_string = state_string[0]
		alpha_string = alpha_string.split("~")
		alpha_string = alpha_string[:-1]
		objective_string = state_string[1:]

		r=0.

		for i in range(len(self.objectives)):
			r+=float(alpha_string[i])*self.objectives[i].get_reward(objective_string[i],a)

		
		return r





