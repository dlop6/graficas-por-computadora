import numpy as np
from typing import Dict, Any, List, Tuple
from MathLib import barycentric_coordinates

def vertex_shader(vertex: np.ndarray, 
                 texcoord: np.ndarray,
                 normal: np.ndarray,
                 uniforms: Dict[str, Any]) -> Dict[str, Any]:
    """
    Vertex Shader: Transforma vértices del espacio de objeto al espacio de pantalla
    """
    # Obtener matrices de uniforms
    model_matrix = uniforms.get('model_matrix', np.eye(4))
    view_matrix = uniforms.get('view_matrix', np.eye(4))
    projection_matrix = uniforms.get('projection_matrix', np.eye(4))
    viewport_matrix = uniforms.get('viewport_matrix', np.eye(4))
    
    # Convertir vértice a coordenadas homogéneas
    vertex_h = np.array([vertex[0], vertex[1], vertex[2], 1.0])
    
    # Pipeline de transformación completo:
    # Object Space -> World Space (Model Matrix)
    world_vertex = model_matrix @ vertex_h
    
    # World Space -> View Space (View Matrix)  
    view_vertex = view_matrix @ world_vertex
    
    # View Space -> Clip Space (Projection Matrix)
    clip_vertex = projection_matrix @ view_vertex
    
    # Clip Space -> NDC (Perspective divide)
    if clip_vertex[3] != 0:
        ndc_vertex = clip_vertex / clip_vertex[3]
    else:
        ndc_vertex = clip_vertex
    
    # NDC -> Screen Space (Viewport Matrix)
    screen_vertex = viewport_matrix @ ndc_vertex
    
    # Transformar normal (solo rotación y escala, no traslación)
    normal_matrix = model_matrix[:3, :3]
    world_normal = normal_matrix @ normal
    
    # Retornar datos del vértice transformado
    return {
        'position': screen_vertex[:3],  # x, y, z en coordenadas de pantalla
        'world_position': world_vertex[:3],  # Posición en espacio mundo
        'texcoord': texcoord,
        'normal': world_normal,
        'depth': view_vertex[2]  # Profundidad para z-buffer
    }

def fragment_shader(fragment_data: Dict[str, Any], uniforms: Dict[str, Any]) -> Tuple[int, int, int]:
    """
    Fragment Shader: Calcula el color final de un píxel
    """
    # Obtener datos del fragmento
    texcoord = fragment_data.get('texcoord', np.array([0.0, 0.0]))
    normal = fragment_data.get('normal', np.array([0.0, 0.0, 1.0]))
    world_pos = fragment_data.get('world_position', np.array([0.0, 0.0, 0.0]))
    
    # Obtener uniforms
    model = uniforms.get('model')
    light_dir = uniforms.get('light_direction', np.array([0.0, 0.0, 1.0]))
    light_color = uniforms.get('light_color', np.array([1.0, 1.0, 1.0]))
    ambient_strength = uniforms.get('ambient_strength', 0.3)
    
    # Color base (textura o color sólido)
    if model and model.texture_data is not None:
        # Usar textura
        base_color = np.array(model.get_texture_color(texcoord[0], texcoord[1]))
    else:
        # Color sólido para pelota de fútbol clásica (blanco y negro)
        # Crear patrón basado en posición
        u, v = texcoord[0], texcoord[1]
        
        # Patrón de pentágonos/hexágonos simulado
        pattern_u = int(u * 8) % 2
        pattern_v = int(v * 8) % 2
        
        if (pattern_u + pattern_v) % 2 == 0:
            base_color = np.array([240, 240, 240])  # Blanco
        else:
            base_color = np.array([40, 40, 40])     # Negro
    
    # Normalizar la normal
    normal_length = np.linalg.norm(normal)
    if normal_length > 0:
        normal = normal / normal_length
    
    # Calcular iluminación difusa (Lambertian)
    light_dir_normalized = light_dir / np.linalg.norm(light_dir)
    diffuse_factor = max(0.0, np.dot(normal, light_dir_normalized))
    
    # Calcular especular simple
    view_dir = np.array([0.0, 0.0, 1.0])  # Vista desde Z positivo
    reflect_dir = 2.0 * np.dot(normal, light_dir_normalized) * normal - light_dir_normalized
    specular_factor = max(0.0, np.dot(view_dir, reflect_dir)) ** 32
    
    # Combinar iluminación
    ambient = ambient_strength
    diffuse = diffuse_factor * 0.7
    specular = specular_factor * 0.3
    lighting = min(1.0, ambient + diffuse + specular)
    
    # Aplicar iluminación al color base
    final_color = base_color * lighting
    
    # Asegurar que los valores estén en el rango [0, 255]
    final_color = np.clip(final_color, 0, 255)
    
    return tuple(final_color.astype(int))

def interpolate_vertex_data(v1_data: Dict[str, Any], 
                          v2_data: Dict[str, Any], 
                          v3_data: Dict[str, Any], 
                          barycentric: Tuple[float, float, float]) -> Dict[str, Any]:
    """
    Interpola datos de vértices usando coordenadas baricéntricas
    """
    u, v, w = barycentric
    
    # Interpolación de coordenadas de textura
    texcoord1 = v1_data.get('texcoord', np.array([0.0, 0.0]))
    texcoord2 = v2_data.get('texcoord', np.array([0.0, 0.0]))
    texcoord3 = v3_data.get('texcoord', np.array([0.0, 0.0]))
    
    interpolated_texcoord = u * texcoord1 + v * texcoord2 + w * texcoord3
    
    # Interpolación de normales
    normal1 = v1_data.get('normal', np.array([0.0, 0.0, 1.0]))
    normal2 = v2_data.get('normal', np.array([0.0, 0.0, 1.0]))
    normal3 = v3_data.get('normal', np.array([0.0, 0.0, 1.0]))
    
    interpolated_normal = u * normal1 + v * normal2 + w * normal3
    
    # Interpolación de posición mundo
    world_pos1 = v1_data.get('world_position', np.array([0.0, 0.0, 0.0]))
    world_pos2 = v2_data.get('world_position', np.array([0.0, 0.0, 0.0]))
    world_pos3 = v3_data.get('world_position', np.array([0.0, 0.0, 0.0]))
    
    interpolated_world_pos = u * world_pos1 + v * world_pos2 + w * world_pos3
    
    # Interpolación de profundidad
    depth1 = v1_data.get('depth', 0.0)
    depth2 = v2_data.get('depth', 0.0)
    depth3 = v3_data.get('depth', 0.0)
    
    interpolated_depth = u * depth1 + v * depth2 + w * depth3
    
    return {
        'texcoord': interpolated_texcoord,
        'normal': interpolated_normal,
        'world_position': interpolated_world_pos,
        'depth': interpolated_depth
    }
