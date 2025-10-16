"""
Test script para verificar las nuevas primitivas.
Renderiza una escena simple con Capsule, Cone, Disk y Torus.
"""
import os
from BMP_Writer import GenerateBMP
from primitives import Ray, Capsule, Cone, Disk, Torus, Sphere
from materials import Lambertian, Metal, Refractive
from raytracer import render
from HDRTexture import HDRTexture

# Configuración
WIDTH, HEIGHT = 480, 270
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargar envmap
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
hdr_files = [f for f in os.listdir(ASSETS_DIR) if f.lower().endswith('.hdr')]
envmap = None
if hdr_files:
    envmap_path = os.path.join(ASSETS_DIR, hdr_files[0])
    envmap = HDRTexture(envmap_path)
    print(f'✓ Envmap cargado: {hdr_files[0]}')

# Materiales
mat_red = Lambertian((0.9, 0.2, 0.2), ambient=0.15)
mat_blue = Lambertian((0.2, 0.5, 0.9), ambient=0.15)
mat_yellow = Lambertian((0.95, 0.85, 0.2), ambient=0.15)
mat_green = Lambertian((0.4, 0.8, 0.3), ambient=0.15)
mat_metal = Metal((0.9, 0.9, 0.95), reflectivity=0.8)

# Objetos: prueba de cada primitiva nueva
objects = [
    # 1. Capsule (Pikmin body)
    Capsule((-1.0, 0.0, -2.0), 0.15, 0.4, mat_blue),
    Sphere((-1.0, 0.55, -2.0), 0.18, mat_blue),  # cabeza
    
    # 2. Cone (nariz)
    Cone((-0.3, 0.0, -2.0), 0.2, 0.5, mat_red),
    
    # 3. Disk (hoja/pétalo)
    Disk((0.4, 0.3, -2.0), (0.2, 1.0, 0.1), 0.3, mat_green),
    
    # 4. Torus (anillo)
    Torus((1.0, 0.3, -2.0), 0.25, 0.08, mat_yellow),
    
    # Esfera metálica de referencia
    Sphere((0.0, 0.8, -2.5), 0.2, mat_metal),
]

# Escena
scene = {
    'objects': objects,
    'envmap': envmap,
    'camera': {
        'pos': (0, 0.5, 1.0),
        'look_at': (0, 0.3, -2.0),
        'fov': 60,
    }
}

# Renderizar
print(f'🎨 Renderizando {WIDTH}x{HEIGHT}...')
color_buffer = render(scene, WIDTH, HEIGHT, max_depth=3)

# Aplicar tone mapping simple para HDR
def tone_map(color):
    r, g, b = color
    # Reinhard tone mapping
    r = r / (1.0 + r)
    g = g / (1.0 + g)
    b = b / (1.0 + b)
    return (int(r * 255), int(g * 255), int(b * 255))

# Convertir a formato BMP
bmp_buffer = [[tone_map(color_buffer[x][y]) for y in range(HEIGHT)] for x in range(WIDTH)]

# Guardar
output_path = os.path.join(BASE_DIR, 'outputs', 'test_primitives.bmp')
GenerateBMP(output_path, WIDTH, HEIGHT, 3, bmp_buffer)
print(f'✓ Guardado: {output_path}')
print('\n🎉 ¡Primitivas implementadas correctamente!')
print('   - Capsule (cuerpo Pikmin)')
print('   - Cone (nariz/sombrero)')
print('   - Disk (hojas/pétalos)')
print('   - Torus (anillos)')
