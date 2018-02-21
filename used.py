
# -*- coding: utf-8 -*-

from __future__ import division

from scipy import sin, cos, pi

import pygame
from pygame.locals import *

WINDOWWIDTH = 640
WINDOWWHEIGHT = 480
middlehight = WINDOWWIDTH/2
middlewheight = WINDOWWHEIGHT/2
#
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LBLUE = (240,240,255)

TILECOLOR = GREEN
TEXTCOLOR = WHITE
BACK = LBLUE

def makeText(text, color, bgcolor, top, left, size = 32):
	BASICFONT = pygame.font.Font("bkant.ttf", size)
	#Create the Surface and make Rect objects for some text.
	textSurf = BASICFONT.render(text, True, color, bgcolor)
	textRect = textSurf.get_rect()
	textRect.topleft = (top, left)
	return (textSurf, textRect)
	
def makeSquarre(color, middlehight = WINDOWWIDTH/2, middlewheight = WINDOWWHEIGHT/2, size = 32):
	BASICFONT_SQUARRE = pygame.font.Font("bkant.ttf", size)
	squarreSurf = BASICFONT_SQUARRE.render('     ', True, color, color)
	squarreRect = squarreSurf.get_rect()
	squarreRect.center = (middlehight, middlewheight)
	return (squarreSurf, squarreRect)

def makeBarre(nbpoints, color, middlehight = WINDOWWIDTH/2, middlewheight = WINDOWWHEIGHT/2, size = 32):
	barreSurf, barreRect = [], []
	for point in range(nbpoints):
		newPointSurf, newPointRect = makeSquarre(color, middlehight = middlehight+point*size+nbpoints, middlewheight = middlewheight, size = size)
		barreSurf.append(newPointSurf)
		barreRect.append(newPointRect)
	return (barreSurf, barreRect)

def makeCircle(color, middlehight = WINDOWWIDTH/2, middlewheight = WINDOWWHEIGHT/2, size = 32, rayon = 1, anglemin = 0, anglemax = 2*pi):
	circleSurf, circleRect = [], []
	for point in range(int(anglemin//(pi/180)),int(anglemax//(pi/180))+1):
		newPointSurf, newPointRect = makeSquarre(color, middlehight = middlehight+rayon*cos(point*pi/180), middlewheight = middlewheight + rayon*sin(point*pi/180), size = size)
		circleSurf.append(newPointSurf)
		circleRect.append(newPointRect)
	return (circleSurf, circleRect)

def BlitListImage(fenetre, liste):
	for i in liste:
		fenetre.blit(i.surf, (i.rect))

class Image():
	def fblit(self, fenetre, surf = None, rect = None):
		if surf == None and self.surf != None:
			surf=self.surf
		if rect == None and self.rect != None:
			rect=self.rect

		if surf and rect:
			fenetre.blit(surf, rect)

class Point(Image):
	def __init__(self, color = (0,0,0), x = 0, y = 0, size = 2):
		self.color = color
		self.size = size
		self.contour = False
		self.surf, self.rect = makeSquarre(color, size = self.size-1*self.contour, middlehight = x, middlewheight = y )
		if self.contour:
			self.surf_contour, self.rect_contour = makeSquarre((0,0,0), size = self.size, middlehight = x, middlewheight = y )
		self.x = x
		self.y = y

	def fblit(self, fenetre, surf = None, rect = None):
		if surf == None and self.surf != None:
			surf=self.surf
		if rect == None and self.rect != None:
			rect=self.rect

		if surf and rect:
			if self.contour:
				fenetre.blit(self.surf_contour, self.rect_contour)
			fenetre.blit(surf, rect)

class Arc(Image):
	def __init__(self, rayon = 1):
		self.color = (100,100,100)
		self.rayon = rayon
		self.points_surf, self.points_rect = makeCircle(color=self.color, size = 2, rayon = self.rayon)

	def fblit(self, fenetre, anglemax, anglemin):
		for point in range(int(anglemin//(pi/(180))), int((anglemax-anglemin)//(pi/(180))) + int(anglemin//(pi/(180)))):
			fenetre.blit(self.points_surf[point%360], self.points_rect[point%360])

class Barre(Image):
	def __init__(self, angle = 0):
		self.angle = angle
		self.longueur = 40
		self.color = (100,100,100)
		self.points_surf, self.points_rect = makeBarre(self.longueur, color=self.color, size = 2)
		self.lock = False
		for point in range(self.longueur):
			self.points_rect[point].center = (WINDOWWIDTH/2 + point*cos(self.angle), WINDOWWHEIGHT/2 + point*sin(self.angle))

	def rot(self, speed = 1, anglemax = None, anglemin = None):
		if not self.lock:
			if anglemax != None:
				if anglemax - 2*pi <= self.angle + speed*pi/180 <= anglemax:
					self.angle+=speed*pi/180
					for point in range(self.longueur):
						self.points_rect[point].center = (WINDOWWIDTH/2 + point*cos(self.angle), WINDOWWHEIGHT/2 + point*sin(self.angle))
			elif anglemin != None:
				if anglemin <= self.angle + speed*pi/180 <= anglemin + 2*pi:
					self.angle+=speed*pi/180
					for point in range(self.longueur):
						self.points_rect[point].center = (WINDOWWIDTH/2 + point*cos(self.angle), WINDOWWHEIGHT/2 + point*sin(self.angle))

	def fblit(self, fenetre):
		for point in range(self.longueur):
			fenetre.blit(self.points_surf[point], self.points_rect[point])

