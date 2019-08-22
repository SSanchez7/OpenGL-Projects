#Se importan librerias a ocupar

from OpenGL.GL import *

import numpy as np

import scene_graph as sg
import easy_shaders as es
import basic_shapes as bs
import transformations as tr

def piezaTrasera():
	vertexData = np.array([
		 1.5,  2.5, 0, 87/255, 98/255, 112/255, 
		 0.5,  2.5, 0, 87/255, 98/255, 112/255,
		-2.5,  1.5, 0, 87/255, 98/255, 112/255,
		 -3 , -0.5, 0, 87/255, 98/255, 112/255,
		-1.5, -1.5, 0, 87/255, 98/255, 112/255,
		-1  , -0.5, 0, 87/255, 98/255, 112/255,
		 0  ,    0, 0, 87/255, 98/255, 112/255,
		 1  , -0.5, 0, 87/255, 98/255, 112/255,
		 1.5, -1.5, 0, 87/255, 98/255, 112/255,
		 2.5, -1.5, 0, 87/255, 98/255, 112/255,
		 1  ,    1, 0, 87/255, 98/255, 112/255,
		 2  ,    3, 0, 87/255, 98/255, 112/255,
		 0.5,  2.5, 0, 87/255, 98/255, 112/255],dtype=np.float32)
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

def piezaCentral():
	vertexData = np.array([
		 0.5,   2, 0, 87/255, 98/255, 112/255,
		-2.5,   2, 0, 87/255, 98/255, 112/255,
		-2.9, 0.2, 0, 87/255, 98/255, 112/255,
		-1.5,  -2, 0, 87/255, 98/255, 112/255,
		   2,  -2, 0, 87/255, 98/255, 112/255,
		   3, 0.5, 0, 87/255, 98/255, 112/255,
		  -2, 2.5, 0, 87/255, 98/255, 112/255,
		   1,   3, 0, 87/255, 98/255, 112/255,
		 3.5,   2, 0, 87/255, 98/255, 112/255], dtype=np.float32)
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

def piezaDelantera():
	vertexData = np.array([
		   0,   0,  0, 87/255, 98/255, 112/255,
		   1, -0.5, 0, 87/255, 98/255, 112/255,
		 1.5, -1.5, 0, 87/255, 98/255, 112/255,
		   3, -1.5, 0, 87/255, 98/255, 112/255,
		   4, -0.5, 0, 87/255, 98/255, 112/255,
		 3.5,    1, 0, 87/255, 98/255, 112/255,
		   2,    2, 0, 87/255, 98/255, 112/255,
		-1.5,  2.5, 0, 87/255, 98/255, 112/255,
		  -2,    1, 0, 87/255, 98/255, 112/255,
		-2.7, -0.5, 0, 87/255, 98/255, 112/255,
		  -3, -1.5, 0, 87/255, 98/255, 112/255,
		-1.5, -1.5, 0, 87/255, 98/255, 112/255,
		 - 1, -0.5, 0, 87/255, 98/255, 112/255], dtype=np.float32)
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

def vehiculo():
	p1 = es.toGPUShape(piezaTrasera())
	p2 = es.toGPUShape(piezaCentral())
	p3 = es.toGPUShape(piezaDelantera())

	piezaT = sg.SceneGraphNode("piezaTrasera")
	piezaT.transform = tr.matmul([tr.translate(-0.4,-0.05,0),tr.uniformScale(0.1)])
	piezaT.childs += [p1]

	piezaC = sg.SceneGraphNode("piezaCentral")
	piezaC.transform = tr.uniformScale(0.1)
	piezaC.childs += [p2]
	
	piezaD = sg.SceneGraphNode("piezaDelantera")
	piezaD.transform = tr.matmul([tr.translate(0.5,-0.05,0),tr.uniformScale(0.1)])
	piezaD.childs += [p3]

	auto = sg.SceneGraphNode("Vehiculo")
	auto.transform = tr.uniformScale(0.5)
	auto.childs += [piezaT]
	auto.childs += [piezaC]
	auto.childs += [piezaD]
	auto.childs += [ventanas()]
	auto.childs += [diseño()]
	
	return auto


def linea(color):
	vertexData = np.array([
		-0.5,  0.025, 0, color[0], color[1], color[2],
		-0.5, -0.025, 0, color[0], color[1], color[2],
		 0.5, -0.025, 0, color[0], color[1], color[2],
		 0.5,  0.025, 0, color[0], color[1], color[2]], dtype=np.float32)
	indices = np.array(
		[0, 1, 2,
		2, 3, 0], dtype=np.uint32)
	return bs.Shape(vertexData, indices)

def createTriangulo(r, g, b):
	vertexData = np.array([
		-0.5, -0.5, 0, r, g, b,
		 0.5, -0.5, 0, r, g, b,
		   0,  0.5, 0, r, g, b], dtype=np.float32)
	indices = np.array(
		[0, 1, 2], dtype=np.uint32)
	return bs.Shape(vertexData, indices)

def rueda(n,d):
	vertexData = []
	for i in range(n):
		np.append(vertexData, [0, 0, 0,])

