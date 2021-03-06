#Se importan librerias a ocupar

from OpenGL.GL import *

import numpy as np

import scene_graph as sg
import easy_shaders as es
import basic_shapes as bs
import transformations as tr
from capasShape import *


def createPiezaTrasera(color):
	vertexData = np.array([
		 1.5,  2.5, 0, color[0]-0.05, color[1]-0.05, color[2]-0.05,
		 0.5,  2.5, 0, color[0]-0.05, color[1]-0.05, color[2]-0.05,
		-2.5,  1.5, 0, color[0]-0.05, color[1]-0.05, color[2]-0.05,
		 -3 , -0.5, 0, color[0], color[1], color[2], 
		-1.5, -1.5, 0, color[0], color[1], color[2], 
		-1  , -0.5, 0, color[0], color[1], color[2], 
		 0  ,    0, 0, color[0], color[1], color[2], 
		 1  , -0.5, 0, color[0], color[1], color[2], 
		 1.5, -1.5, 0, color[0], color[1], color[2], 
		 2.5, -1.5, 0, color[0], color[1], color[2], 
		 1  ,    1, 0, color[0], color[1], color[2], 
		 2  ,    3, 0, color[0], color[1], color[2], 
		 0.5,  2.5, 0, color[0], color[1], color[2], ],dtype=np.float32)
	indices = np.array(
		[0, 1, 6,
		 1, 2, 6,
		 6, 2, 5,
		 5, 2, 3,
		 5, 3, 4,
		 0, 6, 7,
		 9, 8, 10,
		 10, 8, 7,
		 0, 11, 12,
		 12, 1, 2], dtype=np.uint32)
	return bs.Shape(vertexData,indices)

def createPiezaCentral(color):
	vertexData = np.array([
		 0.5,   2, 0, color[0]-0.05, color[1]-0.05, color[2]-0.05, 
		-2.5,   2, 0, color[0]-0.05, color[1]-0.05, color[2]-0.05, 
		-2.9, 0.2, 0, color[0], color[1], color[2], 
		-1.5,  -2, 0, color[0], color[1], color[2], 
		   2,  -2, 0, color[0], color[1], color[2], 
		   3, 0.5, 0, color[0], color[1], color[2], 
		  -2, 2.5, 0, color[0], color[1], color[2], 
		   1,   3, 0, color[0], color[1], color[2], 
		 3.5,   2, 0, color[0], color[1], color[2]], dtype=np.float32)
	indice = np.array(
		[0, 5, 4,
		 0, 4, 3,
		 0, 3, 2,
		 0, 1, 2,
		 0, 1, 6,
		 0, 7, 6,
		 5, 0, 7,
		 5, 8, 7], dtype=np.uint32)
	return bs.Shape(vertexData,indice)

def createPiezaDelantera(color):
	vertexData = np.array([
		   0,   0,  0, color[0], color[1], color[2], 
		   1, -0.5, 0, color[0], color[1], color[2], 
		 1.5, -1.5, 0, color[0], color[1], color[2], 
		   3, -1.5, 0, color[0], color[1], color[2], 
		   4, -0.5, 0, color[0], color[1], color[2], 
		 3.5,    1, 0, color[0]+0.1, color[1]+0.1, color[2]+0.1, 
		   2,    2, 0, color[0]+0.1, color[1]+0.1, color[2]+0.1, 
		-1.5,  2.5, 0, color[0], color[1], color[2], 
		  -2,    1, 0, color[0], color[1], color[2], 
		-2.7, -0.5, 0, color[0], color[1], color[2], 
		  -3, -1.5, 0, color[0], color[1], color[2], 
		-1.5, -1.5, 0, color[0], color[1], color[2], 
		 - 1, -0.5, 0, color[0], color[1], color[2], ], dtype=np.float32)
	indices = np.array(
		[0, 6, 7,
		 0, 7, 8,
		 0, 8, 12,
		 8, 12, 9,
		 9, 12, 10,
		 10, 11, 12,
		 0, 5, 6,
		 0, 5, 4,
		 0, 4, 3,
		 3, 2, 1], dtype=np.uint32)
	return bs.Shape(vertexData,indices)

