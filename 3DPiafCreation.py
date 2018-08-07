# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

from builtins import input

import numpy as np

import pygame
from pygame.locals import *

import utils as uts
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
	fenetre = pygame.display.set_mode((uts.WINDOWWIDTH, uts.WINDOWWHEIGHT), RESIZABLE)

	BASICFONT = pygame.font.Font("bkant.ttf", 32)
	axe = 'x'

	QUIT_SURF, QUIT_RECT = uts.makeText('QUIT', uts.TEXTCOLOR, uts.TILECOLOR, uts.WINDOWWIDTH - 120, uts.WINDOWWHEIGHT - 90)
	SAVE_SURF, SAVE_RECT = uts.makeText('SAVE', uts.TEXTCOLOR, uts.TILECOLOR, uts.WINDOWWIDTH/2 - 250, 40)
	LOAD_SURF, LOAD_RECT = uts.makeText('LOAD', uts.TEXTCOLOR, uts.TILECOLOR, uts.WINDOWWIDTH/2 - 150, 40)
	EXPORT_SURF, EXPORT_RECT = uts.makeText('EXPORT', uts.TEXTCOLOR, uts.TILECOLOR, uts.WINDOWWIDTH/2 - 30, 40)
	EDITOR_SURF, EDITOR_RECT = uts.makeText('EDITOR', uts.TEXTCOLOR, uts.TILECOLOR, uts.WINDOWWIDTH/2 + 120, 40)
	LIGHT_SURF, LIGHT_RECT = uts.makeText('LIGHT', uts.TEXTCOLOR, uts.TILECOLOR, uts.WINDOWWIDTH/2 + 120, 90)
	TEXT_SURF = BASICFONT.render(axe, True, uts.TEXTCOLOR)
	TEXT_RECT = TEXT_SURF.get_rect()
	TEXT_RECT.center = (110, 15)

	black_surf, black_rect = uts.makeSquarre(uts.BACK, h = uts.WINDOWWHEIGHT, w = uts.WINDOWWIDTH)

	imagex = []
	imagey = []
	imagez = []
	#print(imagex)
	#print(imagey)
	#print(imagez)
	ob = Objet3D()
	ob.Load()
	cam = Camera()

	dzoom = 1

	pygame.key.set_repeat(400, 30)
	#BOUCLE INFINIE
	continuer = 1
	press = True
	rot_press = False
	r = v = b = 0
	list_points = []
	pointlist = []
	if ob.f == []:
		list_f = List_v(ob, cam)
		ob.Save_f()
	else:
		list_f = ob.f
	point_f = []
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
						ob.Save(name = input("Save to :"))
					else:
						ob.Save(name = ob.name)
				elif LOAD_RECT.collidepoint(event.pos):
					ob.Load(name = input("Load :"))
					list_f = List_v(ob, cam)
					#ob.Save_f()
					press = True
				elif EXPORT_RECT.collidepoint(event.pos):
					ExportToObj(ob)
				elif LIGHT_RECT.collidepoint(event.pos):
					if cam.light:
						cam.light = False
					else:
						cam.light = True
					press = True
				elif EDITOR_RECT.collidepoint(event.pos):
					[ob.contourx, ob.contoury, ob.contourz] = Editor(fenetre, ob.contourx, ob.contoury, ob.contourz)
					ob.LoadNewContours(imagex = ob.contourx, imagey = ob.contoury, imagez = ob.contourz)
					list_f = List_v(ob, cam)
					ob.Save_f()
					press = True
				else:
					if event.button == 1:
						rot_press = True
					if event.button == 4:
						cam.r += dzoom
						if cam.r <= 1:
							cam.r = 2
						list_points = List_points2(ob, cam)
						point_f = []
						for f in list_f:
							point_f.append([(list_points[f[0]].x, list_points[f[0]].y), 
								(list_points[f[1]].x, list_points[f[1]].y), 
								(list_points[f[2]].x, list_points[f[2]].y), 
								(list_points[f[3]].x, list_points[f[3]].y)])
					if event.button == 5:
						cam.r -= dzoom
						if cam.r >= 480:
							cam.r = 480
						list_points = List_points2(ob, cam)
						point_f = []
						for f in list_f:
							point_f.append([(list_points[f[0]].x, list_points[f[0]].y), 
								(list_points[f[1]].x, list_points[f[1]].y), 
								(list_points[f[2]].x, list_points[f[2]].y), 
								(list_points[f[3]].x, list_points[f[3]].y)])
			if event.type == MOUSEBUTTONUP:
				if event.button == 1:
					rot_press = False
			if event.type == MOUSEMOTION:
				if rot_press:
					x, y = pygame.mouse.get_rel()
					axe = 'None'
					cam.Rot(dtheta=y*np.pi/180, dphi=x*np.pi/180)
					move = True
					if move:
						TEXT_SURF = BASICFONT.render(axe + str('%d' %cam.r), True, uts.TEXTCOLOR)
						list_points = List_points2(ob, cam)
						point_f = []
						for f in list_f:
							point_f.append([(list_points[f[0]].x, list_points[f[0]].y), 
								(list_points[f[1]].x, list_points[f[1]].y), 
								(list_points[f[2]].x, list_points[f[2]].y), 
								(list_points[f[3]].x, list_points[f[3]].y)])
			if event.type == KEYDOWN:
				key = pygame.key.get_pressed()  #checking pressed keys
				if key[pygame.K_x]:
					axe = 'x'
					press = True
					cam.phi = 0
					cam.theta = np.pi/2
				if key[pygame.K_y]:
					axe = 'y'
					press = True
					cam.phi = np.pi/2
					cam.theta = np.pi/2
				if key[pygame.K_w]:
					axe = 'z'
					press = True
					cam.phi = np.pi/2
					cam.theta = 0
				if key[pygame.K_RIGHT]:
					axe = 'None'
					cam.Rot(dphi=np.pi/180)
					press = True
				if key[pygame.K_LEFT]:
					axe = 'None'
					cam.Rot(dphi=-np.pi/180)
					press = True
				if key[pygame.K_UP]:
					axe = 'None'
					cam.Rot(dtheta=-np.pi/180)
					press = True
				if key[pygame.K_DOWN]:
					axe = 'None'
					cam.Rot(dtheta=np.pi/180)
					press = True
				if key[pygame.K_b]:
					cam.r -= dzoom
					if cam.r <= 1:
						cam.r = 2
					press = True
				if key[pygame.K_n]:
					cam.r += dzoom
					if cam.r >= 480:
						cam.r = 480
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
					ob.Load(name = input("Load :"))
					press = True
				if key[pygame.K_s]:
					if ob.name == "":
						ob.Save(name = input("Save to :"))
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
					namex = input("Name imagex:")
					namey = input("Name imagey:")
					namez = input("Name imagez:")
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
			TEXT_SURF = BASICFONT.render(axe + str('%d' %cam.r), True, uts.TEXTCOLOR)
			press = False
			list_points = List_points2(ob, cam)
			pointlist = []
			for point in list_points:
				pointlist.append([(point.x, point.y)])
			try:
				point_f = []
				for f in list_f:
					point_f.append([(list_points[f[0]].x, list_points[f[0]].y), 
									(list_points[f[1]].x, list_points[f[1]].y), 
									(list_points[f[2]].x, list_points[f[2]].y), 
									(list_points[f[3]].x, list_points[f[3]].y)])
			except:
				print('error in f')
				list_f = List_v(ob, cam)
				list_points = List_points2(ob, cam)
				ob.Save_f()
				point_f = []
				print('len(list_points) = ', len(list_points))
				for f in list_f:
					print(f)
					point_f.append([(list_points[f[0]].x, list_points[f[0]].y), 
									(list_points[f[1]].x, list_points[f[1]].y), 
									(list_points[f[2]].x, list_points[f[2]].y), 
									(list_points[f[3]].x, list_points[f[3]].y)])
		#Re-collage
		fenetre.blit(black_surf, black_rect)
		#for point in list_points:
		#	point.fblit(fenetre)
		#pygame.draw.polygon(fenetre, (0,0,255), pointlist)
		for f in point_f:
		#	#pygame.draw.polygon(fenetre, (0,0,255), f)
			squarreSurf, squarreRect = makeSquarre((0,0,255), middlehight = (f[3][0]-f[0][0])/2 + f[0][0], middlewheight = np.fabs(f[3][1]-f[0][1])/2 + f[0][1], top = -1, left = -1, w = abs(f[3][0]-f[0][0])+1, h = abs(f[3][1]-f[0][1])+1)
			fenetre.blit(squarreSurf, squarreRect)
		# This draws a triangle using the polygon command
		#pygame.draw.polygon(fenetre, uts.BLACK, [[100, 100], [0, 200], [200, 200]], 5)
		fenetre.blit(TEXT_SURF, TEXT_RECT)
		fenetre.blit(QUIT_SURF, QUIT_RECT)
		fenetre.blit(SAVE_SURF, SAVE_RECT)
		fenetre.blit(LOAD_SURF, LOAD_RECT)
		fenetre.blit(EXPORT_SURF, EXPORT_RECT)
		fenetre.blit(EDITOR_SURF, EDITOR_RECT)
		fenetre.blit(LIGHT_SURF, LIGHT_RECT)
		#Rafraichissement
		pygame.display.flip()
	pygame.quit()

