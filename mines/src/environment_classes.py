#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
from mines.msg import subobjective as subobjective_msg
from mines.msg import objective as objective_msg
from mines.msg import environment as environment_msg
from mines.msg import o_r_state as o_r_state_msg
from mines.msg import cross_trajectory as cross_trajectory_msg

size=10

objective_parameter_list=[]
objective_map={}
objective_parameter_list.append(('test1',1,"mine",1))
objective_parameter_list.append(('test2',1,"service",1))
objective_parameter_list.append(('test3',1,"service2",1))
#objective_parameter_list.append(('fourth',1,"service3",1))
#objective_parameter_list.append(('test5',1,"service4",1))
#objective_parameter_list.append(('test6',1,"service5",1))
objective_map["mine"]=0
objective_map["service"]=1
objective_map["service2"]=2
#objective_map["service3"]=3
#objective_map["service4"]=4
#objective_map["service5"]=5

def interact_string_evolve(interact_string_by_agent,objective_type):


	per_region_state=interact_string_by_agent.split('@')[0].split('.')[:-1] #list of strings
	task_list = interact_string_by_agent.split('@')[1].split(',')[:-1]
	interact_list = interact_string_by_agent.split('@')[2].split(',')[:-1]

	#print "bn"
	#print per_region_state
	#print task_list
	#print interact_list

	for i in range(len(interact_list)):
		if interact_list[i]=='-':
			continue
		if int(interact_list[i])==0:
			interact_list[i]='-'
			o_states=per_region_state[i].split(',')[-1]
			for o_state in o_states:
				if int(o_state)>0:
					o_state=str(int(o_state)-1)
			per_region_state[i]=''
			for o_state in o_states:
				per_region_state[i]=per_region_state[i]+o_state+","
			

		else:
			interact_list[i]=str(int(interact_list[i]))

	reg_state=''
	task_state=''
	interact_state=''

	for i in range(1,len(interact_list)):
		reg_state=reg_state+per_region_state[i]+"."	
		interact_state=interact_state+interact_list[i]+","

	for i in range(1,len(task_list)):
		task_state=task_state+task_list[i]+","

	return reg_state + "@" + task_state + "@" +interact_state+"@"

def get_interact_intersection(interact_string_by_agent,objective_type):
	
	interact_list = interact_string_by_agent.split('@')[2].split(',')[:-1]
	task_list = interact_string_by_agent.split('@')[1].split(',')[:-1]

	complete_list=[]

	#print interact_list

	for i in range(len(interact_list)-1):
		if interact_list[i]=='-':
			continue
		if int(interact_list[i])==0:
			if task_list[i]==objective_type:
			#	print task_list[i],objective_type,"added"
				complete_list.append(i)
			#else:
				#print task_list[i],objective_type,"compe"


	#print task_list,objective_type
	#if len(complete_list)>0:
		
	#	print complete_list
	return complete_list
	


def get_intersect_list_from_k(string):
	return string.split('|')[2].split('+')[k].split('@')[2]


def get_k_from_string(string):
	mod_string=string.split('|')
	reg_state=mod_string[1]
	reg_state_list=reg_state.split(',')[:-1]
	return len(reg_state_list)

def get_objective_state_from_string(k,state_string,obj_type):
	mod_string=state_string.split('|')
	o_state=mod_string[0]
	region_o_state_list=o_state.split('.')[:-1]
	o =region_o_state_list[k].split(',')
	try:	
	 	int(o[objective_map[obj_type]])
    	except ValueError:
		print "Value Error,", region_o_state_list[k],k,objective_map[obj_type]
		return 0
	return int(o[objective_map[obj_type]])

def modify_interact_string(main_string,interact_string):
	mod_string=main_string.split('|')
	o_state=mod_string[0]
	reg_state=mod_string[1]
	return o_state+"|"+reg_state+"|"+interact_string+"|"

