#!/usr/bin/env python

import numpy as np

def get_transition_x(action_):
	if action_ is 0 or action_ is 3 or action_ is 7:
		return 0
	elif action_ is 1 or action_ is 2 or action_ is 8:
		return 1
	else:
		return -1

def get_transition_y(action_):
	if action_ is 0 or action_ is 1 or action_ is 5:
		return 0
	elif action_ is 2 or action_ is 3 or action_ is 4:
		return 1
	else:
		return -1

def action_to_string(action_):
	if action_ is 1:
		return "Right"
	elif action_ is 2:
		return "Up Right"
	elif action_ is 3:
		return "Up"
	elif action_ is 4:
		return "Up Left"
	elif action_ is 5:
		return "Left"
	elif action_ is 6:
		return "Down Left"
	elif action_ is 7:
		return "Down"
	elif action_ is 8:
		return "Down Right"
	elif action_ is 0:
		return "Stay"



