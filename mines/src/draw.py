#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
from PIL import Image
import numpy as numpy
from agent_classes import Agent
from environment_classes import get_sqr_loc
from environment_classes import get_norm_size
from environment_classes import Mine_Data

import math
import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid
from agent_classes import Agent
window = 0                                             # glut window number
width, height = 1600, 1200                               # window size
AR=1600./1200.

import os
import sys

map_size=100
s=Mine_Data(map_size)
agent_dict={}





def TexFromPNG(filename):
	img = Image.open(filename)
	img_data = numpy.array(list(img.getdata()), numpy.uint8)

	texture = glGenTextures(1)
	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	glBindTexture(GL_TEXTURE_2D, texture)

	# Texture parameters are part of the texture object, so you need to 
	# specify them only once for a given texture object.
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	#glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
	#glTexImage2D(GL_TEXTURE_2D, 0, 3, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

	#gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, width,height, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
	return texture

glutInit(sys.argv)                                             # initialize glut
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)                      # set window size
glutInitWindowPosition(10, 0)                           # set window position

window = glutCreateWindow("mine swarm")              # create window with title

images =  [TexFromPNG (os.path.dirname(os.path.abspath(__file__)) + "/object.png")]
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__)) + "/uuv.png"))
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__)) + "/arrow.png"))
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__)) + "/uuv1.png"))
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__)) + "/reset.png"))



def setupTexture(graphics_index):
	glEnable(GL_BLEND)
	glLoadIdentity()                                   # reset position
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_TEXTURE_2D)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	#glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
	glBindTexture(GL_TEXTURE_2D, images[graphics_index])
	gluPerspective(90,AR,0,3)
	gluLookAt(.5, 0, 1.1,  .5, 0, 0, 0, 1, 0)



	                               

def clear():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen





def begin_basic():
	glColor3f(.3, .3, 1.)
	glDisable( GL_CULL_FACE)
	glDisable( GL_LIGHTING)
	glLoadIdentity()
	glDisable(GL_BLEND)
	glDisable(GL_TEXTURE_2D)
	gluPerspective(90,AR,0,3)
	gluLookAt(.5, 0, 1.1,  .5, 0, 0, 0, 1, 0)


def draw_basic(x, y, width, height, depth):     

	#x=x/AR
	#y=y/AR
	#width=width/AR
	#height=height/AR

	glBegin(GL_QUADS);

	glVertex3f(x+(-width), y+(height),  depth);
	glVertex3f( x+(width), y+(height),  depth);
	glVertex3f(x+(width),  y+(-height),  depth);
	glVertex3f( x+(-width),  y+(-height),  depth);

	glEnd()

def draw(x, y, width, height, graphics_index, alpha, orientation, depth, canvas_size):     

	#set_size(canvas_size)
	glColor4f(1., 1., 1.,alpha)
	orientation_=360./8.*(orientation+4.)*3.14/180.


	#x=x/AR
	#y=y/AR
	#width=width/AR
	#height=height/AR

	#width = width/canvas_size
	#height= height/canvas_size
	#x=x#/canvas_size
	#y=y#/canvas_size

	px=[1,1,1,1]
	py=[1,1,1,1]

	px[0]=math.cos(orientation_)*(-width)-math.sin(orientation_)*height
	px[1]=math.cos(orientation_)*(width)-math.sin(orientation_)*height
	px[2]=math.cos(orientation_)*(-width)-math.sin(orientation_)*(-height)
	px[3]=math.cos(orientation_)*(width)-math.sin(orientation_)*(-height)

	py[0]=math.sin(orientation_)*(-width)+math.cos(orientation_)*(height)
	py[1]=math.sin(orientation_)*(width)+math.cos(orientation_)*(height)
	py[2]=math.sin(orientation_)*(-width)+math.cos(orientation_)*(-height)
	py[3]=math.sin(orientation_)*(width)+math.cos(orientation_)*(-height)




	glBegin(GL_QUADS);

	glTexCoord2f(0.0, 1.0); glVertex3f(x+px[0], y+py[0],  depth);
	glTexCoord2f(1.0, 1.0); glVertex3f( x+px[1], y+py[1],  depth);
	glTexCoord2f(1.0, 0.0); glVertex3f(x+px[3],  y+py[3],  depth);
	glTexCoord2f(0.0, 0.0); glVertex3f( x+px[2],  y+py[2],  depth);

	glEnd()

def draw_text(x,y,msg):
	glDisable(GL_TEXTURE_2D)

	drawText( msg, int(800+x*800),int(600+y*570), width,height)


def drawText(value, x,y,  windowHeight, windowWidth, step = 18 ):
	"""Draw the given text at given 2D position in window
	"""
	glColor3f(1., 1., 1.)

	glMatrixMode(GL_PROJECTION);
	# For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
	# glPushMatrix()
	matrix = glGetDouble( GL_PROJECTION_MATRIX )

	glLoadIdentity();
	glOrtho(0.0, windowHeight or 32, 0.0, windowWidth or 32, -1.0, 1.0)
	gluPerspective(90,AR,0,3)
	gluLookAt(.5, 0, 1.1,  .5, 0, 0, 0, 1, 0)
	glMatrixMode(GL_MODELVIEW);
	glPushMatrix();
	glLoadIdentity();
	glRasterPos2i(x, y);
	lines = 0
	for character in value:
		if character == '\n':
			glRasterPos2i(x, y-(lines*18))
		else:
			glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character));
	glPopMatrix();
	glMatrixMode(GL_PROJECTION);
	# For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
	# glPopMatrix();
	glLoadMatrixd( matrix ) # should have un-decorated alias for this...

	glMatrixMode(GL_MODELVIEW);


def end_draw():
	glutSwapBuffers() 




def draw_all(s,agent_dict,map_size):
	start=time.time()
	clear()
	begin_basic()	
	for i in range(map_size):
		for j in range(map_size):
			if s.seen[i][j] == 0:
				draw_basic(get_sqr_loc(i,map_size),get_sqr_loc(j,map_size),get_norm_size(map_size),get_norm_size(map_size),-.1)
		
	print time.time()-start
	setupTexture(1)

	for k,a in agent_dict.items():
		draw(get_sqr_loc(a.x,map_size), get_sqr_loc(a.y,map_size), get_norm_size(map_size),get_norm_size(map_size),1, 1,0,-.1,map_size/10.)

	## DRAW STATUS BLOCK
	setupTexture(3)
	count=0
	for k,a in agent_dict.items():
		draw(1.2, .1+count/4., .1,.1,1, 1,3,-.1,map_size/10.)
		count+=1


	setupTexture(4)

	draw(-.1, -1.05, .1,.1,1, 1,0,-.1,map_size/10.)

	count=0
	for k,a in agent_dict.items():
		draw_text(1.2,+.2+count/4.,"Agent: " + str(k))
		draw_text(1.2,-.05+.2+count/4.,"Battery: " + str(a.battery))
		draw_text(1.2,-.1+.2+count/4.,"Action: " + str(a.current_action.index))
		count+=1

	end_draw()



#def start():
#	glutIdleFunc(draw_all)
#	glutMainLoop() 

#def init(s_,agent_dict_,map_size_):
#	map_size=map_size_
#	s=s_
#	agent_dict=agent_dict_

	#glutDisplayFunc(draw)                                  # set draw function callback
#glutIdleFunc(draw)                                     # draw all the time
#glutMainLoop() 



		



