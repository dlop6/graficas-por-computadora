import pygame
import random
from typing import List, Tuple, Callable, Optional
from model import Model

# Constantes para tipos de primitivas
POINTS = 0
LINES = 1
TRIANGLES = 2

class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width, self.height = screen.get_size()

        # Framebuffer: matriz 2D de pixeles RGB (tuplas)
        self.frameBuffer: List[List[Tuple[int, int, int]]] = [
            [(0, 0, 0) for _ in range(self.width)] for _ in range(self.height)
        ]

        # Lista de modelos a renderizar
        self.models: List['Model'] = []

        # Tipo de primitiva actual
        self.primitiveType = TRIANGLES

    def glClear(self):
        # Limpia framebuffer y pantalla
        self.frameBuffer = [
            [(0, 0, 0) for _ in range(self.width)] for _ in range(self.height)
        ]
        self.screen.fill((0, 0, 0))

    def glRender(self):
        for model in self.models:
            # Verifica que el modelo tenga un vertexShader válido
            if model.vertexShader is None:
                continue

            modelMatrix = model.GetModelMatrix()
            verts = model.vertices

            # Según el tipo de primitiva:
            if self.primitiveType == POINTS:
                # Dibujar cada vértice como punto
                for i in range(0, len(verts), 3):
                    vertex = verts[i:i+3]
                    screen_coord = model.vertexShader(vertex, {
                        "modelMatrix": modelMatrix,
                        "width": self.width,
                        "height": self.height
                    })
                    x, y = int(screen_coord[0]), int(screen_coord[1])
                    if 0 <= x < self.width and 0 <= y < self.height:
                        color = self.randomColor()
                        self.frameBuffer[y][x] = color
                        self.screen.set_at((x, y), color)

            elif self.primitiveType == LINES:
                # Dibujar líneas entre pares de vértices consecutivos
                for i in range(0, len(verts) - 3, 3):
                    v0 = verts[i:i+3]
                    v1 = verts[i+3:i+6]

                    p0 = model.vertexShader(v0, {
                        "modelMatrix": modelMatrix,
                        "width": self.width,
                        "height": self.height
                    })
                    p1 = model.vertexShader(v1, {
                        "modelMatrix": modelMatrix,
                        "width": self.width,
                        "height": self.height
                    })

                    self.drawLine(int(p0[0]), int(p0[1]), int(p1[0]), int(p1[1]),
                                  self.randomColor())

            elif self.primitiveType == TRIANGLES:
                # Dibujar triángulos cada 3 vértices
                for i in range(0, len(verts), 9):
                    triVerts = [verts[i:i+3], verts[i+3:i+6], verts[i+6:i+9]]

                    screen_coords = []
                    for v in triVerts:
                        sc = model.vertexShader(v, {
                            "modelMatrix": modelMatrix,
                            "width": self.width,
                            "height": self.height
                        })
                        screen_coords.append(sc)

                    # Color aleatorio para cada triángulo
                    color = self.randomColor()
                    
                    # Convertir coordenadas a enteros
                    x0, y0 = int(screen_coords[0][0]), int(screen_coords[0][1])
                    x1, y1 = int(screen_coords[1][0]), int(screen_coords[1][1])
                    x2, y2 = int(screen_coords[2][0]), int(screen_coords[2][1])
                    
                    # Ordenar vértices por y
                    if y0 > y1:
                        x0, y0, x1, y1 = x1, y1, x0, y0
                    if y0 > y2:
                        x0, y0, x2, y2 = x2, y2, x0, y0
                    if y1 > y2:
                        x1, y1, x2, y2 = x2, y2, x1, y1

                    # Encontrar bounding box
                    min_x = max(0, min(x0, x1, x2))
                    max_x = min(self.width - 1, max(x0, x1, x2))
                    min_y = max(0, min(y0, y1, y2))
                    max_y = min(self.height - 1, max(y0, y1, y2))
                    
                    # Rellenar triángulo
                    for x in range(min_x, max_x + 1):
                        for y in range(min_y, max_y + 1):
                            # Calcular denominador para coordenadas baricéntricas
                            denominator = ((y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2))
                            
                            # Evitar división por cero
                            if abs(denominator) < 1e-6:
                                continue
                                
                            # Calcular coordenadas baricéntricas
                            w0 = ((y1 - y2) * (x - x2) + (x2 - x1) * (y - y2)) / denominator
                            w1 = ((y2 - y0) * (x - x2) + (x0 - x2) * (y - y2)) / denominator
                            w2 = 1 - w0 - w1
                            
                            # Si el punto está dentro del triángulo
                            if w0 >= 0 and w1 >= 0 and w2 >= 0:
                                if 0 <= x < self.width and 0 <= y < self.height:
                                    self.frameBuffer[y][x] = color
                                    self.screen.set_at((x, y), color)

    def randomColor(self) -> Tuple[int, int, int]:
        return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def drawLine(self, x0: int, y0: int, x1: int, y1: int, color: Tuple[int, int, int]):
        # Algoritmo de Bresenham para dibujar línea
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0

        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1

        if dy <= dx:
            err = dx / 2.0
            while x != x1:
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.frameBuffer[y][x] = color
                    self.screen.set_at((x, y), color)
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
            # Pintar último punto
            if 0 <= x1 < self.width and 0 <= y1 < self.height:
                self.frameBuffer[y1][x1] = color
                self.screen.set_at((x1, y1), color)
        else:
            err = dy / 2.0
            while y != y1:
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.frameBuffer[y][x] = color
                    self.screen.set_at((x, y), color)
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
            # Pintar último punto
            if 0 <= x1 < self.width and 0 <= y1 < self.height:
                self.frameBuffer[y1][x1] = color
                self.screen.set_at((x1, y1), color)
