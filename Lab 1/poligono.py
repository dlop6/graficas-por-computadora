from BMP_Writer import GenerateBMP

WIDTH, HEIGHT = 1920, 1080

coordenadas = {
    "poligono1": [
        (165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360),
        (250, 380), (220, 385), (205, 410), (193, 383)
    ],
    "poligono2": [
        (321, 335), (288, 286), (339, 251), (374, 302)
    ],
    "poligono3": [
        (377, 249), (411, 197), (436, 249)
    ],
    "poligono4": [
        (413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
        (750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
        (597, 215), (552, 214), (517, 144), (466, 180)
    ],
    "poligono5": [
        (682, 175), (708, 120), (735, 148), (739, 170)
    ]
}


def dibujar_linea(x0, y0, x1, y1, color, buffer):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    if dx > dy:
        err = dx // 2
        while x != x1:
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                buffer[x][y] = color
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy // 2
        while y != y1:
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                buffer[x][y] = color
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy

    if 0 <= x1 < WIDTH and 0 <= y1 < HEIGHT:
        buffer[x1][y1] = color


def fill(coordenadas, color, buffer):
    min_y = min(p[1] for p in coordenadas)
    max_y = max(p[1] for p in coordenadas)

    for y in range(min_y, max_y + 1):
        intersec = []
        for i in range(len(coordenadas)):
            (x0, y0) = coordenadas[i]
            (x1, y1) = coordenadas[(i + 1) % len(coordenadas)]

            if y0 == y1:
                continue  # línea horizontal

            # FIX para evitar dobles intersecciones en vértices
            if y < min(y0, y1) or y >= max(y0, y1):
                continue

            x_intersec = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            intersec.append(x_intersec)

        intersec.sort()

        for i in range(0, len(intersec), 2):
            if i + 1 >= len(intersec):
                break
            x_start = int(intersec[i])
            x_end = int(intersec[i + 1])
            for x in range(x_start, x_end + 1):
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    buffer[x][y] = color


def dibujo(WIDTH, HEIGHT, coordenadas, matriz=None):
    if matriz is None:
        matriz = [[(0, 0, 0) for _ in range(HEIGHT)] for _ in range(WIDTH)]

    colores = {
        "poligono1": (153, 255, 153),     # rojo
        "poligono2": (102, 255, 102),     # verde
        "poligono3": (51, 204, 51),     # azul
        "poligono4": (0, 153, 51),   # amarillo
        "poligono5": (0, 0, 0),       # negro (agujero)
    }

    # Dibujar bordes
    for nombre, puntos in coordenadas.items():
        color = colores[nombre]
        for i in range(len(puntos)):
            x0, y0 = puntos[i]
            x1, y1 = puntos[(i + 1) % len(puntos)]
            dibujar_linea(x0, y0, x1, y1, color, matriz)

    # Rellenar polígonos
    for nombre, puntos in coordenadas.items():
        color = colores[nombre]
        fill(puntos, color, matriz)

    return matriz


# Ejecutar y guardar
matriz = dibujo(WIDTH, HEIGHT, coordenadas)
GenerateBMP("poligonos23747.bmp", WIDTH, HEIGHT, 3, matriz)
