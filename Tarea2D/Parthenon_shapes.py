import scene_graph as sg;
import basic_shapes as bs;
import easy_shaders as es;
import transformations as tr;
from OpenGL.GL import *

def base():
	gpuQuad = es.toGPUShape(bs.createTextureQuad("ground.jpg"), GL_REPEAT, GL_NEAREST)

	base_s =  sg.SceneGraphNode("base_scaled")
	base_s.transform = tr.matmul([tr.uniformScale(1),tr.scale(39,84,1)])
	base_s.childs += [gpuQuad]

	return base_s