def List_points(ob, cam):
	ob.arraie()
	points = np.empty((len(ob.points[0]),3))
	for idx, pos in enumerate(ob.points[0]):
		points[idx] = pos
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
	x0, y0, z0 = (xmax-xmin)/2, (ymax-ymin)/2, (zmax-zmin)/2
	X -= x0
	Y -= y0
	Z -= z0
	posx = -X*np.sin(cam.phi) + Y*np.cos(cam.phi)
	posy = X*np.cos(cam.theta)*np.cos(cam.phi) + Y*np.cos(cam.theta)*np.sin(cam.phi) - Z*np.sin(cam.theta)
	posy*=-1
	posx*=-1
	list_points = [0]*len(points)
	
	cam.x = cam.r*np.sin(cam.theta)*np.cos(cam.phi)
	cam.y = cam.r*np.sin(cam.theta)*np.sin(cam.phi)
	cam.z = cam.r*np.cos(cam.theta)
	for index in range(len(points)):
		if cam.light:
			list_points[index] = uts.Point((0,0,255-int(np.sqrt((X[index]-cam.x)**2 + (Y[index]-cam.y)**2 + (Z[index]-cam.z)**2))), x = posx[index]*cam.r + uts.middlehight, y = posy[index]*cam.r + uts.middlewheight, size = cam.r)
		else:
			list_points[index] = uts.Point((0,0,255), x = posx[index]*cam.r + uts.middlehight, y = posy[index]*cam.r + uts.middlewheight, size = cam.r)
	return list_points

