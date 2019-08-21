#Se importan librerias a ocupar
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import transformations as tr
import sys

INT_BYTES = 4

##VARIBABLS GLOBALES (CONTROLLER)##
class Controller:
    def __init__(self):
        self.av1 = 0.0
        self.av2 = 0.0
        self.av3 = 0.0
        self.fillPolygon = True
controller=Controller()

##CAMBIOS AL TECLEAR (ON_KEY)##
def on_key(window, key, scancode, action, mods):
    global controller
    if action == glfw.REPEAT or action ==glfw.PRESS:
        if key == glfw.KEY_SPACE:
            controller.av1-=0.04
            controller.av2-=0.02
            controller.av3-=0.01
        if action != glfw.PRESS:
            return
        elif key == glfw.KEY_1:
            controller.fillPolygon = not controller.fillPolygon
        elif key == glfw.KEY_ESCAPE:
            sys.exit()
        else:
            print("Unknow key")

##GPUSHAPE##
class GPUShape:
    def __init__(self):
        self.vao = 0
        self.vbo = 0
        self.ebo = 0
        self.texture = 0
        self.size = 0

##FUNCION DIBUJAR (DRAWSHAPE)##
def drawShape(shaderProgram, shape, transform):
    glBindVertexArray(shape.vao)
    glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)
    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_TRUE, transform)
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)
    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)
    glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)

##FUNCIONES DE CREACION DE FIGURAS##
def escena(color, inicio):
    gpuShape = GPUShape()

    vertexData = np.array([
        inicio[0]-0.5, inicio[1]-0.5, 0.0, color[0], color[1], color[2],
        inicio[0]+0.5, inicio[1]-0.5, 0.0, color[0], color[1], color[2],
        inicio[0]+0.5, inicio[1]+0.5, 0.0, color[0], color[1], color[2],
        inicio[0]-0.5, inicio[1]+0.5, 0.0, color[0], color[1], color[2]
    
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

    ##SHADERS##
    vertex_shader = """
    #version 130
    in vec3 position;
    in vec3 color;

    out vec3 fragColor;

    uniform mat4 transform;

    void main()
    {
        fragColor = color;
        gl_Position = transform * vec4(position, 1.0f);
    }
    """

    fragment_shader = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor, 1.0f);
    }
    """

    ##DECLARACION DEL PIPELINE##
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))
    glUseProgram(shaderProgram)

    glClearColor(0.85, 0.85, 0.85, 1.0)

    f1=np.array([escena([1, 0, 1],[0,-0.5]), escena([1, 0, 1],[2,-0.5])])
    f2=np.array([escena([0, 1, 1],[0,   0]), escena([0, 1, 1],[2,   0])])
    f3=np.array([escena([1, 1, 0],[0, 0.5]), escena([1, 1, 0],[2, 0.5])])

    while not glfw.window_should_close(window):
        glfw.poll_events()
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glClear(GL_COLOR_BUFFER_BIT)
        
        t3 = tr.translate(controller.av3, 0, 0)
        t2 = tr.translate(controller.av2, 0, 0)
        t1 = tr.translate(controller.av1, 0, 0)

        if controller.av1<=-2:
            controller.av1=0
        if controller.av2<=-2:
            controller.av2=0
        if controller.av3<=-2:
            controller.av3=0

        for i in range(2):
            drawShape(shaderProgram, f3[i], t3)
            drawShape(shaderProgram, f2[i], t2)
            drawShape(shaderProgram, f1[i], t1)


        glfw.swap_buffers(window)
    glfw.terminate()
main()