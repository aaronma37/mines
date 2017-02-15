#!/usr/bin/env python

from OpenGLContext import testingcontext
#BaseContext = testingcontext.getInteractive()
from drawing import basic_2
from Environment import Mine_Environment
from Agents import Agent_aaron_multi
from multiprocessing import Process, Queue
import multiprocessing
import time

#DIAGNOSTICS
sample_size=100
max_num_steps=5
num_workers=multiprocessing.cpu_count()-1
time_to_work=.05
num_steps=5
num_agents=5

#CHOOSE ENVIRONMENT PARAMETERS
map_size=50
#CHOOSE AGENT PARAMETERS
max_depth=10
depth=1
Gamma=.9
upper_confidence_c=1000
action_space_num=9#GET THIS FROM ACTUAL MODEL

target = open('test_alt.txt', 'w')	
target.truncate()

target.write("Settings: \n")
target.write("time per move: " + str(time_to_work) +"\n")
target.write("map size: " +  str(map_size)+ "\n")

class Simulation:

	def __init__(self):
		self.e = Mine_Environment.Environment(map_size)
		self.a=[]
		self.a_imaginary=[]
		for i in range(num_agents):
			self.a.append(Agent_aaron_multi.Agent(map_size/2,map_size/2,map_size,self.e.mine_data))
			self.a_imaginary.append(Agent_aaron_multi.Agent(map_size/2,map_size/2,map_size,self.e.mine_data))

		self.i_a=[]
		self.i_a_=[]
		self.e_=[]

		for i in range(num_workers):
			self.i_a.append(Agent_aaron_multi.Agent(map_size/2,map_size/2,map_size,self.e.mine_data))
			self.i_a_.append(Agent_aaron_multi.Agent(map_size/2,map_size/2,map_size,self.e.mine_data))
			self.e_.append(Mine_Environment.Environment(map_size))

		#self.e.mine_data.update_agent_location((self.a.get_x(),self.a.get_y()))

	
		#for o in self.a.root_task.get_sub_tasks():
		#	o.available(self.a.abstractions.abf(self.e.mine_data))
		#self.solver=POMCP_R.Solver(max_depth,depth,Gamma,upper_confidence_c,action_space_num,self.e.mine_data,map_size)
		self.count=0
		self.moving_total=[]
		self.total=0
		self.num_steps=25
		self.rounds=0
		self.evaluation=[]
		self.last_round=0
		self.eval_num=12.


	def draw(self):
		#loc=(self.a.x,self.a.y)
		basic_2.clear()

		for i in range(0, map_size):
			for j in range(0, map_size):
				if bool(self.e.get_mine_data().seen[i][j]) is False:
					basic_2.draw(self.e.get_loc_info(i,j).get_x(),self.e.get_loc_info(i,j).get_y(),self.e.get_loc_info(i,j).get_width(),self.e.get_loc_info(i,j).get_height(),0,self.e.get_mine_data().get_color(i,j)*map_size*map_size/2,0,-.1,map_size/10.)
				
		for i in range(num_agents):
			for arrow in self.a[i].arrows:
				X=arrow[0][0]
				Y=arrow[0][1]
				hh=arrow[2]/5
				ww=arrow[2]
				if arrow[1] == (1,0):
					#ww=arrow[2]/1
					#hh=arrow[2]
					dire=4
				elif arrow[1] == (-1,0):
					#ww=arrow[2]/1
					#hh=arrow[2]
					dire=0
				elif arrow[1] == (0,1):
					#ww=arrow[2]
					#hh=arrow[2]/1
					dire=6
				else:
					dire=2
					#ww=arrow[2]
					#hh=arrow[2]/1	


				basic_2.draw(self.e.get_sqr_loc(X), self.e.get_sqr_loc(Y), self.e.get_norm_size()*ww, self.e.get_norm_size()*hh,2, 1,dire,-.1,map_size/10.)
		


		for i in range(num_agents):
			basic_2.draw(self.e.get_sqr_loc(self.a[i].x), self.e.get_sqr_loc(self.a[i].y), self.e.get_norm_size(), self.e.get_norm_size(),1, 1,0,-.1,map_size/10.)

	
		basic_2.draw(self.e.get_loc_info(self.e.mine_data.get_mine_location().get_x(),self.e.mine_data.get_mine_location().get_y()).get_x(), self.e.get_loc_info(self.e.mine_data.get_mine_location().get_x(),self.e.mine_data.get_mine_location().get_y()).get_y(), self.e.get_loc_info(self.e.mine_data.get_mine_location().get_x(),self.e.mine_data.get_mine_location().get_y()).get_width(), self.e.get_loc_info(self.e.mine_data.get_mine_location().get_x(),self.e.mine_data.get_mine_location().get_y()).get_height(), 1, 1,0,-.1,map_size/10.)









		basic_2.end_draw()

	def reset_func(self):
		self.e.mine_data.reset()

		for i in range(num_agents):
			self.a[i].reset(self.e.mine_data)
			self.a_imaginary[i].reset(self.e.mine_data)
		#self.e.mine_data.update_agent_location((self.a.get_x(),self.a.get_y()))


		self.rounds+=1
		self.total+=self.count
		self.count=0


	def evaluate_reset(self,a,a_,e):
		e.mine_data.reset()
		for i in range(num_agents):
			a[i].reset(e.mine_data)
			a_[i].reset(e.mine_data)
		e.mine_data.update_agent_location((a.get_x(),a.get_y()))

		count=0	

	def ind_eval(self,num_eval,a,a_,e,q):
		total=0
		count=0
		i=0
		self.evaluate_reset(a,a_,e)
		while i < num_eval:
			for i in range(num_agents):			
				a[i].step(e.mine_data,0, a_,0)
				count+=1
				if e.mine_data.get_complete() is True:
					self.evaluate_reset(a,a_,e)
					total+=count
					count=0
					i+=1
				if count>map_size*map_size/2 :
					self.evaluate_reset(a,a_,e)
					total+=count
					count=0				
					i+=1
		q.put(total)

	def evaluate(self,to_draw):
		print "Evaluating at", self.rounds
		self.evaluation.append(0.)
		#self.solver=self.a.solver
		for i in range(agents):
			self.i_a[i].solver=self.a[i].solver
			self.i_a_[i].solver=self.a[i].solver

		i=0
		q=[]
		p=[]
		total=0
		for i in range(0,num_workers):
			q.append(Queue())
			p.append(Process(target=self.ind_eval, args=(self.eval_num,self.i_a[i],self.i_a_[i],self.e_[i],q[i])))

		for i in range(0,num_workers):
			p[i].start()


		for i in range(0,num_workers):
			p[i].join()


		for i in range(0,num_workers):
			evaluation=(q[i].get())
			total+=evaluation

		print total/(self.eval_num*num_workers)

		to_write=str(self.rounds) + ", " + str(total/(self.eval_num*num_workers)) + "\n"
		target.write(to_write)



		#while i < self.eval_num:

		#	for j in range(num_agents):
		#		self.a.step(self.e.mine_data,0, self.a_imaginary,0)
		#	self.count+=1
		#	if self.e.mine_data.get_complete() is True:
		#		self.evaluate_reset()
		#		i+=1
		#	if self.count>map_size*map_size/2 :
		#		self.evaluate_reset()
		#		i+=1
		#	if to_draw is True:
		#		self.draw()
		#print "ROUND: ", self.rounds, "AVERAGE", self.evaluation[len(self.evaluation)-1]/self.eval_num





	def run(self, to_draw, q,time_to_work,num_steps):
		start = time.time()
		end = time.time()
		while end - start < 50000:

			for j in range(num_agents):
				self.a[j].step(self.e.mine_data,100, self.a_imaginary[j],time_to_work)
			self.count+=1
			if self.e.mine_data.get_complete() is True:
				self.reset_func()
				end = time.time()
			if self.count>map_size*map_size/2 :
				self.reset_func()
				end = time.time()
				print "max reached"

			if self.rounds % 100 is 0 and self.rounds > self.last_round:
				self.last_round=self.rounds
				self.evaluate(to_draw)


	
			if to_draw is True:
				self.draw()
		q.put((self.rounds,self.total))

print "Starting threads... Machine limit: ", multiprocessing.cpu_count()

for i in range(0,100):
	num_steps=5+i*25
		
	s=[]
	q=[]
	p=[]
	evaluation=()
	rounds=0
	total=0

	s.append(Simulation())
	q.append(Queue())
	
	s[0].run(True,q[0],time_to_work,100)

#	for i in range(0,num_workers):
#		s.append(Simulation())
#		q.append(Queue())
#		p.append(Process(target=s[i].run, args=(False,q[i],time_to_work,num_steps)))

#	for i in range(0,num_workers):
#		p[i].start()

#	for i in range(0,num_workers):
#		evaluation=(q[i].get())
#		rounds+=evaluation[0]
#		total+=evaluation[1]

#	for i in range(0,num_workers):
#		p[i].join()




	print "#", num_steps," Average: ", total/rounds, " for ", rounds, " rounds"