def List_points2(ob, cam):
	points = np.empty((len(ob.points[0]),3))
	for idx, pos in enumerate(ob.points[0]):
		points[idx] = pos
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
	x0, y0, z0 = (xmax-xmin)/2, (ymax-ymin)/2, (zmax-zmin)/2
	X -= x0
	Y -= y0
	Z -= z0
	posx = -X*np.sin(cam.phi) + Y*np.cos(cam.phi)
	posy = X*np.cos(cam.theta)*np.cos(cam.phi) + Y*np.cos(cam.theta)*np.sin(cam.phi) - Z*np.sin(cam.theta)
	posy*=-1
	posx*=-1
	list_points = [0]*len(points)
	
	cam.x = cam.r*np.sin(cam.theta)*np.cos(cam.phi)
	cam.y = cam.r*np.sin(cam.theta)*np.sin(cam.phi)
	cam.z = cam.r*np.cos(cam.theta)
	for index in range(len(points)):
		if cam.light:
			list_points[index] = uts.Point((0,0,255-int(np.sqrt((X[index]-cam.x)**2 + (Y[index]-cam.y)**2 + (Z[index]-cam.z)**2))), x = posx[index]*cam.r + uts.middlehight, y = posy[index]*cam.r + uts.middlewheight, size = cam.r)
		else:
			list_points[index] = uts.Point((0,0,255), x = posx[index]*cam.r + uts.middlehight, y = posy[index]*cam.r + uts.middlewheight, size = cam.r)
	return list_points

