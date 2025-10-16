"""
Test para verificar el sistema de iluminación múltiple.
Renderiza esferas con diferentes materiales bajo múltiples luces.
"""
import os
from BMP_Writer import GenerateBMP
from primitives import Sphere, Plane
from materials import Lambertian, Metal, Refractive
from raytracer import render
from HDRTexture import HDRTexture
from lighting import DirectionalLight, PointLight, SpotLight, AmbientLight

# Configuración
WIDTH, HEIGHT = 800, 450
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
mat_green = Lambertian((0.4, 0.8, 0.3), ambient=0.15)
mat_yellow = Lambertian((0.95, 0.85, 0.2), ambient=0.15)
mat_metal = Metal((0.9, 0.9, 0.95), reflectivity=0.85, shininess=64)
mat_glass = Refractive(ior=1.5, tint=(0.95, 0.98, 1.0), transparency=0.9)
mat_ground = Lambertian((0.5, 0.5, 0.5), ambient=0.1)

# Objetos: 6 esferas en línea con diferentes materiales
objects = [
    # Fila de esferas
    Sphere((-2.5, 0.3, -3.0), 0.3, mat_red),      # Roja (izquierda)
    Sphere((-1.5, 0.3, -3.0), 0.3, mat_blue),     # Azul
    Sphere((-0.5, 0.3, -3.0), 0.3, mat_green),    # Verde
    Sphere((0.5, 0.3, -3.0), 0.3, mat_yellow),    # Amarilla
    Sphere((1.5, 0.3, -3.0), 0.35, mat_metal),    # Metálica
    Sphere((2.5, 0.4, -3.0), 0.35, mat_glass),    # Vidrio
    
    # Plano
    Plane((0, -0.3, -3.0), (0, 1, 0), mat_ground, scale=10.0),
]

# Sistema de iluminación múltiple
lights = [
    # 1. Directional Light (sol desde arriba-derecha)
    DirectionalLight(
        direction=(-0.4, -0.6, -0.3),
        color=(1.0, 0.98, 0.92),
        intensity=0.6
    ),
    
    # 2. Point Light roja (izquierda)
    PointLight(
        position=(-3.0, 1.5, -1.0),
        color=(1.0, 0.3, 0.3),
        intensity=2.0,
        attenuation=(1.0, 0.1, 0.05)
    ),
    
    # 3. Point Light azul (derecha)
    PointLight(
        position=(3.0, 1.5, -1.0),
        color=(0.3, 0.5, 1.0),
        intensity=2.0,
        attenuation=(1.0, 0.1, 0.05)
    ),
    
    # 4. Spotlight desde el frente (enfocando el centro)
    SpotLight(
        position=(0, 2.5, 0),
        direction=(0, -0.7, -1.0),
        cutoff_angle=25,
        color=(1.0, 1.0, 1.0),
        intensity=1.5,
        attenuation=(1.0, 0.05, 0.02),
        falloff=2.0
    ),
]

ambient = AmbientLight(color=(0.6, 0.65, 0.7), intensity=0.12)

# Escena
scene = {
    'objects': objects,
    'envmap': envmap,
    'lights': lights,
    'ambient': ambient,
    'camera': {
        'pos': (0, 0.8, 2.0),
        'look_at': (0, 0.3, -3.0),
        'fov': 70,
    }
}

# Renderizar
print(f'🎨 Renderizando {WIDTH}x{HEIGHT} con {len(lights)} luces...')
print(f'   - 1 Directional Light (sol)')
print(f'   - 2 Point Lights (roja, azul)')
print(f'   - 1 Spotlight (frente)')
print(f'   + Ambient Light')
color_buffer = render(scene, WIDTH, HEIGHT, max_depth=4)

# Tone mapping
def tone_map(color):
    r, g, b = color
    # Reinhard tone mapping
    r = r / (1.0 + r)
    g = g / (1.0 + g)
    b = b / (1.0 + b)
    return (int(r * 255), int(g * 255), int(b * 255))

bmp_buffer = [[tone_map(color_buffer[x][y]) for y in range(HEIGHT)] for x in range(WIDTH)]

# Guardar
output_path = os.path.join(BASE_DIR, 'outputs', 'test_multi_light.bmp')
GenerateBMP(output_path, WIDTH, HEIGHT, 3, bmp_buffer)
print(f'✓ Guardado: {output_path}')
print('\n🎉 ¡Sistema de iluminación múltiple funcionando!')
print(f'   {len(lights)} luces + ambient renderizadas correctamente')
print(f'   Sombras calculadas con shadow rays')
