# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

#CONSTANTES

ANCHO_VENTANA = 600
ALTO_VENTANA = 400

COLOR_FONDO = 0

#VARIABLES

pos_camara = [0,0]

lista_vertices = []
lista_poligonos = []

descanso_mouse = 0

#CLASES

class Poligono:
	def __init__(self,listaVertices,color):
		self.listaVertices = listaVertices
		self.color = color

#MAIN

def main():

	global pos_camara
	global lista_vertices
	global lista_poligonos
	global descanso_mouse
	
	pygame.init()
	ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), DOUBLEBUF|OPENGL)
	pygame.display.set_caption("Proba_OpenGL")
	init_gl()
	
	while True:
	
		reloj = pygame.time.Clock()
		
		#LIMPIAR VENTANA ######
		
		limpiar_ventana()

		#DEBUXAR ######
		
		debuxar_lienzo()
		
		for i in lista_poligonos:
			debuxar_poligono(i.listaVertices,i.color)
		
		debuxar_linhas_poligono()
		
		for i in lista_vertices:
			debuxar_punto(i)
			
		debuxar_cruz_central()
		
		#############################################################
		#EVENTOS ####################################################
		#############################################################
		
		#MOUSE ######
		
		if descanso_mouse > 0:
			descanso_mouse -= 1
		
		if descanso_mouse == 0:
			pos_mouse = pygame.mouse.get_pos()
		
		if descanso_mouse == 0:
			teclas_mouse_pulsadas = pygame.mouse.get_pressed()
		
		if descanso_mouse == 0 and teclas_mouse_pulsadas[0]:
			lista_vertices.append([pos_mouse[0]-pos_camara[0],abs(pos_mouse[1]-ALTO_VENTANA)-pos_camara[1]])
			descanso_mouse = 10
				 
		#TECLAS ######
				
		tecla_pulsada = pygame.key.get_pressed()
		
		if tecla_pulsada[K_UP] or tecla_pulsada[K_w]:
			pos_camara[1] -= 5
			
		if tecla_pulsada[K_DOWN] or tecla_pulsada[K_s]:
			pos_camara[1] += 5
		
		if tecla_pulsada[K_LEFT] or tecla_pulsada[K_a]:
			pos_camara[0] += 5
		
		if tecla_pulsada[K_RIGHT] or tecla_pulsada[K_d]:
			pos_camara[0] -= 5
			
		for event in pygame.event.get():
		
			if event.type == pygame.KEYDOWN:
				
				if event.key == pygame.K_RETURN:
					pos_camara = [0,0]
					
				if event.key == pygame.K_DELETE:
					if len(lista_vertices) == 0:	
						lista_poligonos = []
					lista_vertices = []
					
				if event.key == pygame.K_SPACE:
					if len(lista_vertices) > 2:
						lista_poligonos.append(Poligono(lista_vertices,[0.5,0,0,1]))
					lista_vertices = []
		
			if event.type == pygame.QUIT:
				pygame.quit()
				return
				
		#ACTUALIZAR VENTANA ######
		
		pygame.display.flip()
		
		inicio = False
				
		reloj.tick(60)

##############################################################
#OPENGL	######################################################
##############################################################

def init_gl():
	glViewport(0, 0, ANCHO_VENTANA, ALTO_VENTANA)
	glClearColor(COLOR_FONDO, COLOR_FONDO, COLOR_FONDO, 1)
	glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
	
def limpiar_ventana():
	glClear(GL_COLOR_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluOrtho2D(0, ANCHO_VENTANA, 0, ALTO_VENTANA)
	glTranslatef(0 + pos_camara[0],0 + pos_camara[1], 0)
	glMatrixMode(GL_MODELVIEW)
	
def debuxar_rect(pos,ancho,alto,color):
	glColor4f(color[0], color[1], color[2], color[3])
	glBegin(GL_QUADS)
	glVertex2f(pos[0], pos[1])
	glVertex2f(pos[0]+ancho, pos[1])
	glVertex2f(pos[0]+ancho, pos[1]+alto)
	glVertex2f(pos[0], pos[1]+alto)
	glEnd()
	
def debuxar_lienzo():
	for i in range(10):
		engadido = i*5
		debuxar_rect([0-engadido/2,0-engadido/2],ANCHO_VENTANA+engadido,ALTO_VENTANA+engadido,[0.7,0.7,0.7,1-i/10.])
	
def debuxar_punto(pos):
	glPointSize(2)
	glColor4f(1, 0, 0, 1)
	glBegin(GL_POINTS)
	glVertex2f(pos[0], pos[1])
	glEnd()
	
def debuxar_poligono(listaVer,color):
	glColor4f(color[0],color[1],color[2],color[3])
	glBegin(GL_POLYGON)
	for i in listaVer:
		glVertex2f(i[0],i[1])
	glEnd()
	
def debuxar_linhas_poligono():
	if len(lista_vertices) > 1:
		glColor4f(1, 1, 1, 0.5)
		glBegin(GL_LINES)
		for i in range(len(lista_vertices)):
			glVertex2f(lista_vertices[i-1][0], lista_vertices[i-1][1])
			glVertex2f(lista_vertices[i][0], lista_vertices[i][1])
		glEnd()
	
def debuxar_cruz_central():
	glLineWidth(1)
	glColor4f(1, 1, 1, 0.5)
	glBegin(GL_LINES)
	glVertex2f(ANCHO_VENTANA/2, ALTO_VENTANA/2-10)
	glVertex2f(ANCHO_VENTANA/2, ALTO_VENTANA/2+10)
	glVertex2f(ANCHO_VENTANA/2-10, ALTO_VENTANA/2)
	glVertex2f(ANCHO_VENTANA/2+10, ALTO_VENTANA/2)
	glEnd()
	
if __name__ == '__main__':
	main()