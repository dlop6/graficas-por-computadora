from OpenGL.GL import *
from buffer import Buffer
import glm

class Stage(object):
	"""plataforma procedural simple para el diorama"""
	def __init__(self, size=50, height=1.0):
		self.position = glm.vec3(0, 0, 0)
		self.rotation = glm.vec3(0, 0, 0)
		self.scale = glm.vec3(1, 1, 1)

		# crear geometría de plataforma (simple cubo plano)
		half = size / 2.0
		h = height

		# vértices del cubo
		positions = [
			# cara superior (donde van los pokémon)
			-half, h, -half,
			 half, h, -half,
			 half, h,  half,
			-half, h, -half,
			 half, h,  half,
			-half, h,  half,

			# cara inferior
			-half, 0, -half,
			 half, 0,  half,
			 half, 0, -half,
			-half, 0, -half,
			-half, 0,  half,
			 half, 0,  half,

			# cara frontal
			-half, 0,  half,
			-half, h,  half,
			 half, h,  half,
			-half, 0,  half,
			 half, h,  half,
			 half, 0,  half,

			# cara trasera
			-half, 0, -half,
			 half, h, -half,
			-half, h, -half,
			-half, 0, -half,
			 half, 0, -half,
			 half, h, -half,

			# cara izquierda
			-half, 0, -half,
			-half, h, -half,
			-half, h,  half,
			-half, 0, -half,
			-half, h,  half,
			-half, 0,  half,

			# cara derecha
			 half, 0, -half,
			 half, h,  half,
			 half, h, -half,
			 half, 0, -half,
			 half, 0,  half,
			 half, h,  half,
		]

		# coordenadas de textura simples
		texCoords = []
		for i in range(36):  # 6 caras * 6 vértices
			face_idx = i // 6
			vert_idx = i % 6
			# patrón básico para cada cara
			tc = [(0,0), (1,0), (1,1), (0,0), (1,1), (0,1)]
			texCoords.extend(tc[vert_idx])

		# normales para cada cara
		normals = [
			# superior
			0, 1, 0,  0, 1, 0,  0, 1, 0,
			0, 1, 0,  0, 1, 0,  0, 1, 0,
			# inferior
			0, -1, 0,  0, -1, 0,  0, -1, 0,
			0, -1, 0,  0, -1, 0,  0, -1, 0,
			# frontal
			0, 0, 1,  0, 0, 1,  0, 0, 1,
			0, 0, 1,  0, 0, 1,  0, 0, 1,
			# trasera
			0, 0, -1,  0, 0, -1,  0, 0, -1,
			0, 0, -1,  0, 0, -1,  0, 0, -1,
			# izquierda
			-1, 0, 0,  -1, 0, 0,  -1, 0, 0,
			-1, 0, 0,  -1, 0, 0,  -1, 0, 0,
			# derecha
			1, 0, 0,  1, 0, 0,  1, 0, 0,
			1, 0, 0,  1, 0, 0,  1, 0, 0,
		]

		self.posBuffer = Buffer(positions)
		self.texCoordsBuffer = Buffer(texCoords)
		self.normalsBuffer = Buffer(normals)
		self.vertexCount = 36

	def GetModelMatrix(self):
		identity = glm.mat4(1)
		translateMat = glm.translate(identity, self.position)
		pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
		yawMat = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
		rollMat = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))
		rotationMat = pitchMat * yawMat * rollMat
		scaleMat = glm.scale(identity, self.scale)
		return translateMat * rotationMat * scaleMat

	def Render(self):
		self.posBuffer.Use(0, 3)
		self.texCoordsBuffer.Use(1, 2)
		self.normalsBuffer.Use(2, 3)

		glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		glDisableVertexAttribArray(2)
