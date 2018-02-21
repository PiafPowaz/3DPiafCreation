# -*- coding: utf-8 -*-

from __future__ import division

from scipy import *

import pygame
from pygame.locals import *

from used import *
from editor import *

import os
import platform
import argparse

if int(platform.python_version_tuple()[0]) < 3:
	python_version_3 = False
else:
	python_version_3 = True

def main():
	pygame.init()

	#Ouverture de la fenêtre Pygame
	fenetre = pygame.display.set_mode((WINDOWWIDTH, WINDOWWHEIGHT), RESIZABLE)

	BASICFONT = pygame.font.Font("bkant.ttf", 32)
	axe = 'x'

	QUIT_SURF, QUIT_RECT = makeText('QUIT', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWWHEIGHT - 90)
	SAVE_SURF, SAVE_RECT = makeText('SAVE', TEXTCOLOR, TILECOLOR, WINDOWWIDTH/2 - 250, 40)
	LOAD_SURF, LOAD_RECT = makeText('LOAD', TEXTCOLOR, TILECOLOR, WINDOWWIDTH/2 - 150, 40)
	EXPORT_SURF, EXPORT_RECT = makeText('EXPORT', TEXTCOLOR, TILECOLOR, WINDOWWIDTH/2 - 30, 40)
	EDITOR_SURF, EDITOR_RECT = makeText('EDITOR', TEXTCOLOR, TILECOLOR, WINDOWWIDTH/2 + 120, 40)
	TEXT_SURF = BASICFONT.render(axe, True, TEXTCOLOR)
	TEXT_RECT = TEXT_SURF.get_rect()
	TEXT_RECT.center = (110, 15)

	black_surf, black_rect = makeSquarre(BACK, size = WINDOWWIDTH*3)

	imagex = []
	imagey = []
	imagez = []
	"""
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
	fy = open("imagey.txt", 'a')
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
	"""
	#print(imagex)
	#print(imagey)
	#print(imagez)
	ob = Objet3D()
	"""
	ob.contour_axe(axe = 'x', image = imagex)
	ob.contour_axe(axe = 'y', image = imagey)
	ob.contour_axe(axe = 'z', image = imagez)
	"""
	ob.Load()
	#for point in ob.contour:
	#	print([point.x, point.y, point.z])
	cam = Camera()

	zoom = 10
	dzoom = 1
	zoomx = zoom#/WINDOWWIDTH
	zoomy = zoom#/WINDOWWHEIGHT

	pygame.key.set_repeat(400, 30)
	#BOUCLE INFINIE
	continuer = 1
	press = False
	rot_press = False
	r = v = b = 0
	list_points = []
	if ob.contourx != None:
		for point in ob.contourx:
			list_points.append(Point((0,0,255), x = point[0]*zoomx+ middlehight, y = point[1]*zoomy + middlewheight, size = zoom))
	while continuer:
		for event in pygame.event.get():    #Attente des événements
			if event.type == QUIT:
				continuer = 0
			if event.type == MOUSEBUTTONDOWN:
				pygame.mouse.get_rel()
				if QUIT_RECT.collidepoint(event.pos):
					continuer = 0
				elif SAVE_RECT.collidepoint(event.pos):
					if ob.name == "":
						if python_version_3:
							ob.Save(name = input("Save to :"))
						else:
							ob.Save(name = raw_input("Save to :"))
					else:
						ob.Save(name = ob.name)
				elif LOAD_RECT.collidepoint(event.pos):
					if python_version_3:
						ob.Load(name = input("Load :"))
					else:
						ob.Load(name = raw_input("Load :"))
					press = True
				elif EXPORT_RECT.collidepoint(event.pos):
					ExportToObj(ob)
				elif EDITOR_RECT.collidepoint(event.pos):
					[ob.contourx, ob.contoury, ob.contourz] = Editor(fenetre, ob.contourx, ob.contoury, ob.contourz)
					ob.LoadNewContours(imagex = ob.contourx, imagey = ob.contoury, imagez = ob.contourz)
					press = True
				else:
					if event.button == 1:
						rot_press = True
					if event.button == 4:
						zoom += dzoom
						if zoom <= 1:
							zoom = 2
						list_points = List_points(ob, zoom, cam)
					if event.button == 5:
						zoom -= dzoom
						if zoom >= 480:
							zoom = 480
						list_points = List_points(ob, zoom, cam)
			if event.type == MOUSEBUTTONUP:
				if event.button == 1:
					rot_press = False
			if event.type == MOUSEMOTION:
				if rot_press:
					x, y = pygame.mouse.get_rel()
					axe = 'None'
					cam.Rot(dtheta=-y*pi/180, dphi=x*pi/180)
					move = True
					if move:
						TEXT_SURF = BASICFONT.render(axe + str('%d' %zoom), True, TEXTCOLOR)
						list_points = List_points(ob, zoom, cam)
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
					if zoom <= 1:
						zoom = 2
					zoomx = zoom#/WINDOWWIDTH
					zoomy = zoom#/WINDOWWHEIGHT
					press = True
				if key[pygame.K_n]:
					zoom += dzoom
					if zoom >= 480:
						zoom = 480
					zoomx = zoom#/WINDOWWIDTH
					zoomy = zoom#/WINDOWWHEIGHT
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
					if python_version_3:
						ob.Load(name = input("Load :"))
					else:
						ob.Load(name = raw_input("Load :"))
					press = True
				if key[pygame.K_s]:
					if ob.name == "":
						if python_version_3:
							ob.Save(name = input("Save to :"))
						else:
							ob.Save(name = raw_input("Save to :"))
					else:
						ob.Save(name = ob.name)
				if key[pygame.K_i]:
					ConvertImageToBinary()
				if key[pygame.K_e]:
					ExportToObj(ob)
				if key[pygame.K_g]:
					pygame.quit()
					return ConsoleMode(ob)
				if key[pygame.K_TAB]:
					if python_version_3:
						namex = input("Name imagex:")
						namey = input("Name imagey:")
						namez = input("Name imagez:")
					else:
						namex = raw_input("Name imagex:")
						namey = raw_input("Name imagey:")
						namez = raw_input("Name imagez:")
					imagex = []
					imagey = []
					imagez = []
					if namex == 'None':
						imagex = None
					else:
						fx = open(namex, 'a')
						fx.close()
						with open(namex, 'r') as fx:
							for line in fx:
								line_list = list(line)
								if line_list.count('\n') != 0:
									line_list.remove('\n')
								imagex.append(line_list)
							if imagex == []:
								imagex = None
					if namey == 'None':
						imagey = None
					else:
						fy = open(namey, 'a')
						fy.close()
						with open(namey, 'r') as fy:
							for line in fy:
								line_list = list(line)
								if line_list.count('\n') != 0:
									line_list.remove('\n')
								imagey.append(line_list)
							if imagey == []:
								imagey = None
					if namez == 'None':
						imagez = None
					else:
						fz = open(namez, 'a')
						fz.close()
						with open(namez, 'r') as fz:
							for line in fz:
								line_list = list(line)
								if line_list.count('\n') != 0:
									line_list.remove('\n')
								imagez.append(line_list)
							if imagez == []:
								imagez = None
					ob.LoadNewImages(imagex = imagex, imagey = imagey, imagez = imagez)
					press = True
		if press:
			TEXT_SURF = BASICFONT.render(axe + str('%d' %zoom), True, TEXTCOLOR)
			press = False
			list_points = List_points(ob, zoom, cam)
		#Re-collage
		fenetre.blit(black_surf, black_rect)
		for point in list_points:
			point.fblit(fenetre)
		fenetre.blit(TEXT_SURF, TEXT_RECT)
		fenetre.blit(QUIT_SURF, QUIT_RECT)
		fenetre.blit(SAVE_SURF, SAVE_RECT)
		fenetre.blit(LOAD_SURF, LOAD_RECT)
		fenetre.blit(EXPORT_SURF, EXPORT_RECT)
		fenetre.blit(EDITOR_SURF, EDITOR_RECT)
		#Rafraichissement
		pygame.display.flip()
	pygame.quit()

