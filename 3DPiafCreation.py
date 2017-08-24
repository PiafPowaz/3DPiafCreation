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
GREEN = (0, 204, 0)
BLUE =  (0, 0, 204)
BLUE2 = (0, 0, 180)
BLUE3 = (0, 0, 150)

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

def main():
	pygame.init()

	#Ouverture de la fen�tre Pygame
	fenetre = pygame.display.set_mode((WINDOWWIDTH, WINDOWWHEIGHT), RESIZABLE)

	TILECOLOR = GREEN
	TEXTCOLOR = WHITE

	BASICFONT = pygame.font.Font("bkant.ttf", 32)

	QUIT_SURF, QUIT_RECT = makeText('QUIT', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWWHEIGHT - 90)
	TEXT_SURF = BASICFONT.render('x', True, TEXTCOLOR)
	TEXT_RECT = TEXT_SURF.get_rect()
	TEXT_RECT.center = (110, 15)

	black_surf, black_rect = makeSquarre(BLACK, size = WINDOWWIDTH*3)

	ob = Objet3D()
	ob.contour_axe(axe = 'x', image = imagex)
	ob.contour_axe(axe = 'y', image = imagey)
	ob.contour_axe(axe = 'z', image = imagez)
	#for point in ob.contour:
	#	print([point.x, point.y, point.z])
	#print(len(ob.contour))
	cam = Camera() 

	pygame.key.set_repeat(400, 30)
	#BOUCLE INFINIE
	continuer = 1
	press = False
	r = v = b = 0
	timeactu = sequence_actu = 0
	list_points = []
	for point in ob.contourx:
		list_points.append(Point((0,0,255), angle = 0, x = point[0]*10+ middlehight, y = point[1]*10 + middlewheight, size = 8))
	while continuer:
		for event in pygame.event.get():    #Attente des �v�nements
			if event.type == QUIT:
				continuer = 0
			if event.type == MOUSEBUTTONUP and event.button == 3 and event.pos[1] < 100:
				print ("Zone dangereuse")
			if event.type == MOUSEBUTTONDOWN:
				if QUIT_RECT.collidepoint(event.pos):
					continuer = 0
			if event.type == KEYDOWN:
				key = pygame.key.get_pressed()  #checking pressed keys
				if key[pygame.K_x]:
					axe = 'x'
					press = True
					cam.phi = 0
					cam.theta = pi/2
				if key[pygame.K_y]:
					axe = 'y'
					press = True
					cam.phi = pi/2
					cam.theta = pi/2
				if key[pygame.K_w]:
					axe = 'z'
					press = True
					cam.phi = pi/2
					cam.theta = 0
				if key[pygame.K_RIGHT]:
					axe = 'None'
					cam.Rot(dphi=pi/180)
					press = True
				if key[pygame.K_LEFT]:
					axe = 'None'
					cam.Rot(dphi=-pi/180)
					press = True
				if key[pygame.K_UP]:
					axe = 'None'
					cam.Rot(dtheta=-pi/180)
					press = True
				if key[pygame.K_DOWN]:
					axe = 'None'
					cam.Rot(dtheta=pi/180)
					press = True
				if press:
					TEXT_SURF = BASICFONT.render(axe, True, TEXTCOLOR)
					press = False
					list_points = []
					for point in ob.contour:
						posx = point.x*sin(cam.phi) + point.y*cos(cam.phi)
						posy = point.y*cos(cam.theta) + point.z*sin(cam.theta)
						list_points.append(Point((0,0,255), angle = 0, x = posx*10+ middlehight, y = posy*10 + middlewheight, size = 8))
		#Re-collage
		fenetre.blit(black_surf, black_rect)
		fenetre.blit(TEXT_SURF, (TEXT_RECT))
		fenetre.blit(QUIT_SURF, (QUIT_RECT))
		for point in list_points:
			point.fblit(fenetre)
		#Rafraichissement
		pygame.display.flip()
	pygame.quit()

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
	def __init__(self, color = (0,0,0), angle = 0, x = 0, y = 0, size = 2):
		self.color = color
		self.size = size
		self.surf, self.rect = makeSquarre(color, size = self.size, middlehight = x, middlewheight = y )
		self.time_number = 0
		self.angle = angle
		self.speed = 3
		self.x = x
		self.y = y

	def actTime(self):
		self.time_number += 1
		self.rect.center = (WINDOWWIDTH/2 + self.speed*cos(self.angle)*self.time_number, WINDOWWHEIGHT/2 + self.speed*sin(self.angle)*self.time_number)

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

imagex = [
		[1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1],
		[0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0]]
