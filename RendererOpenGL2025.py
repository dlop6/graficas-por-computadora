import pygame
import pygame.display
from pygame.locals import *

import glm

from gl import Renderer
from buffer import Buffer
from model import Model
from vertexShaders import *
from fragmentShaders import *
<<<<<<< HEAD
from postProcessingShaders import *
=======
>>>>>>> Lab-9

width = 960
height = 540

deltaTime = 0.0


screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()


rend = Renderer(screen)
rend.pointLight = glm.vec3(1,1,1)

currVertexShader = vertex_shader
<<<<<<< HEAD
currFragmentShader = fragment_shader

rend.SetShaders(currVertexShader, currFragmentShader)

rend.SetPostProcessingShaders(vertex_postProcess, none_postProcess)


=======
currFragmentShader = rim_lighting_shader

rend.SetShaders(currVertexShader, currFragmentShader)

>>>>>>> Lab-9
skyboxTextures = ["skybox/right.jpg",
				  "skybox/left.jpg",
				  "skybox/top.jpg",
				  "skybox/bottom.jpg",
				  "skybox/front.jpg",
				  "skybox/back.jpg"]

rend.CreateSkybox(skyboxTextures)


<<<<<<< HEAD
faceModel = Model("models/model.obj")
faceModel.AddTexture("textures/model.bmp")
faceModel.AddTexture("textures/lava_cracks.jpg")
faceModel.position.z = -5
faceModel.visible = True

spiderman = Model("models/spidey.obj")
spiderman.AddTexture("textures/spidey_body_diff.png")
spiderman.AddTexture("textures/lava_cracks.jpg")
spiderman.position.z = -5
spiderman.rotation.y = 180
spiderman.scale.x = 0.02
spiderman.scale.y = 0.02
spiderman.scale.z = 0.02
spiderman.visible = False


modelIndex = 0
postProcessIndex = 0

postProcesses = [none_postProcess,
				 grayScale_postProcess,
				 negative_postProcess,
				 hurt_postProcess,
				 depth_postProcess,
				 fog_postProcess,
				 dof_postProcess,
				 edgeDetection_postProcess,
				 outline_postProcess]

camAngle = 0

rend.scene.append(faceModel)
rend.scene.append(spiderman)
=======
faceModel = Model("models/iron_golem.obj")
# Texture will be loaded automatically from MTL file
faceModel.AddTexture("textures/lava_cracks.jpg")  # Additional texture for effects
faceModel.position.y = -10
faceModel.position.z = -45  # Moved back for better view
faceModel.scale = glm.vec3(0.8, 0.8, 0.8)  # Slightly smaller for better framing

rend.scene.append(faceModel)
>>>>>>> Lab-9

isRunning = True

while isRunning:

	deltaTime = clock.tick(60) / 1000

	rend.elapsedTime += deltaTime

	keys = pygame.key.get_pressed()
<<<<<<< HEAD
	mouseVel = pygame.mouse.get_rel()

=======
>>>>>>> Lab-9

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False

<<<<<<< HEAD

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[2]:
				modelIndex += 1
				modelIndex %= len(rend.scene)
				for i in range(len(rend.scene)):
					rend.scene[i].visible = i == modelIndex


		elif event.type == pygame.MOUSEWHEEL:
			rend.camera.position.z -= event.y * deltaTime * 10


=======
>>>>>>> Lab-9
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_f:
				rend.ToggleFilledMode()

<<<<<<< HEAD

			if event.key == pygame.K_TAB:
				postProcessIndex += 1
				postProcessIndex %= len(postProcesses)
				rend.SetPostProcessingShaders(vertex_postProcess, postProcesses[postProcessIndex])

			if event.key == pygame.K_1:
				currFragmentShader = fragment_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_2:
				currFragmentShader = toon_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_3:
				currFragmentShader = negative_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_4:
				currFragmentShader = magma_shader
=======
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
>>>>>>> Lab-9
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


<<<<<<< HEAD
=======
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

	if keys[K_s]:
		rend.pointLight.z += 10 * deltaTime

	if keys[K_a]:
		rend.pointLight.x -= 10 * deltaTime

	if keys[K_d]:
		rend.pointLight.x += 10 * deltaTime

	if keys[K_q]:
		rend.pointLight.y -= 10 * deltaTime

	if keys[K_e]:
		rend.pointLight.y += 10 * deltaTime


>>>>>>> Lab-9
	if keys[K_z]:
		if rend.value > 0.0:
			rend.value -= 1 * deltaTime

	if keys[K_x]:
		if rend.value < 1.0:
			rend.value += 1 * deltaTime

<<<<<<< HEAD
	if pygame.mouse.get_pressed()[0]:
		rend.camera.position.x += mouseVel[0] * deltaTime
		rend.camera.position.y += mouseVel[1] * deltaTime
=======


	faceModel.rotation.y += 45 * deltaTime

>>>>>>> Lab-9

	rend.Render()
	pygame.display.flip()

pygame.quit()