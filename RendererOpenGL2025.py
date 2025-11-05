import pygame
import pygame.display
from pygame.locals import *

import glm

from gl import Renderer
from buffer import Buffer
from model import Model
from vertexShaders import *
from fragmentShaders import *

width = 960
height = 540

deltaTime = 0.0


screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()


rend = Renderer(screen)
rend.pointLight = glm.vec3(0, 5, -5)  # Light above and in front of models
rend.ambientLight = 0.4  # More ambient light to see models better

# Ensure back-face culling is disabled so models with arbitrary winding are visible
glDisable(GL_CULL_FACE)

# Make sure filled mode is ON (not wireframe)
if not rend.filledMode:
    rend.ToggleFilledMode()

currVertexShader = vertex_shader
currFragmentShader = rim_lighting_shader

rend.SetShaders(currVertexShader, currFragmentShader)

skyboxTextures = ["skybox/right.jpg",
				  "skybox/left.jpg",
				  "skybox/top.jpg",
				  "skybox/bottom.jpg",
				  "skybox/front.jpg",
				  "skybox/back.jpg"]

rend.CreateSkybox(skyboxTextures)


faceModel = Model("models/iron_golem.obj")
# Texture will be loaded automatically from MTL file
faceModel.AddTexture("textures/lava_cracks.jpg")  # Additional texture for effects
faceModel.position.y = -10
faceModel.position.z = -45  # Moved back for better view
faceModel.scale = glm.vec3(0.8, 0.8, 0.8)  # Slightly smaller for better framing

rend.scene.append(faceModel)

isRunning = True

while isRunning:

	deltaTime = clock.tick(60) / 1000

	rend.elapsedTime += deltaTime

	keys = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_f:
				rend.ToggleFilledMode()

			if event.key == pygame.K_1:
				currFragmentShader = rim_lighting_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_2:
				currFragmentShader = fresnel_metallic_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_3:
				currFragmentShader = procedural_patterns_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_4:
				currFragmentShader = gooch_shading_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_5:
				currFragmentShader = psychedelic_warp_shader
				rend.SetShaders(currVertexShader, currFragmentShader)


			if event.key == pygame.K_7:
				currVertexShader = vertex_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_8:
				currVertexShader = fat_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_9:
				currVertexShader = water_shader
				rend.SetShaders(currVertexShader, currFragmentShader)


	if keys[K_UP]:
		rend.camera.position.z += 1 * deltaTime

	if keys[K_DOWN]:
		rend.camera.position.z -= 1 * deltaTime

	if keys[K_RIGHT]:
		rend.camera.position.x += 1 * deltaTime

	if keys[K_LEFT]:
		rend.camera.position.x -= 1 * deltaTime



	if keys[K_w]:
		rend.pointLight.z -= 10 * deltaTime

	# if keys[K_s]:
	# 	rend.pointLight.z += 10 * deltaTime

	# if keys[K_a]:
	# 	rend.pointLight.x -= 10 * deltaTime

	# if keys[K_d]:
	# 	rend.pointLight.x += 10 * deltaTime

	# if keys[K_q]:
	# 	rend.pointLight.y -= 10 * deltaTime

	# if keys[K_e]:
	# 	rend.pointLight.y += 10 * deltaTime


	if keys[K_z]:
		if rend.value > 0.0:
			rend.value -= 1 * deltaTime

	if keys[K_x]:
		if rend.value < 1.0:
			rend.value += 1 * deltaTime



	# Rotate the current model
	models[currentModelIndex].rotation.y += 45 * deltaTime


	rend.Render()
	pygame.display.flip()

pygame.quit()