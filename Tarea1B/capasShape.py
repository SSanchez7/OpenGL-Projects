from OpenGL.GL import *

import numpy as np

import scene_graph as sg
import easy_shaders as es
import basic_shapes as bs
import transformations as tr
import autoShape as ash
import random

def foco():
	blackQuad = es.toGPUShape(createMulticolorQuad([0.08,0.08,0.08],[98/255,70/255,21/255]))
	shadowQuad = es.toGPUShape(createMulticolorQuad([0.08,0.08,0.08],[0.08,0.08,0.08]))
	whiteQuad = es.toGPUShape(createMulticolorQuad([1,1,1],[0.9,0.9,0.9]))
	greenQuad = es.toGPUShape(createMulticolorQuad([10/255,50/255,10/255],[10/255,50/255,10/255]))

	#Crea cuerpo del foco
	soporte = sg.SceneGraphNode("soporte")
	soporte.transform = tr.matmul([tr.rotationZ(90*np.pi/180), tr.scale(1,0.04,1)])
	soporte.childs += [blackQuad]
	baseLuz = sg.SceneGraphNode("baseLuz")
	baseLuz.transform = tr.matmul([tr.translate(0,0.5,0), tr.scale(0.2,-0.05,1)])
	baseLuz.childs += [blackQuad]
	luz = sg.SceneGraphNode("luzFoco")
	luz.transform = tr.matmul([tr.translate(0, 0.47, 0), tr.scale(0.1, 0.025, 1)])
	luz.childs += [whiteQuad]
	focoSimple = sg.SceneGraphNode("focoSimple")
	focoSimple.childs += [soporte]
	focoSimple.childs += [baseLuz]
	focoSimple.childs += [luz]

	#Crea brillo y sombra generadas por el foco
	brillo = sg.SceneGraphNode("brilloFoco")
	brillo.transform = tr.matmul([tr.translate(0,-0.55,0), tr.scale(0.4,0.1,1)])
	brillo.childs += [ash.circle(20,0.1,[62/255, 151/255, 62/255])]
	sombraPoste = sg.SceneGraphNode("sombraPoste")
	sombraPoste.transform = tr.matmul([tr.translate(-0.47,-0.57,0), tr.rotationZ(10*np.pi/180), tr.scale(1,0.04,1)])
	sombraPoste.childs += [shadowQuad]
	sombraBaseLuz = sg.SceneGraphNode("sombraBaseLuz")
	sombraBaseLuz.transform = tr.matmul([tr.translate(-0.97,-0.67,0), tr.shearing(1,0,0,0,0,0), tr.rotationZ(-30*np.pi/180), tr.scale(0.27,-0.04,1)])
	sombraBaseLuz.childs += [shadowQuad]
	arregloSombra = sg.SceneGraphNode("arregloSombra1")
	arregloSombra.transform = tr.matmul([tr.translate(-0.47,-0.57,0), tr.rotationZ(10*np.pi/180), tr.shearing(-4,0,0,0,0,0), tr.translate(0.2,0,0), tr.scale(0.57,0.04,1)])
	arregloSombra.childs += [greenQuad]
	sombraLuzFoco = sg.SceneGraphNode("sombraFoco")
	sombraLuzFoco.childs += [brillo]
	sombraLuzFoco.childs += [sombraPoste]
	sombraLuzFoco.childs += [sombraBaseLuz]
	sombraLuzFoco.childs += [arregloSombra]

	#Ensamblaje de foco
	foco = sg.SceneGraphNode("foco")
	foco.childs += [sombraLuzFoco]
	foco.childs += [focoSimple]
	
	return foco

def cerca():
	brownQuad = es.toGPUShape(createMulticolorQuad([80/255, 20/255, 0/255],[119/255, 51/255, 2/255]))

	cerca = sg.SceneGraphNode("carca")
	for i in range (18):
		palo = sg.SceneGraphNode("palo")
		palo.transform = tr.matmul([tr.translate(-0.9+0.111*i,-0.4,0), tr.scale(0.1,0.15,1), tr.rotationZ(90*np.pi/180)])
		palo.childs += [brownQuad]
		cerca.childs += [palo]

	return cerca