def List_points(ob, zoom, cam):
	zoomx = zoom#/WINDOWWIDTH
	zoomy = zoom#/WINDOWWHEIGHT
	ob.arraie()
	points = empty((len(ob.contour),3))
	for idx,z_list in enumerate(ob.points):
		for idx2, pos in enumerate(z_list):
			points[idx+idx2] = pos
	X = points[:, 0]
	Y = points[:, 1]
	Z = points[:, 2]
	if len(X) == 0 or len(Y) == 0 or len(Z) == 0:
		return []
	xmin = X[0]
	xmax = X[0]
	ymin = Y[0]
	ymax = Y[0]
	zmin = Z[0]
	zmax = Z[0]
	for x in X:
		if xmin > x:
			xmin = x
		if xmax < x:
			xmax = x
	for y in Y:
		if ymin > y:
			ymin = y
		if ymax < y:
			ymax = y
	for z in Z:
		if zmin > z:
			zmin = z
		if zmax < z:
			zmax = z
	x0, y0, z0 = xmax-xmin/2, ymax-ymin/2, zmax-zmin/2
	X -= x0
	Y -= y0
	Z -= z0
	posx = -X*sin(cam.phi) + Y*cos(cam.phi)
	posy = X*cos(cam.theta)*cos(cam.phi) + Y*cos(cam.theta)*sin(cam.phi) - Z*sin(cam.theta)
	posy*=-1
	posx*=-1
	list_points = [0]*len(points)
	for index in range(len(points)):
		list_points[index] = Point((0,0,255), x = posx[index]*zoomx+ middlehight, y = posy[index]*zoomy + middlewheight, size = zoom)
	return list_points

