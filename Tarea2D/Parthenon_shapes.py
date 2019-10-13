import scene_graph as sg;
import basic_shapes as bs;
import easy_shaders as es;
import transformations as tr;
from mathlib import _normal_3_points as _normal3
import numpy as np
from OpenGL.GL import *

def vertexUnpack3(vertex):
    if len(vertex) == 2:
        vertex = vertex + (0,)
    return vertex

def create4VertexColorNormal(p1, p2, p3, p4, r, g, b):
    p1 = vertexUnpack3(p1)
    p2 = vertexUnpack3(p2)
    p3 = vertexUnpack3(p3)
    p4 = vertexUnpack3(p4)

    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3
    x4, y4, z4 = p4

    normal = _normal3(p3, p2, p1)
    normal_x = normal.get_x()
    normal_y = normal.get_y()
    normal_z = normal.get_z()

    vertices = np.array([
        x1, y1, z1, r, g, b, normal_x, normal_y, normal_z,
        x2, y2, z2, r, g, b, normal_x, normal_y, normal_z,
        x3, y3, z3, r, g, b, normal_x, normal_y, normal_z,
        x4, y4, z4, r, g, b, normal_x, normal_y, normal_z])

    indices = np.array([
        		0, 1, 2,
        		2, 3, 0])

    return bs.Shape(vertices, indices)

def create4VertexTextureNormal(image_filename, p1, p2, p3, p4, nx=1, ny=1):
    p1 = vertexUnpack3(p1)
    p2 = vertexUnpack3(p2)
    p3 = vertexUnpack3(p3)
    p4 = vertexUnpack3(p4)

    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3
    x4, y4, z4 = p4

    normal = _normal3(p3, p2, p1)
    normal_x = normal.get_x()
    normal_y = normal.get_y()
    normal_z = normal.get_z()

    vertices = np.array([
        x1, y1, z1, 0, 0, normal_x, normal_y, normal_z,
        x2, y2, z2, nx, 0, normal_x, normal_y, normal_z,
        x3, y3, z3, nx, ny, normal_x, normal_y, normal_z,
        x4, y4, z4, 0, ny, normal_x, normal_y, normal_z])
    indices = np.array([
    			0, 1, 2,
        		2, 3, 0])

    return bs.Shape(vertices, indices, image_filename)

def createTriangleTextureNormal(image_filename, p1, p2, p3, nx=1, ny=1):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3

    normal = _normal3(p3, p2, p1)
    normal_x = normal.get_x()
    normal_y = normal.get_y()
    normal_z = normal.get_z()

    vertices = np.array([
        x1, y1, z1, (nx + ny) / 2, nx, normal_x, normal_y, normal_z,
        x2, y2, z2, 0.0, 0.0, normal_x, normal_y, normal_z,
        x3, y3, z3, ny, 0.0, normal_x, normal_y, normal_z])

    indices = np.array([
        		0, 1, 2])

    return bs.Shape(vertices, indices, image_filename)

def cilindro(h,r,N,image_filename=None,color=None):
    dang = 2 * np.pi / N
    a = [r*np.cos(0), r*np.sin(0), h]
    b = [r*np.cos(dang), r*np.sin(dang), h]
    c = [r*np.cos(dang), r*np.sin(dang), 0]
    d = [r*np.cos(0), r*np.sin(0), 0]
    shape = es.toGPUShape(create4VertexTextureNormal(image_filename, a, b, c, d), GL_REPEAT, GL_NEAREST) if image_filename != None and color==None else (
    		es.toGPUShape(create4VertexColorNormal(a, b, c, d, color[0], color[1], color[2]), GL_REPEAT, GL_NEAREST))
    cylinder_shape = sg.SceneGraphNode("cylinder_shape")
    for i in range(N): 
        aux = sg.SceneGraphNode("aux")
        aux.transform = tr.rotationZ(i*dang)
        aux.childs += [shape]
        cylinder_shape.childs += [aux]
    return 	cylinder_shape