def List_v(ob, cam):
	#ob.f = optimization_between_f(ob)
	#print(len(ob.f))
	#return ob.f
	ob.arraie()
	"""
	f = []
	print(len(ob.points[0]))
	trans_points = list(ob.points[0][:])
	trans_pointsx = trans_points[:]
	trans_pointsy = trans_points[:]
	trans_pointsz = trans_points[:]
	trans_pointsxy = trans_points[:]
	trans_pointsxz = trans_points[:]
	trans_pointsyz = trans_points[:]
	for idx, pt in enumerate(ob.points[0]):
		x = -1
		z = -1
		xz = -1
		y = -1
		xy = -1
		yz = -1
		f_trans = [idx]
		for idx2, pt2 in enumerate(trans_pointsx):
			if pt2[0] == pt[0] + 1 and pt2[1] == pt[1] and pt2[2] == pt[2]:
				x = idx2
				del trans_pointsx[idx2]
				break
		for idx2, pt2 in enumerate(trans_pointsy):
			if pt2[0] == pt[0] and pt2[1] == pt[1] + 1 and pt2[2] == pt[2]:
				y = idx2
				del trans_pointsy[idx2]
				break
		for idx2, pt2 in enumerate(trans_pointsz):
			if pt2[0] == pt[0] and pt2[1] == pt[1] and pt2[2] == pt[2] + 1:
				z = idx2
				del trans_pointsz[idx2]
				break
		for idx2, pt2 in enumerate(trans_pointsxy):
			if pt2[0] == pt[0] + 1 and pt2[1] == pt[1] + 1 and pt2[2] == pt[2]:
				xy = idx2
				del trans_pointsxy[idx2]
				break
		for idx2, pt2 in enumerate(trans_pointsxz):
			if pt2[0] == pt[0] + 1 and pt2[1] == pt[1] and pt2[2] == pt[2] + 1:
				xz = idx2
				del trans_pointsxz[idx2]
				break
		for idx2, pt2 in enumerate(trans_pointsyz):
			if pt2[0] == pt[0] and pt2[1] == pt[1] + 1 and pt2[2] == pt[2] + 1:
				yz = idx2
				del trans_pointsyz[idx2]
				break
		if xz != -1:
			if x != -1:
				f.append([idx, x, xz])
			if z != -1:
				f.append([idx, z, xz])
		else:
			if x != -1 and z != -1:
				f.append([idx, x, z])
		if xy != -1:
			if x != -1:
				f.append([idx, x, xy])
			if y != -1:
				f.append([idx, y, xy])
		else:
			if x != -1 and y != -1:
				f.append([idx, x, y])
		if yz != -1:
			if y != -1:
				f.append([idx, y, yz])
			if z != -1:
				f.append([idx, z, yz])
		else:
			if y != -1 and z != -1:
				f.append([idx, y, z])
		print(idx)
	"""
	ob.f = []
	print(len(ob.points[0]))
	trans_points = ob.points[0]
	X = trans_points[:, 0]
	Y = trans_points[:, 1]
	Z = trans_points[:, 2]
	for idx, pt in enumerate(ob.points[0]):
		x = -1
		z = -1
		xz = -1
		y = -1
		xy = -1
		yz = -1
		xyz = -1
		for idx2, x_trans in enumerate(X):
			if x_trans == pt[0] + 1:
				if Y[idx2] == pt[1] and Z[idx2] == pt[2]: 
					x = idx2
				elif Y[idx2] == pt[1] and Z[idx2] == pt[2] + 1:
					xz = idx2
				elif Y[idx2] == pt[1] + 1 and Z[idx2] == pt[2]:
					xy = idx2
				elif Y[idx2] == pt[1] + 1 and Z[idx2] == pt[2] + 1:
					xyz = idx2
			elif x_trans == pt[0] and (y != -1 or z != -1 or yz != -1):
				if Y[idx2] == pt[1] + 1 and Z[idx2] == pt[2]: 
					y = idx2
				elif Y[idx2] == pt[1] and Z[idx2] == pt[2] + 1:
					z = idx2
				elif Y[idx2] == pt[1] + 1 and Z[idx2] == pt[2] + 1:
					yz = idx2
			if xyz != -1 and x != -1 and y != -1 and z != -1 and yz != -1 and xy != -1 and xz != -1:
				break
		if x != -1 and z != -1 and xz != -1:
			ob.f.append([idx, x, z, xz])
		if x != -1 and y != -1 and xy != -1:
			ob.f.append([idx, x, y, xy])
		if y != -1 and z != -1 and yz != -1:
			ob.f.append([idx, y, z, yz])
		if x != -1 and xy != -1 and xz != -1 and xyz != -1:
			ob.f.append([x, xy, xz, xyz])
		if y != -1 and xy != -1 and yz != -1 and xyz != -1:
			ob.f.append([y, xy, yz, xyz])
		if z != -1 and xz != -1 and yz != -1 and xyz != -1:
			ob.f.append([z, xz, yz, xyz])
		"""
		bord_x = True
		bord_y = True
		bord_z = True
		for idx2, x_trans in enumerate(X):
			if x_trans > pt[0]:
				if Y[idx2] == pt[1] and Z[idx2] == pt[2]: 
					bord_x = False
			elif x_trans == pt[0]:
				if Y[idx2] > pt[1] and Z[idx2] == pt[2]: 
					bord_y = False
				elif Y[idx2] == pt[1] and Z[idx2] > pt[2]:
					bord_z = False
		"""
		if y == -1 or z == -1 or yz == -1 or x == -1 or xz == -1 or xy == -1:
			extra_points = ob.points[0].copy()
			f_xy = False
			f_yz = False
			f_xz = False
			f_xyz_x = False
			f_xyz_y = False
			f_xyz_z = False
			for idx2, point in enumerate(extra_points):
				if pt[0]+1 == point[0] and pt[1]+1 == point[1] and pt[2]+1 == point[2] and xyz == -1:
					xyz = idx2
					f_xyz_x = True
					f_xyz_y = True
					f_xyz_z = True
				elif pt[0] == point[0] and pt[1]+1 == point[1] and pt[2] == point[2] and y == -1:
					y = idx2
					f_xy = True
					f_yz = True
					f_xyz_y = True
				elif pt[0]+1 == point[0] and pt[1] == point[1] and pt[2] == point[2] and x == -1:
					x = idx2
					f_xz = True
					f_xy = True
					f_xyz_x = True
				elif pt[0] == point[0] and pt[1] == point[1] and pt[2]+1 == point[2] and z == -1:
					z = idx2
					f_xz = True
					f_yz = True
					f_xyz_z = True
				elif pt[0] == point[0] and pt[1]+1 == point[1] and pt[2]+1 == point[2] and yz == -1:
					yz = idx2
					f_yz = True
					f_xyz_y = True
					f_xyz_z = True
				elif pt[0]+1 == point[0] and pt[1]+1 == point[1] and pt[2] == point[2] and xy == -1:
					xy = idx2
					f_xy = True
					f_xyz_x = True
					f_xyz_y = True
				elif pt[0]+1 == point[0] and pt[1] == point[1] and pt[2]+1 == point[2] and xz == -1:
					xz = idx2
					f_xz = True
					f_xyz_x = True
					f_xyz_z = True
				if xyz != -1 and x != -1 and y != -1 and z != -1 and yz != -1 and xy != -1 and xz != -1:
					break
			if xyz == -1:
				extra_points = np.append(extra_points, [[pt[0]+1, pt[1]+1, pt[2]+1]], axis = 0)
				xyz = len(extra_points)-1
				f_xyz_x = True
				f_xyz_y = True
				f_xyz_z = True
			#if xz == -1 and xy == -1:
			#	
			if y == -1:
				extra_points = np.append(extra_points, [[pt[0], pt[1]+1, pt[2]]], axis = 0)
				y = len(extra_points)-1
				f_xy = True
				f_yz = True
			if z == -1:
				extra_points = np.append(extra_points, [[pt[0], pt[1], pt[2]+1]], axis = 0)
				z = len(extra_points)-1
				f_xz = True
				f_yz = True
			if yz == -1:
				extra_points = np.append(extra_points, [[pt[0], pt[1]+1, pt[2]+1]], axis = 0)
				yz = len(extra_points)-1
				f_yz = True
				f_xyz_y = True
				f_xyz_z = True
			if x == -1:
				extra_points = np.append(extra_points, [[pt[0] + 1, pt[1], pt[2]]], axis = 0)
				x = len(extra_points)-1
				f_xz = True
				f_xy = True
			if xy == -1:
				extra_points = np.append(extra_points, [[pt[0] + 1, pt[1] + 1, pt[2]]], axis = 0)
				xy = len(extra_points)-1
				f_xy = True
				f_xyz_x = True
				f_xyz_y = True
			if xz == -1:
				extra_points = np.append(extra_points, [[pt[0] + 1, pt[1], pt[2]+1]], axis = 0)
				xz = len(extra_points)-1
				f_xz = True
				f_xyz_x = True
				f_xyz_z = True
			if f_xy and x != idx and y != idx and xy != idx and x != y and y != xy and x != xy:
				ob.f.append([idx, x, y, xy])
			if f_xz and x != idx and z != idx and xz != idx and x != z and z != xz and x != xz:
				ob.f.append([idx, x, z, xz])
			if f_yz and y != idx and z != idx and yz != idx and y != z and z != yz and y != yz:
				ob.f.append([idx, y, z, yz])
			if f_xyz_x and x != xy and xyz != xy and xz != xy and x != xyz and xyz != xz and x != xz:
				ob.f.append([x, xy, xz, xyz])
			if f_xyz_y and y != xy and xyz != xy and yz != xy and y != xyz and xyz != xy and y != yz:
				ob.f.append([y, xy, yz, xyz])
			if f_xyz_z and z != xz and xyz != xz and yz != xz and z != xyz and xyz != yz and z != yz:
				ob.f.append([z, xz, yz, xyz])
			ob.points = []
			ob.points.append(extra_points)
			#print(len(ob.points[0]))
		if 0 <= idx % (len(trans_points)/100) <= 1 and idx != 1:
			print(idx/len(trans_points)*100 , '%')
	print('Total points: ', len(ob.points[0])+1)
	#make threads optimization and switch f between each
	print('Before Same f : ', len(ob.f))
	del_f = []
	for idx, f in enumerate(ob.f):
		for idx2, f2 in enumerate(ob.f):
			if idx != idx2:
				if f == f2:
					if not idx2 in del_f:
						del_f.append(idx2)
					if not idx in del_f:
						del_f.append(idx)
	del_f.sort()
	del_f.reverse()
	for idx in del_f:
		del ob.f[idx]
	print('After Same f : ', len(ob.f))
	ob.Save_f()
	ob.SSave()
	#ob.f = optimization_between_f(ob)
	print(len(ob.f))
	return ob.f
	"""
	v = []
	for pt in ob.points:
		right = False
		top = False
		top_right = False
		for pt2 in ob.points:
			if pt2.x == pt.x + 1 and pt2.y == pt.y and pt2.z == pt.z:
				right = True
			elif pt2.x == pt.x + 1 and pt2.y == pt.y and pt2.z == pt.z + 1:
				top = True
			elif pt2.x == pt.x and pt2.y == pt.y and pt2.z == pt.z +1:
				top_right = True
			if top and right and top_right:
				v.append([[pt.x, pt.y, pt.z], [pt.x + 1, pt.y, pt.z], [pt.x + 1, pt.y, pt.z + 1]])
				break
	"""