class Objet3D():
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z
		file = open("Last_" + ".3DPiaf", 'a')
		file.close()
		self.contour = []
		self.contour_opti = False
		self.contourx, self.contoury, self.contourz = None, None, None
		self.name = ""

	def contour_axe(self, axe = 'x', image=None, print_point = False):
		if image != None:
			coord = []
			refresh = 0
			contour_trans = []
			if self.contourx != None and axe != 'x':
				contour_trans = self.contourx[:]
			if self.contoury != None and axe != 'y':
				contour_trans = self.contoury[:]
			if self.contourz != None and axe != 'z':
				contour_trans = self.contourz[:]
			top = -1
			left = -1
			for y in range(len(image)):
				if top == -1:
					for x in range(len(image[0])):
						if image[y][x] == '1':
							top = y
							break
			for x in range(len(image[0])):
				if left == -1:
					for y in range(len(image)):
						if image[y][x] == '1':
							left = x
							break
			for y in range(len(image)):
				for x in range(len(image[0])):
					if image[y][x] == '1':
						coord.append([x-left,y-top])
			if len(coord) > 10000:
				print("Too much point ", len(coord))
				#return 1
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
								if print_point:
									print(ob)
								self.contour.append(ob)
				else:
					for point in coord:
						if print_point:
							print(point)
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
								if print_point:
									print(ob)
								self.contour.append(ob)
				else:
					for point in coord:
						if print_point:
							print(point)
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
					i = 0
					for ob in contour_trans_ob:
						for x, y in coord:
							if x == ob.x and y == ob.y:
								if print_point or True:
									i+=1
									print(i)
								self.contour.append(ob)
								break
				else:
					for point in coord:
						if print_point:
							print(point)
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

	def arraie(self):
		z_list = []
		self.points = array([])
		line = array([])
		points = []
		for point in self.contour:
			if not (point.z in z_list):
				z_list.append(point.z)
		for idx,z_value in enumerate(z_list):
			z_value_list = []
			for point in self.contour:
				if point.z == z_value:
					z_value_list.append([point.x,point.y,point.z])
			points += z_value_list
		self.points = array([points])

	def Save(self, name = "Last_"):
		if name != "Last_" and self.name == "":
			self.name = name
		dir_name = "models"
		path = dir_name + '/'
		if not os.path.exists(dir_name):
			os.mkdir(dir_name)
		if not self.contour_opti:
			self.file = open(path + name + ".3DPiaf", 'w')
		else:
			self.file = open(path + name + ".3DPiaf", 'w')
		for point in self.contour:
			self.file.write(str('%d' %point.x) + ',' +  str('%d' %point.y) + ',' +str('%d' %point.z) + '\n')
		if self.contourx != None:
			self.file.write('imagex\n')
			for point in self.contourx:
				self.file.write(str('%d' %point[0]) + ',' +  str('%d' %point[1]) + '\n')
		if self.contoury != None:
			self.file.write('imagey\n')
			for point in self.contoury:
				self.file.write(str('%d' %point[0]) + ',' +  str('%d' %point[1]) + '\n')
		if self.contourz != None:
			self.file.write('imagez\n')
			for point in self.contourz:
				self.file.write(str('%d' %point[0]) + ',' +  str('%d' %point[1]) + '\n')
		self.file.close()
		print("File Saved")

	def Load(self, name = "Last_", opti = False, console = False):
		if name != "Last_":
			self.name = name
		dir_name = "models"
		path = dir_name + '/'
		if opti:
			ext = ".3DPiafm"
		else:
			ext = ".3DPiaf"
		if os.path.exists(dir_name):
			if name + ext in os.listdir(dir_name):
				self.file = open(path + name + ext, 'r')
			else:
				self.file = open(name + ext, 'r')
		else:
			self.file = open(name + ext, 'r')
		self.contour = []
		image = ""
		for line in self.file:
			if len(line) <= 0:
				break
			if line.split('\n')[0] == 'imagex':
				image = 'x'
				self.contourx = []
			elif line.split('\n')[0] == 'imagey':
				image = 'y'
				self.contoury = []
			elif line.split('\n')[0] == 'imagez':
				image = 'z'
				self.contourz = []
			elif image == 'x':
				x, y = line.split(',')[:2]
				self.contourx.append([float(x),float(y)])
			elif image == 'y':
				x, y = line.split(',')[:2]
				self.contoury.append([float(x),float(y)])
			elif image == 'z':
				x, y = line.split(',')[:2]
				self.contourz.append([float(x),float(y)])
			elif len(line.split(',')) >= 2:
				x, y, z = line.split(',')[:3]
				self.contour.append(Objet3D(x = float(x), y = float(y), z = float(z)))
		self.file.close()
		print("File Loaded")
		print(len(self.contour), " points")
		self.Save()
		if not console:
			self.arraie()

	def minimizeContour(self):
		c_minimize = False
		for file in os.listdir(os.getcwd()):
			if file == "3Dminimize.exe":
				if self.name != "":
					name = self.name
				else:
					if python_version_3:
						name = input("Name : ")
					else:
						name = raw_input("Name : ")
					self.name = name
				config = open("config.txt", 'w')
				config.write(name)
				config.close()
				os.system("3Dminimize.exe")
				c_minimize = True
				break
		if c_minimize:
			dir_name = "models"
			path = dir_name + '/'
			if os.path.exists(dir_name):
				if name + ".3DPiafm" in os.listdir(dir_name):
					self.file = open(path + name + ".3DPiafm", 'r')
				else:
					self.file = open(name + ".3DPiafm", 'r')
			else:
				self.file = open(name + ".3DPiafm", 'r')
			self.contour = []
			image = ""
			for line in self.file:
				if line.split('\n')[0] == 'imagex':
					image = 'x'
					self.contourx = []
				elif line.split('\n')[0] == 'imagey':
					image = 'y'
					self.contoury = []
				elif line.split('\n')[0] == 'imagez':
					image = 'z'
					self.contourz = []
				elif image == 'x':
					x, y = line.split(',')[:2]
					self.contourx.append([float(x),float(y)])
				elif image == 'y':
					x, y = line.split(',')[:2]
					self.contoury.append([float(x),float(y)])
				elif image == 'z':
					x, y = line.split(',')[:2]
					self.contourz.append([float(x),float(y)])
				elif len(line.split(',')) >= 2:
					x, y, z = line.split(',')[:3]
					self.contour.append(Objet3D(x = float(x), y = float(y), z = float(z)))
			self.file.close()
			print(len(self.contour), " points")
			self.Save(name)
		else:
			self.contour_remove = []
			nbpoint = 0
			totnbpoint = len(self.contour)
			chargement = 0
			pos = []
			for point in self.contour:
				pos += [point.x, point.y, point.z]
			for point in self.contour:
				prox = 0
				nbpoint += 1
				if nbpoint//(totnbpoint/100) > chargement:
					chargement = nbpoint//(totnbpoint/100)
					print('Loading : ', chargement, '%')
				if point.x == None or point.y == None or point.z == None:
					self.contour_remove.append(point)
				else:
					sens = 1
					for i in range(2):
						if [point.x, point.y, point.z + sens] in pos:
							prox += 1
						if [point.x, point.y + sens, point.z] in pos:
							prox += 1
						if [point.x + sens, point.y, point.z] in pos:
							prox += 1
						sens *= -1
					if prox >= 6:
						self.contour_remove.append(point)
			nbpoint = chargement = 0
			totnbpoint2 = len(self.contour_remove)
			for point in self.contour_remove:
				self.contour.remove(point)
				nbpoint += 1
				if nbpoint//(totnbpoint/100) > chargement:
					chargement = nbpoint//(totnbpoint2/100)
					print('Remove Loading : ', chargement, '%')
			print(totnbpoint, " initials points")
			print(totnbpoint2, 'removed points')
			print('Now', len(self.contour), 'points')
		self.Save()
		self.contour_opti = True

	def LoadNewImages(self, imagex = None, imagey = None, imagez = None):
		self.contour = []
		self.contour_opti = False
		self.contourx, self.contoury, self.contourz = None, None, None
		if imagex != None:
			self.contour_axe(axe = 'x', image=imagex, print_point = True)
		if imagey != None:
			self.contour_axe(axe = 'y', image=imagey, print_point = True)
		if imagez != None:
			self.contour_axe(axe = 'z', image=imagez, print_point = True)
		self.Save()

	def LoadNewContours(self, imagex = None, imagey = None, imagez = None):
		self.contour = []
		self.contour_opti = False
		refresh = 0
		for point in self.contourx:
			x = None
			y = point[0]
			z = point[1]
			self.contour.append(Objet3D(x = x, y = y, z = z))
		contour_trans = self.contourz[:]
		for point in self.contoury:
			x = point[0]
			y = None
			z = point[1]
			found = False
			for ob in contour_trans:
				if x == ob[0] and self.contourz != None:
					found = True
					refresh += 1
					if refresh == 1:
						self.contour = []
					self.contour.append(Objet3D(x = x, y = ob[1], z = z))
			if not found:
				self.contour.append(Objet3D(x = x, y = y, z = z))
		if self.contourx != None and self.contoury != None:
			contour_trans_ob = self.contour
			self.contour = []
			for ob in contour_trans_ob:
				for x, y in self.contourz:
					if x == ob.x and y == ob.y:
						self.contour.append(ob)
						break
		self.Save()

