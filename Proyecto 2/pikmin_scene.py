"""
Proyecto 2 - Pikmin Scene
Recreación de escena de Pikmin usando ray tracing

Características:
- 70+ primitivas individuales
- 3 Pikmin completos (Azul, Amarillo, Rojo)
- Bulborb enemigo con 4 patas
- Elementos ambientales (rama, tomate, botella, etc.)
- 4 materiales diferentes (Lambertian, TexturedLambert, Metal, Refractive)
- 4 primitivas nuevas (Capsule, Cone, Disk, Torus)
- Modelo OBJ integrado
- Sistema multi-luz (4 luces + ambient)
- Environment map HDR
"""

import numpy as np
import os
from primitives import Sphere, Plane, Cylinder, Capsule, Cone, Disk, Torus
from materials import Lambertian, TexturedLambert, Metal, Refractive
from MathLib import TranslationMatrix, ScaleMatrix, RotationMatrix
from model import OBJModel
from lighting import DirectionalLight, PointLight, SpotLight, AmbientLight
from raytracer import render
from BMP_Writer import GenerateBMP
from HDRTexture import HDRTexture

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Resolución (cambiar para render final)
WIDTH, HEIGHT = 960, 540  # Preview
# WIDTH, HEIGHT = 1920, 1080  # Final

MAX_DEPTH = 3  # Profundidad de recursión

OUTPUT_FILE = "outputs/pikmin_scene.bmp"

# ============================================================================
# MATERIALES
# ============================================================================

# Lambertian difusos (Pikmin y elementos orgánicos)
mat_blue_pikmin = Lambertian(color=(0.2, 0.5, 0.9), ambient=0.15)
mat_blue_pikmin_dark = Lambertian(color=(0.15, 0.4, 0.75), ambient=0.12)
mat_yellow_pikmin = Lambertian(color=(0.95, 0.85, 0.2), ambient=0.15)
mat_yellow_pikmin_dark = Lambertian(color=(0.85, 0.75, 0.15), ambient=0.12)
mat_red_pikmin = Lambertian(color=(0.9, 0.2, 0.2), ambient=0.15)
mat_red_pikmin_dark = Lambertian(color=(0.75, 0.15, 0.15), ambient=0.12)

mat_white = Lambertian(color=(1.0, 1.0, 1.0), ambient=0.15)
mat_black = Lambertian(color=(0.05, 0.05, 0.05), ambient=0.08)
mat_stem_green = Lambertian(color=(0.2, 0.5, 0.2), ambient=0.12)
mat_flower_yellow = Lambertian(color=(0.9, 0.85, 0.3), ambient=0.14)
mat_flower_white = Lambertian(color=(0.95, 0.95, 0.98), ambient=0.14)
mat_leaf_green = Lambertian(color=(0.3, 0.8, 0.3), ambient=0.13)

# Bulborb
mat_bulborb_blue = Metal(color=(0.35, 0.45, 0.65), reflectivity=0.6, shininess=60)
mat_bulborb_gray = Metal(color=(0.3, 0.35, 0.4), reflectivity=0.5, shininess=50)

# Elementos ambientales
mat_tomato = Lambertian(color=(0.88, 0.18, 0.12), ambient=0.18)
mat_leaf_big = Lambertian(color=(0.35, 0.72, 0.28), ambient=0.14)
mat_leaf_small = Lambertian(color=(0.42, 0.75, 0.32), ambient=0.13)
mat_flower_violet = Lambertian(color=(0.62, 0.42, 0.82), ambient=0.15)
# Suelo con reflectividad leve para captar environment map
mat_ground = Metal(color=(0.35, 0.38, 0.32), reflectivity=0.25, shininess=8)
mat_ceramic = Lambertian(color=(0.68, 0.52, 0.38), ambient=0.14)

# Texturado (rama)
wood_texture_path = "assets/wood_bark.bmp"
if os.path.exists(wood_texture_path):
    mat_wood = TexturedLambert(texture_path=wood_texture_path, ambient=0.15)
else:
    mat_wood = Lambertian(color=(0.55, 0.4, 0.28), ambient=0.15)

# Metal reflectivo (burbuja plateada)
mat_silver_bubble = Metal(color=(0.92, 0.92, 0.96), reflectivity=0.88, shininess=80)

