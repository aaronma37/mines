#!/usr/bin/env python

import Regions
from random import randint
class Event():
	def __init__(self,event_type,time_horizon):
		self.type=event_type
		self.data={}
		self.id=0
		self.time_horizon=time_horizon
		for region in range(len(Regions.region)):
			self.data[region]={}
			for time in range(time_horizon):
				self.data[region][time]=[]
				
	def clear(self):
		self.data={}
		for region in range(len(Regions.region)):
			self.data[region]={}
			for time in range(self.time_horizon):
				self.data[region][time]=[]


	def update(self,e):
		self.data={}
		self.id=e.event_id
		for region in range(len(Regions.region)):
			self.data[region]={}
			for time in range(self.time_horizon):
				self.data[region][time]=[]
				for event in e.region[region].time[time].event:
					self.append(region,time,event)

	def cull(self):
		for region in range(len(Regions.region)):
			for time in range(self.time_horizon-1):
				self.data[region][time]=self.data[region][time+1]
			self.data[region][time+1]=[]



	def append(self,region,time,event):
		self.data[region][time].append(event)
	