class Camera:
	def __init__(self, phi = 0, theta = pi/2):
		self.phi = phi
		self.theta = theta

	def Rot(self, dphi = 0, dtheta = 0):
		self.phi += dphi
		self.theta += dtheta

def ConvertImageToBinary():
	name = raw_input("png name:")
	nameNoExt = name.split('.')[0]
	import cv2
	import numpy as np
	img = cv2.imread(name,0)
	if python_version_3:
		rvb_min = int(input("RVB min TRESH_BINARY: "))
	else:
		rvb_min = int(raw_input("RVB min TRESH_BINARY: "))
	ret,thresh_img = cv2.threshold(img,rvb_min,255,cv2.THRESH_BINARY)
	nbpoint = 0
	bin_file = open(nameNoExt+'.txt', 'w')
	nbline = 0
	for line in thresh_img:
		for point in line:
			nbpoint += 1
			bin_point = '0'
			if point == 0:
				bin_point = '1'
			bin_file.write(bin_point)
		nbline +=1
		if nbline < len(thresh_img):
			bin_file.write('\n')
	bin_file.close()
	print(nbpoint)

def ConsoleMode(ob):
	imagex, imagey, imagez = [], [], []
	command = ''
	print('CONSOLE MODE')
	while command != 'quit':
		if python_version_3:
			command = input("Command : ")
		else:
			command = raw_input("Command : ")
		if command == 'help':
			print("Commands : 'quit', 'minimize', 'load', 'save', 'convert', 'export', 'change'")
		if command == 'minimize':
			ob.minimizeContour()
		if command == 'load':
			if python_version_3:
				ob.Load(name = input("Load :"), console = True)
			else:
				ob.Load(name = raw_input("Load :"), console = True)
		if command == 'save':
			if python_version_3:
				ob.Save(name = input("Save to :"))
			else:
				ob.Save(name = raw_input("Save to :"))
		if command == 'convert':
			ConvertImageToBinary()
		if command == 'export':
			ExportToObj(ob)
		if command == 'change':
			if python_version_3:
				namex = input("Name imagex:")
				namey = input("Name imagey:")
				namez = input("Name imagez:")
			else:
				namex = raw_input("Name imagex:")
				namey = raw_input("Name imagey:")
				namez = raw_input("Name imagez:")
			imagex = []
			imagey = []
			imagez = []
			if namex == 'None':
				imagex = None
			else:
				fx = open(namex, 'a')
				fx.close()
				with open(namex, 'r') as fx:
					for line in fx:
						line_list = list(line)
						if line_list.count('\n') != 0:
							line_list.remove('\n')
						imagex.append(line_list)
					if imagex == []:
						imagex = None
			if namey == 'None':
				imagey = None
			else:
				fy = open(namey, 'a')
				fy.close()
				with open(namey, 'r') as fy:
					for line in fy:
						line_list = list(line)
						if line_list.count('\n') != 0:
							line_list.remove('\n')
						imagey.append(line_list)
					if imagey == []:
						imagey = None
			if namez == 'None':
				imagez = None
			else:
				fz = open(namez, 'a')
				fz.close()
				with open(namez, 'r') as fz:
					for line in fz:
						line_list = list(line)
						if line_list.count('\n') != 0:
							line_list.remove('\n')
						imagez.append(line_list)
					if imagez == []:
						imagez = None
			ob.LoadNewImages(imagex = imagex, imagey = imagey, imagez = imagez)
	return 0

