
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from used import *


def mainEditor(fenetre, imagex, imagey, imagez):
	"""
	TEXT_SURF = BASICFONT.render(axe + str('%d' %zoom), True, TEXTCOLOR)
	list_points = []
	for point in ob.contour:
		if point.x != None and point.y != None and point.z != None:
			posx = point.x*sin(cam.phi) + point.y*cos(cam.phi)
			posy = point.y*cos(cam.theta) + point.z*sin(cam.theta)
			list_points.append(Point((0,0,255), x = posx*zoomx+ middlehight, y = posy*zoomy + middlewheight, size = zoom))
	"""
	black_surf, black_rect = makeSquarre(BACK, size = WINDOWWIDTH*3)
	IMAGEX_SURF, IMAGEX_RECT = makeText('X', TEXTCOLOR, TILECOLOR, WINDOWWIDTH/2 - 250, 40)
	IMAGEY_SURF, IMAGEY_RECT = makeText('Y', TEXTCOLOR, TILECOLOR, WINDOWWIDTH/2 - 150, 40)
	IMAGEZ_SURF, IMAGEZ_RECT = makeText('Z', TEXTCOLOR, TILECOLOR, WINDOWWIDTH/2 - 30, 40)
	RETURN_SURF, RETURN_RECT = makeText('RETURN', TEXTCOLOR, TILECOLOR, WINDOWWIDTH/2 + 120, 40)
	fenetre.blit(black_surf, black_rect)
	fenetre.blit(IMAGEX_SURF, IMAGEX_RECT)
	fenetre.blit(IMAGEY_SURF, IMAGEY_RECT)
	fenetre.blit(IMAGEZ_SURF, IMAGEZ_RECT)
	fenetre.blit(RETURN_SURF, RETURN_RECT)
	#Rafraichissement
	pygame.display.flip()
	continuer = 1
	while continuer:
		for event in pygame.event.get():    #Attente des événements
			if event.type == QUIT:
				continuer = 0
				return [imagex, imagey, imagez]
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					continuer = 0
					return [imagex, imagey, imagez]
			if event.type == MOUSEBUTTONDOWN:
				if IMAGEX_RECT.collidepoint(event.pos):
					imagex = drawImage(fenetre, imagex)
					fenetre.blit(black_surf, black_rect)
					fenetre.blit(IMAGEX_SURF, IMAGEX_RECT)
					fenetre.blit(IMAGEY_SURF, IMAGEY_RECT)
					fenetre.blit(IMAGEZ_SURF, IMAGEZ_RECT)
					fenetre.blit(RETURN_SURF, RETURN_RECT)
					#Rafraichissement
					pygame.display.flip()
				if IMAGEY_RECT.collidepoint(event.pos):
					imagey = drawImage(fenetre, imagey)
					fenetre.blit(black_surf, black_rect)
					fenetre.blit(IMAGEX_SURF, IMAGEX_RECT)
					fenetre.blit(IMAGEY_SURF, IMAGEY_RECT)
					fenetre.blit(IMAGEZ_SURF, IMAGEZ_RECT)
					fenetre.blit(RETURN_SURF, RETURN_RECT)
					#Rafraichissement
					pygame.display.flip()
				if IMAGEZ_RECT.collidepoint(event.pos):
					imagez = drawImage(fenetre, imagez)
					fenetre.blit(black_surf, black_rect)
					fenetre.blit(IMAGEX_SURF, IMAGEX_RECT)
					fenetre.blit(IMAGEY_SURF, IMAGEY_RECT)
					fenetre.blit(IMAGEZ_SURF, IMAGEZ_RECT)
					fenetre.blit(RETURN_SURF, RETURN_RECT)
					#Rafraichissement
					pygame.display.flip()
				if RETURN_RECT.collidepoint(event.pos):
					return [imagex, imagey, imagez]

def drawImage(fenetre, image):
	list_points = []
	coord = []
	newImage = [['0']*(WINDOWWIDTH/2)]*(WINDOWWHEIGHT/2)
	if image == None:
		image = [['1']*(WINDOWWIDTH/2)]*(WINDOWWHEIGHT/2)
	"""
	for y in range(len(image)):
		for x in range(len(image[0])):
			if image[y][x] == '1':
				coord.append([x,y])
				newImage[y][x] = '1'
	"""
	for point in image:
		list_points.append(Point((0,0,255), x = (int(point[0])+1)*10, y = (int(point[1])+1)*10, size = 10))
		newImage[int(point[1])][int(point[0])] = '1'
	continuer = 1
	black_surf, black_rect = makeSquarre(BACK, size = WINDOWWIDTH*3)
	create_down = False
	erase_down = False
	while continuer:
		for event in pygame.event.get():    #Attente des événements
			if event.type == QUIT:
				continuer = 0
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					continuer = 0
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					x, y = pygame.mouse.get_pos()
					if x//10 > 0 and y//10 > 0:
						if image.count([x//10-1,y//10-1]) == 0:
							image.append([x//10-1,y//10-1])
						list_points.append(Point((0,0,255), x = x//10*10, y = y//10*10, size = 10))
						newImage[y//10][x//10] = '1'
					create_down = True
				elif event.button == 3:
					x, y = pygame.mouse.get_pos()
					if x//10 > 0 and y//10 > 0:
						if image.count([x//10-1,y//10-1]) != 0:
							image.remove([x//10 -1,y//10-1])
						for point in list_points:
							if point.x == x//10*10 and point.y == y//10*10:
								list_points.remove(point)
								break
						newImage[y//10][x//10] = '0'
					erase_down = True
			elif event.type == MOUSEMOTION:
				if create_down and not erase_down:
					x, y = pygame.mouse.get_pos()
					if x//10 > 0 and y//10 > 0:
						if image.count([x//10-1,y//10-1]) == 0:
							image.append([x//10-1,y//10-1])
						list_points.append(Point((0,0,255), x = x//10*10, y = y//10*10, size = 10))
						newImage[y//10][x//10] = '1'
				elif erase_down and not create_down:
					x, y = pygame.mouse.get_pos()
					if x//10 > 0 and y//10 > 0:
						if image.count([x//10-1,y//10-1]) != 0:
							image.remove([x//10 -1,y//10-1])
						for point in list_points:
							if point.x == x//10*10 and point.y == y//10*10:
								list_points.remove(point)
								break
						newImage[y//10][x//10] = '0'
			elif event.type == MOUSEBUTTONUP:
				if event.button == 1:
					create_down = False
				elif event.button == 3:
					erase_down = False
		fenetre.blit(black_surf, black_rect)
		for point in list_points:
			point.fblit(fenetre)
		#Rafraichissement
		pygame.display.flip()
	return image