##VEHICULO: CARROCERIA, RUEDAS, SOMBRA, LUZPISO, PULSO
		  ##CARROCERIA: Partes (TRASERA, CENTRAL, DELANTERA), VENTANAS, DISE??O, SOMBRARUEDA, FOCOAUTO
def vehiculo(color):
	parte1 = es.toGPUShape(createPiezaTrasera(color))
	parte2 = es.toGPUShape(createPiezaCentral(color))
	parte3 = es.toGPUShape(createPiezaDelantera(color))
	luz = es.toGPUShape(createQuad([1,1,1]))
	grayQuad = es.toGPUShape(createQuad([0.08,0.08,0.08]))
	
	#Ensamblanje de piezas traseras, central y delantera
	piezaT = sg.SceneGraphNode("piezaTrasera")
	piezaT.transform = tr.matmul([tr.translate(-0.4,-0.05,0),tr.uniformScale(0.1)])
	piezaT.childs += [parte1]
	piezaC = sg.SceneGraphNode("piezaCentral")
	piezaC.transform = tr.uniformScale(0.1)
	piezaC.childs += [parte2]
	piezaD = sg.SceneGraphNode("piezaDelantera")
	piezaD.transform = tr.matmul([tr.translate(0.5,-0.05,0),tr.uniformScale(0.1)])
	piezaD.childs += [parte3]

	#Ensamblaje de foco
	focoAuto = sg.SceneGraphNode("focoAuto")
	focoAuto.transform = tr.matmul([tr.translate(0.84,-0.05,0), tr.shearing(-0.3,0,0,0,0,0), tr.scale(0.07,0.14,0.1)])
	focoAuto.childs += [luz]

	#Creacion de luzPiso, sombraPiso y pulso (elementos ajenos al autos que se mueven junto a el)
	luzPiso = sg.SceneGraphNode("luzPiso")
	luzPiso.childs += [circle(20,0.1,[0.5,0.5,0.5])]
	sombraPiso = sg.SceneGraphNode("sombraPiso")
	sombraPiso.childs += [grayQuad]
	pulso = sg.SceneGraphNode("pulso")
	for j in range (2):
		newNode = sg.SceneGraphNode("pul"+str(j+1))
		newNode.transform = tr.matmul([tr.translate(0.5 if j==0 else -0.4, 0.08, 0), tr.scale(0.65, 0.25, 1)])
		newNode.childs += [ring(20, 0.08, 0.06, [0, 1, 1])]			
		pulso.childs += [newNode]

	#Ensamblaje de ruedas costado derecho (visibles)
	ruedaTrasera = sg.SceneGraphNode("ruedaTrasera")
	ruedaTrasera.childs += [rueda()]
	ruedaDelantera = sg.SceneGraphNode("ruedaDelantera")
	ruedaDelantera.childs += [rueda()]
	ruedas = sg.SceneGraphNode("ruedas")
	ruedas.childs += [ruedaTrasera]
	ruedas.childs += [ruedaDelantera]

	#Ensamblaje de zonas tras las ruedas y ruedas costado izquierda (no visibles)
	piezaBI = sg.SceneGraphNode("piezaBajoIzq")
	piezaBI.transform = tr.matmul([tr.translate(-0.4,-0.2,0), tr.rotationZ(99*np.pi/180), tr.uniformScale(0.6)])
	piezaBI.childs += [semiCircle(20, 0.08, [0.02, 0.02, 0.02])]
	piezaBD = sg.SceneGraphNode("piezaBajoDer")
	piezaBD.transform = tr.matmul([tr.translate(0.5,-0.2,0), tr.rotationZ(99*np.pi/180), tr.uniformScale(0.6)])
	piezaBD.childs += [semiCircle(20, 0.08, [0.02, 0.02, 0.02])]
	ruedaSombra1 = sg.SceneGraphNode("ruedaSombra1")
	ruedaSombra1.transform = tr.translate(0.6,-0.14,0)
	ruedaSombra1.childs += [circle(20, 0.034, [0.01, 0.01, 0.01])]
	ruedaSombra2 = sg.SceneGraphNode("ruedaSombra2")
	ruedaSombra2.transform = tr.translate(-0.3,-0.14,0)
	ruedaSombra2.childs += [circle(20, 0.034, [0.01, 0.01, 0.01])]
	ruedaSombra = sg.SceneGraphNode("ruedaSombra")
	ruedaSombra.childs += [ruedaSombra1]
	ruedaSombra.childs += [ruedaSombra2]
	ruedaSombra.childs += [piezaBI]
	ruedaSombra.childs += [piezaBD]

	#Ensamblaje de carroceria
	carroceria = sg.SceneGraphNode("carroceria")
	carroceria.childs += [ruedaSombra]
	carroceria.childs += [piezaT]
	carroceria.childs += [piezaC]
	carroceria.childs += [piezaD]
	carroceria.childs += [ventanas()]
	carroceria.childs += [dise??o(color)]
	carroceria.childs += [focoAuto]

	#Ensamblaje de vehiculo completo
	vehiculo = sg.SceneGraphNode("vehiculo")
	vehiculo.transform = tr.matmul([tr.translate(-0.4,-0.6,0), tr.uniformScale(0.7)])
	vehiculo.childs += [sombraPiso]
	vehiculo.childs += [pulso]
	vehiculo.childs += [carroceria]
	vehiculo.childs += [ruedas]
	vehiculo.childs += [luzPiso]
	
	return vehiculo