def ExportToObj(ob):
	import numpy
	from pymesh_mod import obj

	if python_version_3:
		name = input("Name of .obj without .obj:")
	else:
		name = raw_input("Name of .obj without .obj:")
	mesh_ori = obj.Obj()
	translate = 2
	nbpoint = chargement = 0
	totnbpoint = len(ob.contour)
	"""
	tab = [[]]
	plusline = False
	f_line = []
	found = False
	y_tab = []
	z_tab_min = []
	z_tab_max = []
	for point in ob.contour:
		if point.x == 45.0:
			if y_tab.count(point.y) == 0:
				z_tab_min.append(point.z)
				z_tab_max.append(point.z)
				y_tab.append(point.y)
			if z_tab_max[y_tab.index(point.y)] + 2.0 == point.z:
				z_tab_max[y_tab.index(point.y)] = point.z
			if z_tab_min[y_tab.index(point.y)] > point.z:
				z_tab_min[y_tab.index(point.y)] = point.z
	for y in y_tab:
		mesh = obj.Obj("Cube.obj")
		mesh.scale(1, 1, z_tab_max[y_tab.index(point.y)]-z_tab_min[y_tab.index(y)])
		mesh.translate_x(translate*45)
		mesh.translate_y(translate*y)
		mesh.translate_z(translate*z_tab_min[y_tab.index(y)])
		mesh_ori.join(mesh)
	for point in ob.contour:
		nbpoint += 1
		if nbpoint//(totnbpoint/100) > chargement:
			chargement = nbpoint//(totnbpoint/100)
			print("Model Loading : {} %".format(chargement))
		if point.x != 45.0:
			zmax = 0
			zmin = point.z
			if not [point.x, point.y] in tab:
				plus = False
				for point2 in ob.contour:
					if point.x == point2.x and point.y == point2.y:
						if point.z +1 == point2.z:
							zmax = point2.z
							plus = True
						elif point2.z > point.z:
							plus = False
						if point2.z < zmin:
							zmin = point2.z
				mesh = obj.Obj("Cube.obj")
				mesh.scale(1, 1, zmax-zmin)
				mesh.translate_x(translate*point.x)
				mesh.translate_y(translate*point.y)
				mesh.translate_z(translate*zmin)
				mesh_ori.join(mesh)
				if plus:
					tab.append([point.x, point.y])
	pos = []
	for point in ob.contour:
		pos += [point.x, point.y, point.z]
	for point in ob.contour:
		nbpoint += 1
		if nbpoint//(totnbpoint/100) > chargement:
			chargement = nbpoint//(totnbpoint/100)
			print("Model Loading : {} %".format(chargement))
		new_mesh = None
		sens = 1
		for i in range(2):
			if not [point.x, point.y, point.z + sens] in pos:
				if sens == 1:
					new_mesh = obj.Obj("Top.obj")
				else:
					if new_mesh != None:
						mesh = obj.Obj("Bot.obj")
						new_mesh.join(mesh)
					else:
						new_mesh = obj.Obj("Bot.obj")
			if not [point.x, point.y + sens, point.z] in pos:
				if sens == 1:
					if new_mesh != None:
						mesh = obj.Obj("Right.obj")
						new_mesh.join(mesh)
					else:
						new_mesh = obj.Obj("Right.obj")
				else:
					if new_mesh != None:
						mesh = obj.Obj("Left.obj")
						new_mesh.join(mesh)
					else:
						new_mesh = obj.Obj("Left.obj")
			if not [point.x + sens, point.y, point.z] in pos:
				if sens == 1:
					if new_mesh != None:
						mesh = obj.Obj("Front.obj")
						new_mesh.join(mesh)
					else:
						new_mesh = obj.Obj("Front.obj")
				else:
					if new_mesh != None:
						mesh = obj.Obj("Back.obj")
						new_mesh.join(mesh)
					else:
						new_mesh = obj.Obj("Back.obj")
			sens *= -1
		if new_mesh != None:
			new_mesh.translate_x(translate*point.x)
			new_mesh.translate_y(translate*point.y)
			new_mesh.translate_z(translate*point.z)
			mesh_ori.join(new_mesh)
	"""
	for point in ob.contour:
		nbpoint += 1
		if nbpoint//(totnbpoint/100) > chargement:
			chargement = nbpoint//(totnbpoint/100)
			print("Model Loading : {} %".format(chargement))
		mesh = obj.Obj("Cube.obj")
		mesh.translate_x(translate*point.x)
		mesh.translate_y(translate*point.y)
		mesh.translate_z(translate*point.z)
		mesh_ori.join(mesh)
	print('Starting to export')
	c_export = False
	for file in os.listdir(os.getcwd()):
		if file == "ExportObj.exe":
			config = open("config.txt", "w")
			config.write(name)
			config.close()
			mesh_ori.update_normals()
			vectors_key_list = []
			normals_key_list = []
			file = open("bones.txt", "w")
			for i, vector in enumerate(mesh_ori.vectors):
				for j in range(3):
					v_key = ",".join(map(str, mesh_ori.vectors[i][j][:3]))
					file.write( ":{}\n".format(v_key))
				n_key = ",".join(map(str, mesh_ori.normals[i][:3]))
				file.write( "/{}\n".format(n_key))
			file.close()
			os.system("ExportObj.exe")
			c_export = True
	if not c_export:
		name = "objects/" + name + ".obj"
		mesh_ori.save_obj(name)