def optimization_between_f(ob):
	ob.SLoad()
	print('Before Between f : ', len(ob.f))
	del_f = []
	for idx, f in enumerate(ob.f):
		before = False
		after = False
		i = -1
		for j in range(3):
			if ob.points[0][f[0]][j] == ob.points[0][f[1]][j] and ob.points[0][f[2]][j] == ob.points[0][f[0]][j] and ob.points[0][f[3]][j] == ob.points[0][f[0]][j]:
				i = j
				break
		l_3 = [0, 1, 2]
		l_3.remove(i)
		for idx2, f2 in enumerate(ob.f):
			if idx != idx2:
				if ob.points[0][f2[0]][i] == ob.points[0][f2[1]][i] and ob.points[0][f2[2]][i] == ob.points[0][f2[0]][i] and ob.points[0][f2[3]][i] == ob.points[0][f2[0]][i]:
					if ob.points[0][f2[0]][i]+1 == ob.points[0][f[0]][i]:
						for p in f:
							found = False
							for p2 in f2:
								if ob.points[0][p][l_3[0]] == ob.points[0][p2][l_3[0]] and ob.points[0][p][l_3[1]] == ob.points[0][p2][l_3[1]]:
									found = True
									break
							if not found:
								break
						if found:
							after = True
					elif ob.points[0][f2[0]][i]-1 == ob.points[0][f[0]][i]:
						for p in f:
							found = False
							for p2 in f2:
								if ob.points[0][p][l_3[0]] == ob.points[0][p2][l_3[0]] and ob.points[0][p][l_3[1]] == ob.points[0][p2][l_3[1]]:
									found = True
									break
							if not found:
								break
						if found:
							before = True
					if before and after:
						del_f.append(idx)
						#print("f {}".format(f))
						break
		if 0 <= idx % (len(ob.f)/100) <= 1 and idx != 1:
			print(idx/len(ob.f)*100 , '%')
	nb_keep = 0
	del_f.reverse()
	for e, idx in enumerate(del_f):
		f = ob.f[idx]
		pl = []
		keep = True
		#laregeur de 1 regarder si coter  = bords
		#pas 3 fois du même coté 4 points reliés
		for idx2, f2 in enumerate(ob.f):
			if not idx2 in del_f:
				nb_found = 0
				for p in f:
					if p in f2:
						nb_found += 1
						if nb_found == 2:
							break
				if nb_found == 2:
					s = -1
					for j in range(3):
						if ob.points[0][f2[0]][j] == ob.points[0][f2[1]][j] and ob.points[0][f2[2]][j] == ob.points[0][f2[0]][j] and ob.points[0][f2[3]][j] == ob.points[0][f2[0]][j]:
							s = j
							break
					pl.append(s)
					if pl.count(s) > 2:
						keep = False
						break
					pl.append([s,ob.points[0][f2[0]][s]])
					if pl.count([s,ob.points[0][f2[0]][s]]) > 1:
						keep = False
						break
		if len(pl) < 4:
			keep = False
		if keep:
			del_f.remove(idx)
			nb_keep += 1
		if 0 <= e % (len(del_f)/100) <= 1 and e != 1:
			print(e/len(del_f)*100 , '%')
	for idx in range(len(del_f)):
		del ob.f[del_f[len(del_f)-1-idx]]
	print('After Between f : ', len(ob.f))
	print('Keep f : ', nb_keep)
	ob.Save_f('hstairs2')
	return ob.f