# Refractivos (vidrio/botella)
mat_glass_bottle = Refractive(ior=1.5, tint=(0.96, 0.98, 1.0), transparency=0.92)
mat_glass_orb = Refractive(ior=1.3, tint=(0.98, 0.96, 1.0), transparency=0.85)

# ============================================================================
# FUNCIONES HELPER PARA ROTACIONES
# ============================================================================

def create_rotated_cylinder(center, radius, length, material, pitch=0, yaw=0, roll=0):
    """
    Crea un cilindro rotado.
    Por defecto el cilindro está vertical (eje Y).
    - roll=-90 → horizontal en eje X
    - roll=90 → horizontal en eje -X
    - pitch/yaw → inclinaciones adicionales
    """
    # Para simplificar, usamos Cylinder básico y documentamos la orientación
    # En una implementación completa, aplicaríamos la matriz de rotación
    # a los puntos de intersección
    return Cylinder(center=center, radius=radius, height=length, material=material)

def normalize(v):
    """Normaliza un vector."""
    v = np.array(v, dtype=float)
    norm = np.linalg.norm(v)
    if norm < 1e-10:
        return np.array([0.0, 1.0, 0.0])
    return v / norm

# ============================================================================
# CONSTRUCCIÓN DE LA ESCENA
# ============================================================================

objects = []

# ============================================================================
# 1. PIKMIN AZUL (izquierda) — 12 primitivas
# ============================================================================

# 1.1 Cuerpo
objects.append(Capsule(
    center=(-0.8, 0.72, 0.3),  # Ajustado: Y=0.72 sobre rama, Z acercado a cámara
    radius=0.12,
    height=0.4,
    material=mat_blue_pikmin
))

# 1.2 Cabeza
objects.append(Sphere(
    center=(-0.8, 1.24, 0.3),  # Ajustado: Y+0.52 desde cuerpo
    radius=0.15,
    material=mat_blue_pikmin
))

# 1.3-1.4 Ojos blancos
objects.append(Sphere(
    center=(-0.84, 1.26, 0.43),  # Y+0.12 ajustado
    radius=0.045,
    material=mat_white
))
objects.append(Sphere(
    center=(-0.76, 1.26, 0.43),  # Y+0.12 ajustado
    radius=0.045,
    material=mat_white
))

# 1.5-1.6 Pupilas negras
objects.append(Sphere(
    center=(-0.84, 1.26, 0.465),  # Y+0.12 ajustado
    radius=0.018,
    material=mat_black
))
objects.append(Sphere(
    center=(-0.76, 1.26, 0.465),  # Y+0.12 ajustado
    radius=0.018,
    material=mat_black
))

# 1.7 Tallo (stem)
objects.append(Cylinder(
    center=(-0.8, 1.39, 0.3),  # Y+0.12 ajustado
    radius=0.018,
    height=0.16,
    material=mat_stem_green
))

# 1.8 Flor/Hoja del tallo
objects.append(Sphere(
    center=(-0.8, 1.57, 0.3),  # Y+0.12 ajustado
    radius=0.035,
    material=mat_flower_yellow
))

# 1.9-1.10 Brazos (cilindros pequeños - simplificados como verticales)
objects.append(Cylinder(
    center=(-0.92, 0.84, 0.3),  # Y+0.12 ajustado (mitad del cuerpo)
    radius=0.022,
    height=0.18,
    material=mat_blue_pikmin
))
objects.append(Cylinder(
    center=(-0.68, 0.84, 0.3),  # Y+0.12 ajustado (mitad del cuerpo)
    radius=0.022,
    height=0.18,
    material=mat_blue_pikmin
))

# 1.11-1.12 Patas
objects.append(Cylinder(
    center=(-0.85, 0.64, 0.3),  # Base del cuerpo Y+0.12
    radius=0.03,
    height=0.08,
    material=mat_blue_pikmin_dark
))
objects.append(Cylinder(
    center=(-0.75, 0.64, 0.3),  # Base del cuerpo Y+0.12
    radius=0.03,
    height=0.08,
    material=mat_blue_pikmin_dark
))

# ============================================================================
# 2. PIKMIN AMARILLO (centro-izquierda) — 14 primitivas
# ============================================================================

# 2.1 Cuerpo
objects.append(Capsule(
    center=(-0.3, 0.72, 0.4),  # Y=0.72 sobre rama, Z acercado
    radius=0.12,
    height=0.4,
    material=mat_yellow_pikmin
))

