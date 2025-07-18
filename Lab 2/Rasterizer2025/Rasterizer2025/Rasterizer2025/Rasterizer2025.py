# Rasterizer2025.py
# ------------------------------------------------------------
#   Rasterizador 3D básico
#   • Carga un modelo .OBJ (triangulado o quads)
#   • Lo centra y escala para caber dentro de [-1,1] en NDC
#   • Renderiza con colores aleatorios por triángulo (wireframe)
#   • Guarda el resultado en output.bmp
# ------------------------------------------------------------
import os
import pygame
from typing import cast
from gl import *
from model import Model
from shaders import vertexShader
from BMP_Writer import GenerateBMP

# ---------------------------------------------------- Configuración ventana
pygame.init()
WIDTH, HEIGHT = 800, 600  # Ventana más grande para mejor visualización
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption('Rasterizador 3D')
clock = pygame.time.Clock()

rend = Renderer(screen)

# -------------------------------------------------- Cargar modelo 3D
model = Model()
# Asegurarse de que la carpeta obj existe
current_dir = os.path.dirname(os.path.abspath(__file__))
obj_dir = os.path.join(current_dir, "obj")
if not os.path.exists(obj_dir):
    os.makedirs(obj_dir)
    print(f"Creada carpeta obj en: {obj_dir}")
    print("Por favor, coloca tu archivo .obj en esta carpeta")
    
# Ruta completa al archivo OBJ
model_path = os.path.join(current_dir, "obj", "Ball OBJ.obj")
if not os.path.exists(model_path):
    print(f"Error: No se encuentra el archivo: {model_path}")
    print("Por favor, asegúrate de colocar el archivo .obj en la carpeta obj")
    pygame.quit()
    exit()

model.load_from_obj(model_path)
model.vertexShader = vertexShader

# ----------- Auto‑centrar y escalar para caber en NDC [-1,1]
xs = model.vertices[0::3]
ys = model.vertices[1::3]
zs = model.vertices[2::3]

min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)
min_z, max_z = min(zs), max(zs)

cx, cy, cz = (max_x + min_x) / 2, (max_y + min_y) / 2, (max_z + min_z) / 2
extent = max(max_x - min_x, max_y - min_y, max_z - min_z)

scaleFactor = 1.8 / extent  # Deja ~10% de margen
model.scale = [scaleFactor] * 3
model.translation = [-cx * scaleFactor,
                     -cy * scaleFactor,
                     -cz * scaleFactor]

rend.models.append(model)

# --------------------------------------------------------- Loop principal
isRunning = True
while isRunning:
    dt = clock.tick(60) / 1000.0  # deltaTime en segundos

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

    # ------------- Transformaciones interactivas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        model.translation[0] += 1.0 * dt
    if keys[pygame.K_LEFT]:
        model.translation[0] -= 1.0 * dt
    if keys[pygame.K_UP]:
        model.translation[1] += 1.0 * dt
    if keys[pygame.K_DOWN]:
        model.translation[1] -= 1.0 * dt

    if keys[pygame.K_d]:
        model.rotation[1] += 45 * dt  # yaw
    if keys[pygame.K_a]:
        model.rotation[1] -= 45 * dt
    if keys[pygame.K_w]:
        model.scale = [s + 0.5 * dt for s in model.scale]
    if keys[pygame.K_s]:
        model.scale = [max(0.1, s - 0.5 * dt) for s in model.scale]

    # -------------------------------------------- Dibujar frame
    rend.glClear()
    rend.glRender()
    pygame.display.flip()

# ------------------------------------------------------- Guardar BMP
# Cast explícito para evitar warning de tipos
GenerateBMP(
    "output.bmp",
    WIDTH,
    HEIGHT,
    3,
    cast(list[list[tuple[int, int, int]]], rend.frameBuffer)
)

pygame.quit()

# ---------------------------------------------------- Controles:
# Flechas: Mover modelo (traslación X/Y)
# A/D: Rotar modelo (yaw)
# W/S: Escalar modelo (agrandar/achicar)
# 1,2,3: Cambiar modo de renderizado (puntos, líneas, triángulos)
# ----------------------------------------------------