class Objet3D():
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z
		self.f = []
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
			#    print([point.x, point.y, point.z])
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
		self.points = np.array([])
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
		self.points = np.array([points])

	def SSave(self, name = "Last_"):
		if name != "Last_" and self.name == "":
			self.name = name
		if self.name != "":
			name = self.name
		dir_name = "models"
		path = dir_name + '/'
		if not os.path.exists(dir_name):
			os.mkdir(dir_name)
		if not self.contour_opti:
			self.file = open(path + name + ".3DPiaf_s", 'w')
		else:
			self.file = open(path + name + ".3DPiaf_s", 'w')
		for point in self.points[0]:
			self.file.write("{},{},{}\n".format(int(point[0]), int(point[1]), int(point[2])))
		self.file.close()
		print("File Saved")

	def SLoad(self, name = "Last_", opti = False, console = False):
		if name != "Last_":
			self.name = name
		if self.name != "":
			name = self.name
		print(name)
		dir_name = "models"
		path = dir_name + '/'
		if opti:
			ext = ".3DPiafm"
		else:
			ext = ".3DPiaf_s"
		if os.path.exists(dir_name):
			if name + ext in os.listdir(dir_name):
				self.file = open(path + name + ext, 'r')
			else:
				self.file = open(name + ext, 'r')
		else:
			self.file = open(name + ext, 'r')
		self.points = np.array([])
		points = []
		for line in self.file:
			if len(line) <= 0:
				break
			if len(line.split(',')) >= 2:
				x, y, z = line.split(',')[:3]
				points.append([float(x), float(y), float(z)])
		self.file.close()
		self.points = np.array([points])
		print("SFile Loaded")
		try:
			self.Load_f(name=name)
		except:
			print('f file not loaded')
			pass

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
		#self.Save_f()
		print("File Saved")

	def Save_f(self, name="Last_"):
		if name != "Last_":
			self.name = name
		if self.name != "":
			name = self.name
		dir_name = "models"
		path = dir_name + '/'
		if not os.path.exists(dir_name):
			os.mkdir(dir_name)
		if not self.contour_opti:
			self.file = open(path + name + ".3DPiaff", 'w')
		else:
			self.file = open(path + name + ".3DPiaff", 'w')
		faces = self.f[:]
		for f in faces:
			self.file.write('{} {} {} {}'.format(f[0], f[1], f[2], f[3]) + '\n')
		print('f: ', len(faces))
		self.file.close()
		print("f File Saved")

	def Load(self, name = "Last_", opti = False, console = False):
		try:
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
			try:
				self.Load_f(name=name)
			except:
				print('f file not loaded')
				pass
			if not console:
				self.arraie()
		except:
			pass

	def Load_f(self, name = "Last_", opti = False, console = False):
		dir_name = "models"
		path = dir_name + '/'
		if opti:
			ext = ".3DPiaff"
		else:
			ext = ".3DPiaff"
		if os.path.exists(dir_name):
			if name + ext in os.listdir(dir_name):
				self.file = open(path + name + ext, 'r')
			else:
				self.file = open(name + ext, 'r')
		else:
			self.file = open(name + ext, 'r')
		self.f = []
		for line in self.file:
			if len(line) <= 0:
				break
			face = line.split()
			for idx, f in enumerate(face):
				face[idx] = int(f)
			self.f.append(face)
		self.file.close()
		print("f file Loaded")

	def minimizeContour(self):
		c_minimize = False
		for file in os.listdir(os.getcwd()):
			if file == "3Dminimize.exe":
				if self.name != "":
					name = self.name
				else:
					name = input("Name : ")
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
	def __init__(self, phi = 0, theta = np.pi/2, zoom = 2):
		self.phi = phi
		self.theta = theta
		self.r = zoom
		self.light = False

	def Rot(self, dphi = 0, dtheta = 0):
		self.phi += dphi
		self.theta += dtheta

