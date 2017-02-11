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
	glTexImage2D(GL_TEXTURE_2D, 0, 3, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
	#gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, width,height, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
	return texture



def setupTexture(graphics_index):
	glEnable(GL_BLEND)
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


def draw(x, y, width, height, graphics_index, alpha, orientation, depth, canvas_size):     
	setupTexture(graphics_index)
	glLoadIdentity()                                   # reset position
	#clear()

	set_size(canvas_size)
	glColor4f(1., 1., 1.,alpha)

	orientation_=360./8.*(orientation+4.)*3.14/180.

	width = width/canvas_size
	height= height/canvas_size
	x=x/canvas_size
	y=y/canvas_size

	p1x=-width*math.cos(orientation_)-(-height)*math.sin(orientation_)
	p1y=width*math.sin(orientation_)+(-height)*math.cos(orientation_)
	p2x=width*math.cos(orientation_)-(-height)*math.sin(orientation_)
	p2y=width*math.sin(orientation_)+(-height)*math.cos(orientation_)
	p3x=width*math.cos(orientation_)-(height)*math.sin(orientation_)
	p3y=width*math.sin(orientation_)+(height)*math.cos(orientation_)
	p4x=-width*math.cos(orientation_)-(height)*math.sin(orientation_)
	p4y=-width*math.sin(orientation_)+(height)*math.cos(orientation_)


	glBegin(GL_QUADS)

#	glTexCoord2f(0.0, 0.0)
#	glVertex3f(x+p1x, y+p1y, -1.0)
#	glTexCoord2f(1.0, 0.0)
#	glVertex3f(x+p2x, y+p2y, -1.0)
#	glTexCoord2f(1.0, 1.0)
#	glVertex3f(x+p3x, y+p3y, -1.0)
#	glTexCoord2f(0.0, 1.0)
#	glVertex3f(x+p4x, y+p4y, -1.0)

	glTexCoord2f(0.0, 0.0)
	glVertex3f(x+p1x, y+p1y, depth)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(x+p2x, y+p2y, depth)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(x+p3x, y+p3y, depth)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(x+p4x, y+p4y, depth)

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

window = glutCreateWindow("noobtuts.com")              # create window with title
#glutDisplayFunc(draw)                                  # set draw function callback
#glutIdleFunc(draw)                                     # draw all the time
#glutMainLoop() 



images =  [TexFromPNG (os.path.dirname(os.path.abspath(__file__))
+ "/object.png")]
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__))
+ "/uuv.png"))
images.append(TexFromPNG (os.path.dirname(os.path.abspath(__file__))
+ "/arrow.png"))


