import scene_graph as sg;
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
		self.pos = [0.0, -47.0, 0.5]
		self.posSolX = 70
		self.mousePos = (0.0, 0.0)
		self.alpha = 0
		self.sol = True
controller = Controller()

def cursor_pos_callback(window, x, y):
    global controller
    controller.mousePos = (x,y)

def on_key(window, key, scancode, action, mods):
	global controller
	if action != glfw.PRESS:
		return
	if key == glfw.KEY_ENTER:
		controller.fillPolygon = not controller.fillPolygon
		print("Toggle GL_FILL/GL_LINE")
	if key == glfw.KEY_I:
		controller.sol = not controller.sol
	elif key == glfw.KEY_ESCAPE:
		sys.exit()	
	else:
		print("Unknow key")
			
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
	phongPipelineColor = ls.SimplePhongShaderProgram()

	# Telling OpenGL to use our shader program
	glUseProgram(phongPipeline.shaderProgram)

	# Setting up the clear screen program
	glClearColor(1, 1, 1, 1.0)

	estructura = estructura()
	fondo_ = fondo([118/255,197/255,228/255])
	suelo = suelo("suelo.jpg")

	glEnable(GL_DEPTH_TEST)
	# Our shapes here are always fully painted
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

	# Proyeccion (Perspectiva)
	projection = tr.perspective(45, float(width)/float(height), 0.1, 100)
	model = tr.identity()

	t0 = glfw.get_time()
	while not glfw.window_should_close(window):
		# Using GLFW to check for input events
		glfw.poll_events()

		t1 = glfw.get_time()
		dt = t1 - t0
		t0 = t1

		# Filling or not the chapes depending on the controller state
		if controller.fillPolygon:
			glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
		else:
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


		# Movimiento
		step=0.3
		if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
			controller.pos[0] += step*np.cos(-controller.alpha)
			controller.pos[1] += step*np.sin(-controller.alpha)
		if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
			controller.pos[0] -= step*np.cos(-controller.alpha)
			controller.pos[1] -= step*np.sin(-controller.alpha)
		if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
			controller.pos[0] += step*np.sin(controller.alpha)
			controller.pos[1] += step*np.cos(controller.alpha)
		if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
			controller.pos[0] -= step*np.sin(controller.alpha)
			controller.pos[1] -= step*np.cos(controller.alpha)
		if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
			controller.pos[2] -= step/3
		if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
			controller.pos[2] += step/3

		# Clearing the screen in both, color and depth
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		# Vista-Camara
		mousePosX = 2 * (controller.mousePos[0] - width/2) / width
		controller.alpha = mousePosX*np.pi

		mousePosX = np.sin(controller.alpha)
		mousePosY = np.cos(controller.alpha)
		mousePosZ = 2 * (height/2 - controller.mousePos[1]) / height

		sense = 1
		at  = np.array([controller.pos[0]+sense*mousePosX, controller.pos[1]+sense*mousePosY, controller.pos[2]+2*sense*mousePosZ]) #Listo
		eye = np.array([controller.pos[0], controller.pos[1], controller.pos[2]])
		up  = np.array([0,0,1])
		normal_view = tr.lookAt(eye, at, up)

		if controller.sol:
			controller.posSolX = 120 if controller.posSolX<-120 else controller.posSolX
			controller.posSolX -= dt*8
		
		#Iluminacion
		glUseProgram(phongPipeline.shaderProgram)

		#Cielo noche     0.5, 0.5, 0.7
		#Cielo Amanecer  1.0, 1.0, 0.7
		#Cielo Mediodia  1.0, 1.0, 1.0
		#Cielo Atardecer 1.0, 0.8, 0.7
		
		night  = np.array([0.5, 0.5, 0.6])
		dawn   = np.array([0.8, 0.8, 0.7])
		midday = np.array([1.0, 1.0, 1.0])
		sunset = np.array([0.8, 0.7, 0.6])
		
		luz = ((controller.posSolX-70)*(dawn-night)/(50-70)) + night  if controller.posSolX<70 and controller.posSolX>50  else (
			   (controller.posSolX-50)*(midday-dawn)/(0-50)) + dawn   if controller.posSolX<50 and controller.posSolX>0   else (
			   (controller.posSolX)*(sunset-midday)/(-50-0)) + midday if controller.posSolX<0  and controller.posSolX>-50 else (
		    (controller.posSolX+50)*(night-sunset)/(-70+50)) + sunset if controller.posSolX<-50 and controller.posSolX>-70 else night

		night = np.array([0.0, 0.0, 0.0])
		refl = ((controller.posSolX-70)*(dawn-night)/(50-70)) + night  if controller.posSolX<70 and controller.posSolX>50  else (
			   (controller.posSolX-50)*(midday-dawn)/(0-50)) + dawn   if controller.posSolX<50 and controller.posSolX>0   else (
			   (controller.posSolX)*(sunset-midday)/(-50-0)) + midday if controller.posSolX<0  and controller.posSolX>-50 else (
		    (controller.posSolX+50)*(night-sunset)/(-70+50)) + sunset if controller.posSolX<-50 and controller.posSolX>-70 else night


		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "La"), luz[0], luz[1], luz[2])
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ld"), refl[0], refl[1], refl[2])
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ls"), refl[0], refl[1], refl[2])

		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ka"), 0.5, 0.5, 0.3)
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Kd"), 0.6, 0.6, 0.6)
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ks"), 0.3, 0.3, 0.3)
		
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "lightPosition"), controller.posSolX, 0, 30)
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "viewPosition"), eye[0], eye[1], eye[2])
		glUniform1ui(glGetUniformLocation(phongPipeline.shaderProgram, "shininess"), 100)

		glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "constantAttenuation"), 0.0001)
		glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "linearAttenuation"), 0.01)
		glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "quadraticAttenuation"), 0.001)

		glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
		glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "view"), 1, GL_TRUE, normal_view)
		glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "model"), 1, GL_TRUE, model)

		sg.drawSceneGraphNode(estructura,phongPipeline,"model")

		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ka"), 0.5, 0.5, 0.5)
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
		glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ks"), 0.0, 0.0, 0.0)
		
		sg.drawSceneGraphNode(suelo,phongPipeline,"model")

		glUseProgram(phongPipelineColor.shaderProgram)

		#Tono claro  1.0, 1.0, 1.0
		#Tono oscuro 0.3, 0.3, 0.3

		tono=((70-abs(controller.posSolX))*0.7/70)+0.3 if abs(controller.posSolX)<70 else 0.3

		glUniform3f(glGetUniformLocation(phongPipelineColor.shaderProgram, "Ka"),tono, tono, tono) 
		glUniform3f(glGetUniformLocation(phongPipelineColor.shaderProgram, "Kd"), 0.0, 0.0, 0.0)
		glUniform3f(glGetUniformLocation(phongPipelineColor.shaderProgram, "Ks"), 0.0, 0.0, 0.0)

		glUniform3f(glGetUniformLocation(phongPipelineColor.shaderProgram, "La"), luz[0], luz[1], luz[2])
		glUniform3f(glGetUniformLocation(phongPipelineColor.shaderProgram, "Ld"), refl[0], refl[1], refl[2])
		glUniform3f(glGetUniformLocation(phongPipelineColor.shaderProgram, "Ls"), refl[0], refl[1], refl[2])
		
		glUniform3f(glGetUniformLocation(phongPipelineColor.shaderProgram, "lightPosition"), controller.posSolX, 0, 30)
		glUniform3f(glGetUniformLocation(phongPipelineColor.shaderProgram, "viewPosition"), eye[0], eye[1], eye[2])
		glUniform1ui(glGetUniformLocation(phongPipelineColor.shaderProgram, "shininess"), 100)

		glUniform1f(glGetUniformLocation(phongPipelineColor.shaderProgram, "constantAttenuation"), 0.0001)
		glUniform1f(glGetUniformLocation(phongPipelineColor.shaderProgram, "linearAttenuation"), 0.01)
		glUniform1f(glGetUniformLocation(phongPipelineColor.shaderProgram, "quadraticAttenuation"), 0.001)

		glUniformMatrix4fv(glGetUniformLocation(phongPipelineColor.shaderProgram, "projection"), 1, GL_TRUE, projection)
		glUniformMatrix4fv(glGetUniformLocation(phongPipelineColor.shaderProgram, "view"), 1, GL_TRUE, normal_view)
		glUniformMatrix4fv(glGetUniformLocation(phongPipelineColor.shaderProgram, "model"), 1, GL_TRUE, model)

		sg.drawSceneGraphNode(fondo_,phongPipelineColor,"model")

		glfw.swap_buffers(window)
	glfw.terminate()