##CAPA4: FOCO, CERCA, CALLE, PASTO
def mapa4():
	street = es.toGPUShape(createMulticolorQuad([0.25,0.25,0.25],[0.2,0.2,0.2])) 
	garden = es.toGPUShape(createMulticolorQuad([10/255,50/255,10/255],[22/255,112/255,22/255]))
	linea = es.toGPUShape(ash.createLine([0.3,0.3,0.3]))

	division = sg.SceneGraphNode("dividir")
	division.transform = tr.matmul([tr.translate(0,-0.6,0),tr.scale(2,0.4,1)])
	division.childs += [linea]
	
	calles = sg.SceneGraphNode("calle")
	calles.transform = tr.matmul([tr.translate(0,-0.8,0),tr.scale(2,0.4,1)])
	calles.childs += [street]

	pasto = sg.SceneGraphNode("pasto")
	pasto.transform = tr.matmul([tr.translate(0,-0.51,0),tr.scale(2,0.19,1)])
	pasto.childs += [garden]

	mapa4 = sg.SceneGraphNode("capa1")
	mapa4.childs += [calles]
	mapa4.childs += [cerca()]
	mapa4.childs += [pasto]
	mapa4.childs += [division]
	mapa4.childs += [foco()]

	return mapa4

def createSemiPuente(color):
	vertexData = np.array([
		0, 2, 0, color[0], color[1], color[2],
		0, 0, 0, color[0], color[1], color[2],
		-2, -0.5, 0, color[0], color[1], color[2],
		-5, -2.5, 0, color[0], color[1], color[2],
		-6, -4, 0, color[0], color[1], color[2],
		-8, -4, 0 , color[0]-0.1, color[1]-0.1, color[2]-0.1,
		-8, -3.5, 0, color[0], color[1], color[2],
		-7.5, -3.5, 0, color[0], color[1], color[2],
		-7.5, 1, 0, color[0]-0.1, color[1]-0.1, color[2]-0.1,
		-8, 1.5, 0, color[0]-0.1, color[1]-0.1, color[2]-0.1,
		-8, 2, 0, color[0], color[1], color[2],

		-7, -3.5, 0, color[0], color[1], color[2],
		-7, 1, 0, color[0]-0.1, color[1]-0.1, color[2]-0.1,
		-6.5, 1.5, 0, color[0]-0.1, color[1]-0.1, color[2]-0.1,
		-6, 1, 0, color[0]-0.1, color[1]-0.1, color[2]-0.1,
		-5.5, 1, 0, color[0]-0.1, color[1]-0.1, color[2]-0.1,
		-5, 1.5, 0, color[0]-0.1, color[1]-0.1, color[2]-0.1,
		-4.5, 1, 0, color[0]-0.1, color[1]-0.1, color[2]-0.1,
		-4, 1.5, 0, color[0]-0.1, color[1]-0.1, color[2]-0.1,
		-3.5, 1.5, 0, color[0]-0.1, color[1]-0.1, color[2]-0.1,
		-3, 1, 0, color[0]-0.1, color[1]-0.1, color[2]-0.1,
		-3, -0.5, 0, color[0], color[1], color[2],
		-4, -1, 0, color[0], color[1], color[2],
		-4.5, -1.5, 0, color[0], color[1], color[2],
		-5.5, -2, 0, color[0], color[1], color[2],
		-6, -3, 0, color[0], color[1], color[2]],dtype=np.float32)

	indices = np.array(
		[0, 1, 2,
		 0, 2, 20,
		 0, 19, 20,
		 0, 10, 19,
		 20, 21, 2,
		 21, 22, 2,
		 22, 3, 2,
		 23, 22, 3,
		 24, 23, 3,
		 24, 25, 3,
		 25, 3, 4,
		 11, 25, 4,
		 7, 11, 4,
		 7, 5, 4,
		 5, 6, 7,
		 8, 9, 10,
		 10, 8, 12,
		 10, 12, 13,
		 10, 13, 16,
		 13, 14, 15,
		 13, 15, 16,
		 10, 16, 19,
		 16, 17, 19,
		 17, 18, 19,
		 22, 23, 17,
		 17, 18, 22,
		 14, 15, 24,
		 24, 25, 14,
		 7, 11, 12,
		 7, 8, 12], dtype=np.uint32)
	return bs.Shape(vertexData, indices)