def ventanas():
	cuadrado = es.toGPUShape(bs.createColorQuad(0.08, 0.08, 0.08))
	triangulo = es.toGPUShape(createTriangulo(0.08, 0.08, 0.08))

	ventanaFrente = sg.SceneGraphNode("ventanaFrente")
	ventanaFrente.transform = tr.matmul([tr.translate(0.22,0.19,0),tr.rotationZ(157*np.pi/180),tr.scale(0.3,0.1,1)])
	ventanaFrente.childs += [cuadrado]
	
	ventanaLado2 = sg.SceneGraphNode("ventanaLado2")
	ventanaLado2.transform = tr.matmul([tr.translate(-0.06, 0.14, 0),tr.rotationZ(25*np.pi/180),tr.scale(0.27, 0.1, 1)])
	ventanaLado2.childs += [triangulo]
	
	ventanaLado1 = sg.SceneGraphNode("ventanaLado1")
	ventanaLado1.transform = tr.matmul([tr.translate(0.08, 0.1, 0), tr.scale(0.48, 0.1, 1)])
	ventanaLado1.childs += [triangulo]
	
	ventanaLado = sg.SceneGraphNode("ventanaLado")
	ventanaLado.childs += [ventanaLado1]
	ventanaLado.childs += [ventanaLado2]

	ventanaAtras = sg.SceneGraphNode("ventanaAtras")
	ventanaAtras.transform = tr.matmul([tr.translate(-0.33, 0.1, 0),tr.rotationZ(210*np.pi/180),tr.scale(0.27, 0.1, 1)])
	ventanaAtras.childs += [triangulo]

	ventanas = sg.SceneGraphNode("ventanas")
	ventanas.childs += [ventanaFrente]
	ventanas.childs += [ventanaLado]
	ventanas.childs += [ventanaAtras]

	return ventanas

def diseño():
	cuadrado = es.toGPUShape(bs.createColorQuad(0.08, 0.08, 0.08))
	blackLine = es.toGPUShape(linea([0,0,0]))
	grayLine = es.toGPUShape(linea([0.2,0.2,0.2]))

	l1= sg.SceneGraphNode("downLine")
	l1.transform = tr.matmul([tr.translate(0.06,-0.1,0),tr.scale(0.71,0.5,1)])
	l1.childs += [blackLine]

	l3= sg.SceneGraphNode("backLine")
	l3.transform = tr.matmul([tr.translate(0.06,-0.2,0),tr.scale(0.64,1,1)])
	l3.childs += [blackLine]

	l2 = sg.SceneGraphNode("RigtLine")
	l2.transform = tr.matmul([tr.translate(0.3,0,0),tr.rotationZ(70*np.pi/180),tr.scale(0.4,0.15,1)])
	l2.childs += [grayLine]

	l4 = sg.SceneGraphNode("LeftLine")
	l4.transform = tr.matmul([tr.translate(-0.2,-0.07,0),tr.rotationZ(110*np.pi/180),tr.scale(0.3,0.15,1)])
	l4.childs += [grayLine]

	l5 = sg.SceneGraphNode("UpLine")
	l5.transform = tr.matmul([tr.translate(0.2,0.15,0),tr.rotationZ(155*np.pi/180),tr.scale(0.3,0.15,1)])
	l5.childs += [grayLine]

	l6= sg.SceneGraphNode("OnLine")
	l6.transform = tr.matmul([tr.translate(-0.065,0.21,0),tr.scale(0.28,0.15,1)])
	l6.childs += [grayLine]

	l7 = sg.SceneGraphNode("UpLine")
	l7.transform = tr.matmul([tr.translate(-0.23,0.13,0),tr.rotationZ(70*np.pi/180),tr.scale(0.16,0.15,1)])
	l7.childs += [grayLine]

	l7 = sg.SceneGraphNode("UpLine")
	l7.transform = tr.matmul([tr.translate(-0.23,0.13,0),tr.rotationZ(70*np.pi/180),tr.scale(0.16,0.15,1)])
	l7.childs += [grayLine]

	l8 = sg.SceneGraphNode("UpLine")
	l8.transform = tr.matmul([tr.translate(0.55,0.06,0),tr.rotationZ(-8*np.pi/180),tr.scale(0.5,0.15,1)])
	l8.childs += [grayLine]

	l9 = sg.SceneGraphNode("UpLine")
	l9.transform = tr.matmul([tr.translate(0.55,0.06,0),tr.rotationZ(-8*np.pi/180),tr.scale(0.5,0.15,1)])
	l9.childs += [grayLine]

	sombra= sg.SceneGraphNode("Sombra")
	sombra.transform = tr.matmul([tr.translate(0.1,-0.3,0),tr.scale(1.5,0.1,1)])
	sombra.childs += [cuadrado]

	diseño = sg.SceneGraphNode("Diseño")
	diseño.childs += [l4]
	diseño.childs += [l2]
	diseño.childs += [l5]
	diseño.childs += [l1]
	diseño.childs += [l3]
	diseño.childs += [l6]
	diseño.childs += [l7]
	diseño.childs += [l8]
	diseño.childs += [sombra]
	
	return diseño


def quad(color, inicio):
    vertexData = np.array([
        inicio[0]-0.5, inicio[1]-0.5, 0.0, color[0], color[1], color[2],
        inicio[0]+0.5, inicio[1]-0.5, 0.0, color[0], color[1], color[2],
        inicio[0]+0.5, inicio[1]+0.5, 0.0, color[0], color[1], color[2],
        inicio[0]-0.5, inicio[1]+0.5, 0.0, color[0], color[1], color[2]], dtype=np.float32)
    indices = np.array(
		[0, 1, 2,
         2, 3, 0], dtype=np.uint32)
    return bs.Shape(vertexData,indices)




