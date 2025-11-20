import pygame
import pygame.display
from pygame.locals import *

import glm

from gl import Renderer
from buffer import Buffer
from model import Model
from vertexShaders import *
from fragmentShaders import *
from OpenGL.GL import (
    glDisable,
    glDisableVertexAttribArray,
    glDrawArrays,
    glPolygonMode,
    GL_CULL_FACE,
    GL_FRONT_AND_BACK,
    GL_FILL,
    GL_TRIANGLES,
)

width = 960
height = 540

deltaTime = 0.0

DEBUG_TRIANGLE = True  # Fase A: pipeline mínimo


screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()


rend = Renderer(screen)
rend.pointLight = glm.vec3(0, 8, -10)  # Light above and in front of models
rend.ambientLight = 0.6  # More ambient light to see models better

# Ensure back-face culling is disabled so models with arbitrary winding are visible
glDisable(GL_CULL_FACE)

# Make sure filled mode is ON (not wireframe)
if not rend.filledMode:
    rend.ToggleFilledMode()
glDisable(GL_CULL_FACE)
# Ensure polygon mode is set for both faces (defensive)
glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

currVertexShader = vertex_shader
# start with a calmer shader to avoid neon artifacts on untextured city
basic_vertex_debug = """
#version 330 core
layout (location = 0) in vec3 inPosition;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
void main() {
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(inPosition, 1.0);
}
"""
flat_color_shader = """
#version 330 core
out vec4 fragColor;
void main() { fragColor = vec4(1.0, 0.2, 0.2, 1.0); }
"""
# start with simple flat shading for debugging visibility
currVertexShader = basic_vertex_debug
currFragmentShader = flat_color_shader

rend.SetShaders(currVertexShader, currFragmentShader)

# Disable skybox temporarily to debug model visibility
# skyboxTextures = ["skybox/right.jpg",
# 				  "skybox/left.jpg",
# 				  "skybox/top.jpg",
# 				  "skybox/bottom.jpg",
# 				  "skybox/front.jpg",
# 				  "skybox/back.jpg"]
# rend.CreateSkybox(skyboxTextures)


# Scene setup: Amaryllis City + Pokémon (Fase 3)
if DEBUG_TRIANGLE:
	class DebugTriangle:
		def __init__(self):
			self.buffer = Buffer([
				-0.5, -0.5, -2.0,
				0.5, -0.5, -2.0,
				0.0,  0.5, -2.0
			])
			self.position = glm.vec3(0,0,0)
			self.rotation = glm.vec3(0,0,0)
			self.scale = glm.vec3(1,1,1)
		def GetModelMatrix(self):
			return glm.mat4(1)
		def Render(self):
			self.buffer.Use(0,3)
			glDrawArrays(GL_TRIANGLES, 0, 3)
			glDisableVertexAttribArray(0)

	scene_models = [DebugTriangle()]
	print("\n" + "="*60)
	print("DEBUG TRIANGLE MODE")
	print("="*60)
	amaryllis = None
else:
	print("\n" + "="*60)
	print("LOADING DIORAMA MODELS...")
	print("="*60)

	scene_models = []

	def center_and_place(model, target_height, world_pos):
		verts = model.objFile.vertices
		min_x = min(v[0] for v in verts)
		max_x = max(v[0] for v in verts)
		min_y = min(v[1] for v in verts)
		max_y = max(v[1] for v in verts)
		min_z = min(v[2] for v in verts)
		max_z = max(v[2] for v in verts)
		center = glm.vec3((min_x + max_x) / 2.0, (min_y + max_y) / 2.0, (min_z + max_z) / 2.0)
		height = max_y - min_y if (max_y - min_y) != 0 else 1.0
		scale_val = target_height / height
		model.scale = glm.vec3(scale_val, scale_val, scale_val)
		model.position = glm.vec3(world_pos) - center * scale_val

	try:
		bulbasaur = Model("models/bulbasur/Bulbasaur.obj")
		center_and_place(bulbasaur, target_height=6.0, world_pos=glm.vec3(-4, 0, -20))
		scene_models.append(bulbasaur)
		print(f"[OK] Bulbasaur loaded ({len(bulbasaur.objFile.vertices)} verts)")
	except Exception as e:
		print(f"[ERR] Bulbasaur: {e}")

	try:
		charizard = Model("models/charizard/006 - Charizard/Charizard.obj")
		center_and_place(charizard, target_height=7.0, world_pos=glm.vec3(4, 0, -18))
		scene_models.append(charizard)
		print(f"[OK] Charizard loaded ({len(charizard.objFile.vertices)} verts)")
	except Exception as e:
		print(f"[ERR] Charizard: {e}")

	try:
		eevee = Model("models/eve/Pokemon XY/Eevee/Eevee.obj")
		center_and_place(eevee, target_height=5.0, world_pos=glm.vec3(-8, 0, -16))
		scene_models.append(eevee)
		print(f"[OK] Eevee loaded ({len(eevee.objFile.vertices)} verts)")
	except Exception as e:
		print(f"[ERR] Eevee: {e}")

	try:
		umbreon = Model("models/umbreon/Umbreon/UmbreonLowPoly.obj")
		center_and_place(umbreon, target_height=4.0, world_pos=glm.vec3(10, 0, -14))
		scene_models.append(umbreon)
		print(f"[OK] Umbreon loaded ({len(umbreon.objFile.vertices)} verts)")
	except Exception as e:
		print(f"[ERR] Umbreon: {e}")

	try:
		pokeball = Model("models/pokeball/pokeball.obj")
		center_and_place(pokeball, target_height=3.0, world_pos=glm.vec3(0, 0, -10))
		scene_models.append(pokeball)
		print(f"[OK] Pokeball loaded ({len(pokeball.objFile.vertices)} verts)")
	except Exception as e:
		print(f"[ERR] Pokeball: {e}")

	# Temporarily skip the city to debug visibility
	amaryllis = None