def techo(image_filename):
	a=[19.5,-42,14.4];b=[19.5,42,14.4];c=[0,42,18.5];d=[0,-42,18.5];e=[0,-42,14.4];f=[-19.5,42,14.4];g=[-19.5,-42,14.4]
	gpuTriangle = es.toGPUShape(createTriangleTextureNormal("marmol_semidark.jpg",d,a,e), GL_REPEAT, GL_NEAREST)
	gpuQuad2 = es.toGPUShape(create4VertexTextureNormal(image_filename,a,b,f,g), GL_REPEAT, GL_NEAREST)
	gpuQuad = es.toGPUShape(create4VertexTextureNormal(image_filename,a,d,c,b), GL_REPEAT, GL_NEAREST)
	

	semi_techo_p1 = sg.SceneGraphNode("semi_techo_p1")
	semi_techo_p1.childs += [gpuQuad]

	semi_techo_p2_1 = sg.SceneGraphNode("semi_techo_p2_1")
	semi_techo_p2_1.childs += [gpuTriangle]

	semi_techo_p2_2 = sg.SceneGraphNode("semi_techo_p2_2")
	semi_techo_p2_2.transform = tr.matmul([tr.translate(0,0,0),tr.scale(1,-1,1)])
	semi_techo_p2_2.childs += [gpuTriangle]

	semi_techo_p2 = sg.SceneGraphNode("semi_techo_p2")
	semi_techo_p2.childs += [semi_techo_p2_1]
	semi_techo_p2.childs += [semi_techo_p2_2]

	semi_techo = sg.SceneGraphNode("semi_techo")
	semi_techo.childs += [semi_techo_p1]
	semi_techo.childs += [semi_techo_p2]

	semi_techo_r = sg.SceneGraphNode("semi_techo_r")
	semi_techo_r.transform = tr.scale(-1,1,1)
	semi_techo_r.childs += [semi_techo]

	base = sg.SceneGraphNode("base")
	base.childs += [gpuQuad2]

	adornos = sg.SceneGraphNode("adornos")
	for i in range(3):
		for j in range(3):
			capa = -41.5 if i==0 else 0 if i==1 else 41.5
			pos = [-18.7,14.7] if j==0 else [0,18.5] if j==1 else [18.7,14.7]
			translate = tr.translate(pos[0],capa,0.6+pos[1])
			aux = sg.SceneGraphNode("aux")
			aux.transform = translate
			aux.childs += [adorno()]
			adornos.childs += [aux]

	techo = sg.SceneGraphNode("techo")
	techo.childs += [semi_techo]
	techo.childs += [semi_techo_r]
	techo.childs += [base]
	techo.childs += [adornos]

	return techo

def adorno():
	gpuQuad = es.toGPUShape(bs.createTextureNormalsCube("marmol_semidark.jpg"), GL_REPEAT, GL_NEAREST)

	base_adorno = sg.SceneGraphNode("base_adorno")
	base_adorno.transform = tr.matmul([tr.translate(0.7,0,0),tr.scale(0.5,1,1)])
	base_adorno.childs += [gpuQuad]

	deco = sg.SceneGraphNode("deco")
	deco.transform = tr.matmul([tr.rotationY(45*np.pi/180),tr.scale(1,0.2,1)])
	deco.childs += [gpuQuad]

	adorno = sg.SceneGraphNode("adorno")
	adorno.transform = tr.matmul([tr.rotationY(90*np.pi/180),tr.uniformScale(0.9)])
	adorno.childs += [base_adorno]
	adorno.childs += [deco]

	return adorno


