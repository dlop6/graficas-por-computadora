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


# Load all three models
print("\n" + "="*60)
print("LOADING MODELS...")
print("="*60)

ironGolemModel = Model("models/iron_golem_clean/iron_golem.obj")
ironGolemModel.AddTexture("textures/lava_cracks.jpg")  # Additional texture for effects
ironGolemModel.position = glm.vec3(0, 0, -10)  # Closer and centered
ironGolemModel.scale = glm.vec3(2.0, 2.0, 2.0)  # Bigger
print(f"✓ Iron Golem loaded - Vertices: {len(ironGolemModel.objFile.vertices)}, Faces: {len(ironGolemModel.objFile.faces)}")

trexModel = Model("models/trex/trex.obj")
trexModel.position = glm.vec3(0, -5, -15)  # Closer
trexModel.scale = glm.vec3(0.05, 0.05, 0.05)  # T-Rex is usually very large, scale down
print(f"✓ T-Rex loaded - Vertices: {len(trexModel.objFile.vertices)}, Faces: {len(trexModel.objFile.faces)}")

titanModel = Model("models/titan_clean/titan.obj")
titanModel.position = glm.vec3(0, 0, -10)  # Closer and centered
titanModel.scale = glm.vec3(3.0, 3.0, 3.0)  # Bigger
print(f"✓ Titan loaded - Vertices: {len(titanModel.objFile.vertices)}, Faces: {len(titanModel.objFile.faces)}")

# List of all models
models = [ironGolemModel, trexModel, titanModel]
currentModelIndex = 0

# Add only the current model to the scene
rend.scene.append(models[currentModelIndex])
print(f"\nStarting with: Iron Golem (Model 1/3)")
print("="*60 + "\n")

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

			# Model switching (M, N, B keys)
			if event.key == pygame.K_m:
				# Remove current model from scene
				rend.scene.remove(models[currentModelIndex])
				# Switch to Iron Golem
				currentModelIndex = 0
				rend.scene.append(models[currentModelIndex])
				print(f"\n========================================")
				print(f"SWITCHED TO: Iron Golem (Model 1/3)")
				print(f"Position: {models[currentModelIndex].position}")
				print(f"Scale: {models[currentModelIndex].scale}")
				print(f"========================================\n")

			if event.key == pygame.K_n:
				# Remove current model from scene
				rend.scene.remove(models[currentModelIndex])
				# Switch to T-Rex
				currentModelIndex = 1
				rend.scene.append(models[currentModelIndex])
				print(f"\n========================================")
				print(f"SWITCHED TO: T-Rex (Model 2/3)")
				print(f"Position: {models[currentModelIndex].position}")
				print(f"Scale: {models[currentModelIndex].scale}")
				print(f"========================================\n")

			if event.key == pygame.K_b:
				# Remove current model from scene
				rend.scene.remove(models[currentModelIndex])
				# Switch to Titan
				currentModelIndex = 2
				rend.scene.append(models[currentModelIndex])
				print(f"\n========================================")
				print(f"SWITCHED TO: Titan (Model 3/3)")
				print(f"Position: {models[currentModelIndex].position}")
				print(f"Scale: {models[currentModelIndex].scale}")
				print(f"========================================\n")

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