"""
Lab 4 - Shaders Creativos
Shaders personalizados para efectos visuales únicos
"""

import numpy as np
import math
import time
from typing import Dict, Any, Tuple

# Variable global para tiempo de animación
start_time = time.time()

def get_animation_time() -> float:
    """Obtiene el tiempo actual para animaciones"""
    return time.time() - start_time

def vertex_shader(vertex: np.ndarray, 
                 texcoord: np.ndarray,
                 normal: np.ndarray,
                 uniforms: Dict[str, Any]) -> Dict[str, Any]:
    """
    Vertex Shader - Igual que el Lab 3 pero con tiempo añadido
    """
    # Obtener matrices de uniforms
    model_matrix = uniforms.get('model_matrix', np.eye(4))
    view_matrix = uniforms.get('view_matrix', np.eye(4))
    projection_matrix = uniforms.get('projection_matrix', np.eye(4))
    viewport_matrix = uniforms.get('viewport_matrix', np.eye(4))
    
    # Convertir vértice a coordenadas homogéneas
    vertex_h = np.array([vertex[0], vertex[1], vertex[2], 1.0])
    
    # Pipeline de transformación completo
    world_vertex = model_matrix @ vertex_h
    view_vertex = view_matrix @ world_vertex
    clip_vertex = projection_matrix @ view_vertex
    
    # Perspective divide
    if clip_vertex[3] != 0:
        ndc_vertex = clip_vertex / clip_vertex[3]
    else:
        ndc_vertex = clip_vertex
    
    # Screen space
    screen_vertex = viewport_matrix @ ndc_vertex
    
    # Transformar normal
    normal_matrix = model_matrix[:3, :3]
    world_normal = normal_matrix @ normal
    
    # NUEVO: Añadir tiempo de animación
    animation_time = get_animation_time()
    
    return {
        'position': screen_vertex[:3],
        'world_position': world_vertex[:3],
        'texcoord': texcoord,
        'normal': world_normal,
        'depth': view_vertex[2],
        'time': animation_time  # ¡Nuevo parámetro!
    }

# =============================================================================
# SHADER 1: 🌊 AGUA ANIMADA
# =============================================================================

def water_fragment_shader(fragment_data: Dict[str, Any], uniforms: Dict[str, Any]) -> Tuple[int, int, int]:
    """
    Shader de Agua Animada
    Crea ondas procedurales que se mueven con el tiempo
    """
    texcoord = fragment_data.get('texcoord', np.array([0.0, 0.0]))
    anim_time = fragment_data.get('time', 0.0)
    
    u, v = texcoord[0], texcoord[1]
    
    # Crear ondas usando funciones seno
    # Onda 1: Horizontal
    wave1 = math.sin(u * 8.0 + anim_time * 2.0) * 0.1
    
    # Onda 2: Vertical  
    wave2 = math.sin(v * 6.0 + anim_time * 1.5) * 0.1
    
    # Onda 3: Diagonal
    wave3 = math.sin((u + v) * 10.0 + anim_time * 3.0) * 0.05
    
    # Combinar todas las ondas
    wave_height = wave1 + wave2 + wave3
    
    # Colores base del agua (azul-verde)
    base_red = 0.05
    base_green = 0.3 + wave_height * 0.5
    base_blue = 0.6 + wave_height * 0.3
    
    # Añadir brillos donde las ondas son altas
    if wave_height > 0.15:
        brightness = (wave_height - 0.15) * 3.0
        base_red += brightness * 0.3
        base_green += brightness * 0.2
        base_blue += brightness * 0.1
    
    # Convertir a RGB (0-255)
    final_color = np.array([base_red, base_green, base_blue])
    final_color = np.clip(final_color * 255, 0, 255)
    
    return tuple(final_color.astype(int))

# =============================================================================
# SHADER 2: 🔥 FUEGO/PLASMA
# =============================================================================

