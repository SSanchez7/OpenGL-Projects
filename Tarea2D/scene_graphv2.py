# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-2
A simple scene graph class and functionality
"""

from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import basic_shapes as bs

import transformations as tr
import easy_shaders as es


# A simple class to handle a scene graph
# Each node represents a group of objects
# Each leaf represents a basic figure (GPUShape)
# To identify each node properly, it MUST have a unique name
class SceneGraphNode:
    def __init__(self, name):
        self.name = name
        self.transform = tr.identity()
        self.childs = []

    
def findNode(node, name):

    # The name was not found in this path
    if isinstance(node, bs.Shape):
        return None

    # This is the requested node
    if node.name == name:
        return node
    
    # All childs are checked for the requested name
    else:
        for child in node.childs:
            foundNode = findNode(child, name)
            if foundNode != None:
                return foundNode

    # No child of this node had the requested name
    return None


def findTransform(node, name, parentTransform=tr.identity()):

    # The name was not found in this path
    if isinstance(node, bs.Shape):
        return None

    newTransform = np.matmul(parentTransform, node.transform)

    # This is the requested node
    if node.name == name:
        return newTransform
    
    # All childs are checked for the requested name
    else:
        for child in node.childs:
            foundTransform = findTransform(child, name, newTransform)
            if isinstance(foundTransform, (np.ndarray, np.generic) ):
                return foundTransform

    # No child of this node had the requested name
    return None


def findPosition(node, name, parentTransform=tr.identity()):
    foundTransform = findTransform(node, name, parentTransform)

    if isinstance(foundTransform, (np.ndarray, np.generic) ):
        zero = np.array([[0,0,0,1]], dtype=np.float32).T
        foundPosition = np.matmul(foundTransform, zero)
        return foundPosition

    return None

def nueva(node,vertices=[],indices=[],parentTransform=tr.identity()):
    
    vertices_ = vertices
    indices_  = indices
    

    newTransform = np.matmul(parentTransform, node.transform)

    if isinstance(node, bs.Shape):
        textura_  = node.textureFileName
        p = 9 if textura_== None else 8
        v = node.vertices
        k = len(v)/p
        for i in range(k):
            v[p*i,p*i+3] = np.matmul(newTransform,v[p*i,p*i+3])
        vertices_ += v
        k = len(vertices_)/p
        indices_ += k+node.indices
        return vertices_,indices_,textura_
    else:
        for child in node.childs:
            nueva(child,newTransform)
            


    # No child of this node had the requested name
    return None



def drawSceneGraphNode(node, pipeline, transformName, parentTransform=tr.identity(), wrapMode=None, filterMode=None):
    assert(isinstance(node, SceneGraphNode))

    # Composing the transformations through this path
    newTransform = np.matmul(parentTransform, node.transform)

    # If the child node is a leaf, it should be a GPUShape.
    # Hence, it can be drawn with drawShape
    if len(node.childs) == 1 and isinstance(node.childs[0], bs.Shape):
        leaf = es.toGPUShape(node.childs[0], wrapMode, filterMode)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, transformName), 1, GL_TRUE, newTransform)
        pipeline.drawShape(leaf)

    # If the child node is not a leaf, it MUST be a SceneGraphNode,
    # so this draw function is called recursively
    else:
        for child in node.childs:
            drawSceneGraphNode(child, pipeline, transformName, newTransform)

