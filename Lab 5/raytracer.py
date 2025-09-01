"""
Raytracer - Lab 5
Implementación de un raytracer básico con esferas y modelo de iluminación Phong
"""

import numpy as np
from BMP_Writer import GenerateBMP
from MathLib import normalize

class Raytracer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.aspect_ratio = width / height
        
        # Buffer de colores
        self.color_buffer = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
        
        # Configuración de la cámara virtual
        self.camera_position = np.array([0.0, 0.0, 0.0])
        self.fov = 60  # Field of view en grados
        
        # Luces y objetos
        self.lights = []
        self.objects = []
        
        # Luz ambiental
        self.ambient_light = np.array([0.1, 0.1, 0.1])
        
        # Color de fondo
        self.background_color = np.array([0.1, 0.1, 0.2])  # Azul oscuro
    
    def add_object(self, obj):
        """Añade un objeto a la escena"""
        self.objects.append(obj)
    
    def add_light(self, light):
        """Añade una luz a la escena"""
        self.lights.append(light)
    
    def set_camera(self, position):
        """Establece la posición de la cámara"""
        self.camera_position = np.array(position)
    
    def generate_ray(self, x, y):
        """
        Genera un rayo desde la cámara hacia el pixel (x, y)
        """
        # Convertir coordenadas de pantalla a coordenadas NDC [-1, 1]
        ndc_x = (2.0 * x) / self.width - 1.0
        ndc_y = 1.0 - (2.0 * y) / self.height
        
        # Ajustar por aspect ratio
        ndc_x *= self.aspect_ratio
        
        # Calcular dirección del rayo
        fov_rad = np.radians(self.fov)
        pixel_camera_x = ndc_x * np.tan(fov_rad / 2.0)
        pixel_camera_y = ndc_y * np.tan(fov_rad / 2.0)
        
        # Dirección del rayo en espacio de cámara (hacia -Z)
        ray_direction = np.array([pixel_camera_x, pixel_camera_y, -1.0])
        ray_direction = normalize(ray_direction)
        
        return self.camera_position, ray_direction
    
    def cast_ray(self, ray_origin, ray_direction):
        """
        Lanza un rayo y encuentra la intersección más cercana
        """
        closest_distance = float('inf')
        closest_object = None
        
        for obj in self.objects:
            hit, distance = obj.ray_intersect(ray_origin, ray_direction)
            if hit and distance < closest_distance and distance > 0:
                closest_distance = distance
                closest_object = obj
        
        if closest_object:
            # Calcular punto de intersección
            hit_point = ray_origin + ray_direction * closest_distance
            return closest_object, hit_point, closest_distance
        
        return None, None, None
    
    def calculate_lighting(self, obj, hit_point, ray_direction):
        """
        Calcula la iluminación en un punto usando el modelo Phong
        """
        if not obj.material:
            return np.array([1.0, 1.0, 1.0])  # Color blanco por defecto
        
        # Calcular normal en el punto de intersección
        normal = obj.get_normal(hit_point)
        
        # Dirección hacia la cámara (opuesta al rayo)
        view_direction = -ray_direction
        view_direction = normalize(view_direction)
        
        # Calcular color usando el material
        color = obj.material.get_color(
            self.ambient_light,
            self.lights,
            hit_point,
            normal,
            view_direction
        )
        
        return color
    
    def render_pixel(self, x, y):
        """
        Renderiza un pixel individual
        """
        # Generar rayo
        ray_origin, ray_direction = self.generate_ray(x, y)
        
        # Lanzar rayo
        closest_object, hit_point, distance = self.cast_ray(ray_origin, ray_direction)
        
        if closest_object:
            # Calcular iluminación
            color = self.calculate_lighting(closest_object, hit_point, ray_direction)
        else:
            # Color de fondo
            color = self.background_color
        
        # Convertir color a enteros [0-255]
        color_int = (
            int(np.clip(color[0] * 255, 0, 255)),
            int(np.clip(color[1] * 255, 0, 255)),
            int(np.clip(color[2] * 255, 0, 255))
        )
        
        return color_int
    
    def render(self):
        """
        Renderiza la escena completa
        """
        print(f"Renderizando imagen de {self.width}x{self.height}...")
        
        total_pixels = self.width * self.height
        processed_pixels = 0
        
        for y in range(self.height):
            for x in range(self.width):
                # Renderizar pixel
                color = self.render_pixel(x, y)
                self.color_buffer[y][x] = color
                
                # Mostrar progreso
                processed_pixels += 1
                if processed_pixels % (total_pixels // 20) == 0:
                    progress = (processed_pixels / total_pixels) * 100
                    print(f"Progreso: {progress:.1f}%")
        
        print("Renderizado completado!")
    
    def save_image(self, filename):
        """
        Guarda la imagen renderizada en un archivo BMP
        """
        GenerateBMP(filename, self.width, self.height, 3, self.color_buffer)
        print(f"Imagen guardada como: {filename}")
    
    def set_background_color(self, color):
        """
        Establece el color de fondo
        """
        self.background_color = np.array(color)
    
    def clear_scene(self):
        """
        Limpia todos los objetos y luces de la escena
        """
        self.objects.clear()
        self.lights.clear()