#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math

## Definitions of regions

zone = (((0,5),(-1,2)),((-4,1),(-1,2)),((-1,2),(-4,1)),((-1,2),(0,5)) )
region = [(10,10),(10,30),(10,50),(10,70),(10,90),(30,10),(50,10),(70,10),(90,10),(30,30),(50,30),(70,30),(90,30),(30,50),(50,50),(70,50),(90,50),(30,70),(50,70),(70,70),(90,70),(30,90),(50,90),(70,90),(90,90)]
region_modded=[[10,10],[10,30],[10,50],[10,70],[10,90],[30,10],[50,10],[70,10],[90,10],[30,30],[50,30],[70,30],[90,30],[30,50],[50,50],[70,50],[90,50],[30,70],[50,70],[70,70],[90,70],[30,90],[50,90],[70,90],[90,90],[50,50],[50,50]]
region_size=10

region_list=[]

def get_distance(x,y,x2,y2):
	return max(math.fabs(x2-x),math.fabs(y2-y))

for i in range(25):
	region_list.append([])
	for j in range(region[i][0]-region_size,region[i][0]+region_size):
		for k in range(region[i][1]-region_size,region[i][1]+region_size):	
			region_list[i].append((j,k))


greedy_regions = [(1,1),(-1,1),(-1,-1),(1,-1), (0,1), (1,0), (0,-1), (-1,0)]

def get_region(x,y):
	for i in range(len(region)):
		if x >= region[i][0]-region_size and x < region[i][0] + region_size:
			if y >= region[i][1]-region_size and y < region[i][1] + region_size:
				return i

def get_region_type(num):
	if num==14:
		return 1
	elif num==13 or num==15 or num ==10 or num ==18:
		return 2
	elif num==17 or num==19 or num==9 or num==11:
		return 3
	elif num==2 or num == 22 or num == 16 or num == 6:
		return 4
	else:
		return 5


