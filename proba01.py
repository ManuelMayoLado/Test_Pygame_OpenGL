# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

#CONSTANTES

ANCHO_CADRO = 30
ALTO_CADRO = 30

CADROS_FILA = 15
CADROS_COLUMNA = 10

ANCHO_VENTANA = CADROS_FILA * ANCHO_CADRO
ALTO_VENTANA = CADROS_COLUMNA * ALTO_CADRO

NUM_CADROS = CADROS_FILA * CADROS_COLUMNA

#VARIABLES

pos_camara = [0,0]
angulo = 0
cadricula = True
zoom = 0

lista_cadros = []
lista_rectangulos = []

for i in range(NUM_CADROS):
	lista_cadros.append(0)

#CLASES

class rectangulo:
	def __init__(self,pos,ancho,alto,color):
		self.pos = pos
		self.ancho = ancho
		self.alto = alto
		self.color = color

#FUNCIONS

def main():

	global cadricula
	global lista_rectangulos
	global lista_cadros
	global angulo
	global zoom
	global pos_camara
	
	pygame.init()
	ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), DOUBLEBUF|OPENGL)
	pygame.display.set_caption("Proba_OpenGL")
	init_gl()
	
	while True:
	
		reloj = pygame.time.Clock()
		
		#LIMPIAR VENTANA
		
		limpiar_ventana()

		#DEBUXAR
		
		if cadricula:
			for i in range(0,ANCHO_VENTANA+1,ANCHO_CADRO):
				debuxar_linha([i,0],[i,ALTO_VENTANA])
			for i in range(0,ALTO_VENTANA+1,ALTO_CADRO):
				debuxar_linha([0,i],[ANCHO_VENTANA,i])
		
		for r in lista_cadros:
			if r:
				debuxar_rectangulo(r)
		
			#MOUSE
			
		pos_mouse = pygame.mouse.get_pos()
		
		ancho_ventana_gl = ANCHO_VENTANA+zoom*2
		alto_ventana_gl = ALTO_VENTANA+zoom*2
		
		marco_zoom_x = zoom * ANCHO_VENTANA / ancho_ventana_gl
		marco_zoom_y = zoom * ALTO_VENTANA / alto_ventana_gl
		
		if ((pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]) and
			(pos_mouse[0]-pos_camara[0] > marco_zoom_x and pos_mouse[0]-pos_camara[0] < ANCHO_VENTANA-marco_zoom_x
			and pos_mouse[1]+pos_camara[1] > marco_zoom_y and pos_mouse[1]+pos_camara[1] < ALTO_VENTANA-marco_zoom_y)):
			
			ancho_rejilla = ANCHO_VENTANA * ANCHO_VENTANA / ancho_ventana_gl
			alto_rejilla = ALTO_VENTANA * ALTO_VENTANA / alto_ventana_gl
			
			ancho_cadro_gl = ancho_rejilla / CADROS_FILA
			alto_cadro_gl = alto_rejilla / CADROS_COLUMNA
		
			lista_rectangulos = []
			cadro_presionado = [(pos_mouse[0]-pos_camara[0]-marco_zoom_x)/ancho_cadro_gl,(pos_mouse[1]+pos_camara[1]-marco_zoom_y)/alto_cadro_gl]
			indice = pos_a_indice(cadro_presionado)
			
			if pygame.mouse.get_pressed()[0] and (indice < len(lista_cadros) and indice >= 0):
				lista_cadros[indice] = (rectangulo
					([cadro_presionado[0]*ANCHO_CADRO,abs(cadro_presionado[1]*ALTO_CADRO-(ALTO_VENTANA-ALTO_CADRO))]
					,ANCHO_CADRO,ALTO_CADRO,[1,random.uniform(0,0.8),random.uniform(0,0.8)]))
			if pygame.mouse.get_pressed()[2]:
				lista_cadros[indice] = 0
				
				#TECLAS
				
		tecla_pulsada = pygame.key.get_pressed()
		
		if tecla_pulsada[K_UP] or tecla_pulsada[K_w]:
			pos_camara[1] -= ALTO_CADRO / 2
			
		if tecla_pulsada[K_DOWN] or tecla_pulsada[K_s]:
			pos_camara[1] += ALTO_CADRO / 2
		
		if tecla_pulsada[K_LEFT] or tecla_pulsada[K_a]:
			pos_camara[0] += ANCHO_CADRO / 2
		
		if tecla_pulsada[K_RIGHT] or tecla_pulsada[K_d]:
			pos_camara[0] -= ANCHO_CADRO / 2
		
		if tecla_pulsada[K_r]:
			angulo -= 1
		if tecla_pulsada[K_e]:
			angulo += 1
		
			
		for event in pygame.event.get():
		
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 4:
					zoom -= ANCHO_CADRO / 2
				if event.button == 5:
					zoom += ANCHO_CADRO / 2
				zoom = max(-100,zoom)
				zoom = min(200,zoom)
		
			if event.type == pygame.KEYDOWN:
			
				if event.key == pygame.K_c:
					if cadricula:
						cadricula = False
					else:
						cadricula = True
						
				if event.key == pygame.K_DELETE:
					zoom = 0
					angulo = 0
					pos_camara = [0,0]
		
			if event.type == pygame.QUIT:
				pygame.quit()
				return
				
		#ACTUALIZAR VENTANA
		
		pygame.display.flip()
				
		reloj.tick(60)

#VARIAS

def pos_a_indice(pos):
	return pos[0] + pos[1] * CADROS_FILA
		
#OPENGL		

def init_gl():
	glViewport(0, 0, ANCHO_VENTANA, ALTO_VENTANA)
	glClearColor(1, 1, 1, 1)
	glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
	
def limpiar_ventana():
	glClear(GL_COLOR_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glRotatef(angulo,0,0,1)
	gluOrtho2D(-zoom, ANCHO_VENTANA+zoom, -zoom, ALTO_VENTANA+zoom)
	glTranslatef(0 + pos_camara[0],0 + pos_camara[1], 0)
	glMatrixMode(GL_MODELVIEW)
	
def debuxar_rectangulo(rect):
	glLoadIdentity()
	glColor3f(rect.color[0], rect.color[1], rect.color[2])
	glBegin(GL_QUADS)
	glVertex2f(rect.pos[0], rect.pos[1])
	glVertex2f(rect.pos[0]+rect.ancho, rect.pos[1])
	glVertex2f(rect.pos[0]+rect.ancho, rect.pos[1]+rect.alto)
	glVertex2f(rect.pos[0], rect.pos[1]+rect.alto)
	glEnd()
	
def debuxar_linha(pos1,pos2):
	glLineWidth(1); 
	glColor4f(0, 0, 0, 0.3);
	glBegin(GL_LINES);
	glVertex2f(pos1[0], pos1[1]);
	glVertex2f(pos2[0], pos2[1]);
	glEnd();
	
if __name__ == '__main__':
	main()