imagey = [
		[0,0,0,0,1,1,1],
		[0,0,0,0,1,1,0],
		[0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0]]
imagez = [
		[0,0,0,0,1,1,1],
		[0,0,0,0,1,1,1],
		[0,0,0,0,1,1,1],
		[0,0,0,0,1,0,1],
		[0,0,0,0,1,1,1],
		[0,0,0,0,1,1,1],
		[0,0,0,0,1,1,1]]

class Objet3D():
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z
		self.contour = []
		self.contourx, self.contoury, self.contourz = None, None, None

	def contour_axe(self, axe = 'x', image=None):
		if image != None:
			coord = []
			refresh = 0
			contour_trans = []
			if self.contourx != None and axe != 'x':
				contour_trans = self.contourx[:]
			if self.contoury != None and axe != 'x':
				contour_trans = self.contoury[:]
			if self.contourz != None and axe != 'z':
				contour_trans = self.contourz[:]
			for y in range(len(image)):
				for x in range(len(image[0])):
					if image[y][x] == 1:
						coord.append([x,y])
			#print(len(contour_trans))
			#for point in self.contour:
			#	print([point.x, point.y, point.z])
			if axe == 'x':
				self.contourx = coord
				if self.contoury != None and self.contourz != None:
					contour_trans_ob = self.contour
					self.contour = []
					for ob in contour_trans_ob:
						for y, z in coord:
							if y == ob.y and z == ob.z:
								self.contour.append(ob)
				else:
					for point in coord:
						x = None
						y = point[0]
						z = point[1]
						found = False
						for ob in contour_trans:
							if z == ob[1] and self.contoury != None:
								found = True
								refresh += 1
								if refresh == 1:
									self.contour = []
								self.contour.append(Objet3D(x = ob[0], y = y, z = z))
							elif y == ob[1] and self.contourz != None:
								found = True
								refresh += 1
								if refresh == 1:
									self.contour = []
								self.contour.append(Objet3D(x = ob[0], y = y, z = z))
							elif ob[1] == y and ob[1] == z and self.contoury != None and self.contourz != None:
								found = True
						if not found:
							self.contour.append(Objet3D(x = x, y = y, z = z))
			if axe == 'y':
				self.contoury = coord
				if self.contourx != None and self.contourz != None:
					contour_trans_ob = self.contour
					self.contour = []
					for ob in contour_trans_ob:
						for x, z in coord:
							if x == ob.x and z == ob.z:
								self.contour.append(ob)
				else:
					for point in coord:
						x = point[0]
						y = None
						z = point[1]
						found = False
						for ob in contour_trans:
							if z == ob[1] and self.contourx != None:
								found = True
								refresh += 1
								if refresh == 1:
									self.contour = []
								self.contour.append(Objet3D(x = x, y = ob[0], z = z))
							elif x == ob[0] and self.contourz != None:
								found = True
								refresh += 1
								if refresh == 1:
									self.contour = []
								self.contour.append(Objet3D(x = x, y = ob[1], z = z))
							elif ob[0] == x and ob[1] == z and self.contourx != None and self.contourz != None:
								found = True
						if not found:
							self.contour.append(Objet3D(x = x, y = y, z = z))
			if axe == 'z':
				self.contourz = coord
				if self.contourx != None and self.contoury != None:
					contour_trans_ob = self.contour
					self.contour = []
					for ob in contour_trans_ob:
						for x, y in coord:
							if x == ob.x and y == ob.y:
								self.contour.append(ob)
				else:
					for point in coord:
						x = point[0]
						y = point[1]
						z = None
						found = False
						for ob in contour_trans:
							if y == ob[0] and self.contourx != None:
								found = True
								refresh += 1
								if refresh == 1:
									self.contour = []
								self.contour.append(Objet3D(x = x, y = y, z = ob[1]))
							elif x == ob[0] and self.contoury != None:
								found = True
								refresh += 1
								if refresh == 1:
									self.contour = []
								self.contour.append(Objet3D(x = x, y = y, z = ob[1]))
							elif ob[0] == x and ob[0] == y and self.contourx != None and self.contoury != None:
								found = True
						if not found:
							self.contour.append(Objet3D(x = x, y = y, z = z))

class Camera:
	def __init__(self, phi = 0, theta = pi/2):
		self.phi = phi
		self.theta = theta

	def Rot(self, dphi = 0, dtheta = 0):
		self.phi += dphi
		self.theta += dtheta

	def RotAxe(self, axe = 'x'):
		self.phi = 0
		self.theta = detheta
		self.x = self.x*cos(self.phi)
		self.y = self.y*sin(self.phi)
		self.z = self.z*cos(self.theta)

main()