def boya(color):
	quad = es.toGPUShape(createMulticolorQuad([color[0],color[1],color[2]],[color[0]-0.2,color[1]-0.2,color[2]-0.2]))
	tri = es.toGPUShape(ash.createTriangle([color[0],color[1],color[2]]))
	linea = es.toGPUShape(ash.createLine([color[0],color[1],color[2]]))
	refl = es.toGPUShape(createMulticolorQuad([10/255,40/255,60/255],[20/255,90/255,100/255]))

	l1 = sg.SceneGraphNode("l1")
	l1.transform = tr.matmul([tr.translate(0,0.05,0), tr.rotationZ(90*np.pi/180), tr.scale(0.15,0.08,1)])
	l1.childs += [linea]
	l2 = sg.SceneGraphNode("l2")
	l2.transform = tr.matmul([tr.translate(-0.025,0.05,0), tr.rotationZ(70*np.pi/180), tr.scale(0.15,0.08,1)])
	l2.childs += [linea]
	l3 = sg.SceneGraphNode("l3")
	l3.transform = tr.matmul([tr.translate(0.025,0.05,0), tr.rotationZ(110*np.pi/180), tr.scale(0.15,0.08,1)])
	l3.childs += [linea]

	baseAlta = sg.SceneGraphNode("baseAlta")
	baseAlta.transform = tr.identity()
	baseAlta.childs += [l1]
	baseAlta.childs += [l2]
	baseAlta.childs += [l3]

	baseMedia = sg.SceneGraphNode("baseMedia")
	baseMedia.transform = tr.matmul([tr.translate(0,-0.05,0), tr.scale(0.1,0.1,1)])
	baseMedia.childs += [quad]

	baseBaja = sg.SceneGraphNode("baseBaja")
	baseBaja.transform = tr.matmul([tr.translate(0,-0.1,0), tr.scale(0.1,0.1,0.1)])
	baseBaja.childs += [tri]

	reflejo = sg.SceneGraphNode("reflejoPez")
	reflejo.transform = tr.matmul([tr.translate(0,-0.29,0), tr.scale(0.1,0.3,1)])
	reflejo.childs += [refl]

	cuerpo = sg.SceneGraphNode("cuerpoBoya")
	cuerpo.childs += [baseBaja]
	cuerpo.childs += [baseMedia]
	cuerpo.childs += [baseAlta]

	boya = sg.SceneGraphNode("pez")
	boya.transform = tr.matmul([tr.translate(0,-0.1,0), tr.uniformScale(0.8)])
	boya.childs += [reflejo]
	boya.childs += [cuerpo]
	
	return boya

##CAPA3: PUENTE, REFLEJO, LAGO
def mapa3():
	semiP = es.toGPUShape(createSemiPuente([0.2, 0.2, 0.2]))
	refl = es.toGPUShape(createMulticolorQuad([10/255,40/255,60/255],[20/255,90/255,100/255]))
	agua = es.toGPUShape(createMulticolorQuad([20/255,90/255,100/255],[1/255,40/255,70/255]))

	reflejo1 = sg.SceneGraphNode("reflejo1")
	reflejo1.transform = tr.matmul([tr.translate(1-0.125,-0.374,0), tr.scale(0.25,0.25,0)])
	reflejo1.childs += [refl]
	reflejo2 = sg.SceneGraphNode("reflejo2")
	reflejo2.transform = tr.matmul([tr.translate(-1+0.125,-0.374,0), tr.scale(0.25,0.25,0)])
	reflejo2.childs += [refl]

	semiPuente1 = sg.SceneGraphNode("semiPuente")
	semiPuente1.transform = tr.uniformScale(0.125)
	semiPuente1.childs += [semiP]
	semiPuente2 = sg.SceneGraphNode("semiPuenteR")
	semiPuente2.transform = tr.matmul([tr.scale(-1,1,1), tr.uniformScale(0.125)])
	semiPuente2.childs += [semiP]

	reflejo = sg.SceneGraphNode("reflejo")
	reflejo.childs += [reflejo1]
	reflejo.childs += [reflejo2]

	puente = sg.SceneGraphNode("puente")
	puente.transform = tr.translate(0,0.25,0)
	puente.childs += [semiPuente1]
	puente.childs += [semiPuente2]
	
	lago = sg.SceneGraphNode("lago")
	lago.transform = tr.matmul([tr.translate(0,-0.2,0), tr.scale(2,0.9,1)])
	lago.childs += [agua]

	mapa3 = sg.SceneGraphNode("capa3")
	mapa3.childs += [lago]
	mapa3.childs += [reflejo]
	mapa3.childs += [puente]
	mapa3.childs += [boya([128/255,4/255,4/255])]



	return mapa3

##CAPA2: ISLAS
def mapa2():
	isla1 = sg.SceneGraphNode("isla1")
	isla1.transform = tr.matmul([tr.translate(0.3, 0.2, 0), tr.rotationZ(110*np.pi/180)])
	isla1.childs += [ash.semiCircle(10,0.25,[40/255,90/255,10/255])]
	isla2 = sg.SceneGraphNode("isla2")
	isla2.transform = tr.matmul([tr.translate(0.05, 0.2, 0), tr.rotationZ(110*np.pi/180)])
	isla2.childs += [ash.semiCircle(10,0.2,[30/255,79/255,6/255])]

	islas = sg.SceneGraphNode("islas")
	islas.childs += [isla1]
	islas.childs += [isla2]

	mapa2 = sg.SceneGraphNode("capa2")
	mapa2.childs += [islas]

	return mapa2

