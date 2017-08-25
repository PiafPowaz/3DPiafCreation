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

	#Ouverture de la fenêtre Pygame
	fenetre = pygame.display.set_mode((WINDOWWIDTH, WINDOWWHEIGHT), RESIZABLE)

	TILECOLOR = GREEN
	TEXTCOLOR = WHITE

	BASICFONT = pygame.font.Font("bkant.ttf", 32)
	axe = 'x'

	QUIT_SURF, QUIT_RECT = makeText('QUIT', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWWHEIGHT - 90)
	TEXT_SURF = BASICFONT.render(axe, True, TEXTCOLOR)
	TEXT_RECT = TEXT_SURF.get_rect()
	TEXT_RECT.center = (110, 15)

	black_surf, black_rect = makeSquarre(BLACK, size = WINDOWWIDTH*3)

	imagex = []
	imagey = []
	imagez = []
	fx = open("imagex.txt", 'a')
	fx.close()
	with open("imagex.txt", 'r') as fx:
		for line in fx:
			line_list = list(line)
			if line_list.count('\n') != 0:
				line_list.remove('\n')
			imagex.append(line_list)
		if imagex == []:
			imagex = None
	fy = open("imagez.txt", 'a')
	fy.close()
	with open("imagey.txt", 'r') as fy:
		for line in fy:
			line_list = list(line)
			if line_list.count('\n') != 0:
				line_list.remove('\n')
			imagey.append(line_list)
		if imagey == []:
			imagey = None
	fz = open("imagez.txt", 'a')
	fz.close()
	with open("imagez.txt", 'r') as fz:
		for line in fz:
			line_list = list(line)
			if line_list.count('\n') != 0:
				line_list.remove('\n')
			imagez.append(line_list)
		if imagez == []:
			imagez = None
	#print(imagex)
	#print(imagey)
	#print(imagez)
	ob = Objet3D()
	ob.contour_axe(axe = 'x', image = imagex)
	ob.contour_axe(axe = 'y', image = imagey)
	ob.contour_axe(axe = 'z', image = imagez)
	#for point in ob.contour:
	#	print([point.x, point.y, point.z])
	cam = Camera()

	zoom = 10
	dzoom = 1
	zoomx = zoom/WINDOWWIDTH
	zoomy = zoom/WINDOWWHEIGHT

	pygame.key.set_repeat(400, 30)
	#BOUCLE INFINIE
	continuer = 1
	press = False
	r = v = b = 0
	list_points = []
	for point in ob.contourx:
		list_points.append(Point((0,0,255), x = point[0]*zoomx+ middlehight, y = point[1]*zoomy + middlewheight, size = 8))
	while continuer:
		for event in pygame.event.get():    #Attente des événements
			if event.type == QUIT:
				continuer = 0
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
				if key[pygame.K_b]:
					zoom -= dzoom
					if zoom <= 0:
						zoom = 1
					zoomx = zoom/WINDOWWIDTH
					zoomy = zoom/WINDOWWHEIGHT
					press = True
				if key[pygame.K_n]:
					zoom += dzoom
					if zoom >= 480:
						zoom = 480
					zoomx = zoom/WINDOWWIDTH
					zoomy = zoom/WINDOWWHEIGHT
					press = True
				if key[pygame.K_v]:
					dzoom += 1
					if dzoom >= 480:
						dzoom = 480
				if key[pygame.K_c]:
					dzoom -= 1
					if dzoom <= 1:
						dzoom = 1
				if key[pygame.K_o]:
					ob.minimizeContour()
				if key[pygame.K_l]:
					ob.Load()
				if key[pygame.K_s]:
					ob.Save()
				if press:
					TEXT_SURF = BASICFONT.render(axe + str('%d' %zoom), True, TEXTCOLOR)
					press = False
					list_points = []
					for point in ob.contour:
						if point.x != None and point.y != None and point.z != None:
							posx = point.x*sin(cam.phi) + point.y*cos(cam.phi)
							posy = point.y*cos(cam.theta) + point.z*sin(cam.theta)
							list_points.append(Point((0,0,255), x = posx*zoomx+ middlehight, y = posy*zoomy + middlewheight, size = 8))
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
	def __init__(self, color = (0,0,0), x = 0, y = 0, size = 2):
		self.color = color
		self.size = size
		self.surf, self.rect = makeSquarre(color, size = self.size, middlehight = x, middlewheight = y )
		self.x = x
		self.y = y

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

class Objet3D():
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z
		self.contour = []
		self.contour_opti = False
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
					if image[y][x] == '1':
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
		else:
			print(axe, image)

	def Save(self, name = "Save"):
		if not self.contour_opti:
			self.file = open(name + "_ori.3DPiaf", 'w')
		else:
			self.file = open(name + ".3DPiaf", 'w')
		for point in self.contour:
			self.file.write(str('%d' %point.x) + ',' +  str('%d' %point.y) + ',' +str('%d' %point.z) + '\n')
		self.file.close()
		print("File Saved")

	def Load(self, name = "Save"):
		self.file = open(name + ".3DPiaf", 'r')
		self.contour = []
		for line in self.file:
			if len(line.split(',')) >= 2:
				x, y, z = line.split(',')[:3]
				self.contour.append(Objet3D(x = float(x), y = float(y), z = float(z)))
		self.file.close()
		print("File Loaded")

	def minimizeContour(self):
		self.contour_remove = []
		nbpoint = 0
		totnbpoint = len(self.contour)
		chargement = 0
		print(totnbpoint, " initials points")
		for point in self.contour:
			prox = 0
			nbpoint += 1
			if nbpoint//(totnbpoint/100) > chargement:
				chargement = nbpoint//(totnbpoint/100)
				print('Loading : ', chargement, '%')
			if point.x == None or point.y == None or point.z == None:
				self.contour_remove.append(point)
			else:
				for proximal_point in self.contour:
					sens = 1
					if proximal_point.x != None and proximal_point.y != None and proximal_point.z != None:
						for i in range(2):
							if proximal_point.x == point.x and proximal_point.y == point.y and proximal_point.z + sens == point.z:
								prox += 1
							if proximal_point.x == point.x and proximal_point.y + sens == point.y and proximal_point.z == point.z:
								prox += 1
							if proximal_point.x + sens == point.x and proximal_point.y == point.y and proximal_point.z == point.z:
								prox += 1
							sens *= -1
						if prox >= 6:
							self.contour_remove.append(point)
							break
		nbpoint = chargement = 0
		totnbpoint = len(self.contour_remove)
		print('Remove', totnbpoint, 'points')
		for point in self.contour_remove:
			self.contour.remove(point)
			nbpoint += 1
			if nbpoint//(totnbpoint/100) > chargement:
				chargement = nbpoint//(totnbpoint/100)
				print('Remove Loading : ', chargement, '%')
		print('Now', len(self.contour), 'points')
		self.contour_opti = True

class Camera:
	def __init__(self, phi = 0, theta = pi/2):
		self.phi = phi
		self.theta = theta

	def Rot(self, dphi = 0, dtheta = 0):
		self.phi += dphi
		self.theta += dtheta

main()
