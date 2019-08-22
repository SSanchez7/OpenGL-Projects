#Se importan librerias a ocupar
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations as tr
import scene_graph as sg
import easy_shaders as es
from shapes import *


##VARIBABLS GLOBALES (CONTROLLER)##
class Controller:
    def __init__(self):
        self.av1 = 0.0
        self.av2 = 0.0
        self.av3 = 0.0
        self.av4 = 0.0
        self.fillPolygon = True
controller=Controller()

##CAMBIOS AL TECLEAR (ON_KEY)##
def on_key(window, key, scancode, action, mods):
    global controller
    if action == glfw.REPEAT or action ==glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            controller.av1-=0.008
            controller.av2-=0.015
            controller.av3-=0.025
            controller.av4-=0.04
        elif key == glfw.KEY_LEFT:
            controller.av1+=0.001
            controller.av2+=0.008
            controller.av3+=0.018
            controller.av4+=0.033
        if action != glfw.PRESS:
            return
        elif key == glfw.KEY_1:
            controller.fillPolygon = not controller.fillPolygon
        elif key == glfw.KEY_ESCAPE:
            sys.exit()
        else:
            print("Unknow key")

##GPUSHAPE##

##FUNCION DIBUJAR (DRAWSHAPE)##

##FUNCIONES DE CREACION DE FIGURAS##
def escena():
    mapa = np.array([es.toGPUShape(quad([1, 1, 1],[0, 0.66])),
					 es.toGPUShape(quad([1, 1, 0],[0, 0.33])),
					 es.toGPUShape(quad([0, 1, 1],[0,-0.33])),
					 es.toGPUShape(quad([1, 0, 1],[0,-0.66])),])

    escena = sg.SceneGraphNode("escena")
    baseName="mapa"
    for i in range(len(mapa)):
    	firstNode = sg.SceneGraphNode("capa"+str(i+1))
    	for j in range(3):
    		p=-1 if j==0 else 0 if j==1 else +1
    		secondNode = sg.SceneGraphNode(baseName+str(i+1)+str(p))
    		secondNode.transform = tr.translate(2*p,0,0)
    		secondNode.childs += [mapa[i]]
    		firstNode.childs += [secondNode]
    	escena.childs += [firstNode]
    
    escena.childs += [vehiculo()]
    
    return escena

##OPENGL MAIN##
def main():
    if not glfw.init():
        sys.exit()
    width = 600
    height = 600
    window = glfw.create_window(width,height,"Drawing", None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)

    glfw.set_key_callback(window, on_key)

    pipeline = es.SimpleTransformShaderProgram()

    ##SHADERS## 

    ##DECLARACION DEL PIPELINE##

    glUseProgram(pipeline.shaderProgram)

    glClearColor(0.85, 0.85, 0.85, 1.0)

    nuevaEscena=escena()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glClear(GL_COLOR_BUFFER_BIT)

        if abs(controller.av4)>2:
        	controller.av4=0
        if abs(controller.av3)>2:
        	controller.av3=0
       	if abs(controller.av2)>2:
        	controller.av2=0
       	if abs(controller.av1)>2:
        	controller.av1=0

        sg.findNode(nuevaEscena, "capa1").transform = tr.translate(controller.av1, 0,0)
        sg.findNode(nuevaEscena, "capa2").transform = tr.translate(controller.av2, 0,0)
        sg.findNode(nuevaEscena, "capa3").transform = tr.translate(controller.av3, 0,0)
        sg.findNode(nuevaEscena, "capa4").transform = tr.translate(controller.av4, 0,0)
        
        sg.drawSceneGraphNode(nuevaEscena, pipeline, "transform")


        glfw.swap_buffers(window)
    glfw.terminate()
main()