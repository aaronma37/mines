#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
from PIL import Image
import numpy as numpy

import math
import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid
#from agent_classes import Agent


import pygame
from pygame.locals import *



window = 0                                             # glut window number
width, height = 1600, 1200                               # window size
AR=1600./1200.

import os
import sys

agent_dict={}
RESET=0
HIGHLIGHT=1

objective_colors={}
objective_colors["mine"]=(1, 0, 0)
objective_colors["service"]=(.5, .5, .5)
objective_colors["service2"]=(0, 1, .5)
objective_colors["obj3"]=(.5, 1, .5)
objective_colors["obj4"]=(1, 1, .5)
objective_colors["obj5"]=(0, .5, .5)

class gui_data:
	def __init__(self):
		self.hl=None

class abstract_button:
	def __init__(self, action_index, graphics_index):
		self.action_index=action_index
		self.graphics_index=graphics_index

	def check_click(self,xx,yy,x,y,h,w,k,gui_data,main):
		if math.fabs(y-yy)<h and math.fabs(x-xx)<w:
			action(self.action_index,k,gui_data,main)	


class button:
	def __init__(self, action_index, graphics_index,x,y,w,h):
		self.action_index=action_index
		self.graphics_index=graphics_index
		self.x=x
		self.y=y
		self.w=w
		self.h=h

	def check_click(self,x,y,s,gui_data,main):
		if math.fabs(y-self.y)<self.h and math.fabs(x-self.x)<self.w:
			action(self.action_index,s,gui_data,main)


def action(action_index,s,gd,main):
	if action_index == RESET:
		main(True)
		s.reset()
		time.sleep(.05)
	elif action_index==HIGHLIGHT:
		gd.hl=s
		print gd.hl, "hl"
buttons  = []

buttons.append(button(RESET,0,0,-1.1,.1,.1))

a_buttons = []
a_buttons.append(abstract_button(HIGHLIGHT,0))


SCREEN_SIZE = (width, height)

def loadImage(image):
    textureSurface = pygame.image.load(image)
 
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
 
    width = textureSurface.get_width()
    height = textureSurface.get_height()
 
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
        GL_UNSIGNED_BYTE, textureData)
 
    return texture#, width, height

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
#glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
#glutInitWindowSize(width, height)                      # set window size
#glutInitWindowPosition(10, 0)                           # set window position

#window = glutCreateWindow("mine swarm")              # create window with title


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
images =  [TexFromPNG (os.path.dirname(os.path.abspath(__file__)) + "/object.png")]
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__)) + "/uuv.png"))
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__)) + "/arrow.png"))
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__)) + "/uuv1.png"))
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__)) + "/reset.png"))
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__)) + "/green_box.png"))
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__)) + "/yellow_box.png"))
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__)) + "/mine.png"))
#images =  [loadImage (os.path.dirname(os.path.abspath(__file__)) + "/object.png")]
#images.append(loadImage (os.path.dirname(os.path.abspath(__file__)) + "/uuv.png"))
#images.append(loadImage (os.path.dirname(os.path.abspath(__file__)) + "/arrow.png"))
#images.append(loadImage (os.path.dirname(os.path.abspath(__file__)) + "/uuv1.png"))
#images.append(loadImage (os.path.dirname(os.path.abspath(__file__)) + "/reset.png"))


#clock = pygame.time.Clock()    

#init()
#time.sleep(1)


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
	#pygame.font.init() # you have to call this at the start, 

	# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
	#myfont = pygame.font.SysFont("monospace", 15)

	# render text
	#textsurface = myfont.render('Sometext', False, (0,0,0))

	#screen.blit(textsurface, (100, 100))

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
			glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(character));
	glPopMatrix();
	glMatrixMode(GL_PROJECTION);
	# For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
	# glPopMatrix();
	glLoadMatrixd( matrix ) # should have un-decorated alias for this...

	glMatrixMode(GL_MODELVIEW);


def end_draw():
	glutSwapBuffers() 

def get_norm_size(s):
	return 1./s

def get_sqr_loc(x,s):
	return 2.*x/s-1.