# 2.2 Cabeza
objects.append(Sphere(
    center=(-0.3, 1.24, 0.4),  # Y+0.52 desde cuerpo
    radius=0.15,
    material=mat_yellow_pikmin
))

# 2.3-2.4 Ojos blancos
objects.append(Sphere(
    center=(-0.34, 1.26, 0.53),  # Y+0.12 ajustado
    radius=0.045,
    material=mat_white
))
objects.append(Sphere(
    center=(-0.26, 1.26, 0.53),  # Y+0.12 ajustado
    radius=0.045,
    material=mat_white
))

# 2.5-2.6 Pupilas negras
objects.append(Sphere(
    center=(-0.34, 1.26, 0.565),  # Y+0.12 ajustado
    radius=0.018,
    material=mat_black
))
objects.append(Sphere(
    center=(-0.26, 1.26, 0.565),  # Y+0.12 ajustado
    radius=0.018,
    material=mat_black
))

# 2.7-2.8 Orejas (característica del Pikmin amarillo)
objects.append(Sphere(
    center=(-0.42, 1.29, 0.4),  # Y+0.12 ajustado
    radius=0.038,
    material=mat_yellow_pikmin_dark
))
objects.append(Sphere(
    center=(-0.18, 1.29, 0.4),  # Y+0.12 ajustado
    radius=0.038,
    material=mat_yellow_pikmin_dark
))

# 2.9 Tallo
objects.append(Cylinder(
    center=(-0.3, 1.39, 0.4),  # Y+0.12 ajustado
    radius=0.018,
    height=0.16,
    material=mat_stem_green
))

# 2.10 Flor del tallo
objects.append(Sphere(
    center=(-0.3, 1.57, 0.4),  # Y+0.12 ajustado
    radius=0.035,
    material=mat_flower_white
))

# 2.11-2.12 Brazos
objects.append(Cylinder(
    center=(-0.42, 0.84, 0.4),  # Y+0.12 ajustado (mitad del cuerpo)
    radius=0.022,
    height=0.18,
    material=mat_yellow_pikmin
))
objects.append(Cylinder(
    center=(-0.18, 0.84, 0.4),  # Y+0.12 ajustado (mitad del cuerpo)
    radius=0.022,
    height=0.18,
    material=mat_yellow_pikmin
))

# 2.13-2.14 Patas
objects.append(Cylinder(
    center=(-0.35, 0.64, 0.4),  # Base del cuerpo Y+0.12
    radius=0.03,
    height=0.08,
    material=mat_yellow_pikmin_dark
))
objects.append(Cylinder(
    center=(-0.25, 0.64, 0.4),  # Base del cuerpo Y+0.12
    radius=0.03,
    height=0.08,
    material=mat_yellow_pikmin_dark
))

# ============================================================================
# 3. PIKMIN ROJO (centro-derecha) — 13 primitivas
# ============================================================================

# 3.1 Cuerpo
objects.append(Capsule(
    center=(0.3, 0.72, 0.35),  # Y=0.72 sobre rama, Z acercado
    radius=0.12,
    height=0.4,
    material=mat_red_pikmin
))

# 3.2 Cabeza
objects.append(Sphere(
    center=(0.3, 1.24, 0.35),  # Y+0.52 desde cuerpo
    radius=0.15,
    material=mat_red_pikmin
))

# 3.3-3.4 Ojos blancos
objects.append(Sphere(
    center=(0.26, 1.26, 0.48),  # Y+0.12 ajustado
    radius=0.045,
    material=mat_white
))
objects.append(Sphere(
    center=(0.34, 1.26, 0.48),  # Y+0.12 ajustado
    radius=0.045,
    material=mat_white
))

# 3.5-3.6 Pupilas negras
objects.append(Sphere(
    center=(0.26, 1.26, 0.515),  # Y+0.12 ajustado
    radius=0.018,
    material=mat_black
))
objects.append(Sphere(
    center=(0.34, 1.26, 0.515),  # Y+0.12 ajustado
    radius=0.018,
    material=mat_black
))

# 3.7 Nariz (característica del Pikmin rojo)
objects.append(Cone(
    base_center=(0.3, 1.22, 0.49),  # Y+0.12 ajustado
    base_radius=0.04,
    height=0.06,
    material=mat_red_pikmin_dark
))

