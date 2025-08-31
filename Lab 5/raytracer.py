import numpy as np
from BMP_Writer import GenerateBMP
from MathLib import normalize

class Raytracer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.aspect_ratio = width / height
        
        self.color_buffer = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
        
        # Configuración de cámara
        self.camera_position = np.array([0.0, 0.0, 0.0])
        self.fov = 60
        
        self.lights = []
        self.objects = []
        
        self.ambient_light = np.array([0.1, 0.1, 0.1])
        self.background_color = np.array([0.1, 0.1, 0.2])
    
    def add_object(self, obj):
        self.objects.append(obj)
    
    def add_light(self, light):
        self.lights.append(light)
    
    def set_camera(self, position):
        self.camera_position = np.array(position)
    
    def generate_ray(self, x, y):
        # Convertir pixel a coordenadas NDC
        ndc_x = (2.0 * x) / self.width - 1.0
        ndc_y = 1.0 - (2.0 * y) / self.height
        
        ndc_x *= self.aspect_ratio
        
        # Calcular dirección del rayo
        fov_rad = np.radians(self.fov)
        pixel_x = ndc_x * np.tan(fov_rad / 2.0)
        pixel_y = ndc_y * np.tan(fov_rad / 2.0)
        
        ray_direction = np.array([pixel_x, pixel_y, -1.0])
        ray_direction = normalize(ray_direction)
        
        return self.camera_position, ray_direction
    
    def cast_ray(self, ray_origin, ray_direction):
        closest_distance = float('inf')
        closest_object = None
        
        for obj in self.objects:
            hit, distance = obj.ray_intersect(ray_origin, ray_direction)
            if hit and distance < closest_distance and distance > 0:
                closest_distance = distance
                closest_object = obj
        
        if closest_object:
            hit_point = ray_origin + ray_direction * closest_distance
            return closest_object, hit_point, closest_distance
        
        return None, None, None
    
    def calculate_lighting(self, obj, hit_point, ray_direction):
        if not obj.material:
            return np.array([1.0, 1.0, 1.0])
        
        normal = obj.get_normal(hit_point)
        view_direction = -ray_direction
        view_direction = normalize(view_direction)
        
        color = obj.material.get_color(
            self.ambient_light,
            self.lights,
            hit_point,
            normal,
            view_direction
        )
        
        return color
    
    def render_pixel(self, x, y):
        ray_origin, ray_direction = self.generate_ray(x, y)
        closest_object, hit_point, distance = self.cast_ray(ray_origin, ray_direction)
        
        if closest_object:
            color = self.calculate_lighting(closest_object, hit_point, ray_direction)
        else:
            color = self.background_color
        
        # Convertir a RGB entero
        color_int = (
            int(np.clip(color[0] * 255, 0, 255)),
            int(np.clip(color[1] * 255, 0, 255)),
            int(np.clip(color[2] * 255, 0, 255))
        )
        
        return color_int
    
    def render(self):
        print(f"Renderizando {self.width}x{self.height}...")
        
        total_pixels = self.width * self.height
        processed = 0
        
        for y in range(self.height):
            for x in range(self.width):
                self.color_buffer[y][x] = self.render_pixel(x, y)
                
                processed += 1
                if processed % (total_pixels // 10) == 0:
                    progress = (processed / total_pixels) * 100
                    print(f"Progreso: {progress:.0f}%")
        
        print("Terminado!")
    
    def save_image(self, filename):
        GenerateBMP(filename, self.width, self.height, 3, self.color_buffer)
    
    def set_background_color(self, color):
        self.background_color = np.array(color)
    
    def clear_scene(self):
        self.objects.clear()
        self.lights.clear()