def string_evolve(string,obj_type):

	if objective_map.get(obj_type) is not None:

		o_index=objective_map[obj_type]
		mod_string=string.split('|')
		o_state=mod_string[0]
		region_o_state_list=o_state.split('.')[:-1]
		reg_state=mod_string[1]
		reg_state_list=reg_state.split(',')[:-1]
		int_state=mod_string[2]


			
		for i in range(len(region_o_state_list)):
			if i ==0:
				continue
			if reg_state_list[i]=='-':
				continue

			if int(reg_state_list[i])==0:
				h_list=region_o_state_list[i].split(',')[:-1]

				if int(h_list[o_index])>0:
					h_list[o_index]=str(int(h_list[o_index])-1)
					region_o_state_list[i]=''
					for k in range(len(h_list)):
						region_o_state_list[i]=region_o_state_list[i]+h_list[k]+','
				
		for i in range(len(reg_state_list)):
			if reg_state_list[i]=='-':
				continue
			if reg_state_list[i]=='0':
				reg_state_list[i]='-'
				continue
			reg_state_list[i]=str(int(reg_state_list[i])-1)

		reg_state=''
		for i in range(1,len(reg_state_list)):
			reg_state=reg_state+reg_state_list[i]+','


		o_state=''
		for i in range(1,len(region_o_state_list)):
			o_state=o_state+region_o_state_list[i]+'.'
	else:
		mod_string=string.split('|')
		o_state=mod_string[0]
		region_o_state_list=o_state.split('.')[:-1]
		reg_state=mod_string[1]
		reg_state_list=reg_state.split(',')[:-1]
		int_state=mod_string[2]
				
		for i in range(len(reg_state_list)):
			if reg_state_list[i]=='-':
				continue
			if reg_state_list[i]=='0':
				reg_state_list[i]='-'
				continue
			reg_state_list[i]=str(int(reg_state_list[i])-1)

		reg_state=''
		for i in range(1,len(reg_state_list)):
			reg_state=reg_state+reg_state_list[i]+','


		o_state=''
		for i in range(1,len(region_o_state_list)):
			o_state=o_state+region_o_state_list[i]+'.'
		

	return o_state+"|"+reg_state+"|"+int_state+"|"


def get_region(x,y):
	return (int(math.floor(x/size)),int(math.floor(y/size)))

def get_region_parts(r):
	region_list=[]
	for x in range(r[0]*size,(r[0]+1)*size):
		for y in range(r[1]*size,(r[1]+1)*size):		
			region_list.append((x,y))
	return region_list

def is_feasible_travel_path(r1,r2):
	if abs(r1(0)-r2(0))<2 and abs(r1(1)-r2(1))<2:
		return True
	return False



class Sub_Objective():
	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.region=get_region(x,y)


