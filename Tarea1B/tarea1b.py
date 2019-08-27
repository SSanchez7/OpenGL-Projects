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
        self.theta = 0.0
        self.rotate = 0
        self.time = 0
        self.transicion = 0
        self.light = False
        self.special = False
        self.birdTime = 0
        self.boyaTime = 0
controller=Controller()

##CAMBIOS AL TECLEAR (ON_KEY)##
def on_key(window, key, scancode, action, mods):
    global controller


    if action == glfw.REPEAT or action ==glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            controller.time += 0.1
            controller.rotate = 1
            controller.av1-=0.0005
            controller.av2-=0.003
            controller.av3-=0.008
            controller.av4-=0.05
        elif key == glfw.KEY_LEFT:
            controller.time += 0.1
            controller.rotate = -1
            controller.av1+=0.0001
            controller.av2+=0.001
            controller.av3+=0.005
            controller.av4+=0.03
    else:
        controller.time = 0
        controller.rotate = 0

    if action != glfw.PRESS:
        return
    elif key == glfw.KEY_1:
        controller.light = not controller.light
    elif key == glfw.KEY_2:
        controller.special = not controller.special
    elif key == glfw.KEY_ESCAPE:
        sys.exit()
    else:
        print("Unknow key")

##CREATION FIG##
def escena():
	mapa = np.array([mapa1(),
					 mapa2(),
                     mapa3(),
					 mapa4()])

	#ParallaxEffectLayers
	escena = sg.SceneGraphNode("escena")
	for i in range(len(mapa)):
		firstNode = sg.SceneGraphNode("capa"+str(i+1))
		for j in range(3):
			p=-1 if j==0 else 0 if j==1 else +1
			secondNode = sg.SceneGraphNode("C"+str(i+1)+str(p))
			secondNode.transform = tr.translate(2*p,0,0)
			secondNode.childs += [mapa[i]]
			firstNode.childs += [secondNode]
		escena.childs += [firstNode]

	escena.childs += [vehiculo([87/255, 98/255, 112/255])]
	escena.childs += [ave([0.9,0.9,0.9])]

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
    
    glClearColor(0.85, 0.85, 0.85, 1.0)

    nuevaEscena=escena()

    t0=glfw.get_time()
    while not glfw.window_should_close(window):
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        glfw.poll_events()
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(pipeline.shaderProgram)
        
        #TransitionTime
        if controller.special and controller.transicion<=1:
            controller.transicion += 0.04
        elif not controller.special and controller.transicion >=0:
            controller.transicion -= 0.04
        
        #ParallaxEffect
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
        
        #SpecialMovController
        specialScaleShadowLight = 1-controller.transicion*0.5-int(controller.special)*0.2*np.sin(2*controller.theta)
        specialTranslateCar = controller.transicion*0.5+(int(controller.special)*0.05+int(not controller.special)*0.004)*np.sin(2*controller.theta)
        specialScaleWheel = 1+controller.transicion*0.5
        specialTranslateWhell = -0.2+controller.transicion*0.5+int(controller.special)*0.05*np.sin(2*controller.theta)
        specialTranslatePulse = controller.transicion*0.1+int(controller.special)*0.05*np.sin(2*controller.theta)

        #RotationWheels
        if controller.rotate==1:
            controller.theta -= 0.25*(controller.time**2)/2 if controller.time<=0.5 else 3*dt
        if controller.rotate==-1:
            controller.theta += 0.25*(controller.time**2)/2 if controller.time<=0.5 else 1.5*dt
        rotationWheels = int(not controller.special)*controller.theta*1.3

        #MovsCar
        sg.findNode(nuevaEscena, "sombra").transform = tr.matmul([tr.translate(-0.3,-0.35,0),tr.shearing(5,0,0,0,0,0),tr.scale(1.4,0.2,1),tr.uniformScale(specialScaleShadowLight)])
        sg.findNode(nuevaEscena, "luzPiso").transform = tr.matmul([tr.translate(2,int(not controller.light)*3-0.23,0), tr.scale(2,0.25,1), tr.uniformScale(specialScaleShadowLight)])
        sg.findNode(nuevaEscena, "carroceria").transform = tr.translate(0, specialTranslateCar , 0)
        sg.findNode(nuevaEscena, "pulso").transform = tr.translate(0, specialTranslatePulse, 0)
        sg.findNode(nuevaEscena, "ruedaTrasera").transform = tr.matmul([tr.translate(-0.4, specialTranslateWhell, 0),tr.scale(specialScaleWheel,1-controller.transicion*0.5,1), tr.rotationZ(rotationWheels)])
        sg.findNode(nuevaEscena, "ruedaDelantera").transform = tr.matmul([tr.translate(0.5, specialTranslateWhell, 0),tr.scale(specialScaleWheel,1-controller.transicion*0.5,1), tr.rotationZ(rotationWheels)])
        
        #MovAve
        if controller.birdTime <2.8:
        	controller.birdTime += dt*0.2
        else:
        	controller.birdTime = 0
        moveBirdWing = np.sin(50*controller.birdTime)
       	sg.findNode(nuevaEscena, "ave").transform = tr.matmul([tr.translate(1.2-controller.birdTime,0.3,0), tr.uniformScale(0.5)])
       	sg.findNode(nuevaEscena, "alaIzquierda").transform = tr.matmul([tr.translate(0.01,0.67+0.08*moveBirdWing,0), tr.shearing(0.15*moveBirdWing,0,0,0,0,0), tr.scale(0.1,0.1*moveBirdWing,1)])
       	sg.findNode(nuevaEscena, "alaDerecha").transform = tr.matmul([tr.scale(-1,1,1), tr.translate(0.01,0.67+0.08*moveBirdWing,0), tr.shearing(0.15*moveBirdWing,0,0,0,0,0), tr.scale(0.1,0.1*moveBirdWing,1)])
        
        #MovBoya
        controller.boyaTime += dt*3
        moveBoya =0.004*np.sin(2*controller.boyaTime)
        sg.findNode(nuevaEscena, "cuerpoBoya").transform = tr.matmul([tr.translate(0, moveBoya , 0), tr.rotationZ(2*moveBoya)])

        #Draw
        sg.drawSceneGraphNode(nuevaEscena, pipeline, "transform")



        glfw.swap_buffers(window)
    glfw.terminate()
main()