# Add all loaded models to the renderer scene
rend.scene.extend(scene_models)

print(f"\nScene has {len(rend.scene)} objects")
print(f"Filled mode: {rend.filledMode}")
print("="*60 + "\n")

# Orbital camera system variables
cameraYaw = 0.0           # Horizontal rotation angle (degrees)
cameraPitch = 0.0         # Vertical rotation angle (degrees)
cameraDistance = 5.0 if DEBUG_TRIANGLE else 20.0     # Distance from target
# default target: first model if available, otherwise origin
cameraTarget = glm.vec3(rend.scene[0].position) if rend.scene else glm.vec3(0, 0, 0)

# Limits
MIN_DISTANCE = 10.0
MAX_DISTANCE = 100.0
MIN_PITCH = -80.0
MAX_PITCH = 80.0
# Hard clamp to avoid camera going too far behind the city
MAX_DISTANCE_CITY = 150.0

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
	cameraDistance = min(cameraDistance, MAX_DISTANCE_CITY)

	# Convert to radians
	yawRad = glm.radians(cameraYaw)
	pitchRad = glm.radians(cameraPitch)

	# Calculate camera position using spherical coordinates
	x = cameraTarget.x + cameraDistance * glm.cos(pitchRad) * glm.sin(yawRad)
	y = cameraTarget.y + cameraDistance * glm.sin(pitchRad)
	z = cameraTarget.z + cameraDistance * glm.cos(pitchRad) * glm.cos(yawRad)

	rend.camera.position = glm.vec3(x, y, z)

	# Use lookAt to make camera always look at target (and mark usingLookAt)
	rend.camera.LookAt(cameraTarget)

# Initialize camera position
updateOrbitalCamera()

# Focus targets (skip city) and helper
if DEBUG_TRIANGLE:
	focus_targets = []
else:
	focus_targets = [bulbasaur, charizard, eevee, umbreon, pokeball]

def set_focus(idx):
	global cameraTarget
	if 0 <= idx < len(focus_targets):
		cameraTarget = glm.vec3(focus_targets[idx].position)

# set default focus
if not DEBUG_TRIANGLE and focus_targets:
	set_focus(0)

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
				set_focus(0)  # focus Bulbasaur
				currFragmentShader = rim_lighting_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_2:
				set_focus(1)  # focus Charizard
				currFragmentShader = fresnel_metallic_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_3:
				set_focus(2)  # focus Eevee
				currFragmentShader = procedural_patterns_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_4:
				set_focus(3)  # focus Umbreon
				currFragmentShader = gooch_shading_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_5:
				set_focus(4)  # focus Pokeball
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


	if keys[K_z]:
		if rend.value > 0.0:
			rend.value -= 1 * deltaTime

	if keys[K_x]:
		if rend.value < 1.0:
			rend.value += 1 * deltaTime



	# Keep models static during debug
	# for model in rend.scene:
	# 	model.rotation.y += 45 * deltaTime


	rend.Render()
	pygame.display.flip()

pygame.quit()