class Objective():
	def __init__(self,objective_parameters):
		self.sub_objectives=[]
		self.distribution_type=objective_parameters[0]
		self.granularity=objective_parameters[1]
		self.frame_id=objective_parameters[2]
		self.individual_reward=objective_parameters[3]

		
		
	def distribute(self,distribution_type):
		if distribution_type=="All":
			for x in range(100):
				for y in range(100):
					self.sub_objectives.append(Sub_Objective(x,y))

	def repopulate(self):
		self.sub_objectives=[]
		if self.distribution_type=="all":
			for x in range(0,100):
				for y in range(0,100):
					self.sub_objectives.append(Sub_Objective(x,y))	
		elif self.distribution_type=="second":
			for x in range(50,75):
				for y in range(25,75):
					self.sub_objectives.append(Sub_Objective(x,y))	
		elif self.distribution_type=="third":
			#for x in range(15,30):
			#	for y in range(55,75):
			#		self.sub_objectives.append(Sub_Objective(x,y))	
			for x in range(0,20):
				for y in range(0,20):
					self.sub_objectives.append(Sub_Objective(x,y))	
			for x in range(80,90):
				for y in range(15,25):
					self.sub_objectives.append(Sub_Objective(x,y))	
			#for x in range(50,64):
			#	for y in range(20,41):
			#		self.sub_objectives.append(Sub_Objective(x,y))	
			for x in range(41,43):
				for y in range(80,90):
					self.sub_objectives.append(Sub_Objective(x,y))	
			for x in range(25,35):
				for y in range(25,35):
					self.sub_objectives.append(Sub_Objective(x,y))
		elif self.distribution_type=="fourth":
			for x in range(40,50):
				for y in range(40,50):
					self.sub_objectives.append(Sub_Objective(x,y))	
		elif self.distribution_type=="fifth":
			for x in range(55,65):
				for y in range(55,70):
					self.sub_objectives.append(Sub_Objective(x,y))	
	
	
		elif self.distribution_type=="test1":
			#self.sub_objectives.append(Sub_Objective(52,50))
			#self.sub_objectives.append(Sub_Objective(58,50))
			self.sub_objectives.append(Sub_Objective(62,50))
			self.sub_objectives.append(Sub_Objective(68,50))
			self.sub_objectives.append(Sub_Objective(72,50))
			self.sub_objectives.append(Sub_Objective(78,50))

		elif self.distribution_type=="test2":
			self.sub_objectives.append(Sub_Objective(42,40))
			self.sub_objectives.append(Sub_Objective(58,40))
			self.sub_objectives.append(Sub_Objective(42,70))
			self.sub_objectives.append(Sub_Objective(28,15))
			self.sub_objectives.append(Sub_Objective(52,40))
			self.sub_objectives.append(Sub_Objective(48,40))
	

		elif self.distribution_type=="test3":
			self.sub_objectives.append(Sub_Objective(42,43))
			self.sub_objectives.append(Sub_Objective(55,55))
			self.sub_objectives.append(Sub_Objective(53,60))
			self.sub_objectives.append(Sub_Objective(38,60))
			self.sub_objectives.append(Sub_Objective(42,43))
			self.sub_objectives.append(Sub_Objective(63,43))
	

		elif self.distribution_type=="test4":
			self.sub_objectives.append(Sub_Objective(32,30))
			self.sub_objectives.append(Sub_Objective(78,20))
			self.sub_objectives.append(Sub_Objective(42,60))
			self.sub_objectives.append(Sub_Objective(43,55))
			self.sub_objectives.append(Sub_Objective(43,43))
			self.sub_objectives.append(Sub_Objective(66,44))
	

		elif self.distribution_type=="test5":
			self.sub_objectives.append(Sub_Objective(44,53))
			self.sub_objectives.append(Sub_Objective(41,53))
			self.sub_objectives.append(Sub_Objective(35,37))
			self.sub_objectives.append(Sub_Objective(68,31))
			self.sub_objectives.append(Sub_Objective(72,40))
			self.sub_objectives.append(Sub_Objective(78,42))

		elif self.distribution_type=="test7":
			self.sub_objectives.append(Sub_Objective(45,45))
			#self.sub_objectives.append(Sub_Objective(35,35))
			#self.sub_objectives.append(Sub_Objective(25,35))
		elif self.distribution_type=="test8":
			self.sub_objectives.append(Sub_Objective(45,55))
			#self.sub_objectives.append(Sub_Objective(35,35))
			#self.sub_objectives.append(Sub_Obj
	
		elif self.distribution_type=="none":
			return
				
			
		

