import pygame
import pygame.display
from pygame.locals import *

import glm

from gl import Renderer
from buffer import Buffer
from model import Model
from vertexShaders import *
from fragmentShaders import *
from OpenGL.GL import glDisable, GL_CULL_FACE

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


# Load all three models
print("\n" + "="*60)
print("LOADING MODELS...")
print("="*60)

ironGolemModel = Model("models/iron_golem_clean/iron_golem.obj")
ironGolemModel.AddTexture("textures/lava_cracks.jpg")  # Additional texture for effects
ironGolemModel.position = glm.vec3(0, 0, -80)  # Pushed further back
ironGolemModel.scale = glm.vec3(3.0, 3.0, 3.0)  # Larger scale to be visible
print(f"[OK] Iron Golem loaded - Vertices: {len(ironGolemModel.objFile.vertices)}, Faces: {len(ironGolemModel.objFile.faces)}")

trexModel = Model("models/trex/trex.obj")
trexModel.position = glm.vec3(0, -5, -45)  # Pushed further back
trexModel.scale = glm.vec3(0.08, 0.08, 0.08)  # Larger scale
print(f"[OK] T-Rex loaded - Vertices: {len(trexModel.objFile.vertices)}, Faces: {len(trexModel.objFile.faces)}")

titanModel = Model("models/titan_clean/titan.obj")
titanModel.position = glm.vec3(0, 0, -35)  # Pushed further back
titanModel.scale = glm.vec3(5.0, 5.0, 5.0)  # Large scale
print(f"[OK] Titan loaded - Vertices: {len(titanModel.objFile.vertices)}, Faces: {len(titanModel.objFile.faces)}")

# List of all models
models = [ironGolemModel, trexModel, titanModel]
currentModelIndex = 0

# Add only the current model to the scene
rend.scene.append(models[currentModelIndex])
print(f"\nStarting with: Iron Golem (Model 1/3)")
print(f"Scene has {len(rend.scene)} objects")
print(f"Filled mode: {rend.filledMode}")
print("="*60 + "\n")

# Orbital camera system variables
cameraYaw = 0.0           # Horizontal rotation angle (degrees)
cameraPitch = 0.0         # Vertical rotation angle (degrees)
cameraDistance = 50.0     # Distance from target
# la cámara debe apuntar al primer modelo (iron golem)
cameraTarget = glm.vec3(ironGolemModel.position)

# Limits
MIN_DISTANCE = 10.0
MAX_DISTANCE = 100.0
MIN_PITCH = -80.0
MAX_PITCH = 80.0

# Mouse control
mouseSensitivity = 0.2
mousePressed = False
lastMouseX = 0
lastMouseY = 0

def updateOrbitalCamera():
	"""Update camera position based on orbital parameters"""
	global cameraYaw, cameraPitch, cameraDistance, cameraTarget
	
	# Clamp values
	cameraPitch = max(MIN_PITCH, min(MAX_PITCH, cameraPitch))
	cameraDistance = max(MIN_DISTANCE, min(MAX_DISTANCE, cameraDistance))
	
	# Convert to radians
	yawRad = glm.radians(cameraYaw)
	pitchRad = glm.radians(cameraPitch)
	
	# Calculate camera position using spherical coordinates
	x = cameraTarget.x + cameraDistance * glm.cos(pitchRad) * glm.sin(yawRad)
	y = cameraTarget.y + cameraDistance * glm.sin(pitchRad)
	z = cameraTarget.z + cameraDistance * glm.cos(pitchRad) * glm.cos(yawRad)
	
	rend.camera.position = glm.vec3(x, y, z)
	
	# Use lookAt to make camera always look at target
	rend.camera.viewMatrix = glm.lookAt(
		rend.camera.position,
		cameraTarget,
		glm.vec3(0, 1, 0)  # Up vector
	)

# Initialize camera position
updateOrbitalCamera()

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
				
				# Update camera target to look at this model
				cameraTarget = glm.vec3(models[currentModelIndex].position)
				
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
				
				# Update camera target to look at this model
				cameraTarget = glm.vec3(models[currentModelIndex].position)
				
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
				
				# Update camera target to look at this model
				cameraTarget = glm.vec3(models[currentModelIndex].position)
				
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
		
		# Mouse controls for orbital camera
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:  # Left mouse button
				mousePressed = True
				lastMouseX, lastMouseY = pygame.mouse.get_pos()
		
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				mousePressed = False
		
		if event.type == pygame.MOUSEMOTION:
			if mousePressed:
				mouseX, mouseY = pygame.mouse.get_pos()
				deltaX = mouseX - lastMouseX
				deltaY = mouseY - lastMouseY
				
				cameraYaw += deltaX * mouseSensitivity
				cameraPitch -= deltaY * mouseSensitivity  # Inverted for natural control
				
				lastMouseX = mouseX
				lastMouseY = mouseY
		
		if event.type == pygame.MOUSEWHEEL:
			cameraDistance -= event.y * 2.0  # Zoom in/out with mouse wheel

	# Keyboard controls for orbital camera
	if keys[K_a]:  # Rotate left (circular movement)
		cameraYaw -= 60 * deltaTime
	
	if keys[K_d]:  # Rotate right (circular movement)
		cameraYaw += 60 * deltaTime
	
	if keys[K_w]:  # Move up (vertical movement)
		cameraPitch += 40 * deltaTime
	
	if keys[K_s]:  # Move down (vertical movement)
		cameraPitch -= 40 * deltaTime
	
	if keys[K_q]:  # Zoom out
		cameraDistance += 30 * deltaTime
	
	if keys[K_e]:  # Zoom in
		cameraDistance -= 30 * deltaTime
	
	# Update camera position based on orbital parameters
	updateOrbitalCamera()

	# controles de luz comentados porque duplican los de la cámara
	# si necesitas mover la luz, usa otras teclas (ej: ijkl, u, o)
	# if keys[K_w]:
	# 	rend.pointLight.z -= 10 * deltaTime

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