def fire_fragment_shader(fragment_data: Dict[str, Any], uniforms: Dict[str, Any]) -> Tuple[int, int, int]:
    """
    Shader de Fuego/Plasma
    Crea efectos de llama con turbulencia
    """
    texcoord = fragment_data.get('texcoord', np.array([0.0, 0.0]))
    anim_time = fragment_data.get('time', 0.0)
    
    u, v = texcoord[0], texcoord[1]
    
    # Crear turbulencia usando múltiples ondas
    def noise(x, y, t):
        # Combinar diferentes frecuencias para crear ruido
        n1 = math.sin(x * 4.0 + t) * math.cos(y * 3.0 + t * 0.7)
        n2 = math.sin(x * 8.0 + t * 1.3) * math.cos(y * 7.0 + t * 0.9) * 0.5
        n3 = math.sin(x * 16.0 + t * 2.1) * math.cos(y * 13.0 + t * 1.7) * 0.25
        return n1 + n2 + n3
    
    # Generar turbulencia
    turbulence = noise(u * 3.0, v * 3.0, anim_time * 2.0)
    
    # El fuego "sube" - más intenso abajo, menos arriba
    fire_intensity = (1.0 - v) * 0.7 + turbulence * 0.3
    fire_intensity = max(0.0, min(1.0, fire_intensity))
    
    # Gradiente de colores del fuego
    if fire_intensity > 0.7:
        # Núcleo blanco-amarillo (más caliente)
        red = 1.0
        green = 1.0  
        blue = 0.8 + (fire_intensity - 0.7) * 0.7
    elif fire_intensity > 0.4:
        # Zona amarilla-naranja
        red = 1.0
        green = 0.6 + (fire_intensity - 0.4) * 1.3
        blue = 0.1
    elif fire_intensity > 0.2:
        # Zona roja-naranja
        red = 0.8 + (fire_intensity - 0.2) * 1.0
        green = (fire_intensity - 0.2) * 2.0
        blue = 0.0
    else:
        # Zona roja oscura / negro
        red = fire_intensity * 4.0
        green = 0.0
        blue = 0.0
    
    # Convertir a RGB
    final_color = np.array([red, green, blue])
    final_color = np.clip(final_color * 255, 0, 255)
    
    return tuple(final_color.astype(int))

# =============================================================================
# SISTEMA DE SELECCIÓN DE SHADERS
# =============================================================================


# ===============================
# SHADER 1: Toon (Cel Shading)
# ===============================
def toon_fragment_shader(fragment_data: Dict[str, Any], uniforms: Dict[str, Any]) -> Tuple[int, int, int]:
    normal = fragment_data.get('normal', np.array([0, 0, 1]))
    light_dir = uniforms.get('light_direction', np.array([0, 0, 1]))
    base_color = np.array([30, 180, 60])  # Verde cartoon
    intensity = np.dot(normal / np.linalg.norm(normal), light_dir / np.linalg.norm(light_dir))
    intensity = max(0, intensity)
    # 3 niveles de luz
    if intensity > 0.85:
        factor = 1.0
    elif intensity > 0.5:
        factor = 0.7
    elif intensity > 0.2:
        factor = 0.4
    else:
        factor = 0.15
    color = (base_color * factor).astype(int)
    return tuple(np.clip(color, 0, 255))

# ===============================
# SHADER 2: Checkerboard con luz
# ===============================
def checkerboard_light_fragment_shader(fragment_data: Dict[str, Any], uniforms: Dict[str, Any]) -> Tuple[int, int, int]:
    texcoord = fragment_data.get('texcoord', np.array([0.0, 0.0]))
    normal = fragment_data.get('normal', np.array([0, 0, 1]))
    light_dir = uniforms.get('light_direction', np.array([0, 0, 1]))
    u, v = texcoord[0], texcoord[1]
    # Checkerboard
    check = (int(u * 10) % 2) ^ (int(v * 10) % 2)
    color1 = np.array([220, 220, 220])
    color2 = np.array([40, 40, 40])
    base_color = color1 if check else color2
    # Luz difusa
    intensity = np.dot(normal / np.linalg.norm(normal), light_dir / np.linalg.norm(light_dir))
    intensity = max(0.2, intensity)
    color = (base_color * intensity).astype(int)
    return tuple(np.clip(color, 0, 255))