class Sub_Environment:
	def __init__(self):
		self.region_list=[]
		self.state=''
		self.region_list_correlation=''
		self.interaction_state=''
		self.interaction_set=set()
		self.modification_list=[]
		 
	def set_region_list(self,region_list):
		self.region_list=region_list
	
	def set_random_region_list(self,r,L):
		self.region_list=[]
		self.region_list.append(r)
		for k in range(L-1):
			self.region_list.append((self.region_list[-1][0]+random.randint(-1, 1),self.region_list[-1][1]+random.randint(-1, 1)))
		




	def get_sub_sub_environment(self,k):
		return Sub_Environment(self.region_list[0:k],self.state[0:k],self.interaction_set[0:k])

	def append_region(self,r):
		self.region_list.append(r)

	def cull_state_from_back(self,k):
		s=self.state.split(".")

		h=""
		for i in range(0,len(s)-k-1):
			h=h+s[i]+"."

		return h


		

	def cull_state_from_front(self,k):
		s=self.state.split(".")
		h=""
		for i in range(k,len(s)-1):
			h=h+s[i]+"."

		return h

	def get_state_index(self,k):
		return self.state.split(".")[k]

	def get_objective_index(self,k,o_index):

		try:	
		 	int(self.get_state_index(k).split(",")[o_index])
	    	except (ValueError,IndexError):
			return 0
			''' '''
			#print("Oops!  That was no valid number.  Try again..."),self.get_state_index(k).split(","),self.state


		return self.get_state_index(k).split(",")[o_index]

	def get_k(self):
		return len(self.region_list)-1

		
	def update_region_list_correlation(self):
		self.region_list_correlation=''		
		for i in range(len(self.region_list)):
			 if i==0:
				self.region_list_correlation=self.region_list_correlation+'-'+','
			 else:
				signal='-'
				for j in xrange(i-1,-1,-1):
					if self.region_list[i]==self.region_list[j]:
						signal=str(j)
				self.region_list_correlation=self.region_list_correlation+signal+','

		self.region_list_correlation=self.region_list_correlation+"|"
	
	def get_total_state(self):
		return self.state+self.region_list_correlation+self.interaction_state

		
	def update_state(self,complete_environment):
		self.state=""

		self.modification_list=[]
		for agent_id,n_hash in complete_environment.beta_hash.items():
			if agent_id in self.interaction_set and n_hash.get(1) is not None:
				n=1
			else:
				n=0
			if n_hash.get(0) is None:
				break

			for claimed_objective in n_hash[n]:
				self.modification_list.append(claimed_objective)

		for r in self.region_list:
			self.state=self.state
			for obj in complete_environment.objective_list:
				flag=False
				for claimed_objective in self.modification_list:
					if claimed_objective.region.x==r[0] and claimed_objective.region.y==r[1] and claimed_objective.objective_type==obj.frame_id:
						flag=True

				if flag==True:
					self.state=self.state+str(0)+","
				else:
					#self.state=self.state+str(complete_environment.get_region_objective_state(obj_type,r))+","
					self.state=self.state+str(complete_environment.pull_region_objective_state(obj.frame_id,r))+","

			self.state=self.state+"."

		self.state=self.state+"|"
		self.update_interaction_state(complete_environment)
		self.update_region_list_correlation()


		
		

	def evolve(self,agent,complete_environment):
		evolved_environment=Sub_Environment()
		evolved_environment.region_list=self.region_list[1:]
		evolved_environment.update_state(complete_environment)
		return evolved_environment

	def update_interaction_state(self,complete_environment):
		self.interaction_state=''	

		if complete_environment.interaction_list is None or len(self.interaction_set)==0:
			return

		for agent_id in self.interaction_set:
			for agent_trajectory in complete_environment.collective_trajectories_message.agent_trajectory:
				if agent_id==agent_trajectory.frame_id: 
					state_string = agent_trajectory.state.split('|')[0]
					

					action_string=''
					for action in agent_trajectory.task_trajectory:
						action_string=action_string +action+','

					interact_string=''
					for region in agent_trajectory.region_trajectory:
						signal='-'
						for j in xrange(len(self.region_list)-1,-1,-1):
							if (region.x,region.y)==self.region_list[j]:
								signal=str(j)
						interact_string=interact_string+signal+','			
			self.interaction_state=self.interaction_state+state_string+"@"+action_string+"@"+interact_string+"@" +"+"
		self.interaction_state=self.interaction_state+"|"
	


		



