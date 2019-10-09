import scene_graph as sg;
import basic_shapes as bs;
import easy_shaders as es;
import transformations as tr;
import lighting_shaders as ls;
import glfw
from OpenGL.GL import *
import numpy as np;
import sys
from Parthenon_shapes import *

INT_BYTE = 4

class Controller:
	def __init__(self):
		self.fillPolygon = True
		self.pos = [0.0, 0.0, 0.0]
		self.mousePos = (0.0, 0.0)
		self.alpha = 0
controller = Controller()

def cursor_pos_callback(window, x, y):
    global controller
    controller.mousePos = (x,y)

def on_key(window, key, scancode, action, mods):
	step=0.3
	global controller
	if action == glfw.REPEAT or action ==glfw.PRESS:
		if key == glfw.KEY_D:
			controller.pos[0] += step*np.cos(-controller.alpha)
			controller.pos[1] += step*np.sin(-controller.alpha)
		elif key == glfw.KEY_A:
			controller.pos[0] -= step*np.cos(-controller.alpha)
			controller.pos[1] -= step*np.sin(-controller.alpha)
		elif key == glfw.KEY_W:
			controller.pos[0] += step*np.sin(controller.alpha)
			controller.pos[1] += step*np.cos(controller.alpha)
		elif key == glfw.KEY_S:
			controller.pos[0] -= step*np.sin(controller.alpha)
			controller.pos[1] -= step*np.cos(controller.alpha)
		elif key == glfw.KEY_LEFT_SHIFT:
			controller.pos[2] -= step/3
		elif key == glfw.KEY_SPACE:
			controller.pos[2] += step/3

	if action != glfw.PRESS:
		return
	if key == glfw.KEY_ENTER:
		controller.fillPolygon = not controller.fillPolygon
		print("Toggle GL_FILL/GL_LINE")
	elif key == glfw.KEY_ESCAPE:
		sys.exit()	
	else:
		print("Unknow key")

# Model


if __name__ == "__main__":
	if not glfw.init():
		sys.exit()
	width = 1366
	height = 768

	window = glfw.create_window(width, height, "Window Name", None, None)

	if not window:
		glfw.terminate()
		sys.exit()

	glfw.make_context_current(window)

	# Connecting the callback function 'on_key' to handle keyboard events
	glfw.set_key_callback(window, on_key)
	glfw.set_cursor_pos_callback(window, cursor_pos_callback)
	
	# Assembling the shader program (pipeline) with both shaders
	phongPipeline = ls.SimpleTexturePhongShaderProgram()
	TextureShader = es.SimpleTextureModelViewProjectionShaderProgram()
	phongPipeline = ls.SimpleTexturePhongShaderProgram()

	# Telling OpenGL to use our shader program
	glUseProgram(phongPipeline.shaderProgram)

	# Setting up the clear screen program
	glClearColor(1, 1, 1, 1.0)

	# Creating shapes on GPU memory
	ground = base()
	estructura = estructura()

	glEnable(GL_DEPTH_TEST)
	# Our shapes here are always fully painted
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

	# Proyeccion (Perspectiva)
	projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

	model = tr.identity()

	while not glfw.window_should_close(window):
		# Using GLFW to check for input events
		glfw.poll_events()

		# Filling or not the chapes depending on the controller state
		if controller.fillPolygon:
			glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
		else:
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

		# Clearing the screen in both, color and depth
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		# Colisiones

		# Vista-Camara
		mousePosX = 2 * (controller.mousePos[0] - width/2) / width
		controller.alpha = mousePosX*np.pi

		mousePosX = np.sin(controller.alpha)
		mousePosY = np.cos(controller.alpha)
		mousePosZ = 2 * (height/2 - controller.mousePos[1]) / height
		#print(mousePosX, mousePosY, mousePosZ, controller.alpha*180/np.pi)
		sense=1
		at  = np.array([controller.pos[0]+sense*mousePosX, controller.pos[1]+sense*mousePosY, controller.pos[2]+2*sense*mousePosZ]) #Listo
		eye = np.array([controller.pos[0], controller.pos[1], controller.pos[2]])
		up  = np.array([0,0,1])
		normal_view = tr.lookAt(eye, at, up)
		print(at[0],at[1],at[2])

		#Textura
		#glUseProgram(TextureShader.shaderProgram)
		#glUniformMatrix4fv(glGetUniformLocation(TextureShader.shaderProgram, "projection"), 1, GL_TRUE, projection)
		#glUniformMatrix4fv(glGetUniformLocation(TextureShader.shaderProgram, "view"), 1, GL_TRUE, normal_view)
		#glUniformMatrix4fv(glGetUniformLocation(TextureShader.shaderProgram, "model"), 1, GL_TRUE, model)


		#Iluminacion
		glUseProgram(phongPipeline.shaderProgram)
		# White light in all components: ambient, diffuse and specular.
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

		# Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ka"), 0.5, 0.5, 0.3)
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ks"), 0.3, 0.3, 0.3)

		# TO DO: Explore different parameter combinations to understand their effect!
		#7 * np.sin(glfw.get_time() / 2
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "lightPosition"), 10, 0, 20)
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "viewPosition"), eye[0], eye[1], eye[2])
		glUniform1ui(glGetUniformLocation(phongPipeline.shaderProgram, "shininess"), 100)

		glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "constantAttenuation"), 0.001)
		glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "linearAttenuation"), 0.1)
		glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

		glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
		glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "view"), 1, GL_TRUE, normal_view)
		glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "model"), 1, GL_TRUE, model)

		sg.drawSceneGraphNode(estructura, phongPipeline, "model")
		

		# Once the render is done, buffers are swapped, showing only the complete scene.
		glfw.swap_buffers(window)
	glfw.terminate()