def draw_all(complete_environment,agent_dict,gui_data,step_num):

	clear()
	begin_basic()	
	
	#draw_basic(0,0,1,1,-.1)
	
	glColor3f(1, 0, 0)

	map_size=100
		

	for o in complete_environment.objective_list:
		glColor3f(objective_colors[o.frame_id][0], objective_colors[o.frame_id][1], objective_colors[o.frame_id][2])
		for so in o.sub_objectives:
			draw_basic(get_sqr_loc(so.x,map_size),get_sqr_loc(so.y,map_size),1./map_size,1./map_size,-.1)

		
	if gui_data.hl is not None:
		glColor3f(.3, .3, 0)
		draw_basic(get_sqr_loc(agent_dict[gui_data.hl].x,map_size),get_sqr_loc(agent_dict[gui_data.hl].y,map_size),get_norm_size(map_size)*2,get_norm_size(map_size)*2,-.1)

	#setupTexture(5)
	#draw(get_sqr_loc(map_size/2,map_size), get_sqr_loc(map_size/2,map_size), get_norm_size(map_size)*20,get_norm_size(map_size)*20,1, 1,0,-.1,map_size/10.)

	## AGENTS

	setupTexture(1)

	for k,a in agent_dict.items():
		draw(get_sqr_loc(a.x,map_size), get_sqr_loc(a.y,map_size), get_norm_size(map_size),get_norm_size(map_size),1, 1,0,-.1,map_size/10.)



	## AGENTS STATUS
	setupTexture(3)
	count=0
	for k,a in agent_dict.items():
		draw(1.2, 1.-count/4., .1,.1,1, 1,3,-.1,map_size/10.)
		count+=1

	count=0
	for k,a in agent_dict.items():
		draw_text(1.2, 1.1-count/4.,"Agent: " + str(k))
		draw_text(1.2,-.025+ 1.1-count/4.,"Action: " + str(a.my_action))
		draw_text(1.2,-.05+ 1.1-count/4.,"State: " + str(a.current_state))
		draw_text(1.2,-.075+ 1.1-count/4.,"State: " + str(a.my_action_index))
		#draw_text(1.2,-.025+ 1.1-count/4.,"Battery: " + str(a.battery))
		#draw_text(1.2,-.05+ 1.1-count/4.,"Region: " + str(a.trajectory.region_trajectory))
		#draw_text(1.2,-.075+ 1.1-count/4.,"State: " + a.current_state)
		#draw_text(1.2,-.1+ 1.1-count/4.,"Action: " + str(a.trajectory.action_trajectory))
		count+=1


	setupTexture(4)

	for b in buttons:
		draw(b.x, b.y, b.w,b.h,1, 1,0,-.1,map_size/10.)
	


	draw_text(0, 1.1,"step: " + str(step_num))


	setupTexture(4)


                    

def render_once(complete_environment,agent_dict,gui_data,main,step_num):
	       # glEnable(GL_DEPTH_TEST)
	    
	       # glShadeModel(GL_FLAT)
	       # glClearColor(1.0, 1.0, 1.0, 0.0)

	       # glEnable(GL_COLOR_MATERIAL)
	    
	      #  glEnable(GL_LIGHTING)
	       # glEnable(GL_LIGHT0)        
	      #  glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))    

		for event in pygame.event.get():
		    if event.type == QUIT:
		        return
		    if event.type == KEYUP and event.key == K_ESCAPE:
		        return    
		
		draw_all(complete_environment,agent_dict,gui_data,step_num)

		pygame.display.flip()

		pressed = pygame.mouse.get_pressed()
		x,y = pygame.mouse.get_pos()
		x = (x-550.)/500.
		y =-(y-600.)/500.

		if pressed[0]:
			for b in buttons:
				b.check_click(x,y,complete_environment,gui_data,main)
			count=0
			for k,a in agent_dict.items():
				a_buttons[0].check_click(1.2,1.-count/4.,x,y,.1,.1,k,gui_data,main)
				count+=1


		#550, 600 is middle
		# x pos is right y pos is down
		# 50,1100 is (-1,-1)None


		#(x-550)/500, -(y-600)/500
    #clock = pygame.time.Clock()    
    
    #glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))    
    #glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))

    # This object renders the 'map'
    #map = Map()        

    # Camera transform matrix
    #camera_matrix = Matrix44()
    #camera_matrix.translate = (10.0, .6, 10.0)

    # Initialize speeds and directions
    #rotation_direction = Vector3()
    #rotation_speed = radians(90.0)
    #movement_direction = Vector3()
    #movement_speed = 5.0    

    #while True:
        

















		