def ExportToObj2(ob):
	"""
	ob.arraie()
	pos = [0]*len(ob.contour)
	for idx, point in enumerate(ob.contour):
		pos[idx] = [point.x, point.y, point.z]
	top_list = empty((len(ob.contour),3))
	bot_list = empty((len(ob.contour),3))
	left_list = empty((len(ob.contour),3))
	right_list = empty((len(ob.contour),3))
	back_list = empty((len(ob.contour),3))
	front_list = empty((len(ob.contour),3))
	nbpoints = 0
	chargement = 0
	totnbpoint = len(ob.contour)
	top = 0
	bot = 0
	left = 0
	right = 0
	front = 0
	back = 0
	for point in ob.contour:
		nbpoints += 1
		if nbpoints//(totnbpoint/100) > chargement:
			chargement = nbpoints//(totnbpoint/100)
			print("Model Loading : {} %".format(chargement))
		sens = 1
		for i in range(2):
			if not [point.x, point.y, point.z + sens] in pos:
				if sens == 1:
					top_list[top] = [point.x, point.y, point.z]
					top += 1
				elif sens == -1:
					bot_list[bot] = [point.x, point.y, point.z]
					bot += 1
			if not [point.x, point.y + sens, point.z] in pos:
				if sens == 1:
					right_list[right] = [point.x, point.y, point.z]
					right += 1
				elif sens == -1:
					left_list[left] = [point.x, point.y, point.z]
					left += 1
			if not [point.x + sens, point.y, point.z] in pos:
				if sens == 1:
					front_list[front] = [point.x, point.y, point.z]
					front += 1
				elif sens == -1:
					back_list[back] = [point.x, point.y, point.z]
					back += 1
			sens = -1
	top_list, bot_list, left_list, right_list, back_list, front_list = top_list[:top], bot_list[:bot], left_list[:left], right_list[:right], back_list[:back], front_list[:front]
	write_files(top_list, bot_list, right_list, left_list, front_list, back_list)
	"""
	top_list, bot_list, left_list, right_list, back_list, front_list = load_files(ob)
	nbpoints = 0
	file = open("bones.obj", "w")
	file.write("vt 0.0 0.0\nvt 1.0 0.0\nvt 0.0 1.0\nvt 1.0 1.0\n\nvn 0.0 0.0 1.0\nvn 0.0 1.0 0.0\nvn 0.0 0.0 -1.0\nvn 0.0 -1.0 0.0\nvn 1.0 0.0 0.0\nvn -1.0 0.0 0.0\n\n")
	points = bot_list[:].tolist()
	for point_top in top_list:
		for point_bot in points:
			if point_top in right_list and point_bot in right_list:
				if point_top[0] == point_bot[0] and point_top[1] == point_bot[1]:
					nbpoints +=1
					file.write("v {} {} {}\nv {} {} {}\n".format(point_bot[0],point_bot[1],point_bot[2],point_top[0],point_top[1],point_top[2]))
					print(nbpoints)
					points.remove(point_bot)
					if nbpoints > 1:
						file.write("\nf {}/1/6 {}/1/6 {}/1/6\n\n".format(nbpoints*2-1, nbpoints*2, nbpoints*2-2))
					break
			"""
			elif point_top in left_list and point_bot in left_list:
				if point_top[0] == point_bot[0] and point_top[1] == point_bot[1]:
					nbpoints +=1
					file.write("v {} {} {}\nv {} {} {}\n".format(point_bot[0],point_bot[1],point_bot[2],point_top[0],point_top[1],point_top[2]))
					if nbpoints > 1:
						file.write("\nf {}/1/5 {}/1/5 {}/1/5\n\n".format(nbpoints*2-1, nbpoints*2, nbpoints*2-2))
					break
			"""
	file.close()

