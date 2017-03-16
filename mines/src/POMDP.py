#!/usr/bin/env python


from random import randint
import random
import numpy as np
import math
from abstraction_classes import Abstractions
from Heuristics import heuristic
import Heuristics
from sets import Set
import time
import Policies
from random import shuffle
from six.moves import xrange
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import Regions


H=5
Gamma=.99


def distance(x1, y1, x2, y2):
    # Manhattan distance
    dist = abs(x1 - x2) + abs(y1 - y2)

    return dist


# Demand callback
class CreateDemandCallback(object):
	"""Create callback to get demands at location node."""

	def __init__(self, demands):
    		self.matrix = demands

	def Demand(self, from_node, to_node):
    		return self.matrix[from_node]



# Service time (proportional to demand) callback.
class CreateServiceTimeCallback(object):
  	"""Create callback to get time windows at each location."""

	def __init__(self, demands, time_per_demand_unit):
    		self.matrix = demands
    		self.time_per_demand_unit = time_per_demand_unit

  	def ServiceTime(self, from_node, to_node):
    		return self.matrix[from_node] * self.time_per_demand_unit


# Create total_time callback (equals service time plus travel time).
class CreateTotalTimeCallback(object):
	def __init__(self, service_time_callback, dist_callback, speed):
    		self.service_time_callback = service_time_callback
    		self.dist_callback = dist_callback
    		self.speed = speed

  	def TotalTime(self, from_node, to_node):
   		service_time = self.service_time_callback(from_node, to_node)
    		travel_time = self.dist_callback(from_node, to_node) / self.speed
    		return service_time + travel_time

class CreateDistanceCallback(object):
 	"""Create callback to calculate distances and travel times between points."""

	def __init__(self, locations,reward_list):
		"""Initialize distance array."""
    		num_locations = len(locations)
    		self.matrix = {}
		self.reward_matrix= {}

    		for from_node in xrange(num_locations):
      			self.matrix[from_node] = {}
			self.reward_matrix[from_node]=reward_list[from_node]
      			for to_node in xrange(num_locations):
        			if from_node == to_node:
			  		self.matrix[from_node][to_node] = 0
				else:
					  x1 = locations[from_node][0]
					  y1 = locations[from_node][1]
					  x2 = locations[to_node][0]
					  y2 = locations[to_node][1]
					  self.matrix[from_node][to_node] = distance(x1, y1, x2, y2)

    	def NegDistance(self, from_node, to_node):
		#if to_node==25:
		#	print -self.matrix[from_node][to_node], "d", from_node
		#	return 0
			

		if self.reward_matrix[to_node]==0:
			return -1000

		if to_node==25:
		        return -.25*self.matrix[from_node][to_node]
		else:
        		return -.25*self.matrix[from_node][to_node] - 25.


  	def Distance(self, from_node, to_node):
    		return self.matrix[from_node][to_node]

  	def DiscountedDistance(self,from_node,to_node):
		#print from_node,to_node,1/math.pow(Gamma,self.Distance(from_node,to_node)*self.reward_matrix[to_node]/1000.)

		if self.reward_matrix[to_node]==0:
			return 1000
		elif to_node == 25 and from_node==14:
			return 10000
		else:
			#print 1./(math.pow(Gamma,self.Distance(from_node,to_node)/10.)*self.reward_matrix[to_node]*self.reward_matrix[to_node])
			return 1./(math.pow(Gamma,-self.NegDistance(from_node,to_node)/10.)*self.reward_matrix[to_node]*self.reward_matrix[to_node])

    	def MaxDistance(self):
        	maxdist = 0
        	for from_node in self.matrix:
            		for to_node in self.matrix[from_node]:
                		dist = self.Distance(from_node, to_node)
                		if dist > maxdist:
                    			maxdist = dist
        	return(maxdist)



def IsRefuelNode(node):
    """
    Returns true if node is a refueling node,
    based on node / refuel node ratio.
    """

    if node==25:
	return False
    #refuel_node_ratio = 5
    return False