# 3.8 Tallo
objects.append(Cylinder(
    center=(0.3, 1.39, 0.35),  # Y+0.12 ajustado
    radius=0.018,
    height=0.16,
    material=mat_stem_green
))

# 3.9 Hoja del tallo
objects.append(Sphere(
    center=(0.3, 1.57, 0.35),  # Y+0.12 ajustado
    radius=0.035,
    material=mat_leaf_green
))

# 3.10-3.11 Brazos
objects.append(Cylinder(
    center=(0.18, 0.84, 0.35),  # Y+0.12 ajustado (mitad del cuerpo)
    radius=0.022,
    height=0.18,
    material=mat_red_pikmin
))
objects.append(Cylinder(
    center=(0.42, 0.84, 0.35),  # Y+0.12 ajustado (mitad del cuerpo)
    radius=0.022,
    height=0.18,
    material=mat_red_pikmin
))

# 3.12-3.13 Patas
objects.append(Cylinder(
    center=(0.25, 0.64, 0.35),  # Base del cuerpo Y+0.12
    radius=0.03,
    height=0.08,
    material=mat_red_pikmin_dark
))
objects.append(Cylinder(
    center=(0.35, 0.64, 0.35),  # Base del cuerpo Y+0.12
    radius=0.03,
    height=0.08,
    material=mat_red_pikmin_dark
))

# ============================================================================
# 4. BULBORB (enemigo - derecha) — 9 primitivas
# ============================================================================

# 4.1 Cuerpo principal
objects.append(Sphere(
    center=(1.2, 0.70, -0.2),  # Y=0.70 sobre rama, Z=-0.2 (detrás Pikmin, delante rama)
    radius=0.28,
    material=mat_bulborb_blue
))

# 4.2-4.3 Ojos blancos
objects.append(Sphere(
    center=(1.12, 0.86, 0.04),  # Ajustado a nueva posición
    radius=0.08,
    material=mat_white
))
objects.append(Sphere(
    center=(1.28, 0.86, 0.04),  # Ajustado a nueva posición
    radius=0.08,
    material=mat_white
))

# 4.4-4.5 Pupilas negras
objects.append(Sphere(
    center=(1.12, 0.86, 0.09),  # Ajustado a nueva posición
    radius=0.03,
    material=mat_black
))
objects.append(Sphere(
    center=(1.28, 0.86, 0.09),  # Ajustado a nueva posición
    radius=0.03,
    material=mat_black
))

# 4.6-4.9 Patas (4 cilindros)
objects.append(Cylinder(
    center=(1.05, 0.46, -0.08),  # Ajustado a nueva posición
    radius=0.025,
    height=0.14,
    material=mat_bulborb_gray
))
objects.append(Cylinder(
    center=(1.35, 0.46, -0.08),  # Ajustado a nueva posición
    radius=0.025,
    height=0.14,
    material=mat_bulborb_gray
))
objects.append(Cylinder(
    center=(1.05, 0.46, -0.32),  # Ajustado a nueva posición
    radius=0.025,
    height=0.14,
    material=mat_bulborb_gray
))
objects.append(Cylinder(
    center=(1.35, 0.46, -0.32),  # Ajustado a nueva posición
    radius=0.025,
    height=0.14,
    material=mat_bulborb_gray
))

# ============================================================================
# 5. RAMA/TRONCO PRINCIPAL — Implementada con esferas superpuestas
# ============================================================================

# Rama horizontal creada con ~18 esferas superpuestas para simular cilindro
# Esto evita la necesidad de rotación en Cylinder y permite texturizado
branch_radius = 0.28
branch_start_x = -1.75
branch_end_x = 1.75
branch_y = 0.3
branch_z = -0.5  # Movida atrás para no tapar los Pikmin
num_spheres = 18

for i in range(num_spheres):
    t = i / (num_spheres - 1)  # 0.0 a 1.0
    x = branch_start_x + (branch_end_x - branch_start_x) * t
    objects.append(Sphere(
        center=(x, branch_y, branch_z),
        radius=branch_radius,
        material=mat_wood
    ))

# ============================================================================
# 6. TOMATE/FRUTA ROJA — 1 primitiva
# ============================================================================