def ExportToObj3(ob):
	import numpy
	from pymesh_mod import obj

	if python_version_3:
		name = input("Name of .obj without .obj:")
	else:
		name = raw_input("Name of .obj without .obj:")
	mesh_ori = obj.Obj()
	translate = 2
	nbpoint = chargement = 0
	totnbpoint = len(ob.contour)
	top_list, bot_list, left_list, right_list, back_list, front_list = load_files(ob)
	nbpoints = 0
	new_mesh = None
	print("Top")
	for point in top_list:
		if new_mesh != None:
			mesh = obj.Obj("Top.obj")
			new_mesh.join(mesh)
		else:
			new_mesh = obj.Obj("Top.obj")
		new_mesh.translate_x(translate*point[0])
		new_mesh.translate_y(translate*point[1])
		new_mesh.translate_z(translate*point[2])
		mesh_ori.join(new_mesh)
	print("Bot")
	for point in bot_list:
		if new_mesh != None:
			mesh = obj.Obj("Bot.obj")
			new_mesh.join(mesh)
		else:
			new_mesh = obj.Obj("Bot.obj")
		new_mesh.translate_x(translate*point[0])
		new_mesh.translate_y(translate*point[1])
		new_mesh.translate_z(translate*point[2])
		mesh_ori.join(new_mesh)
	print("Right")
	for point in right_list:
		if new_mesh != None:
			mesh = obj.Obj("Right.obj")
			new_mesh.join(mesh)
		else:
			new_mesh = obj.Obj("Right.obj")
		new_mesh.translate_x(translate*point[0])
		new_mesh.translate_y(translate*point[1])
		new_mesh.translate_z(translate*point[2])
		mesh_ori.join(new_mesh)
	print("Left")
	for point in left_list:
		if new_mesh != None:
			mesh = obj.Obj("Left.obj")
			new_mesh.join(mesh)
		else:
			new_mesh = obj.Obj("Left.obj")
		new_mesh.translate_x(translate*point[0])
		new_mesh.translate_y(translate*point[1])
		new_mesh.translate_z(translate*point[2])
		mesh_ori.join(new_mesh)
	print("Back")
	for point in back_list:
		if new_mesh != None:
			mesh = obj.Obj("Back.obj")
			new_mesh.join(mesh)
		else:
			new_mesh = obj.Obj("Back.obj")
		new_mesh.translate_x(translate*point[0])
		new_mesh.translate_y(translate*point[1])
		new_mesh.translate_z(translate*point[2])
		mesh_ori.join(new_mesh)
	print("Front")
	for point in front_list:
		if new_mesh != None:
			mesh = obj.Obj("Front.obj")
			new_mesh.join(mesh)
		else:
			new_mesh = obj.Obj("Front.obj")
		new_mesh.translate_x(translate*point[0])
		new_mesh.translate_y(translate*point[1])
		new_mesh.translate_z(translate*point[2])
		mesh_ori.join(new_mesh)
	print('Starting to export')
	c_export = False
	for file in os.listdir(os.getcwd()):
		if file == "ExportObj.exe" and False:
			config = open("config.txt", "w")
			config.write(name)
			config.close()
			mesh_ori.update_normals()
			vectors_key_list = []
			normals_key_list = []
			file = open("bones.txt", "w")
			file.write("50\n{}\n{}\n{}\n".format(len(mesh_ori.vectors)*3 + len(mesh_ori.normals[:]), len(mesh_ori.vectors[:])*3,len(mesh_ori.normals[:])))
			for i, vector in enumerate(mesh_ori.vectors):
				for j in range(3):
					v_key = ",".join(map(str, mesh_ori.vectors[i][j][:3]))
					file.write( ":{}\n".format(v_key))
				n_key = ",".join(map(str, mesh_ori.normals[i][:3]))
				file.write( "/{}\n".format(n_key))
			file.close()
			os.system("ExportObj.exe")
			c_export = True
	if not c_export:
		name = "objects/" + name + ".obj"
		mesh_ori.save_obj(name)