class Complete_Environment:
	def __init__(self):

		self.objective_parameter_list=objective_parameter_list
		self.objective_list=[]
		self.objective_map={}
		self.interaction_list=None
		self.collective_trajectories_message=None
		self.beta_hash={}
		self.o_r_state={}
		self.cross_trajectory={}
		
	
		for objective_parameters in self.objective_parameter_list:

			self.objective_list.append(Objective(objective_parameters))
			self.objective_map[objective_parameters[2]]=len(self.objective_list)-1
			self.o_r_state[objective_parameters[2]]={}
		self.agent_locations=[]
		self.repopulate()

	def reset(self):
		self.objective_list=[]
		self.objective_map={}
		for objective_parameters in self.objective_parameter_list:
			self.objective_list.append(Objective(objective_parameters))
			self.objective_map[objective_parameters[2]]=len(self.objective_list)-1
		self.repopulate()

	def update_from_agent(self,agent):
		self.interaction_list=agent.interaction_list

	def repopulate(self):
		for o in self.objective_list:
			o.repopulate()


	def get_sub_objectives_in_region(self,objective_type,r):
		sub_objectives=[]
		if objective_type == "wait":
			return sub_objectives
		elif objective_type=="travel":
			return 	get_region_parts(r)	



		if len(self.objective_list)-1<objective_map[objective_type]:
			print "weird"
			return sub_objectives
		for sub_objective in self.objective_list[objective_map[objective_type]].sub_objectives:
			if sub_objective.region==r:
				sub_objectives.append(sub_objective)
		return sub_objectives

	def get_region(self,x,y):
		return get_region(x,y)

	
	def get_feasible_travel_paths(self,r):
		regions=[]
		
		for p in range((int(r[0])-1),(int(r[0])+2)):
			for q in range((int(r[1])-1),(int(r[1])+2)):
				#if r[0] ==p and r[1] ==q:
				#	continue
				regions.append((p,q))		

		return regions

	def get_region_objective_state(self,objective_type,r):
		if objective_type=="wait" or objective_type=="travel":
			return 0
		if len(self.objective_list)-1<objective_map[objective_type]:
			return 0
		c=0
		obj=self.objective_list[objective_map[objective_type]]
		for sub_objective in obj.sub_objectives:
			if sub_objective.region == r:
				c+=obj.granularity
		
		return int(math.ceil(c/float(size*size)))

	def calculate_o_r_state(self):
		for o in self.objective_list:
			self.o_r_state[o.frame_id]={}

		for o in self.objective_list:
			for so in o.sub_objectives:
				if self.o_r_state[o.frame_id].get(so.region) is None:
					self.o_r_state[o.frame_id][so.region]=self.get_region_objective_state(o.frame_id,so.region)


	def pull_region_objective_state(self,obj_type,r):
		if self.o_r_state[obj_type].get(r) is None:
			return 0
		

		try:
			return self.o_r_state[obj_type][r]
		except KeyError:
			print "key error", obj_type,r
			return 0

			

	def execute_objective(self, objective_type, location):
		if objective_type=="travel" or objective_type=="wait":
			return

		if len(self.objective_list)-1<objective_map[objective_type]:
			return

		obj=self.objective_list[objective_map[objective_type]]



		for i in xrange(len(obj.sub_objectives)-1,-1,-1):
			if abs(obj.sub_objectives[i].x-location[0])<2 and abs(obj.sub_objectives[i].y-location[1])<2:
				del obj.sub_objectives[i]



