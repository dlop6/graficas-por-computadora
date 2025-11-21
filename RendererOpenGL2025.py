import pygame
import pygame.display
from pygame.locals import *

import glm

from gl import Renderer
from model import Model
from stage import Stage
from vertexShaders import *
from fragmentShaders import *
from OpenGL.GL import glDisable, GL_CULL_FACE

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
currFragmentShader = gooch_shading_shader  # shader neutral con iluminación básica

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
print("CARGANDO ESCENA...")
print("="*60)

# fase 4: crear plataforma procedural
stage = Stage(size=60, height=2.0)
stage.position = glm.vec3(0, 0, 0)
rend.scene.append(stage)
print("[OK] Plataforma creada (60x60 unidades)")

# fase 5: charizard + umbreon (test incremental)
models = []

# try:
# 	pokeball = Model("models/pokeball/pokeball.obj")
# 	pokeball.position = glm.vec3(0, 2, 0)
# 	pokeball.scale = glm.vec3(0.5, 0.5, 0.5)
# 	rend.scene.append(pokeball)
# 	models.append(("Pokébola", pokeball))
# 	print(f"[OK] Pokébola cargada")
# except Exception as e:
# 	print(f"[WARN] No se pudo cargar pokébola: {e}")

# try:
# 	bulbasaur = Model("models/bulbasaur/bulbasaur.obj")
# 	bulbasaur.position = glm.vec3(-15, 2, -15)
# 	bulbasaur.scale = glm.vec3(0.3, 0.3, 0.3)
# 	rend.scene.append(bulbasaur)
# 	models.append(("Bulbasaur", bulbasaur))
# 	print(f"[OK] Bulbasaur cargado")
# except Exception as e:
# 	print(f"[WARN] No se pudo cargar bulbasaur: {e}")

try:
	charizard = Model("models/charizard/006 - Charizard/Charizard.obj")
	charizard.position = glm.vec3(15, 2, -15)
	charizard.scale = glm.vec3(1, 1, 1)
	rend.scene.append(charizard)
	models.append(("Charizard", charizard))
	print(f"[OK] Charizard cargado")
except Exception as e:
	print(f"[WARN] No se pudo cargar charizard: {e}")

try:
	eevee = Model("models/eve/Pokemon XY/Eevee/Eevee.obj")
	eevee.position = glm.vec3(-15, 2, 15)
	eevee.scale = glm.vec3(0.2, 0.2, 0.2)
	rend.scene.append(eevee)
	models.append(("Eevee", eevee))
	print(f"[OK] Eevee cargado")
except Exception as e:
	print(f"[WARN] No se pudo cargar eevee: {e}")

try:
	umbreon = Model("models/umbreon/Umbreon/UmbreonLowPoly.obj")
	umbreon.position = glm.vec3(0, 5, 0)
	umbreon.scale = glm.vec3(3, 3, 3)
	rend.scene.append(umbreon)
	models.append(("Umbreon", umbreon))
	print(f"[OK] Umbreon cargado")
except Exception as e:
	print(f"[WARN] No se pudo cargar umbreon: {e}")

try:
	bulbasaur = Model("models/bulbasur/Bulbasaur.obj")
	bulbasaur.position = glm.vec3(15, 2, 15)
	bulbasaur.scale = glm.vec3(0.15, 0.15, 0.15)
	rend.scene.append(bulbasaur)
	models.append(("Bulbasaur", bulbasaur))
	print(f"[OK] Bulbasaur cargado")
except Exception as e:
	print(f"[WARN] No se pudo cargar bulbasaur: {e}")

try:
	pokeball = Model("models/ts1d43chvqbk-PokemonBall/Pokemon Go Ball.obj")
	pokeball.position = glm.vec3(0, 3, 15)
	pokeball.scale = glm.vec3(0.04, 0.04, 0.04)
	rend.scene.append(pokeball)
	models.append(("Pokeball", pokeball))
	print(f"[OK] Pokeball cargado")
except Exception as e:
	print(f"[WARN] No se pudo cargar pokeball: {e}")