# ===============================
# SHADER 3: Fresnel (borde brillante)
# ===============================
def fresnel_fragment_shader(fragment_data: Dict[str, Any], uniforms: Dict[str, Any]) -> Tuple[int, int, int]:
    normal = fragment_data.get('normal', np.array([0, 0, 1]))
    view_dir = uniforms.get('view_direction', np.array([0, 0, 1]))
    base_color = np.array([30, 120, 200])
    fresnel = 1.0 - np.dot(normal / np.linalg.norm(normal), view_dir / np.linalg.norm(view_dir))
    fresnel = np.clip(fresnel, 0, 1)
    color = base_color * (0.3 + 0.7 * fresnel)
    return tuple(np.clip(color, 0, 255))

# ===============================
# SHADER 4: Múltiples luces
# ===============================
def multi_light_fragment_shader(fragment_data: Dict[str, Any], uniforms: Dict[str, Any]) -> Tuple[int, int, int]:
    normal = fragment_data.get('normal', np.array([0, 0, 1]))
    base_color = np.array([60, 180, 60])
    # Dos luces direccionales
    light1 = np.array([0.7, 0.7, 0.7])
    dir1 = np.array([1, 1, 1])
    light2 = np.array([0.4, 0.4, 1.0])
    dir2 = np.array([-1, 1, 0.5])
    n = normal / np.linalg.norm(normal)
    i1 = max(0, np.dot(n, dir1 / np.linalg.norm(dir1)))
    i2 = max(0, np.dot(n, dir2 / np.linalg.norm(dir2)))
    color = base_color * (0.3 + 0.5 * i1 * light1 + 0.5 * i2 * light2)
    return tuple(np.clip(color, 0, 255))

# Diccionario de shaders disponibles
AVAILABLE_SHADERS = {
    'toon': {
        'name': '🖍️ Toon (Cel Shading)',
        'shader': toon_fragment_shader,
        'description': 'Efecto cartoon con bandas de color'
    },
    'checkerboard_light': {
        'name': '⬛⬜ Checkerboard con luz',
        'shader': checkerboard_light_fragment_shader,
        'description': 'Ajedrez con iluminación difusa'
    },
    'fresnel': {
        'name': '✨ Fresnel',
        'shader': fresnel_fragment_shader,
        'description': 'Borde brillante tipo fresnel'
    },
    'multi_light': {
        'name': '💡 Múltiples luces',
        'shader': multi_light_fragment_shader,
        'description': 'Iluminación con dos fuentes de luz'
    }
}

def get_shader_by_name(shader_name: str):
    """Obtiene un shader por su nombre"""
    return AVAILABLE_SHADERS.get(shader_name, {}).get('shader', water_fragment_shader)

# Función de interpolación mejorada
def interpolate_vertex_data(v1_data: Dict[str, Any], 
                          v2_data: Dict[str, Any], 
                          v3_data: Dict[str, Any], 
                          barycentric: Tuple[float, float, float]) -> Dict[str, Any]:
    """Interpola datos de vértices usando coordenadas baricéntricas"""
    u, v, w = barycentric
    
    # Interpolación de coordenadas de textura
    interpolated_texcoord = u * v1_data.get('texcoord', np.array([0.0, 0.0])) + \
                           v * v2_data.get('texcoord', np.array([0.0, 0.0])) + \
                           w * v3_data.get('texcoord', np.array([0.0, 0.0]))
    
    # Interpolación de normales
    interpolated_normal = u * v1_data.get('normal', np.array([0.0, 0.0, 1.0])) + \
                         v * v2_data.get('normal', np.array([0.0, 0.0, 1.0])) + \
                         w * v3_data.get('normal', np.array([0.0, 0.0, 1.0]))
    
    # Interpolación de posición mundo
    interpolated_world_pos = u * v1_data.get('world_position', np.array([0.0, 0.0, 0.0])) + \
                            v * v2_data.get('world_position', np.array([0.0, 0.0, 0.0])) + \
                            w * v3_data.get('world_position', np.array([0.0, 0.0, 0.0]))
    
    # Interpolación de profundidad
    interpolated_depth = u * v1_data.get('depth', 0.0) + \
                        v * v2_data.get('depth', 0.0) + \
                        w * v3_data.get('depth', 0.0)
    
    # El tiempo es constante para todo el frame
    animation_time = v1_data.get('time', 0.0)
    
    return {
        'texcoord': interpolated_texcoord,
        'normal': interpolated_normal,
        'world_position': interpolated_world_pos,
        'depth': interpolated_depth,
        'time': animation_time
    }
