import scene_graph as sg;
import basic_shapes as bs;
import easy_shaders as es;
import transformations as tr;
from OpenGL.GL import *

def base():
	gpuQuad = es.toGPUShape(bs.createTextureQuad("piedra_caliza.jpg"), GL_REPEAT, GL_NEAREST)

	base_s =  sg.SceneGraphNode("base_scaled")
	base_s.transform = tr.matmul([tr.uniformScale(0.5),tr.scale(39,84,1)])
	base_s.childs += [gpuQuad]

	return base_s

def estructura():
	gpuQuad = es.toGPUShape(bs.createTextureNormalsCube("marmol2.jpg"), GL_REPEAT, GL_NEAREST)

	base = sg.SceneGraphNode("base")
	base.transform = tr.scale(39,84,1)
	base.childs += [gpuQuad]

	tope = sg.SceneGraphNode("tope")
	tope.transform = tr.matmul([tr.translate(0,0,12),tr.scale(39,84,1)])
	tope.childs += [gpuQuad]

	pilar = sg.SceneGraphNode("pilar")
	pilar.transform = tr.scale(2,2,12)
	pilar.childs += [gpuQuad]

	pilarFrente = sg.SceneGraphNode("pilarFrente")
	for i in range (8):
		aux = sg.SceneGraphNode("aux")
		aux.transform = tr.translate(16.5-4.715*i,-39,6)
		aux.childs += [pilar]
		pilarFrente.childs += [aux]

	pilarAtras = sg.SceneGraphNode("pilarAtras")
	pilarAtras.transform = tr.translate(0,78,0)
	pilarAtras.childs += [pilarFrente]

	pilarDerecha = sg.SceneGraphNode("pilarDerecha")
	for i in range (15):
		aux = sg.SceneGraphNode("aux")
		aux.transform = tr.translate(16.5,34-4.85*i,6)
		aux.childs += [pilar]
		pilarDerecha.childs += [aux]

	pilarIzquierda = sg.SceneGraphNode("pilarIzquerda")
	pilarIzquierda.transform = tr.translate(-33,0,0)
	pilarIzquierda.childs += [pilarDerecha]

	estructura = sg.SceneGraphNode("estructura")
	estructura.transform = tr.uniformScale(1)
	estructura.childs += [base]
	estructura.childs += [tope]
	estructura.childs += [pilarFrente]
	estructura.childs += [pilarDerecha]
	estructura.childs += [pilarAtras]
	estructura.childs += [pilarIzquierda]


	return estructura



def createTextureNormalsCylinder(image_filename):

    # Defining locations,texture coordinates and normals for each vertex of the shape  
    vertices = [
    #   positions            tex coords   normals
    # Z+
        -0.5, -0.5,  0.5,    0, 1,        0,0,1,
         0.5, -0.5,  0.5,    1, 1,        0,0,1,
         0.5,  0.5,  0.5,    1, 0,        0,0,1,
        -0.5,  0.5,  0.5,    0, 0,        0,0,1,   
    # Z-          
        -0.5, -0.5, -0.5,    0, 1,        0,0,-1,
         0.5, -0.5, -0.5,    1, 1,        0,0,-1,
         0.5,  0.5, -0.5,    1, 0,        0,0,-1,
        -0.5,  0.5, -0.5,    0, 0,        0,0,-1,
       
    # X+          
         0.5, -0.5, -0.5,    0, 1,        1,0,0,
         0.5,  0.5, -0.5,    1, 1,        1,0,0,
         0.5,  0.5,  0.5,    1, 0,        1,0,0,
         0.5, -0.5,  0.5,    0, 0,        1,0,0,   
    # X-          
        -0.5, -0.5, -0.5,    0, 1,        -1,0,0,
        -0.5,  0.5, -0.5,    1, 1,        -1,0,0,
        -0.5,  0.5,  0.5,    1, 0,        -1,0,0,
        -0.5, -0.5,  0.5,    0, 0,        -1,0,0,   
    # Y+          
        -0.5,  0.5, -0.5,    0, 1,        0,1,0,
         0.5,  0.5, -0.5,    1, 1,        0,1,0,
         0.5,  0.5,  0.5,    1, 0,        0,1,0,
        -0.5,  0.5,  0.5,    0, 0,        0,1,0,   
    # Y-          
        -0.5, -0.5, -0.5,    0, 1,        0,-1,0,
         0.5, -0.5, -0.5,    1, 1,        0,-1,0,
         0.5, -0.5,  0.5,    1, 0,        0,-1,0,
        -0.5, -0.5,  0.5,    0, 0,        0,-1,0
        ]   

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
          0, 1, 2, 2, 3, 0, # Z+
          7, 6, 5, 5, 4, 7, # Z-
          8, 9,10,10,11, 8, # X+
         15,14,13,13,12,15, # X-
         19,18,17,17,16,19, # Y+
         20,21,22,22,23,20] # Y-

    return Shape(vertices, indices, image_filename)