print(f"\nTotal modelos cargados: {len(models) + 1} (plataforma + {len(models)} pokémon)")
print("="*60 + "\n")

# fase 6: asignar shaders únicos a cada modelo (compilados ANTES del loop)
print("Compilando shaders únicos...")
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER

try:
	# compilar shaders creativos UNA SOLA VEZ
	pulsing_program = compileProgram(
		compileShader(vertex_shader, GL_VERTEX_SHADER),
		compileShader(rim_lighting_shader, GL_FRAGMENT_SHADER)
	)
	fire_program = compileProgram(
		compileShader(vertex_shader, GL_VERTEX_SHADER),
		compileShader(fresnel_metallic_shader, GL_FRAGMENT_SHADER)
	)
	shiny_program = compileProgram(
		compileShader(vertex_shader, GL_VERTEX_SHADER),
		compileShader(procedural_patterns_shader, GL_FRAGMENT_SHADER)
	)
	dark_program = compileProgram(
		compileShader(vertex_shader, GL_VERTEX_SHADER),
		compileShader(psychedelic_warp_shader, GL_FRAGMENT_SHADER)
	)

	# asignar shaders a modelos específicos
	pokeball.shaderProgram = pulsing_program
	charizard.shaderProgram = fire_program
	eevee.shaderProgram = shiny_program
	bulbasaur.shaderProgram = shiny_program  # mismo shader, diferente modelo
	umbreon.shaderProgram = dark_program
	# stage NO tiene shader único, usa el default del renderer

	print("[OK] Shaders únicos asignados correctamente")
except Exception as e:
	print(f"[WARN] Error al compilar shaders: {e}")
	print("[INFO] Usando shader por defecto para todos los modelos")

print("="*60 + "\n")

# sistema de cámara orbital independiente
# solución directa: cámara frente a pokeball con profundidad y altura
# pokeball está en (0, 3, 15)
# colocar cámara en (0, 10, 40) mirando a pokeball = altura +7, profundidad +25
cameraYaw = 0.0           # mirando directo hacia adelante (hacia -Z)
cameraPitch = 20.0        # ligeramente elevada
cameraDistance = 50.0     # distancia para ver toda la escena
# target apunta a la pokeball
cameraTarget = glm.vec3(0, 3, 15)  # pokeball

# lista de puntos de interés para saltos de vista (fase 7: cambio de vista entre modelos)
# cada entrada apunta a la posición exacta de cada modelo cargado
viewTargets = [
	glm.vec3(0, 3, 0),        # 0: vista general (centro de plataforma) - TECLA 0
	glm.vec3(0, 3, 15),       # 1: pokeball - TECLA 1
	glm.vec3(15, 2, -15),     # 2: charizard - TECLA 2
	glm.vec3(-15, 2, 15),     # 3: eevee - TECLA 3
	glm.vec3(0, 5, 0),        # 4: umbreon (centro elevado) - TECLA 4
	glm.vec3(15, 2, 15)       # 5: bulbasaur - TECLA 5
]

# límites de cámara ajustados para el diorama
MIN_DISTANCE = 30.0
MAX_DISTANCE = 150.0
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

			# fase 7: cambio de vista entre modelos (15 pts)
			# teclas numéricas 0-5 para enfocar cada modelo
			if event.key == pygame.K_0:
				cameraTarget = viewTargets[0]
				print(f"[CAMERA] Vista: General")

			if event.key == pygame.K_1:
				cameraTarget = viewTargets[1]
				print(f"[CAMERA] Vista: Pokeball")

			if event.key == pygame.K_2:
				cameraTarget = viewTargets[2]
				print(f"[CAMERA] Vista: Charizard")

			if event.key == pygame.K_3:
				cameraTarget = viewTargets[3]
				print(f"[CAMERA] Vista: Eevee")

			if event.key == pygame.K_4:
				cameraTarget = viewTargets[4]
				print(f"[CAMERA] Vista: Umbreon")

			if event.key == pygame.K_5:
				cameraTarget = viewTargets[5]
				print(f"[CAMERA] Vista: Bulbasaur")

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