class Solver: 


	def __init__(self,E,e_args):
		self.N={}#{level_type:{state abstraction: num visited}}
		self.Na={}#{level_type:{state abstraction: {policy: num visited}}
		self.Q={}#{state abstraction:{policy:Expected Reward}}
		self.great=[]
		self.T=Set()
		self.H=heuristic()
		Heuristics.load_file(self.H,'testfile.txt')
		self.A=Abstractions()
		self.environment_data=E(e_args)





	def create_data_array(self,s,a):

  		locations = Regions.region_modded
		
		reward_list=[]
		for i in range(27):
			if i<25:
				reward_list.append(int(s.get_region_score((Regions.region_modded[i][0]-Regions.region_size,Regions.region_modded[i][0]+Regions.region_size),(Regions.region_modded[i][1]-Regions.region_size,Regions.region_modded[i][1]+Regions.region_size)))/(math.pow(10,a.work_load[i])+1))

				#print s.get_region_score((Regions.region_modded[i][0]-Regions.region_size,Regions.region_modded[i][0]+Regions.region_size),(Regions.region_modded[i][1]-Regions.region_size,Regions.region_modded[i][1]+Regions.region_size))/float(a.work_load[i]+1.),i
			else:
				reward_list.append(.1)

		locations[-1]=[a.x,a.y]
		#print len(locations)

  		demands =  []
		start_times=[]
		for i in range(len(locations)):
			demands.append(1)
			start_times.append(0)

		demands[-1]=0

  		data = [locations, demands, start_times, reward_list]


		#print len(demands), len(start_times)
  		return data


	def step(self,s,a):

		# Create the data.
		data = self.create_data_array(s,a)
		locations = data[0]
		demands = data[1]
		start_times = data[2]
		reward_list = data[3]

		num_locations = len(locations)
		depot = len(locations)-1
		end = len(locations)-2
		num_vehicles = 1
		search_time_limit = 400000

		# Create routing model.
		if num_locations > 15:

			# The number of nodes of the VRP is num_locations.
			# Nodes are indexed from 0 to num_locations - 1. By default the start of
			# a route is node 0.
			routing = pywrapcp.RoutingModel(num_locations, num_vehicles, [depot],[end])
			search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()

			# Setting first solution heuristic: the
			# method for finding a first solution to the problem.
			search_parameters.first_solution_strategy = (
			routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

			# The 'PATH_CHEAPEST_ARC' method does the following:
			# Starting from a route "start" node, connect it to the node which produces the
			# cheapest route segment, then extend the route by iterating on the last
			# node added to the route.

			# Put callbacks to the distance function and travel time functions here.

			dist_between_locations = CreateDistanceCallback(locations,reward_list)
			dist_callback = dist_between_locations.DiscountedDistance

			routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
			demands_at_locations = CreateDemandCallback(demands)
			demands_callback = demands_at_locations.Demand

			# Adding capacity dimension constraints.
			#VehicleCapacity = 100;
			#NullCapacitySlack = 0;
			fix_start_cumul_to_zero = True
			#capacity = "Capacity"

			#routing.AddDimension(demands_callback, NullCapacitySlack, VehicleCapacity,
			#                      fix_start_cumul_to_zero, capacity)

			# Adding time dimension constraints.
			time_per_demand_unit = 300
			horizon = 24 * 3600
			time = "Time"
			tw_duration = 5 * 3600000
			speed = 1000

			service_times = CreateServiceTimeCallback(demands, time_per_demand_unit)
			service_time_callback = service_times.ServiceTime

			total_times = CreateTotalTimeCallback(service_time_callback, dist_callback, speed)
			total_time_callback = total_times.TotalTime

			# Add a dimension for time-window constraints and limits on the start times and end times.

			routing.AddDimension(total_time_callback,  # total time function callback
					 0,
					 horizon,
					 fix_start_cumul_to_zero,
					 time)


			# Add limit on size of the time windows.
			time_dimension = routing.GetDimensionOrDie(time)



			for order in range(0, routing.Size()):
			    if not routing.IsStart(order):
				start = start_times[order]
				time_dimension.CumulVar(order).SetRange(start,
				                                        start + tw_duration)
			    elif IsRefuelNode(order):
				# The refuling nodes can be visited any time.
				time_dimension.CumulVar(order).SetRange(0, 24 * 3600)

			# Adding fuel dimension. This dimension consumes a quantity equal to
			# the distance traveled. Only refuel nodes can make the quantity of
			# dimension increase by letting slack variable replenish the fuel.

			#fuel_capacity = dist_between_locations.MaxDistance()
			fuel_capacity = int(a.battery)
			negdist_callback = dist_between_locations.NegDistance

			routing.AddDimension(negdist_callback,  # negative dist callback
				             fuel_capacity,
				             fuel_capacity,
				             False, # fix_start_cumul_to_zero
				             "Fuel")
			# Only let slack free for refueling nodes.
			fuel_dimension = routing.GetDimensionOrDie("Fuel")

			for order in range(0, routing.Size()):
			    if (not IsRefuelNode(order) or routing.IsStart(order)):
				fuel_dimension.SlackVar(order).SetValue(0)
			    # Don't add disjunctions to start nodes.
			    if not routing.IsStart(order) and order !=25:
				# Allow the refuling nodes to be skipped with no penalty
				if IsRefuelNode(order):
				    routing.AddDisjunction([order], 0)
				else:
				    routing.AddDisjunction([order], 500000)

			    # Needed to instantiate fuel quantity at each node.
			    routing.AddVariableMinimizedByFinalizer(fuel_dimension.CumulVar(order))
			print fuel_capacity

			# Solve displays a solution if any.
			assignment = routing.SolveWithParameters(search_parameters)
			if assignment:
				data = self.create_data_array(s,a)
				locations = data[0]
				demands = data[1]
				start_times = data[2]
				size = len(locations)
				# Solution cost.
				print ("Total distance of all routes: " , str(assignment.ObjectiveValue()))
				# Inspect solution.
				#capacity_dimension = routing.GetDimensionOrDie(capacity);
				time_dimension = routing.GetDimensionOrDie(time);

				for vehicle_nbr in xrange(num_vehicles):
					index = routing.Start(vehicle_nbr)
					plan_output = 'Route:'.format(vehicle_nbr)

					while not routing.IsEnd(index):
					    node_index = routing.IndexToNode(index)
					 #   load_var = capacity_dimension.CumulVar(index)
					    time_var = time_dimension.CumulVar(index)
					    fuel_var = fuel_dimension.CumulVar(index)

					    #print(assignment.Value(fuel_transit_var))
					    plan_output += \
						    " {node_index} ->".format(
							node_index=node_index)
					#		load=assignment.Value(load_var),
					#		tmin=str(assignment.Min(time_var)),
					#		tmax=str(assignment.Max(time_var)),
					#		fuel=assignment.Value(fuel_var),
					#		fn=IsRefuelNode(node_index))
					    index = assignment.Value(routing.NextVar(index))

					node_index = routing.IndexToNode(index)
					#load_var = capacity_dimension.CumulVar(index)
					time_var = time_dimension.CumulVar(index)
					fuel_var = fuel_dimension.CumulVar(index)
					plan_output += \
						  " {node_index}".format(
						      node_index=node_index)
					#	      load=assignment.Value(load_var),
					#	      tmin=str(assignment.Min(time_var)),
					#	      tmax=str(assignment.Max(time_var)),
					#	      fuel=assignment.Value(fuel_var))
					print(plan_output)
					print("\n")

			else:
				print ('No solution found.')
				return 25
		else:
			print ('Specify an instance greater than 0.')
		print xrange(num_vehicles)
		print routing.IndexToNode(assignment.Value(routing.NextVar(routing.Start(0))))
		return routing.IndexToNode(assignment.Value(routing.NextVar(routing.Start(0))))



