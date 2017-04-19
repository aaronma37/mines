#!/usr/bin/env python

import Regions

class Event():
	def __init__(self,event_type,time_horizon):
		self.type=event_type
		self.data={}
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
		for region in range(len(Regions.region)):
			self.data[region]={}
			for time in range(self.time_horizon):
				self.data[region][time]=[]
				for event in e.region[region].time[time].event:
					self.append(region,time,event)



	def append(self,region,time,event):
		self.data[region][time].append(event)
	