#
		#for sub_objective in list(obj.sub_objectives):
		#	if abs(sub_objective.x-location[0])<2 and abs(sub_objective.y-location[1])<2:
		#		obj.sub_objectives.delete(sub_objective)





	def generate_environment_msg(self,collective_trajectory_message,trigger_agent,num_agent_traj,step_time):
		env_msg=environment_msg()
		env_msg.frame_id="default"
		
		env_msg.objective=[]
		env_msg.trigger=trigger_agent
		env_msg.num_agent_traj=num_agent_traj
		env_msg.step_time=step_time


		for o in self.objective_list:
			env_msg.objective.append(objective_msg())
			env_msg.objective[-1].frame_id=o.frame_id
			env_msg.objective[-1].param1=o.distribution_type
			env_msg.objective[-1].param2=o.granularity

			for so in o.sub_objectives:
				env_msg.objective[-1].subobjective.append(subobjective_msg())
				env_msg.objective[-1].subobjective[-1].x=so.x
				env_msg.objective[-1].subobjective[-1].y=so.y
				env_msg.objective[-1].subobjective[-1].rx=so.region[0]
				env_msg.objective[-1].subobjective[-1].ry=so.region[1]


		self.calculate_o_r_state()
	

		for o in self.objective_list:
			for k,v in self.o_r_state[o.frame_id].items():
				o_r_state_message=o_r_state_msg()
				o_r_state_message.region.x=k[0]
				o_r_state_message.region.y=k[1]
				o_r_state_message.value=v
				o_r_state_message.obj_type=o.frame_id

				env_msg.o_r_state.append(o_r_state_message)

		helper={}

		for a in collective_trajectory_message.agent_trajectory:
			for r in a.region_trajectory:
				if helper.get((r.x,r.y)) is None:
					helper[(r.x,r.y)]=set()
					helper[(r.x,r.y)].add(a.frame_id)
				else:
					helper[(r.x,r.y)].add(a.frame_id)


		env_msg.cross_trajectory=[]

		for k,v in helper.items():
			
			cross_trajectory_message=cross_trajectory_msg()
			cross_trajectory_message.region.x=k[0]
			cross_trajectory_message.region.y=k[1]
			for val in v:
				cross_trajectory_message.agent_id.append(val)



			env_msg.cross_trajectory.append(cross_trajectory_message)


		env_msg.collective_trajectories=collective_trajectory_message		


		return env_msg

	def update(self,env_msg):
		#self.objective_list=[]
		#self.objective_map={}

		for o in self.objective_list:		
			self.o_r_state[o.frame_id]={}

		for o_r_state_msg in env_msg.o_r_state:
				self.o_r_state[o_r_state_msg.obj_type][(o_r_state_msg.region.x,o_r_state_msg.region.y)]=int(o_r_state_msg.value)	

		self.cross_trajectory={}

		for c_t in env_msg.cross_trajectory:

			if self.cross_trajectory.get((c_t.region.x,c_t.region.y)) is None:
				self.cross_trajectory[(c_t.region.x,c_t.region.y)]=set()

			for agent_id in c_t.agent_id:
				self.cross_trajectory[(c_t.region.x,c_t.region.y)].add(agent_id)
		
		c=0
		for o in env_msg.objective:
			
			self.objective_list[c].sub_objectives=[]
			c+=1
			self.objective_map[o.frame_id]=len(self.objective_list)-1
			for so in list(o.subobjective):
				self.objective_list[-1].sub_objectives.append(Sub_Objective(so.x,so.y))

		self.collective_trajectories_message=env_msg.collective_trajectories

	def print_objective_score(self,objective_type):
		obj=self.objective_list[objective_map[objective_type]]
		#print "score", objective_type, len(obj.sub_objectives)
			

	def modify(self,beta_hash):
		#self.calculate_o_r_state()
		#return
		self.beta_hash=beta_hash
		#print beta_hash
		#self.modification_list=effective_beta.claimed_objective
		#self.calculate_o_r_state()
		return

			

		for o in self.objective_list:
			prev=			len(o.sub_objectives)
			#print "lena", len(o.sub_objectives), len(effective_beta.claimed_objective)
			for claimed_objective in effective_beta.claimed_objective:
				if claimed_objective.objective_type!=o.frame_id:
					continue
				for i in xrange(len(o.sub_objectives)-1,-1,-1):
					if o.sub_objectives[i].region == (claimed_objective.region.x,claimed_objective.region.y):
						o.sub_objectives.remove(o.sub_objectives[i])
			#if len(effective_beta.claimed_objective)<prev:
				#print "reduced"

	def get_aggregate_cost(self):
		c=0
		for o in self.objective_list:
			for sub_objective in o.sub_objectives:
				c+=o.individual_reward

		return c




	
					








