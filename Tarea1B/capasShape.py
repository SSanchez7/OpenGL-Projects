from OpenGL.GL import *

import numpy as np

import scene_graph as sg
import easy_shaders as es
import basic_shapes as bs
import transformations as tr
from autoShape import *

def capa1():
	root = es.toGPUShape(bs.createColorQuad(0.25,0.25,0.25)) 

	calles = sg.SceneGraphNode("calle")
	calles.transform = tr.matmul([tr.translate(0,-0.5,0),tr.scale(2,1,1)])
	calles.childs += [root]

	capa1 = sg.SceneGraphNode("capa1")
	capa1.childs += [calles]

	return capa1
