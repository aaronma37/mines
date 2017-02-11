#!/usr/bin/env python

class node:
	def __init__(self,data):
		self.data=data

	def get_data(self):
		return data

class data:
	def __init__(self,st,num):
		self.a=st
		self.b=num

da = data("b",1)
n = node(da)

print n.data.a,n.data.b

d = n.data
d = data("c",2)

print n.data.a,n.data.b
