#!/usr/bin/env python

from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()
from OpenGL.GL import *

from OpenGL.GLUT import *
from OpenGL.GLU import *


from PIL import Image
import numpy as numpy

import time
try:
    from PIL.Image import open
except ImportError, err:
    from Image import open

import math

window = 0                                             # glut window number
width, height = 500, 400                               # window size


class TestContext( BaseContext ):
    """NeHe 6 Demo"""
    initialPosition = (0,0,0) # set initial camera position, tutorial does the re-positioning

    def OnInit( self ):
        """Load the image on initial load of the application"""
        self.imageID = [self.TexFromPNG ("/home/aaron/mines_mdp_project/drawing/object.png")]

	#self.imageID = self.loadImage()

    def TexFromPNG(self, filename):
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
        glTexImage2D(GL_TEXTURE_2D, 0, 3, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        return texture

    def Render(self, mode):
        """Render scene geometry"""
        BaseContext.Render( self, mode )
        glDisable( GL_LIGHTING) # context lights by default


        glMatrixMode(GL_PROJECTION)

	
        self.setupTexture()
        self.draw(0,0,.1,.1,0,.5,0,-.1)

    def setupTexture( self ):
        """Render-time texture environment setup"""
        glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

        glBindTexture(GL_TEXTURE_2D, self.imageID[0])

    
    def draw(self, x, y, width, height, graphics_index, alpha, orientation, depth):
    	    glColor4f(1, 1, 1,alpha)

            orientation_=360/8*(orientation+4)*3.14/180

            p1x=-width*math.cos(orientation_)-(-height)*math.sin(orientation_)
            p1y=width*math.sin(orientation_)+(-height)*math.cos(orientation_)
            p2x=width*math.cos(orientation_)-(-height)*math.sin(orientation_)
            p2y=width*math.sin(orientation_)+(-height)*math.cos(orientation_)
            p3x=width*math.cos(orientation_)-(height)*math.sin(orientation_)
            p3y=width*math.sin(orientation_)+(height)*math.cos(orientation_)
            p4x=-width*math.cos(orientation_)-(height)*math.sin(orientation_)
            p4y=-width*math.sin(orientation_)+(height)*math.cos(orientation_)


            glBegin(GL_QUADS)


            glVertex3f(x+p1x, y+p1y, -1.0)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(x+p2x, y+p2y, -1.0)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(x+p3x, y+p3y, -1.0)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(x+p4x, y+p4y, -1.0)
           
            glTexCoord2f(0.0, 0.0)
            glVertex3f(x+p1x, y+p1y, depth)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(x+p2x, y+p2y, depth)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(x+p3x, y+p3y, depth)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(x+p4x, y+p4y, depth)


            

            
            #glDisable(GL_BLEND)
            glEnd()
    	

    def OnIdle( self, ):
        """Request refresh of the context whenever idle"""
        self.triggerRedraw(1)
        return 1
if __name__ == "__main__":
    TestContext.ContextMainLoop()
