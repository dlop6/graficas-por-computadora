"""
Test para verificar la integración de modelos OBJ con raytracing.
Renderiza un cubo OBJ junto con primitivas básicas.
"""
import os
from BMP_Writer import GenerateBMP
from model import OBJModel
from primitives import Sphere
from materials import Lambertian, Metal
from raytracer import render
from HDRTexture import HDRTexture
from MathLib import TranslationMatrix, ScaleMatrix, RotationMatrix

# Configuración
WIDTH, HEIGHT = 640, 360
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
mat_cube = Lambertian((0.8, 0.5, 0.3), ambient=0.15)
mat_sphere = Metal((0.9, 0.9, 0.95), reflectivity=0.85)

# Cargar modelo OBJ
obj_path = os.path.join(ASSETS_DIR, 'cube.obj')
print(f'📦 Cargando modelo OBJ: {obj_path}')
obj_model = OBJModel(obj_path)
print(f'   Vértices: {len(obj_model.vertices)}')
print(f'   Caras: {len(obj_model.faces)}')

# Transformar el cubo: trasladar y escalar
transform = TranslationMatrix(-0.5, 0.3, -2.0) @ ScaleMatrix(0.4, 0.4, 0.4) @ RotationMatrix(25, 35, 0)

# Convertir OBJ a triángulos
triangles = obj_model.to_triangles(mat_cube, transform)
print(f'✓ Generados {len(triangles)} triángulos')

# Objetos de la escena
objects = triangles + [
    # Esfera metálica de referencia
    Sphere((0.5, 0.4, -2.5), 0.25, mat_sphere),
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
color_buffer = render(scene, WIDTH, HEIGHT, max_depth=4)

# Tone mapping
def tone_map(color):
    r, g, b = color
    r = r / (1.0 + r)
    g = g / (1.0 + g)
    b = b / (1.0 + b)
    return (int(r * 255), int(g * 255), int(b * 255))

bmp_buffer = [[tone_map(color_buffer[x][y]) for y in range(HEIGHT)] for x in range(WIDTH)]

# Guardar
output_path = os.path.join(BASE_DIR, 'outputs', 'test_obj_model.bmp')
GenerateBMP(output_path, WIDTH, HEIGHT, 3, bmp_buffer)
print(f'✓ Guardado: {output_path}')
print('\n🎉 ¡Modelo OBJ integrado correctamente!')
print(f'   {len(triangles)} triángulos renderizados con éxito')