def write_files(top_list, bot_list, right_list, left_list, front_list, back_list):
	file = open("top_list.txt", "w")
	for point in top_list:
		file.write("{} {} {}\n".format(point[0],point[1],point[2]))
	file.close()
	file = open("bot_list.txt", "w")
	for point in bot_list:
		file.write("{} {} {}\n".format(point[0],point[1],point[2]))
	file.close()
	file = open("right_list.txt", "w")
	for point in right_list:
		file.write("{} {} {}\n".format(point[0],point[1],point[2]))
	file.close()
	file = open("left_list.txt", "w")
	for point in left_list:
		file.write("{} {} {}\n".format(point[0],point[1],point[2]))
	file.close()
	file = open("back_list.txt", "w")
	for point in back_list:
		file.write("{} {} {}\n".format(point[0],point[1],point[2]))
	file.close()
	file = open("front_list.txt", "w")
	for point in front_list:
		file.write("{} {} {}\n".format(point[0],point[1],point[2]))
	file.close()

def load_files(ob):
	top_list, bot_list, left_list, right_list, back_list, front_list = empty((len(ob.contour),3)), empty((len(ob.contour),3)), empty((len(ob.contour),3)), empty((len(ob.contour),3)), empty((len(ob.contour),3)), empty((len(ob.contour),3))
	file = open("top_list.txt", "r")
	top = 0
	for line in file:
		pos = line.split()
		top_list[top] = [float(pos[0]),float(pos[1]),float(pos[2])]
		top +=1
	file.close()
	file = open("bot_list.txt", "r")
	bot = 0
	for line in file:
		pos = line.split()
		bot_list[bot] = [float(pos[0]),float(pos[1]),float(pos[2])]
		bot += 1
	file.close()
	file = open("right_list.txt", "r")
	right = 0
	for line in file:
		pos = line.split()
		right_list[right] = [float(pos[0]),float(pos[1]),float(pos[2])]
		right += 1
	file.close()
	file = open("left_list.txt", "r")
	left = 0
	for line in file:
		pos = line.split()
		left_list[left] = [float(pos[0]),float(pos[1]),float(pos[2])]
		left += 1
	file.close()
	file = open("back_list.txt", "r")
	back = 0
	for line in file:
		pos = line.split()
		back_list[back] = [float(pos[0]),float(pos[1]),float(pos[2])]
		back += 1
	file.close()
	file = open("front_list.txt", "r")
	front = 0
	for line in file:
		pos = line.split()
		front_list[front] = [float(pos[0]),float(pos[1]),float(pos[2])]
		front += 1
	file.close()
	return top_list[:top], bot_list[:bot], left_list[:left], right_list[:right], back_list[:back], front_list[:front]

def Editor(fenetre, imagex, imagey, imagez):
	return mainEditor(fenetre, imagex = imagex, imagey = imagey, imagez = imagez)

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--console", help="console mode",action="store_true")
args = parser.parse_args()
if args.console:
	ob = Objet3D()
	ob.Load()
	ConsoleMode(ob)
else:
	main()
