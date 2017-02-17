#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
from PIL import Image
import numpy as numpy

import math

window = 0                                             # glut window number
width, height = 1200, 1200                               # window size

import os
import sys




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



def setupTexture(graphics_index):
	glEnable(GL_BLEND)
	glLoadIdentity()                                   # reset position
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_TEXTURE_2D)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	#glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
	glBindTexture(GL_TEXTURE_2D, images[graphics_index])


                                            

def refresh2d(width, height):
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
	glMatrixMode (GL_MODELVIEW)
	#glLoadIdentity()

def clear():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen


	gluPerspective(90,1,0,3)
	gluLookAt(0, 0, 1.01,  0, 0, 0, 0, 1, 0)

def begin_basic():
	glColor3f(.3, .3, 1.)
        glDisable( GL_CULL_FACE)
        glDisable( GL_LIGHTING)
        glLoadIdentity()
	glDisable(GL_BLEND)
	glDisable(GL_TEXTURE_2D)

	
def draw_basic(x, y, width, height, depth):     

        glBegin(GL_QUADS);

        glVertex3f(x+(-width), y+(height),  depth);
        glVertex3f( x+(width), y+(height),  depth);
        glVertex3f(x+(width),  y+(-height),  depth);
        glVertex3f( x+(-width),  y+(-height),  depth);

	glEnd()


def draw(x, y, width, height, graphics_index, alpha, orientation, depth, canvas_size):     
	setupTexture(graphics_index)
	#set_size(canvas_size)
	glColor4f(1., 1., 1.,alpha)
	orientation_=360./8.*(orientation+4.)*3.14/180.

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




def end_draw():
	glutSwapBuffers() 

def set_size(size):
	glTranslatef( 0, 0, 1);



#glDisable(GL_BLEND)
	


# initialization
glutInit()                                             # initialize glut
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)                      # set window size
glutInitWindowPosition(10, 0)                           # set window position



window = glutCreateWindow("mine swarm")              # create window with title
#glutDisplayFunc(draw)                                  # set draw function callback
#glutIdleFunc(draw)                                     # draw all the time
#glutMainLoop() 



images =  [TexFromPNG (os.path.dirname(os.path.abspath(__file__))
+ "/object.png")]
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__))
+ "/uuv.png"))
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__))
+ "/arrow.png"))


