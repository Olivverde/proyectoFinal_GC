
# Inner Libs
from matrixTrans import *
from objReader import *
# External Libs
import pygame
import numpy
from PIL import Image
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
import random
# Consts
WIDTH = 800
HEIGHT = 500
ASPECT_RATIO = WIDTH/HEIGHT
# Initial config
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
glClearColor(0, 0, 0, 1)
glEnable(GL_DEPTH_TEST)
clock = pygame.time.Clock()
#-----------ENDS--INITIAL--CONFIGS------------------------------------------------------------


#-----------FIRST--SHADER---------------------------------------------------------------------
# Reference --> https://learnopengl.com/Getting-started/Textures
# Use of Texture
img = Image.open('fire.bmp') 
pixels = numpy.array(list(img.getdata()), numpy.int8)
textureID = glGenTextures(1);
glBindTexture(GL_TEXTURE_2D, textureID);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, pixels)

vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 vTexture;

uniform mat4 matrix;
out vec2 texCoord;
void main()
{
     gl_Position = matrix * vec4(position.x, position.y, position.z, 1);
     texCoord = vTexture; 
}
"""
fragment_shader = """
#version 460
in vec2 texCoord;
out vec4 color;
uniform sampler2D ourTexture;
void main()
{
       color = texture(ourTexture, texCoord); 
}
"""
compiler = compileShader(vertex_shader, GL_VERTEX_SHADER)
fragment = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
secondShader = compileProgram(compiler, fragment)
# Initial Texture
#-----------SECOND--SHADER---------------------------------------------------------------------
# Use of Norms
vertex_shader_the_second = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 currentcolor;
uniform mat4 matrix;
out vec3 choosencolor;
void main() 
{
  gl_Position = matrix * vec4(position.x, position.y, position.z, 1);
  choosencolor = currentcolor;
}
"""
fragment_shader_the_second = """
#version 460
layout(location = 0) out vec4 color;
uniform int clock;
in vec3 choosencolor;
void main()
{
  if (mod(clock/2, 2) == 0) {
    color = vec4(choosencolor.xxx, 1.0f)*vec4(0, 1.0, 1.0, 1.0);
  } else if (mod(clock/2, 1) == 0) {
    color = vec4(choosencolor.yyy, 1.0f)*vec4(0, 1.0, 1.0, 1.0);
  }
}
"""
vertexShader = compileShader(vertex_shader_the_second, GL_VERTEX_SHADER)
fragmentShader = compileShader(fragment_shader_the_second, GL_FRAGMENT_SHADER)
firstShader = compileProgram(vertexShader, fragmentShader)
# -----------THIRD--SHADER---------------------------------------------------------------------
fragment_shader_the_return = """
#version 460
layout(location = 0) out vec4 anotherColor;
uniform vec3 color;
void main()
{
  anotherColor = vec4(color.xyz, 1.0f);
}
"""
compiler_3 = compileShader(vertex_shader, GL_VERTEX_SHADER)
fragment_3 = compileShader(fragment_shader_the_return, GL_FRAGMENT_SHADER)

the_final_shader = compileProgram(compiler_3, fragment_3)

#-----------OBJ--MODEL---------------------------------------------------------------------
objModel = Obj('./alien.obj')
vertex_data = numpy.hstack((numpy.array(objModel.v, dtype=numpy.float32),numpy.array(objModel.vt, dtype=numpy.float32),)).flatten()
index_data = numpy.array([[vertex[0] - 1 for vertex in face] for face in objModel.f], dtype=numpy.uint32).flatten()
vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)

glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
element_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(12))
glEnableVertexAttribArray(1)

glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(24))

#-----------ENDS--INITIAL--CONFIGS------------------------------------------------------------
def render(xR, yR, zR, currentSdr):
  
  # Initial configs
  i = glm.mat4(1.0) # Identity Matrix
  position = glm.translate(i, glm.vec3(0, -2, -2))
  size = glm.scale(i, glm.vec3(1/2, 1/2, 1/2))
  # Variable rotation
  currentRotation = rotationMatrix((xR, yR, zR))
  # Building the Matrix
  alienMod = position*size*currentRotation # Alien in current space
  camera = glm.lookAt(glm.vec3(10, 0, 20), glm.vec3(0, 1, 0), glm.vec3(0, 1, 0)) # Current View
  perspective = glm.perspective(glm.radians(45), ASPECT_RATIO, 0.1, 1000.0) # Current Perspective
  matrix = perspective * camera * alienMod
  glUniformMatrix4fv(glGetUniformLocation(currentSdr, 'matrix'),1,GL_FALSE,glm.value_ptr(matrix))
  
currentSdr = firstShader
# ViewPort
x, y, z = 0, 0, 0
glViewport(0, 0, WIDTH, HEIGHT)
# flags
flag = 0
sdrFlag = 0
booleanFlag = True

while booleanFlag:
  glUseProgram(currentSdr)
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
  # Render Runtime
  render(x, y, z, currentSdr)
  flag += 1

  if (currentSdr != the_final_shader): # clock impl
      glUniform1i(glGetUniformLocation(currentSdr, 'clock'), flag)

  else:
      r,g,b = 1,0,0
      glUniform3f(glGetUniformLocation(currentSdr, 'color'), r, g, b)
      
  clock.tick(25)
  glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, None)
  pygame.display.flip()

  movementScl = 0.4
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      booleanFlag = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP: # Up pad for +X movement
        x += movementScl
      elif event.key == pygame.K_DOWN: # Down pad for -X movement
        x -= movementScl
      elif event.key == pygame.K_RIGHT: # Right pad for +Y movement
        y += movementScl
      elif event.key == pygame.K_LEFT: # Left pad for -Y movement
        y -= movementScl
      elif event.key == pygame.K_1: # N°1 for +Z movement
        z += movementScl
      elif event.key == pygame.K_2: # N°2 for -Z movement
        z -= movementScl
      
      elif event.key == pygame.K_SPACE: # Space pad for Shader Changing
        if (sdrFlag == 0):
          currentSdr = firstShader
        elif (sdrFlag == 1):
          currentSdr = secondShader
        else:
          currentSdr = the_final_shader
        sdrFlag += 1
        sdrFlag = sdrFlag % 3