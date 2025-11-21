import glm # pip install PyGLM
from OpenGL.GL import *
from numpy import array, float32


class Buffer(object):
	def __init__(self, data):
		self.data = data

		# Vertex Buffer
		self.vertexBuffer = array(self.data, dtype = float32)

		# Vertex Buffer Object
		self.VBO = glGenBuffers(1)

		# subir datos a GPU una sola vez (no en cada frame)
		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
		glBufferData(GL_ARRAY_BUFFER,
					 self.vertexBuffer.nbytes,
					 self.vertexBuffer,
					 GL_STATIC_DRAW)
		# unbind para evitar que buffers posteriores sobrescriban este
		glBindBuffer(GL_ARRAY_BUFFER, 0)


	def Use(self, attribNumber, size):

		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

		# ya no llamamos glBufferData aquí - los datos ya están en GPU

		# Atributo
		glVertexAttribPointer(attribNumber,			# Attribute Number
							  size,					# Size
							  GL_FLOAT,				# Type
							  GL_FALSE,				# Is it normalized?
							  0,					# Stride
							  ctypes.c_void_p(0))	# Offset

		glEnableVertexAttribArray(attribNumber)
		