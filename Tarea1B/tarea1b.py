#Se importan librerias a ocupar
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations as tr
import scene_graph as sg
import easy_shaders as es
from autoShape import *
from capasShape import *


##VARIBABLS GLOBALES (CONTROLLER)##
class Controller:
    def __init__(self):
        self.av1 = 0.0
        self.av2 = 0.0
        self.av3 = 0.0
        self.av4 = 0.0
        self.fillPolygon = True
        self.shader_to_use = True
        self.theta = 0.0
        self.rotate = 0
        self.time = 0
        self.transicion = 0
        self.light = False
        self.special = False
controller=Controller()

##CAMBIOS AL TECLEAR (ON_KEY)##
def on_key(window, key, scancode, action, mods):
    global controller


    if action == glfw.REPEAT or action ==glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            controller.time += 0.1
            controller.rotate = 1
            controller.av1-=0.008
            controller.av2-=0.015
            controller.av3-=0.025
            controller.av4-=0.04
        elif key == glfw.KEY_LEFT:
            controller.time += 0.1
            controller.rotate = -1
            controller.av1+=0.001
            controller.av2+=0.008
            controller.av3+=0.018
            controller.av4+=0.033
    else:
        controller.time = 0
        controller.rotate = 0

    if action != glfw.PRESS:
        return
    elif key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon
    elif key == glfw.KEY_1:
        controller.light = not controller.light
    elif key == glfw.KEY_2:
        controller.special = not controller.special
    elif key == glfw.KEY_ENTER:
        controller.shader_to_use = not controller.shader_to_use 
        print("Toggle shader program")
    elif key == glfw.KEY_ESCAPE:
        sys.exit()
    else:
        print("Unknow key")

##GPUSHAPE##

##FUNCION DIBUJAR (DRAWSHAPE)##

##FUNCIONES DE CREACION DE FIGURAS##
def escena():
	mapa = np.array([es.toGPUShape(createQuad([1, 1, 1],[0, 0.66])),
					 es.toGPUShape(createQuad([1, 1, 0],[0, 0.33])),
					 es.toGPUShape(createQuad([0, 1, 1],[0,-0.33])),
					 capa1()])

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

	escena.childs += [vehiculo([87/255, 98/255, 112/255])]



	return escena

##OPENGL MAIN##   
def main():
    if not glfw.init():
        sys.exit()
    width = 700
    height = 700
    window = glfw.create_window(width,height,"Drawing", None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)

    glfw.set_key_callback(window, on_key)

    pipeline = es.SimpleTransformShaderProgram()
    pipelineNight = es.SimpleTransformShaderProgramNight()

    ##SHADERS## 

    ##DECLARACION DEL PIPELINE##

    
    glClearColor(0.85, 0.85, 0.85, 1.0)

    def timeLapse(condicion):
        if condicion and controller.transicion<=1:
            controller.transicion += 0.025
        elif not condicion and controller.transicion >=0:
            controller.transicion -= 0.025


    nuevaEscena=escena()

    t0=glfw.get_time()
    while not glfw.window_should_close(window):

        t1 = glfw.get_time()
        dt = t1 - t0
        t0 =t1

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

        if controller.shader_to_use:
        	glUseProgram(pipeline.shaderProgram)
        else:
        	glUseProgram(pipelineNight.shaderProgram)
       
        
        if controller.rotate==1:
            controller.theta -= 0.25*(controller.time**2)/2 if controller.time<=0.5 else 3*dt
        if controller.rotate==-1:
            controller.theta += 0.25*(controller.time**2)/2 if controller.time<=0.5 else 1.5*dt
        
        #Movimiento especial secreto
        
        timeLapse(controller.special)
        
        
        #SpecialController
        specialScaleShadowLight = 1-controller.transicion*0.5-int(controller.special)*0.2*np.sin(2*controller.theta)
        #specialScaleBar = controller.transicion*4+int(controller.special)*np.sin(2*controller.theta)

        specialTranslateCar = controller.transicion*0.5+(int(controller.special)*0.05+int(not controller.special)*0.004)*np.sin(2*controller.theta)
        specialScaleWheel = 1+controller.transicion*0.5
        specialTranslateWhell = -0.2+controller.transicion*0.5+int(controller.special)*0.05*np.sin(2*controller.theta)
        
        sg.findNode(nuevaEscena, "sombra").transform = tr.matmul([tr.translate(0.1,-0.28,0),tr.shearing(1.3,0,0,0,0,0),tr.scale(1.4,0.1,1),tr.uniformScale(specialScaleShadowLight)])
        sg.findNode(nuevaEscena, "luzPiso").transform = tr.matmul([tr.translate(2,int(not controller.light)*3-0.23,0), tr.scale(2,0.25,1), tr.uniformScale(specialScaleShadowLight)])
        sg.findNode(nuevaEscena, "carroceria").transform = tr.translate(0, specialTranslateCar , 0)
        
        sg.findNode(nuevaEscena, "capa1").transform = tr.translate(controller.av1, 0,0)
        sg.findNode(nuevaEscena, "capa2").transform = tr.translate(controller.av2, 0,0)
        sg.findNode(nuevaEscena, "capa3").transform = tr.translate(controller.av3, 0,0)
        sg.findNode(nuevaEscena, "capa4").transform = tr.translate(controller.av4, 0,0)

        sg.findNode(nuevaEscena, "pulso").transform = tr.translate(0, controller.transicion*0.1+int(controller.special)*0.05*np.sin(2*controller.theta), 0)

        sg.findNode(nuevaEscena, "ruedaTrasera").transform = tr.matmul([tr.translate(-0.4, specialTranslateWhell, 0),tr.scale(specialScaleWheel,1-controller.transicion*0.5,1), tr.rotationZ(int(not controller.special)*controller.theta)])
        sg.findNode(nuevaEscena, "ruedaDelantera").transform = tr.matmul([tr.translate(0.5, specialTranslateWhell, 0),tr.scale(specialScaleWheel,1-controller.transicion*0.5,1), tr.rotationZ(int(not controller.special)*controller.theta)])
        #sg.findNode(nuevaEscena, "special").transform = tr.matmul([tr.translate(0,0.1,0),tr.scale(1,specialScaleBar,1)])
        
        sg.drawSceneGraphNode(nuevaEscena, pipeline, "transform")


        glfw.swap_buffers(window)
    glfw.terminate()
main()