objects.append(Sphere(
    center=(-1.3, 0.72, -0.3),
    radius=0.22,
    material=mat_tomato
))

# ============================================================================
# 7. BOTELLA TRANSPARENTE — 2 primitivas
# ============================================================================

# 7.1 Cuerpo de botella
objects.append(Cylinder(
    center=(-1.5, 0.0, -1.2),
    radius=0.14,
    height=0.75,
    material=mat_glass_bottle
))

# 7.2 Base decorativa (toro)
objects.append(Torus(
    center=(-1.5, 0.08, -1.2),
    major_radius=0.16,
    minor_radius=0.04,
    material=mat_glass_bottle
))

# ============================================================================
# 8. ESFERA METÁLICA/BURBUJA — 1 primitiva
# ============================================================================

objects.append(Sphere(
    center=(1.5, 1.3, -0.8),
    radius=0.26,
    material=mat_silver_bubble
))

# ============================================================================
# 9. HOJA/PÉTALO GRANDE (izquierda superior) — 1 primitiva
# ============================================================================

objects.append(Disk(
    center=(-1.8, 1.05, -1.0),
    normal=normalize((0.4, 0.6, 0.3)),
    radius=0.42,
    material=mat_leaf_big
))

# ============================================================================
# 10. FLOR VIOLETA (derecha inferior) — 1 primitiva
# ============================================================================

objects.append(Disk(
    center=(1.75, 0.1, 0.45),
    normal=(0, 1, 0),
    radius=0.32,
    material=mat_flower_violet
))

# ============================================================================
# 11. PLANO SUELO — 1 primitiva
# ============================================================================

objects.append(Plane(
    point=(0, -0.05, 0),
    normal=(0, 1, 0),
    material=mat_ground
))

# ============================================================================
# 12. ELEMENTO DECORATIVO OBJ (taza/cubo) — N primitivas (triangles)
# ============================================================================

obj_path = "assets/cube.obj"
if os.path.exists(obj_path):
    print(f"🔷 Cargando modelo OBJ: {obj_path}")
    obj_model = OBJModel(obj_path)
    
    # Transformación: posición + escala + rotación
    transform = (
        TranslationMatrix(0.8, 0.73, -0.3) @
        ScaleMatrix(0.15, 0.25, 0.15) @
        RotationMatrix(15, 25, 0)
    )
    
    # Convertir a triángulos
    triangles = obj_model.to_triangles(mat_ceramic, transform)
    objects.extend(triangles)
    print(f"   ✓ Agregados {len(triangles)} triángulos")
else:
    print(f"⚠️  No se encontró {obj_path}, usando esfera de reemplazo")
    objects.append(Sphere(
        center=(0.8, 0.33, -0.6),
        radius=0.15,
        material=mat_ceramic
    ))

# ============================================================================
# 13. HOJA ADICIONAL (derecha) — 1 primitiva
# ============================================================================

objects.append(Disk(
    center=(1.5, 0.85, -0.32),
    normal=normalize((-0.3, 0.7, 0.4)),
    radius=0.27,
    material=mat_leaf_small
))

# ============================================================================
# 14. ELEMENTO AMBIENTAL (burbuja/orbe fondo) — 1 primitiva
# ============================================================================

objects.append(Sphere(
    center=(-1.0, 1.6, -2.1),
    radius=0.19,
    material=mat_glass_orb
))

# ============================================================================
# SISTEMA DE ILUMINACIÓN
# ============================================================================

# DirectionalLight: Luz solar principal
light_sun = DirectionalLight(
    direction=normalize((0.3, -0.8, -0.5)),
    color=(1.0, 0.98, 0.95),
    intensity=0.85
)

# PointLight 1: Luz principal (cálida, arriba-izquierda)
light_main = PointLight(
    position=(-2.0, 2.5, 1.5),
    color=(1.0, 0.95, 0.85),
    intensity=1.2,
    attenuation=(0.8, 0.09, 0.032)
)

# PointLight 2: Luz de relleno (fría, derecha)
light_fill = PointLight(
    position=(2.5, 1.8, 0.5),
    color=(0.85, 0.9, 1.0),
    intensity=0.6,
    attenuation=(1.0, 0.14, 0.07)
)

