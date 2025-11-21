from OpenGL.GL import (
	glGenTextures,
	glBindTexture,
	glTexImage2D,
	glGenerateMipmap,
	glActiveTexture,
	glDrawArrays,
	glDisableVertexAttribArray,
	glTexParameteri,
	GL_TEXTURE_2D,
	GL_RGB,
	GL_UNSIGNED_BYTE,
	GL_TEXTURE0,
	GL_TRIANGLES
)
from obj import Obj
from buffer import Buffer

import glm
import os

import pygame

class Model(object):
	def __init__(self, filename):
		self.objFile = Obj(filename)
		# base path for resolving material texture paths
		self.basePath = os.path.dirname(filename)

		self.position = glm.vec3(0,0,0)
		self.rotation = glm.vec3(0,0,0)
		self.scale = glm.vec3(1,1,1)

		self.textures = []
		# submeshes: list of dicts {posBuffer, texBuffer, normalsBuffer, vertexCount, material, textureID}
		self.submeshes = []
		self.posBuffer = None
		self.texCoordsBuffer = None
		self.normalsBuffer = None
		self.vertexCount = 0

		self.BuildBuffers()

	def GetModelMatrix(self):

		identity = glm.mat4(1)

		translateMat = glm.translate(identity, self.position)

		pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
		yawMat =   glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
		rollMat =  glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

		rotationMat = pitchMat * yawMat * rollMat

		scaleMat = glm.scale(identity, self.scale)

		return translateMat * rotationMat * scaleMat


	def BuildBuffers(self):
		# Group faces by material (material can be None)
		groups = {}
		for i, face in enumerate(self.objFile.faces):
			mat = None
			if hasattr(self.objFile, 'faceMaterials') and i < len(self.objFile.faceMaterials):
				mat = self.objFile.faceMaterials[i]
			groups.setdefault(mat, []).append(face)

		# For each group create buffers
		for mat, faces in groups.items():
			positions = []
			texCoords = []
			normals = []
			vertexCount = 0

			for face in faces:
				facePositions = []
				faceTexCoords = []
				faceNormals = []

				for i in range(len(face)):
					facePositions.append( self.objFile.vertices [ face[i][0] - 1 ] )
					# si el índice es 0, usar el valor por defecto (índice 0)
					texIdx = face[i][1] if face[i][1] > 0 else 0
					normIdx = face[i][2] if face[i][2] > 0 else 0
					faceTexCoords.append( self.objFile.texCoords[ texIdx if texIdx == 0 else texIdx - 1 ] )
					faceNormals.append( self.objFile.normals[ normIdx if normIdx == 0 else normIdx - 1 ] )

				# triangle 0
				for value in facePositions[0]: positions.append(value)
				for value in facePositions[1]: positions.append(value)
				for value in facePositions[2]: positions.append(value)

				for value in faceTexCoords[0]: texCoords.append(value)
				for value in faceTexCoords[1]: texCoords.append(value)
				for value in faceTexCoords[2]: texCoords.append(value)

				for value in faceNormals[0]: normals.append(value)
				for value in faceNormals[1]: normals.append(value)
				for value in faceNormals[2]: normals.append(value)

				vertexCount += 3

				# optional quad -> second triangle
				if len(face) == 4:
					for value in facePositions[0]: positions.append(value)
					for value in facePositions[2]: positions.append(value)
					for value in facePositions[3]: positions.append(value)

					for value in faceTexCoords[0]: texCoords.append(value)
					for value in faceTexCoords[2]: texCoords.append(value)
					for value in faceTexCoords[3]: texCoords.append(value)

					for value in faceNormals[0]: normals.append(value)
					for value in faceNormals[2]: normals.append(value)
					for value in faceNormals[3]: normals.append(value)

					vertexCount += 3

			# create buffers for this submesh
			sub = {}
			sub['posBuffer'] = Buffer(positions)
			sub['texBuffer'] = Buffer(texCoords)
			sub['normalsBuffer'] = Buffer(normals)
			sub['vertexCount'] = vertexCount
			sub['material'] = mat
			# try to auto-load texture from material if available
			sub['textureID'] = None
			if mat is not None and hasattr(self.objFile, 'materials') and mat in self.objFile.materials:
				m = self.objFile.materials[mat]
				if 'map_Kd' in m and m['map_Kd']:
					texpath = os.path.join(self.basePath, m['map_Kd'])
					if os.path.exists(texpath):
						sub['textureID'] = self._load_texture(texpath)

			self.submeshes.append(sub)


	def AddTexture(self, filename):
		textureSurface = pygame.image.load(filename)
		textureData = pygame.image.tostring(textureSurface, "RGB", True)

		texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, texture)

		glTexImage2D(GL_TEXTURE_2D,
					 0,
					 GL_RGB,
					 textureSurface.get_width(),
					 textureSurface.get_height(),
					 0,
					 GL_RGB,
					 GL_UNSIGNED_BYTE,
					 textureData)

		glGenerateMipmap(GL_TEXTURE_2D)

		self.textures.append(texture)

	def _load_texture(self, filename):
		"""Load a texture and return its OpenGL id (does not add to textures list)."""
		try:
			textureSurface = pygame.image.load(filename)

			# intentar convertir a RGB si tiene canal alfa
			if textureSurface.get_bytesize() == 4:
				textureData = pygame.image.tostring(textureSurface, "RGBA", True)
				glFormat = GL_UNSIGNED_BYTE
				internalFormat = 4  # RGBA
			else:
				textureData = pygame.image.tostring(textureSurface, "RGB", True)
				glFormat = GL_UNSIGNED_BYTE
				internalFormat = GL_RGB

			texture = glGenTextures(1)
			glBindTexture(GL_TEXTURE_2D, texture)

			glTexImage2D(GL_TEXTURE_2D,
						 0,
						 internalFormat,
						 textureSurface.get_width(),
						 textureSurface.get_height(),
						 0,
						 GL_RGB if internalFormat == GL_RGB else 6408,  # 6408 = GL_RGBA
						 glFormat,
						 textureData)

			glGenerateMipmap(GL_TEXTURE_2D)

			return texture
		except Exception as e:
			print(f"  [WARN] No se pudo cargar textura {filename}: {e}")
			return None


	def Render(self):

		# If submeshes exist, draw them each with their own texture (if any)
		if hasattr(self, 'submeshes') and len(self.submeshes) > 0:
			for sub in self.submeshes:
				texID = sub.get('textureID')
				if texID is not None:
					glActiveTexture(GL_TEXTURE0)
					glBindTexture(GL_TEXTURE_2D, texID)

				sub['posBuffer'].Use(0, 3)
				sub['texBuffer'].Use(1, 2)
				sub['normalsBuffer'].Use(2, 3)

				glDrawArrays(GL_TRIANGLES, 0, sub['vertexCount'])

			# deshabilitar atributos una sola vez fuera del loop
			glDisableVertexAttribArray(0)
			glDisableVertexAttribArray(1)
			glDisableVertexAttribArray(2)

			return

		# Fallback: legacy single-texture model (kept for compatibility)
		for i in range(len(self.textures)):
			glActiveTexture(GL_TEXTURE0 + i)
			glBindTexture(GL_TEXTURE_2D, self.textures[i])

		# legacy buffers (if present)
		if hasattr(self, 'posBuffer'):
			self.posBuffer.Use(0, 3)
		if hasattr(self, 'texCoordsBuffer'):
			self.texCoordsBuffer.Use(1, 2)
		if hasattr(self, 'normalsBuffer'):
			self.normalsBuffer.Use(2, 3)

		if hasattr(self, 'vertexCount'):
			glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		glDisableVertexAttribArray(2)