#Crea un anillo a partir de un segmento de triangulo
def ring(n, d, x, color):
	t=es.toGPUShape(createSeccionTriangle(n, d, x, color))
	anillo = sg.SceneGraphNode("anillo")

	for i in range(n):
		newNode = sg.SceneGraphNode("cir"+str(i+1))
		newNode.transform = tr.rotationZ(i*np.pi*(360/n)/180)	
		newNode.childs += [t]
		anillo.childs += [newNode]
	return anillo

#Crea un circulo a partir de un triangulo
def circle(n, d, color):
	t=es.toGPUShape(createTriangle2(n, d, color))
	circulo = sg.SceneGraphNode("circulo")
	for i in range(n):
		newNode = sg.SceneGraphNode("cir"+str(i+1))
		newNode.transform = tr.rotationZ(i*np.pi*(360/n)/180)	
		newNode.childs += [t]
		circulo.childs += [newNode]
	return circulo

#Crea un semi circulo a partir de un trianglo
def semiCircle(n, d, color):
	t=es.toGPUShape(createTriangle2(n, d, color))
	semiCirculo = sg.SceneGraphNode("semiCirculo")
	for i in range(n//2):
		newNode = sg.SceneGraphNode("scir"+str(i+1))
		newNode.transform = tr.rotationZ(i*np.pi*(360/n)/180)	
		newNode.childs += [t]
		semiCirculo.childs += [newNode]
	return semiCirculo

def rueda():
	grayCircle = circle(20, 0.08, [0.8, 0.8, 0.8])
	blackCircle = circle(20, 0.08, [0.05, 0.05, 0.05])
	line = es.toGPUShape(createLine([0.2,0.2,0.2]))

	#Crea "neumatico" de la rueda
	neumatico = sg.SceneGraphNode("neumatico")
	neumatico.transform = tr.uniformScale(1)
	neumatico.childs += [blackCircle]
	#Crea "llanta" de la rueda
	llanta = sg.SceneGraphNode("llanta")
	llanta.transform = tr.uniformScale(0.65)
	llanta.childs += [grayCircle]

	#Ensambla ambas partes en una rueda
	rueda = sg.SceneGraphNode("rueda")
	rueda.transform = tr.uniformScale(0.5)

	rueda.childs += [neumatico]
	rueda.childs += [llanta]

	#Crea lineas dentro de rueda
	for i in range(6):
		lineaRueda = sg.SceneGraphNode("lineaRueda")
		lineaRueda.transform = tr.matmul([tr.rotationZ(i*60*np.pi/180),tr.translate(0.1,0,0),tr.scale(0.15,0.15,1)])
		lineaRueda.childs += [line]
		rueda.childs += [lineaRueda]
	return rueda

def ventanas():
	quad = es.toGPUShape(bs.createColorQuad(0.08, 0.08, 0.08))
	triangulo = es.toGPUShape(createTriangle([0.08, 0.08, 0.08]))

	#Ensambla ventanas del frente
	ventanaFrente = sg.SceneGraphNode("ventanaFrente")
	ventanaFrente.transform = tr.matmul([tr.translate(0.21,0.2,0),tr.rotationZ(157*np.pi/180),tr.shearing(-0.1,0,0,0,0,0),tr.scale(0.3,0.1,1)])
	ventanaFrente.childs += [quad]
	
	#Ensmabla ventanas del costado
	ventanaLado1 = sg.SceneGraphNode("ventanaLado1")
	ventanaLado1.transform = tr.matmul([tr.translate(0.07, 0.11, 0), tr.scale(0.48, 0.13, 1)])
	ventanaLado1.childs += [triangulo]
	ventanaLado2 = sg.SceneGraphNode("ventanaLado2")
	ventanaLado2.transform = tr.matmul([tr.translate(-0.04, 0.11, 0),tr.rotationZ(10*np.pi/180),tr.shearing(0,0,0,0,0,0),tr.scale(0.25, 0.09, 1)])
	ventanaLado2.childs += [quad]
	ventanaLado3 = sg.SceneGraphNode("ventanaLado3")
	ventanaLado3.transform = tr.matmul([tr.translate(-0.17, 0.09, 0), tr.rotationZ(4*np.pi/108), tr.scale(0.1, 0.09, 1)])
	ventanaLado3.childs += [triangulo]
	ventanaLado = sg.SceneGraphNode("ventanaLado")
	ventanaLado.childs += [ventanaLado1]
	ventanaLado.childs += [ventanaLado2]
	ventanaLado.childs += [ventanaLado3]

	#Ensambla ventana de atras
	ventanaAtras = sg.SceneGraphNode("ventanaAtras")
	ventanaAtras.transform = tr.matmul([tr.translate(-0.33, 0.07, 0),tr.rotationZ(210*np.pi/180),tr.uniformScale(0.8),tr.scale(0.3, 0.1, 1)])
	ventanaAtras.childs += [triangulo]

	#Ensambla todas las ventanas
	ventanas = sg.SceneGraphNode("ventanas")
	ventanas.childs += [ventanaFrente]
	ventanas.childs += [ventanaLado]
	ventanas.childs += [ventanaAtras]
	return ventanas

#Crea un dise??o simple sobre el vehiculo a partir de "lineas"
def dise??o(color):
	blackLine = es.toGPUShape(createLine([color[0]*0,color[1]*0,color[2]*0]))
	grayLine = es.toGPUShape(createLine([color[0]*0.2,color[1]*0.2,color[2]*0.2]))

	l1= sg.SceneGraphNode("downLine")
	l1.transform = tr.matmul([tr.translate(0.06,-0.1,0),tr.scale(1.5,0.5,1)])
	l1.childs += [blackLine]
	l3= sg.SceneGraphNode("backLine")
	l3.transform = tr.matmul([tr.translate(0.06,-0.2,0),tr.scale(0.64,1,1)])
	l3.childs += [blackLine]
	l2 = sg.SceneGraphNode("RigtLine")
	l2.transform = tr.matmul([tr.translate(0.3,0,0),tr.rotationZ(70*np.pi/180),tr.scale(0.4,0.15,1)])
	l2.childs += [grayLine]
	l4 = sg.SceneGraphNode("LeftLine")
	l4.transform = tr.matmul([tr.translate(-0.21,-0.07,0),tr.rotationZ(120*np.pi/180),tr.scale(0.25,0.15,1)])
	l4.childs += [grayLine]
	l5 = sg.SceneGraphNode("UpLine1")
	l5.transform = tr.matmul([tr.translate(0.2,0.15,0),tr.rotationZ(155*np.pi/180),tr.scale(0.3,0.15,1)])
	l5.childs += [grayLine]
	l6= sg.SceneGraphNode("OnLine2")
	l6.transform = tr.matmul([tr.translate(-0.07,0.19,0),tr.rotationZ(10*np.pi/180),tr.scale(0.28,0.15,1)])
	l6.childs += [grayLine]
	l7 = sg.SceneGraphNode("UpLine3")
	l7.transform = tr.matmul([tr.translate(-0.24,0.1,0),tr.rotationZ(65*np.pi/180),tr.scale(0.15,0.15,1)])
	l7.childs += [grayLine]
	l8 = sg.SceneGraphNode("UpLine4")
	l8.transform = tr.matmul([tr.translate(0.55,0.06,0),tr.rotationZ(-8*np.pi/180),tr.scale(0.5,0.15,1)])
	l8.childs += [grayLine]

	dise??o = sg.SceneGraphNode("Dise??o")
	dise??o.childs += [l4]
	dise??o.childs += [l2]
	dise??o.childs += [l5]
	dise??o.childs += [l1]
	dise??o.childs += [l3]
	dise??o.childs += [l6]
	dise??o.childs += [l7]
	dise??o.childs += [l8]
	
	return dise??o

#BASIC SHAPES
def createLine(color):
	vertexData = np.array([
		-0.5,  0.025, 0, color[0], color[1], color[2],
		-0.5, -0.025, 0, color[0], color[1], color[2],
		 0.5, -0.025, 0, color[0], color[1], color[2],
		 0.5,  0.025, 0, color[0], color[1], color[2]], dtype=np.float32)
	indices = np.array(
		[0, 1, 2,
		2, 3, 0], dtype=np.uint32)
	return bs.Shape(vertexData, indices)

def createTriangle(color):
	vertexData = np.array([
		-0.5, -0.5, 0, color[0], color[1], color[2],
		 0.5, -0.5, 0, color[0], color[1], color[2],
		   0,  0.5, 0, color[0], color[1], color[2]], dtype=np.float32)
	indices = np.array(
		[0, 1, 2], dtype=np.uint32)
	return bs.Shape(vertexData, indices)

def createTriangle2(n, d, color):
	alpha=np.pi*((360/n)/2)/180
	p=d/(2*np.tan(alpha))
	vertexData = np.array([
	       0,  0, 0, color[0], color[1], color[2],
		 d/2, -p, 0, color[0]-0.1, color[1]-0.1, color[2]-0.1,
		-d/2, -p, 0, color[0]-0.1, color[1]-0.1, color[2]-0.1], dtype=np.float32)
	indices = np.array(
	[0, 1, 2], dtype=np.uint32)
	return bs.Shape(vertexData, indices)

def createSeccionTriangle(n, d, x, color):
	alpha=np.pi*((360/n)/2)/180
	p=d/(2*np.tan(alpha))
	q=x/(2*np.tan(alpha))
	vertexData = np.array([
		 d/2, -p, 0, color[0], color[1], color[2],
		-d/2, -p, 0, color[0], color[1], color[2],
		-x/2, -q, 0, color[0]-0.8, color[1]-0.8, color[2]-0.8,
		 x/2, -q, 0, color[0]-0.8, color[1]-0.8, color[2]-0.8], dtype=np.float32)
	indices = np.array(
	[0, 1, 2,
	 2, 3, 0], dtype=np.uint32)
	return bs.Shape(vertexData, indices)

def createQuad(color, inicio=[0,0,0]):
    vertexData = np.array([
        inicio[0]-0.5, inicio[1]-0.5, 0.0, color[0], color[1], color[2],
        inicio[0]+0.5, inicio[1]-0.5, 0.0, color[0], color[1], color[2],
        inicio[0]+0.5, inicio[1]+0.5, 0.0, color[0], color[1], color[2],
        inicio[0]-0.5, inicio[1]+0.5, 0.0, color[0], color[1], color[2]], dtype=np.float32)
    indices = np.array(
		[0, 1, 2,
         2, 3, 0], dtype=np.uint32)
    return bs.Shape(vertexData,indices)




