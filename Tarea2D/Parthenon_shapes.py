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

def pilar(image_filename,h,r,lat,lon):
    dang = 2 * np.pi / lat
    cylinder_shape = sg.SceneGraphNode("cylinder_shape")
    for i in range(lon): 
        for j in range(lat): 
            ang = dang * j
            a = [r * np.cos(ang), r * np.sin(ang), h / lon * (i + 1)]
            b = [r * np.cos(ang + dang), r * np.sin(ang + dang), h / lon * (i + 1)]
            c = [r * np.cos(ang + dang), r * np.sin(ang + dang), h / lon * i]
            d = [r * np.cos(ang), r * np.sin(ang), h / lon * i]
            shape = es.toGPUShape(create4VertexTextureNormal(image_filename, a, b, c, d), GL_REPEAT, GL_NEAREST)
            aux = sg.SceneGraphNode("aux")
            aux.childs += [shape]
            cylinder_shape.childs += [aux]
    return 	cylinder_shape



def techo(image_filename):
	a=[19.5,-42,14.4];b=[19.5,42,14.4];c=[0,42,18.5];d=[0,-42,18.5];e=[0,-42,14.4];
	gpuTriangle = es.toGPUShape(createTriangleTextureNormal(image_filename,a,d,e), GL_REPEAT, GL_NEAREST)
	gpuQuad = es.toGPUShape(create4VertexTextureNormal(image_filename,a,b,c,d), GL_REPEAT, GL_NEAREST)

	semi_techo_p1 = sg.SceneGraphNode("semi_techo_p1")
	semi_techo_p1.childs += [gpuQuad]

	semi_techo_p2_1 = sg.SceneGraphNode("semi_techo_p2_1")
	semi_techo_p2_1.childs += [gpuTriangle]

	semi_techo_p2_2 = sg.SceneGraphNode("semi_techo_p2_2")
	semi_techo_p2_2.transform = tr.translate(0,84,0)
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

	techo = sg.SceneGraphNode("techo")
	techo.childs += [semi_techo]
	techo.childs += [semi_techo_r]

	return techo


def estructura(image_filename):
	gpuQuad = es.toGPUShape(bs.createTextureNormalsCube(image_filename), GL_REPEAT, GL_NEAREST)
	pilar_=pilar(image_filename,12,1,4,1)

	centro = sg.SceneGraphNode("centro")
	centro.transform = tr.matmul([tr.translate(0,0,6),tr.scale(25,60,12)])
	centro.childs += [gpuQuad]

	base = sg.SceneGraphNode("base")
	base.transform = tr.scale(39,84,1)
	base.childs += [gpuQuad]

	media = sg.SceneGraphNode("media")
	media.transform = tr.matmul([tr.translate(0,0,13.5),tr.scale(37,82,2)])
	media.childs += [gpuQuad]

	tope = sg.SceneGraphNode("tope")
	tope.transform = tr.matmul([tr.translate(0,0,12),tr.scale(39,84,1)])
	tope.childs += [gpuQuad]


	pilarFrente = sg.SceneGraphNode("pilarFrente")
	for i in range(8):
		aux = sg.SceneGraphNode("aux")
		aux.transform = tr.translate(16.5-4.715*i,-39,0)
		aux.childs += [pilar_]
		pilarFrente.childs += [aux]

	pilarAtras = sg.SceneGraphNode("pilarAtras")
	pilarAtras.transform = tr.translate(0,78,0)
	pilarAtras.childs += [pilarFrente]

	pilarDerecha = sg.SceneGraphNode("pilarDerecha")
	for i in range (15):
		aux = sg.SceneGraphNode("aux")
		aux.transform = tr.translate(16.5,34-4.85*i,0)
		aux.childs += [pilar_]
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
	estructura.childs += [techo(image_filename)]
	
	return estructura

def fondo(image_filename):
	fondo_ = pilar(image_filename,30,50,10,1)
	tapaCielo_ = es.toGPUShape(create4VertexTextureNormal(image_filename,[-50,50,30],[50,50,30],[50,-50,30],[-50,-50,30]), GL_REPEAT, GL_NEAREST)

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




