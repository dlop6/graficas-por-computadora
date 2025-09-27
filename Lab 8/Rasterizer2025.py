import pygame
from gl import *
from BMP_Writer import GenerateBMP
from model import Model
from shaders import *

width = 256
height = 256

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)

# triangle3 = [[510,70], [550, 160], [570,80] ]

triangleModel = Model()
triangleModel.vertices = [ 110.0,  70.0, 0.0,
						   150.0, 160.0, 0.0,
						   170.0,  80.0, 0.0 ]

triangleModel.vertexShader = vertexShader  # type: ignore

rend.models.append(triangleModel)


isRunning = True
while isRunning:

	deltaTime = clock.tick(60) / 1000.0


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1:
				rend.primitiveType = POINTS

			elif event.key == pygame.K_2:
				rend.primitiveType = LINES

			elif event.key == pygame.K_3:
				rend.primitiveType = TRIANGLES



	keys = pygame.key.get_pressed()

	if keys[pygame.K_RIGHT]:
		triangleModel.translation[0] += 10.0 * deltaTime
	if keys[pygame.K_LEFT]:
		triangleModel.translation[0] -= 10.0 * deltaTime
	if keys[pygame.K_UP]:
		triangleModel.translation[1] += 10.0 * deltaTime
	if keys[pygame.K_DOWN]:
		triangleModel.translation[1] -= 10.0 * deltaTime

	if keys[pygame.K_d]:
		triangleModel.rotation[2] += 20.0 * deltaTime
	if keys[pygame.K_a]:
		triangleModel.rotation[2] -= 20.0 * deltaTime

	if keys[pygame.K_w]:
		triangleModel.scale =  [(i + deltaTime) for i in triangleModel.scale]
	if keys[pygame.K_s]:
		triangleModel.scale = [(i - deltaTime) for i in triangleModel.scale ]










	rend.glClear()

	# Escribir lo que se va a dibujar aqui

	rend.glRender()

	#########################################

	pygame.display.flip()


def convert_buffer(buffer):
	# Convierte listas [r,g,b] a tuplas (r,g,b) para cada pixel, asegurando longitud 3
	return [[tuple(pixel[:3]) if isinstance(pixel, (list, tuple)) and len(pixel) >= 3 else (0,0,0) for pixel in col] for col in buffer]

GenerateBMP("output.bmp", width, height, 3, convert_buffer(rend.frameBuffer))  # type: ignore

pygame.quit()