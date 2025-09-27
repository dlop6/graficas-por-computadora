import numpy as np
import pygame
from typing import List, Tuple, Dict, Any, Optional
from Model import Model
from Camera import Camera
from MathLib import ViewportMatrix, barycentric_coordinates
from Shaders import vertex_shader, interpolate_vertex_data, get_shader_by_name, AVAILABLE_SHADERS

class Renderer:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        # Frame buffer: matriz de píxeles RGB
        self.frame_buffer: List[List[Tuple[int, int, int]]] = [
            [(0, 0, 0) for _ in range(width)] for _ in range(height)
        ]
        
        # Z-buffer para depth testing
        self.z_buffer: List[List[float]] = [
            [float('inf') for _ in range(width)] for _ in range(height)
        ]
        
        # Lista de modelos a renderizar
        self.models: List[Model] = []
        
        # Cámara actual
        self.camera: Optional[Camera] = None
        
        # Configuraciones de iluminación
        self.light_direction = np.array([0.0, 0.0, 1.0])
        self.light_color = np.array([1.0, 1.0, 1.0])
        self.ambient_strength = 0.3
        
        # NUEVO: Configuración de shaders
        self.current_shader = 'water'  # Shader por defecto

    def clear(self, color: Tuple[int, int, int] = (0, 0, 0)):
        """Limpia el frame buffer y z-buffer"""
        self.frame_buffer = [
            [color for _ in range(self.width)] for _ in range(self.height)
        ]
        self.z_buffer = [
            [float('inf') for _ in range(self.width)] for _ in range(self.height)
        ]

    def set_camera(self, camera: Camera):
        """Establece la cámara actual"""
        self.camera = camera
        # Actualizar aspect ratio
        self.camera.aspect = self.width / self.height

    def add_model(self, model: Model):
        """Añade un modelo a la lista de renderizado"""
        self.models.append(model)
    
    # NUEVOS MÉTODOS PARA SHADERS
    def set_shader(self, shader_name: str):
        """Cambia el shader actual"""
        if shader_name in AVAILABLE_SHADERS:
            self.current_shader = shader_name
            print(f"Shader cambiado a: {AVAILABLE_SHADERS[shader_name]['name']}")
        else:
            print(f"Shader '{shader_name}' no encontrado. Disponibles: {list(AVAILABLE_SHADERS.keys())}")
    
    def get_available_shaders(self) -> Dict[str, Dict[str, str]]:
        """Obtiene la lista de shaders disponibles"""
        return AVAILABLE_SHADERS

    def render(self):
        """Renderiza todos los modelos con la cámara actual"""
        if not self.camera:
            print("Error: No hay cámara configurada")
            return
        
        # Calcular matrices de transformación
        view_matrix = self.camera.get_view_matrix()
        projection_matrix = self.camera.get_projection_matrix()
        viewport_matrix = ViewportMatrix(0, 0, self.width, self.height)
        
        # Renderizar cada modelo
        for model in self.models:
            self._render_model(model, view_matrix, projection_matrix, viewport_matrix)

    def _render_model(self, model: Model, view_matrix: np.ndarray, 
                     projection_matrix: np.ndarray, viewport_matrix: np.ndarray):
        """Renderiza un modelo específico"""
        if not model.vertices:
            return
        
        model_matrix = model.get_model_matrix()
        
        # Preparar uniforms para los shaders
        uniforms = {
            'model_matrix': model_matrix,
            'view_matrix': view_matrix,
            'projection_matrix': projection_matrix,
            'viewport_matrix': viewport_matrix,
            'model': model,
            'light_direction': self.light_direction,
            'light_color': self.light_color,
            'ambient_strength': self.ambient_strength
        }
        
        # Procesar vértices en grupos de 3 (triángulos)
        num_vertices = len(model.vertices) // 3
        
        for i in range(0, num_vertices, 3):
            # Obtener datos de los 3 vértices del triángulo
            v1_pos = np.array(model.vertices[i*3:(i+1)*3])
            v2_pos = np.array(model.vertices[(i+1)*3:(i+2)*3])
            v3_pos = np.array(model.vertices[(i+2)*3:(i+3)*3])
            
            v1_tex = np.array(model.texcoords[i*2:(i+1)*2]) if model.texcoords else np.array([0.0, 0.0])
            v2_tex = np.array(model.texcoords[(i+1)*2:(i+2)*2]) if model.texcoords else np.array([0.0, 0.0])
            v3_tex = np.array(model.texcoords[(i+2)*2:(i+3)*2]) if model.texcoords else np.array([0.0, 0.0])
            
            v1_norm = np.array(model.normals[i*3:(i+1)*3]) if model.normals else np.array([0.0, 0.0, 1.0])
            v2_norm = np.array(model.normals[(i+1)*3:(i+2)*3]) if model.normals else np.array([0.0, 0.0, 1.0])
            v3_norm = np.array(model.normals[(i+2)*3:(i+3)*3]) if model.normals else np.array([0.0, 0.0, 1.0])
            
            # Usar vertex shader del Lab 4 (con tiempo de animación)
            v1_data = vertex_shader(v1_pos, v1_tex, v1_norm, uniforms)
            v2_data = vertex_shader(v2_pos, v2_tex, v2_norm, uniforms)
            v3_data = vertex_shader(v3_pos, v3_tex, v3_norm, uniforms)
            
            # Rasterizar triángulo
            self._rasterize_triangle(v1_data, v2_data, v3_data, uniforms)

    def _rasterize_triangle(self, v1_data: Dict[str, Any], v2_data: Dict[str, Any], 
                           v3_data: Dict[str, Any], uniforms: Dict[str, Any]):
        """Rasteriza un triángulo usando scanline"""
        # Obtener posiciones en pantalla
        p1 = v1_data['position'][:2].astype(int)
        p2 = v2_data['position'][:2].astype(int)
        p3 = v3_data['position'][:2].astype(int)
        
        # Encontrar bounding box del triángulo
        min_x = max(0, min(p1[0], p2[0], p3[0]))
        max_x = min(self.width - 1, max(p1[0], p2[0], p3[0]))
        min_y = max(0, min(p1[1], p2[1], p3[1]))
        max_y = min(self.height - 1, max(p1[1], p2[1], p3[1]))
        
        # Rasterizar cada píxel dentro del bounding box
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                # Calcular coordenadas baricéntricas
                bary = barycentric_coordinates(p1, p2, p3, (x, y))
                
                if bary is None:
                    continue
                
                u, v, w = bary
                
                # Verificar si el punto está dentro del triángulo
                if u >= 0 and v >= 0 and w >= 0:
                    # Interpolar profundidad
                    depth = u * v1_data['depth'] + v * v2_data['depth'] + w * v3_data['depth']
                    
                    # Z-buffer test
                    if depth < self.z_buffer[y][x]:
                        self.z_buffer[y][x] = depth
                        
                        # USAR SHADER PERSONALIZADO
                        fragment_data = interpolate_vertex_data(v1_data, v2_data, v3_data, bary)
                        current_fragment_shader = get_shader_by_name(self.current_shader)
                        color = current_fragment_shader(fragment_data, uniforms)
                        
                        # Escribir píxel al frame buffer
                        self.frame_buffer[y][x] = color

    def get_framebuffer_as_surface(self) -> pygame.Surface:
        """Convierte el frame buffer a una superficie de pygame"""
        surface = pygame.Surface((self.width, self.height))
        
        for y in range(self.height):
            for x in range(self.width):
                color = self.frame_buffer[y][x]
                surface.set_at((x, y), color)
        
        return surface

    def save_framebuffer(self, filename: str):
        """Guarda el frame buffer como imagen BMP"""
        surface = self.get_framebuffer_as_surface()
        pygame.image.save(surface, filename)
        print(f"Frame buffer guardado como: {filename}")

    def set_light_direction(self, x: float, y: float, z: float):
        """Establece la dirección de la luz"""
        self.light_direction = np.array([x, y, z])
        # Normalizar
        length = np.linalg.norm(self.light_direction)
        if length > 0:
            self.light_direction = self.light_direction / length