def ConvertImageToBinary():
	name = input("png name:")
	nameNoExt = name.split('.')[0]
	import cv2
	img = cv2.imread(name,0)
	rvb_min = int(input("RVB min TRESH_BINARY: "))
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
	print("Commands : 'quit', 'minimize', 'load', 'save', 'convert', 'export', 'change'")
	while command != 'quit':
		command = input("Command : ")
		if command == 'help':
			print("Commands : 'quit', 'minimize', 'load', 'save', 'convert', 'export', 'change'")
		if command == 'minimize':
			ob.minimizeContour()
		if command == 'load':
			ob.Load(name = input("Load :"), console = True)
		if command == 'save':
			ob.Save(name = input("Save to :"))
		if command == 'convert':
			ConvertImageToBinary()
		if command == 'export':
			ExportToObj(ob)
		if command == 'change':
			namex = input("Name imagex:")
			namey = input("Name imagey:")
			namez = input("Name imagez:")
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
	name = input("Name of .obj without .obj:")
	nbpoint = chargement = 0
	totnbpoint = len(ob.points[0])
	name = "objects/" + name + ".obj"
	file = open(name, "w")
	n_face = 0
	del_p = []
	for idx in range(len(ob.points[0])):
		face = False
		for f in ob.f:
			if idx in f:
				face = True
		if not face:
			n_face += 1
			del_p.append(idx)

	for idx, f in enumerate(ob.f):
		for idx2, v in enumerate(f):
			less = 0
			for p in del_p:
				if p < v:
					less +=1
				elif p > v:
					break
			ob.f[idx][idx2]-=less
	for idx, point in enumerate(ob.points[0]):
		nbpoint += 1
		if nbpoint//(totnbpoint/100) > chargement:
			chargement = nbpoint//(totnbpoint/100)
			print("Model Loading : {} %".format(chargement))
		if not idx in del_p:
			file.write('v {0:.6f} '.format(point[0]))
			file.write('{0:.6f} '.format(point[1]))
			file.write('{0:.6f}\n'.format(point[2]))
	chargement = 0
	file.write('\n\n')
	ob.f.sort()
	for idx, f in enumerate(ob.f):
		if idx//(len(ob.f)/100) > chargement:
			chargement = idx//(len(ob.f)/100)
			print("Model Loading : {} %".format(chargement))
		"""
		file.write('f {}// {}// {}//\n'.format(f[0]+1, f[1]+1, f[3]+1))
		file.write('f {}// {}// {}//\n'.format(f[0]+1, f[2]+1, f[3]+1))
		"""
		file.write('f {} {} {}\n'.format(f[0]+1, f[1]+1, f[3]+1))
		file.write('f {} {} {}\n'.format(f[0]+1, f[2]+1, f[3]+1))
	file.close()
	print('Starting to export')
	print('n_face' , n_face)

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
