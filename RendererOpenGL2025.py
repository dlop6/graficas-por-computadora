import pygame
import pygame.display
from pygame.locals import *

import glm

from gl import Renderer
from model import Model
from vertexShaders import *
from fragmentShaders import *
from OpenGL.GL import glDisable, GL_CULL_FACE, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from OpenGL.GL.shaders import compileProgram, compileShader

width = 960
height = 540

deltaTime = 0.0


screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()


rend = Renderer(screen)
# luz puntual elevada para iluminar toda la ciudad desde arriba
rend.pointLight = glm.vec3(0, 20, 0)
# luz ambiente alta para asegurar buena visibilidad de todos los modelos
rend.ambientLight = 0.5

# desactivar culling para asegurar visibilidad de todos los modelos
glDisable(GL_CULL_FACE)

# asegurar modo filled activo
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


# carga de modelos - fase 4 y 5
print("\n" + "="*60)
print("CARGANDO MODELOS...")
print("="*60)

# fase 4: cargar ciudad base
try:
	cityModel = Model("models/Amaryllis City/OBJ/Amaryllis City.obj")
	# coordenadas originales en miles (-4320 a ~8000 aproximadamente)
	# con escala 0.01 la ciudad queda en ~150 unidades de diámetro
	cityModel.position = glm.vec3(0, -10, 0)  # bajar un poco para apoyar en Y≈0
	cityModel.rotation = glm.vec3(0, 0, 0)
	cityModel.scale = glm.vec3(0.01, 0.01, 0.01)
	rend.scene.append(cityModel)
	print(f"[OK] Amaryllis City cargada - Vértices: {len(cityModel.objFile.vertices)}, Caras: {len(cityModel.objFile.faces)}")
	print(f"    Escala: {cityModel.scale}, Posición: {cityModel.position}")
except Exception as e:
	print(f"[ERROR] No se pudo cargar Amaryllis City: {e}")
	import traceback
	traceback.print_exc()
	cityModel = None

print("="*60 + "\n")

# sistema de cámara orbital independiente
cameraYaw = 0.0           # ángulo de rotación horizontal (grados)
cameraPitch = 20.0        # ángulo inicial mirando un poco hacia abajo
cameraDistance = 100.0    # distancia inicial más alejada para ver la ciudad completa
# target inicial en el centro de la escena (será ajustable con hotkeys en fase 7)
cameraTarget = glm.vec3(0, 0, 0)

# límites de cámara ajustados para escena más grande
MIN_DISTANCE = 20.0
MAX_DISTANCE = 300.0
MIN_PITCH = -80.0
MAX_PITCH = 80.0

# control de mouse
mouseSensitivity = 0.2
mousePressed = False
lastMouseX = 0
lastMouseY = 0

def updateOrbitalCamera():
	"""actualiza posición de cámara basada en parámetros orbitales"""
	global cameraYaw, cameraPitch, cameraDistance, cameraTarget

	# aplicar límites
	cameraPitch = max(MIN_PITCH, min(MAX_PITCH, cameraPitch))
	cameraDistance = max(MIN_DISTANCE, min(MAX_DISTANCE, cameraDistance))

	# convertir a radianes
	yawRad = glm.radians(cameraYaw)
	pitchRad = glm.radians(cameraPitch)

	# calcular posición usando coordenadas esféricas
	x = cameraTarget.x + cameraDistance * glm.cos(pitchRad) * glm.sin(yawRad)
	y = cameraTarget.y + cameraDistance * glm.sin(pitchRad)
	z = cameraTarget.z + cameraDistance * glm.cos(pitchRad) * glm.cos(yawRad)

	rend.camera.position = glm.vec3(x, y, z)

	# lookat siempre apunta al target (independiente de modelos)
	rend.camera.viewMatrix = glm.lookAt(
		rend.camera.position,
		cameraTarget,
		glm.vec3(0, 1, 0)
	)

# inicializar posición de cámara
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

			# teclas 1-5 reservadas para saltos de vista (fase 7)
			# por ahora solo cambian shaders globales temporalmente
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

		# controles de mouse para cámara orbital
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
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
				cameraPitch -= deltaY * mouseSensitivity

				lastMouseX = mouseX
				lastMouseY = mouseY

		if event.type == pygame.MOUSEWHEEL:
			cameraDistance -= event.y * 2.0

	# controles de teclado para cámara orbital
	if keys[K_a]:
		cameraYaw -= 60 * deltaTime

	if keys[K_d]:
		cameraYaw += 60 * deltaTime

	if keys[K_w]:
		cameraPitch += 40 * deltaTime

	if keys[K_s]:
		cameraPitch -= 40 * deltaTime

	if keys[K_q]:
		cameraDistance += 30 * deltaTime

	if keys[K_e]:
		cameraDistance -= 30 * deltaTime

	# actualizar posición de cámara
	updateOrbitalCamera()


	if keys[K_z]:
		if rend.value > 0.0:
			rend.value -= 1 * deltaTime

	if keys[K_x]:
		if rend.value < 1.0:
			rend.value += 1 * deltaTime

	# rotación automática removida - los modelos permanecen estáticos

	rend.Render()
	pygame.display.flip()

pygame.quit()