def ave(color):
	semiC= ash.semiCircle(10,0.08,[color[0],color[2],color[2]])
	triangle = es.toGPUShape(ash.createTriangle([0,0,0]))
	quad1 = es.toGPUShape(ash.createMulticolorQuad([color[0],color[1],color[2]],[color[0]-0.2,color[1]-0.2,color[2]-0.2]))
	quad2 = es.toGPUShape(ash.createMulticolorQuad([color[0]-0.2,color[1]-0.2,color[2]-0.2],[color[0]-0.4,color[1]-0.4,color[2]-0.4]))

	cuerpo = sg.SceneGraphNode("cuerpo")
	cuerpo.transform = tr.matmul([tr.translate(0,0.7,0), tr.scale(1,0.7,1), tr.rotationZ(-72*np.pi/180)])
	cuerpo.childs += [semiC]

	cabeza = sg.SceneGraphNode("cabeza")
	cabeza.transform = tr.matmul([tr.translate(-0.11,0.64,0), tr.scale(0.5,0.5,1), tr.rotationZ(110*np.pi/180)])
	cabeza.childs += [semiC]

	pico = sg.SceneGraphNode("pico")
	pico.transform = tr.matmul([tr.translate(-0.17,0.65,0), tr.scale(0.1,0.03,1)])
	pico.childs += [triangle]

	alaIzquierda = sg.SceneGraphNode("alaIzquierda")
	alaIzquierda.childs += [quad1]
	alaDerecha = sg.SceneGraphNode("alaDerecha")
	alaDerecha.childs += [quad2]

	ave = sg.SceneGraphNode("ave")

	ave.childs += [alaDerecha]
	ave.childs += [cuerpo]
	ave.childs += [cabeza]
	ave.childs += [alaIzquierda]
	ave.childs += [pico]

	return ave

##CAPA1: FONDO, ESTRELLAS
def mapa1():
	f = es.toGPUShape(createFondo())
	tri = es.toGPUShape(ash.createTriangle([1,1,1]))
	fondo = sg.SceneGraphNode("fondo")
	fondo.childs += [f]
	estrellas = sg.SceneGraphNode("estrellas")
	for i in range (20):
		newNode = sg.SceneGraphNode("es"+str(i+1))
		newNode.transform = tr.matmul([tr.translate(random.random()*((-1)**i), random.random(),0), tr.scale(0.009,0.009,0)])
		newNode.childs += [tri]
		estrellas.childs += [newNode]

	mapa1 = sg.SceneGraphNode("background")
	mapa1.childs += [fondo]
	mapa1.childs += [estrellas]
	return mapa1

def createFondo():
	azul = [27/255,23/255,79/255]
	rojo = [255/255,66/255,0/255]
	naranjo = [239/255,157/255,51/255]
	amarillo = naranjo
	vertexData = np.array([
        -1, -1/3, 0,  rojo[0], rojo[1], rojo[2],
         1/3, -1/3, 0,  rojo[0], rojo[1], rojo[2],
         1,  -1/3, 0,  rojo[0], rojo[1], rojo[2],
         1,  1, 0,  azul[0], azul[1], azul[2],
         1/3, 1, 0, azul[0], azul[1], azul[2],
         -1, 1, 0, azul[0], azul[1], azul[2],
         -1, 1/3, 0, naranjo[0], naranjo[1], naranjo[2],
         1/3, 1/3, 0, amarillo[0], amarillo[1], amarillo[2],
         1, 1/3, 0, naranjo[0], naranjo[1], naranjo[2]], dtype=np.float32)
	indices = np.array([
         0, 1, 6,
         1, 6, 7,
         5, 6, 7,
         5, 7, 4,
         4, 7, 8,
         4, 3, 8,
         7, 1, 2,
         7, 8, 2], dtype=np.uint32)

	return bs.Shape(vertexData, indices)

def createMulticolorQuad(color1, color2): 
    vertexData = np.array([
        -0.5, -0.5, 0.0,  color2[0], color2[1], color2[2],
         0.5, -0.5, 0.0,  color2[0], color2[1], color2[2],
         0.5,  0.5, 0.0,  color1[0], color1[1], color1[2],
        -0.5,  0.5, 0.0,  color1[0], color1[1], color1[2]], dtype=np.float32)
    indices = np.array([
         0, 1, 2,
         2, 3, 0], dtype=np.uint32)

    return bs.Shape(vertexData, indices)