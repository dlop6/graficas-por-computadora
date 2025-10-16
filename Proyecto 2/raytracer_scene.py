import os
from BMP_Writer import GenerateBMP
from HDRTexture import HDRTexture

WIDTH, HEIGHT = 160, 120
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargar envmap HDR
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
hdr_files = [f for f in os.listdir(ASSETS_DIR) if f.lower().endswith('.hdr')]
if hdr_files:
    envmap_path = os.path.join(ASSETS_DIR, hdr_files[0])
    envmap = HDRTexture(envmap_path)
    print(f'Envmap cargado: {envmap_path} ({envmap.width}x{envmap.height})')
else:
    envmap = None
    print('No se encontró envmap HDR en assets.')

# Renderizar solo el fondo envmap
image = [ [ (0,0,0) for _ in range(WIDTH) ] for _ in range(HEIGHT) ]
for y in range(HEIGHT):
    for x in range(WIDTH):
        if envmap:
            u = x / WIDTH
            v = 1.0 - (y / HEIGHT)
            r,g,b = envmap.sample_uv(u,v)
            image[y][x] = (int(min(255,r*255)), int(min(255,g*255)), int(min(255,b*255)))
        else:
            image[y][x] = (0,0,0)

OUTPUT_PATH = os.path.join(BASE_DIR, 'outputs', 'envmap_preview.bmp')
# GenerateBMP expects colorBuffer indexed as colorBuffer[x][y]
color_buffer = [ [ (0,0,0) for _ in range(HEIGHT) ] for _ in range(WIDTH) ]
for y in range(HEIGHT):
    for x in range(WIDTH):
        color_buffer[x][y] = image[y][x]

GenerateBMP(OUTPUT_PATH, WIDTH, HEIGHT, 3, color_buffer)
print(f'Preview envmap guardado en {OUTPUT_PATH}')
 
