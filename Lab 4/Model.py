import numpy as np
import pygame
from typing import List, Tuple, Optional
from MathLib import *

class Model:
    def __init__(self):
        # Datos del modelo
        self.vertices: List[float] = []
        self.normals: List[float] = []
        self.texcoords: List[float] = []
        self.faces: List[List[int]] = []
        
        # Transformaciones
        self.translation = [0.0, 0.0, 0.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.scale = [1.0, 1.0, 1.0]
        
        # Textura
        self.texture: Optional[pygame.Surface] = None
        self.texture_data: Optional[np.ndarray] = None

    def load_obj(self, filepath: str, texture_path: str = None):
        """Carga un modelo OBJ y opcionalmente su textura"""
        vertices = []
        normals = []
        texcoords = []
        faces = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('v '):
                        # Vértice
                        parts = line.split()
                        vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                    elif line.startswith('vn '):
                        # Normal
                        parts = line.split()
                        normals.append([float(parts[1]), float(parts[2]), float(parts[3])])
                    elif line.startswith('vt '):
                        # Coordenada de textura
                        parts = line.split()
                        texcoords.append([float(parts[1]), float(parts[2])])
                    elif line.startswith('f '):
                        # Cara
                        parts = line.split()[1:]
                        face_vertices = []
                        face_texcoords = []
                        face_normals = []
                        
                        for part in parts:
                            indices = part.split('/')
                            # Índice de vértice (obligatorio)
                            face_vertices.append(int(indices[0]) - 1)
                            # Índice de textura (opcional)
                            if len(indices) > 1 and indices[1]:
                                face_texcoords.append(int(indices[1]) - 1)
                            # Índice de normal (opcional)
                            if len(indices) > 2 and indices[2]:
                                face_normals.append(int(indices[2]) - 1)
                        
                        # Triangular polígonos (fan triangulation)
                        if len(face_vertices) >= 3:
                            for i in range(1, len(face_vertices) - 1):
                                # Crear triángulo usando vértices 0, i, i+1
                                triangle_vertices = [face_vertices[0], face_vertices[i], face_vertices[i+1]]
                                
                                triangle_texcoords = []
                                if face_texcoords and len(face_texcoords) >= len(face_vertices):
                                    triangle_texcoords = [face_texcoords[0], face_texcoords[i], face_texcoords[i+1]]
                                
                                triangle_normals = []
                                if face_normals and len(face_normals) >= len(face_vertices):
                                    triangle_normals = [face_normals[0], face_normals[i], face_normals[i+1]]
                                
                                faces.append([triangle_vertices, triangle_texcoords, triangle_normals])
        
        except Exception as e:
            print(f"Error cargando modelo OBJ: {e}")
            return False
        
        # Convertir a arrays planos para facilidad de uso
        self.vertices = []
        self.texcoords = []
        self.normals = []
        
        for face in faces:
            vertex_indices, texcoord_indices, normal_indices = face
            
            for i in range(3):
                # Vértices
                v_idx = vertex_indices[i]
                self.vertices.extend(vertices[v_idx])
                
                # Coordenadas de textura
                if texcoord_indices and len(texcoord_indices) > i and texcoord_indices[i] is not None:
                    t_idx = texcoord_indices[i]
                    self.texcoords.extend(texcoords[t_idx])
                else:
                    self.texcoords.extend([0.0, 0.0])
                
                # Normales
                if normal_indices and len(normal_indices) > i and normal_indices[i] is not None:
                    n_idx = normal_indices[i]
                    self.normals.extend(normals[n_idx])
                else:
                    # Calcular normal del triángulo si no hay normales
                    if i == 0:  # Solo calcular una vez por triángulo
                        v1 = np.array(vertices[vertex_indices[0]])
                        v2 = np.array(vertices[vertex_indices[1]]) 
                        v3 = np.array(vertices[vertex_indices[2]])
                        
                        # Calcular normal usando producto cruz
                        edge1 = v2 - v1
                        edge2 = v3 - v1
                        normal = np.cross(edge1, edge2)
                        
                        # Normalizar
                        length = np.linalg.norm(normal)
                        if length > 0:
                            normal = normal / length
                        else:
                            normal = np.array([0.0, 0.0, 1.0])
                        
                        # Guardar normal calculada para este triángulo
                        triangle_normal = normal.tolist()
                    
                    # Usar la normal calculada para todos los vértices del triángulo
                    if i == 0:
                        self.normals.extend(triangle_normal)
                    elif i == 1:
                        self.normals.extend(triangle_normal)
                    else:
                        self.normals.extend(triangle_normal)
        
        # Cargar textura si se especifica
        if texture_path:
            self.load_texture(texture_path)
        
        print(f"Modelo cargado: {len(self.vertices)//3} vértices, {len(faces)} caras")
        return True

    def load_texture(self, texture_path: str):
        """Carga una textura desde un archivo de imagen"""
        try:
            self.texture = pygame.image.load(texture_path)
            # Convertir a array numpy para acceso rápido a píxeles
            self.texture_data = pygame.surfarray.array3d(self.texture)
            print(f"Textura cargada: {self.texture.get_width()}x{self.texture.get_height()}")
            return True
        except Exception as e:
            print(f"Error cargando textura: {e}")
            return False

    def get_model_matrix(self):
        """Calcula la matriz de modelo (Model Matrix)"""
        translation_matrix = TranslationMatrix(*self.translation)
        rotation_matrix = RotationMatrix(*self.rotation)
        scale_matrix = ScaleMatrix(*self.scale)
        
        return translation_matrix @ rotation_matrix @ scale_matrix

    def get_texture_color(self, u: float, v: float) -> Tuple[int, int, int]:
        """Obtiene el color de la textura en las coordenadas UV dadas"""
        if self.texture_data is None:
            return (255, 255, 255)  # Blanco por defecto
        
        # Envolver coordenadas UV
        u = u % 1.0
        v = v % 1.0
        
        # Convertir a coordenadas de píxel
        tex_width, tex_height, _ = self.texture_data.shape
        x = int(u * (tex_width - 1))
        y = int((1.0 - v) * (tex_height - 1))  # Invertir V
        
        # Asegurar que estamos dentro de los límites
        x = max(0, min(x, tex_width - 1))
        y = max(0, min(y, tex_height - 1))
        
        return tuple(self.texture_data[x, y])

    def auto_center_and_scale(self, target_size: float = 2.0):
        """Auto-centra y escala el modelo para caber en un cubo de tamaño dado"""
        if not self.vertices:
            return
        
        # Encontrar límites
        xs = self.vertices[0::3]
        ys = self.vertices[1::3]
        zs = self.vertices[2::3]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        min_z, max_z = min(zs), max(zs)
        
        # Centrar
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        center_z = (min_z + max_z) / 2
        
        # Escalar
        extent = max(max_x - min_x, max_y - min_y, max_z - min_z)
        if extent > 0:
            scale_factor = target_size / extent
            self.scale = [scale_factor, scale_factor, scale_factor]
            self.translation = [-center_x * scale_factor, -center_y * scale_factor, -center_z * scale_factor]
