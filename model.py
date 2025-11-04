<<<<<<< HEAD
from OpenGL.GL import *
=======
from OpenGL.GL import (glGenTextures, glBindTexture, glTexImage2D, glGenerateMipmap,
					   glActiveTexture, glDrawArrays, glDisableVertexAttribArray,
					   GL_TEXTURE_2D, GL_RGB, GL_UNSIGNED_BYTE, GL_TEXTURE0, GL_TRIANGLES)
>>>>>>> Lab-9
from obj import Obj
from buffer import Buffer

import glm
<<<<<<< HEAD
=======
import os
>>>>>>> Lab-9

import pygame

class Model(object):
	def __init__(self, filename):
		self.objFile = Obj(filename)
<<<<<<< HEAD
=======
		# base path for resolving material texture paths
		self.basePath = os.path.dirname(filename)
>>>>>>> Lab-9

		self.position = glm.vec3(0,0,0)
		self.rotation = glm.vec3(0,0,0)
		self.scale = glm.vec3(1,1,1)

<<<<<<< HEAD
		self.BuildBuffers()

		self.textures = []

		self.visible = True

=======
		self.textures = []
		# submeshes: list of dicts {posBuffer, texBuffer, normalsBuffer, vertexCount, material, textureID}
		self.submeshes = []

		self.BuildBuffers()
>>>>>>> Lab-9

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

<<<<<<< HEAD
		positions = []
		texCoords = []
		normals = []

		self.vertexCount = 0

		for face in self.objFile.faces:

			facePositions = []
			faceTexCoords = []
			faceNormals = []

			for i in range(len(face)):
				facePositions.append( self.objFile.vertices [ face[i][0] - 1 ] )
				faceTexCoords.append( self.objFile.texCoords[ face[i][1] - 1 ] )
				faceNormals.append( self.objFile.normals[ face[i][2] - 1 ] )


			for value in facePositions[0]: positions.append(value)
			for value in facePositions[1]: positions.append(value)
			for value in facePositions[2]: positions.append(value)

			for value in faceTexCoords[0]: texCoords.append(value)
			for value in faceTexCoords[1]: texCoords.append(value)
			for value in faceTexCoords[2]: texCoords.append(value)

			for value in faceNormals[0]: normals.append(value)
			for value in faceNormals[1]: normals.append(value)
			for value in faceNormals[2]: normals.append(value)

			self.vertexCount += 3

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

				self.vertexCount += 3


		self.posBuffer = Buffer(positions)
		self.texCoordsBuffer = Buffer(texCoords)
		self.normalsBuffer = Buffer(normals)
=======
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
					faceTexCoords.append( self.objFile.texCoords[ face[i][1] - 1 ] )
					faceNormals.append( self.objFile.normals[ face[i][2] - 1 ] )

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
>>>>>>> Lab-9


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


<<<<<<< HEAD
	def Render(self):

		if not self.visible:
			return

		# Dar la textura
=======
	def _load_texture(self, filename):
		"""Load a texture and return its OpenGL id (does not add to textures list)."""
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

		return texture


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

				glDisableVertexAttribArray(0)
				glDisableVertexAttribArray(1)
				glDisableVertexAttribArray(2)

			return

		# Fallback: legacy single-texture model (kept for compatibility)
>>>>>>> Lab-9
		for i in range(len(self.textures)):
			glActiveTexture(GL_TEXTURE0 + i)
			glBindTexture(GL_TEXTURE_2D, self.textures[i])

<<<<<<< HEAD

		self.posBuffer.Use(0, 3)
		self.texCoordsBuffer.Use(1, 2)
		self.normalsBuffer.Use(2, 3)


		glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)
=======
		# legacy buffers (if present)
		if hasattr(self, 'posBuffer'):
			self.posBuffer.Use(0, 3)
		if hasattr(self, 'texCoordsBuffer'):
			self.texCoordsBuffer.Use(1, 2)
		if hasattr(self, 'normalsBuffer'):
			self.normalsBuffer.Use(2, 3)

		if hasattr(self, 'vertexCount'):
			glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)
>>>>>>> Lab-9

		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		glDisableVertexAttribArray(2)