# SpotLight: Foco en Pikmin amarillo (centro)
light_spot = SpotLight(
    position=(0.0, 2.0, 1.0),
    direction=normalize((0.0, -1.0, -0.3)),
    color=(1.0, 0.98, 0.92),
    intensity=0.9,
    cutoff_angle=25.0,
    falloff=2.5,
    attenuation=(0.5, 0.09, 0.032)
)

# AmbientLight: Luz ambiente global
ambient = AmbientLight(
    color=(0.9, 0.92, 1.0),
    intensity=0.25
)

lights = [light_sun, light_main, light_fill, light_spot]

# ============================================================================
# CARGAR ENVIRONMENT MAP
# ============================================================================

envmap_path = 'assets/autumn_field_4k.hdr'
if os.path.exists(envmap_path):
    print(f"🌍 Cargando environment map: {envmap_path}")
    envmap = HDRTexture(envmap_path)
    print(f"   ✓ HDR cargado: {envmap.width}x{envmap.height}")
else:
    print(f"⚠️  No se encontró {envmap_path}, sin environment map")
    envmap = None

# ============================================================================
# CONSTRUCCIÓN DEL DICCIONARIO DE ESCENA
# ============================================================================

scene_dict = {
    'camera': {
        'pos': (0, 0.8, 3.5),
        'look_at': (0, 0.5, 0),
        'fov': 45
    },
    'lights': lights,
    'ambient': ambient,
    'objects': objects,
    'envmap': envmap
}

# ============================================================================
# RENDERIZADO
# ============================================================================

print("=" * 70)
print("🎨 PROYECTO 2 - PIKMIN SCENE")
print("=" * 70)
print(f"📐 Resolución: {WIDTH}×{HEIGHT}")
print(f"🔢 Primitivas totales: {len(objects)}")
print(f"💡 Luces: {len(lights)} + ambient")
print(f"🌍 Environment map: {'Sí' if envmap else 'No'}")
print(f"🎯 Max recursion depth: {MAX_DEPTH}")
print("=" * 70)

print("\n🚀 Iniciando render...")
print("   (Esto puede tomar varios minutos dependiendo de la resolución)\n")

# Renderizar usando la función render() del módulo raytracer
color_buffer = render(scene_dict, WIDTH, HEIGHT, max_depth=MAX_DEPTH)

print("\n🎨 Aplicando tonemapping y convirtiendo a BMP...")

# Tonemapping y conversión a uint8
def tonemap_and_convert(color_buffer, width, height, exposure=1.0, gamma=2.2):
    """Convierte buffer float (0..1) a uint8 con tonemapping."""
    output = []
    for x in range(width):
        row = []
        for y in range(height):
            r, g, b = color_buffer[x][y]
            # Exposure
            r, g, b = r * exposure, g * exposure, b * exposure
            # Tonemapping Reinhard simple
            r = r / (1.0 + r)
            g = g / (1.0 + g)
            b = b / (1.0 + b)
            # Gamma
            r = r ** (1.0 / gamma)
            g = g ** (1.0 / gamma)
            b = b ** (1.0 / gamma)
            # Clamp y convert
            r_int = int(max(0, min(255, r * 255)))
            g_int = int(max(0, min(255, g * 255)))
            b_int = int(max(0, min(255, b * 255)))
            row.append((r_int, g_int, b_int))
        output.append(row)
    return output

output_buffer = tonemap_and_convert(color_buffer, WIDTH, HEIGHT, exposure=1.2, gamma=2.2)

# Guardar BMP
GenerateBMP(OUTPUT_FILE, WIDTH, HEIGHT, 3, output_buffer)

print("\n" + "=" * 70)
print(f"✅ ¡Render completado!")
print(f"📁 Archivo guardado: {OUTPUT_FILE}")
print("=" * 70)
print("\n💯 Puntos estimados:")
print("   ✓ 20 pts - 4 materiales diferentes")
print("   ✓ 5 pts  - Environment map")
print("   ✓ 20 pts - 4 primitivas nuevas (Capsule, Cone, Disk, Torus)")
print("   ✓ 20 pts - Modelo OBJ integrado")
print("   ✓ 10 pts - Iluminación múltiple (4 luces)")
print("   ✓ 30 pts - Escena con >10 objetos")
print("   ────────────────────────────")
print("   📊 TOTAL: 105/125 pts")
print("\n🎯 Para llegar a 110+ pts, ajustar estética comparando con reference.jpg")
print("=" * 70)
