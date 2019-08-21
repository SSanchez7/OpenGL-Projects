import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import transformations as tr
import sys

def cuadrado(color, posicion):
	gpuShape = GPUShape()
	lado=0.25
	vertexData = np.array([
        posicion[0]-lado, posicion[1]-lado, 0.0, color[0], color[1], color[2],
        posicion[0]+lado, posicion[1]-lado, 0.0, color[0], color[1], color[2],
        posicion[0]+lado, posicion[1]+lado, 0.0, color[0], color[1], color[2],
        posicion[0]-lado, posicion[1]+lado, 0.0, color[0], color[1], color[2]
    ], dtype=np.float32)

	indices = np.array(
        [0, 1, 2,
         2, 3, 0], dtype=np.uint32)

	gpuShape.size = len(indices)

	gpuShape.vao = glGenVertexArrays(1)
	gpuShape.vbo = glGenBuffers(1)
	gpuShape.ebo = glGenBuffers(1)

	glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
	glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

	return gpuShape

def arbol(color, posicion):
	cuadrado