def estructura():
	gpuQuadDark = es.toGPUShape(bs.createTextureNormalsCube("piedras.jpg"), GL_REPEAT, GL_NEAREST)
	gpuQuadSemiDark = es.toGPUShape(bs.createTextureNormalsCube("marmol_semidark.jpg"), GL_REPEAT, GL_NEAREST)

	pilar_=cilindro(10.5,1,3,image_filename="pilar.jpg")


	base_pilar = sg.SceneGraphNode("base_pilar")
	base_pilar.transform = tr.scale(2.3,2.3,1)
	base_pilar.childs += [gpuQuadSemiDark]

	tope_pilar = sg.SceneGraphNode("base_pilar")
	tope_pilar.transform = tr.matmul([tr.translate(0,0,10.5),tr.scale(2.3,2.3,0.7)])
	tope_pilar.childs += [gpuQuadSemiDark]

	pilar = sg.SceneGraphNode("pilar")
	pilar.transform = tr.translate(0,0,1)
	pilar.childs += [base_pilar]
	pilar.childs += [tope_pilar]
	pilar.childs += [pilar_]

	centro = sg.SceneGraphNode("centro")
	centro.transform = tr.matmul([tr.translate(0,0,6),tr.scale(25,60,12)])
	centro.childs += [gpuQuadDark]

	base = sg.SceneGraphNode("base")
	base.transform = tr.scale(39,84,1)
	base.childs += [gpuQuadSemiDark]

	media = sg.SceneGraphNode("media")
	media.transform = tr.matmul([tr.translate(0,0,13.5),tr.scale(37,82,2)])
	media.childs += [gpuQuadDark]

	tope = sg.SceneGraphNode("tope")
	tope.transform = tr.matmul([tr.translate(0,0,12),tr.scale(39,84,1)])
	tope.childs += [gpuQuadSemiDark]


	pilarFrente = sg.SceneGraphNode("pilarFrente")
	for i in range(8):
		aux = sg.SceneGraphNode("aux")
		aux.transform = tr.translate(16.5-4.715*i,-39,0)
		aux.childs += [pilar]
		pilarFrente.childs += [aux]

	pilarAtras = sg.SceneGraphNode("pilarAtras")
	pilarAtras.transform = tr.translate(0,78,0)
	pilarAtras.childs += [pilarFrente]

	pilarDerecha = sg.SceneGraphNode("pilarDerecha")
	for i in range (15):
		aux = sg.SceneGraphNode("aux")
		aux.transform = tr.translate(16.5,34-4.85*i,0)
		aux.childs += [pilar]
		pilarDerecha.childs += [aux]

	pilarIzquierda = sg.SceneGraphNode("pilarIzquerda")
	pilarIzquierda.transform = tr.translate(-33,0,0)
	pilarIzquierda.childs += [pilarDerecha]

	
	estructura = sg.SceneGraphNode("estructura")
	estructura.transform = tr.uniformScale(0.6)
	estructura.childs += [base]
	estructura.childs += [tope]
	estructura.childs += [media]
	estructura.childs += [centro]
	estructura.childs += [pilarFrente]
	estructura.childs += [pilarAtras]
	estructura.childs += [pilarDerecha]
	estructura.childs += [pilarIzquierda]
	estructura.childs += [techo("marmol.jpg")]
	
	return estructura

def fondo(color):
	fondo_ = cilindro(30,50,10,color=color)
	tapaCielo_ = es.toGPUShape(create4VertexColorNormal([-50,50,30],[50,50,30],[50,-50,30],[-50,-50,30],color[0],color[1],color[2]), GL_REPEAT, GL_NEAREST)

	tapaCielo = sg.SceneGraphNode("tapaCielo")
	tapaCielo.childs += [tapaCielo_]

	fondo = sg.SceneGraphNode("fondo")
	fondo.childs += [fondo_]
	fondo.childs += [tapaCielo]

	return fondo

def suelo(image_filename):
	tapaSuelo_ = es.toGPUShape(create4VertexTextureNormal(image_filename,[-50,50,0],[50,50,0],[50,-50,0],[-50,-50,0]), GL_REPEAT, GL_NEAREST)
	tapaSuelo = sg.SceneGraphNode("tapaSuelo")
	tapaSuelo.childs += [tapaSuelo_]
	return tapaSuelo




