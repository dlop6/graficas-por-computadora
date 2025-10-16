"""
Sistema de iluminación para raytracing.
Soporta múltiples tipos de luces: Directional, Point, Spotlight.
"""
import numpy as np
import math


class Light:
    """Clase base para todas las luces."""
    def __init__(self, color=(1.0, 1.0, 1.0), intensity=1.0):
        self.color = np.array(color, dtype=float)
        self.intensity = float(intensity)
    
    def get_light_direction(self, point):
        """Retorna la dirección de la luz desde un punto.
        Debe ser implementado por subclases."""
        raise NotImplementedError
    
    def get_intensity(self, point):
        """Retorna la intensidad de la luz en un punto.
        Incluye atenuación si aplica."""
        raise NotImplementedError
    
    def get_color(self):
        """Retorna el color de la luz."""
        return tuple(self.color * self.intensity)


class DirectionalLight(Light):
    """Luz direccional (como el sol).
    Todos los rayos son paralelos, sin atenuación por distancia."""
    
    def __init__(self, direction, color=(1.0, 1.0, 1.0), intensity=1.0):
        super().__init__(color, intensity)
        self.direction = np.array(direction, dtype=float)
        self.direction = self.direction / np.linalg.norm(self.direction)
    
    def get_light_direction(self, point):
        """Retorna dirección hacia la luz (opuesta a self.direction)."""
        return -self.direction
    
    def get_intensity(self, point):
        """Sin atenuación por distancia."""
        return self.intensity
    
    def is_infinite(self):
        """True para luces infinitas (usado para shadows)."""
        return True


class PointLight(Light):
    """Luz puntual que emite en todas direcciones.
    Atenuación cuadrática con la distancia."""
    
    def __init__(self, position, color=(1.0, 1.0, 1.0), intensity=1.0, 
                 attenuation=(1.0, 0.0, 1.0)):
        """
        Args:
            position: Posición 3D de la luz
            color: Color RGB (0-1)
            intensity: Intensidad base
            attenuation: (constant, linear, quadratic) para I / (c + l*d + q*d^2)
        """
        super().__init__(color, intensity)
        self.position = np.array(position, dtype=float)
        self.attenuation = attenuation  # (constant, linear, quadratic)
    
    def get_light_direction(self, point):
        """Retorna dirección normalizada desde point hacia la luz."""
        direction = self.position - point
        dist = np.linalg.norm(direction)
        if dist < 1e-6:
            return np.array([0, 1, 0], dtype=float)
        return direction / dist
    
    def get_intensity(self, point):
        """Calcula intensidad con atenuación cuadrática."""
        direction = self.position - point
        distance = np.linalg.norm(direction)
        
        # Atenuación: I / (constant + linear*d + quadratic*d^2)
        c, l, q = self.attenuation
        attenuation_factor = c + l * distance + q * distance * distance
        
        if attenuation_factor < 1e-6:
            return 0.0
        
        return self.intensity / attenuation_factor
    
    def get_distance_to_light(self, point):
        """Retorna distancia al punto de luz (para shadow rays)."""
        return np.linalg.norm(self.position - point)
    
    def is_infinite(self):
        return False


class SpotLight(Light):
    """Luz tipo spotlight con cono de iluminación direccional.
    Similar a PointLight pero solo ilumina dentro de un cono."""
    
    def __init__(self, position, direction, cutoff_angle, color=(1.0, 1.0, 1.0), 
                 intensity=1.0, attenuation=(1.0, 0.0, 1.0), falloff=1.0):
        """
        Args:
            position: Posición 3D de la luz
            direction: Dirección del cono de luz
            cutoff_angle: Ángulo del cono en grados (half-angle)
            color: Color RGB (0-1)
            intensity: Intensidad base
            attenuation: (constant, linear, quadratic)
            falloff: Exponente para suavizar bordes del cono (1.0 = hard edges)
        """
        super().__init__(color, intensity)
        self.position = np.array(position, dtype=float)
        self.direction = np.array(direction, dtype=float)
        self.direction = self.direction / np.linalg.norm(self.direction)
        self.cutoff_angle = math.radians(cutoff_angle)
        self.cos_cutoff = math.cos(self.cutoff_angle)
        self.attenuation = attenuation
        self.falloff = falloff
    
    def get_light_direction(self, point):
        """Retorna dirección normalizada desde point hacia la luz."""
        direction = self.position - point
        dist = np.linalg.norm(direction)
        if dist < 1e-6:
            return np.array([0, 1, 0], dtype=float)
        return direction / dist
    
    def get_intensity(self, point):
        """Calcula intensidad con atenuación y spotlight cone falloff."""
        to_light = self.position - point
        distance = np.linalg.norm(to_light)
        
        if distance < 1e-6:
            return 0.0
        
        light_dir = to_light / distance
        
        # Verificar si el punto está dentro del cono
        spot_cos = np.dot(-light_dir, self.direction)
        
        if spot_cos < self.cos_cutoff:
            # Fuera del cono
            return 0.0
        
        # Spotlight factor (smooth falloff)
        spot_factor = spot_cos ** self.falloff
        
        # Atenuación por distancia
        c, l, q = self.attenuation
        attenuation_factor = c + l * distance + q * distance * distance
        
        if attenuation_factor < 1e-6:
            return 0.0
        
        return self.intensity * spot_factor / attenuation_factor
    
    def get_distance_to_light(self, point):
        """Retorna distancia al punto de luz (para shadow rays)."""
        return np.linalg.norm(self.position - point)
    
    def is_infinite(self):
        return False


class AmbientLight:
    """Luz ambiental global (sin dirección).
    No requiere cálculos de dirección o atenuación."""
    
    def __init__(self, color=(0.1, 0.1, 0.1), intensity=1.0):
        self.color = np.array(color, dtype=float)
        self.intensity = float(intensity)
    
    def get_color(self):
        """Retorna color ambiental."""
        return tuple(self.color * self.intensity)


# Función helper para crear configuraciones comunes de luces
def create_default_lighting():
    """Retorna una configuración básica de 3 luces + ambient."""
    return {
        'ambient': AmbientLight(color=(0.7, 0.75, 0.8), intensity=0.15),
        'lights': [
            # Luz principal (sol)
            DirectionalLight(
                direction=(-0.3, -0.5, -0.4),
                color=(1.0, 0.98, 0.92),
                intensity=0.7
            ),
            # Point light de relleno
            PointLight(
                position=(1.5, 2.0, 1.0),
                color=(1.0, 0.95, 0.85),
                intensity=1.2,
                attenuation=(1.0, 0.1, 0.05)
            ),
            # Point light azul (fill)
            PointLight(
                position=(-2.0, 1.5, 0.5),
                color=(0.8, 0.85, 1.0),
                intensity=0.6,
                attenuation=(1.0, 0.15, 0.08)
            ),
        ]
    }


def create_pikmin_lighting():
    """Configuración de luces para la escena Pikmin según scene_plan.md."""
    return {
        'ambient': AmbientLight(color=(0.7, 0.75, 0.8), intensity=0.15),
        'lights': [
            # 1. Directional Light (sol suave)
            DirectionalLight(
                direction=(-0.3, -0.5, -0.4),
                color=(1.0, 0.98, 0.92),
                intensity=0.7
            ),
            # 2. Point Light #1 (luz principal)
            PointLight(
                position=(1.5, 2.0, 1.0),
                color=(1.0, 0.95, 0.85),
                intensity=1.2,
                attenuation=(1.0, 0.09, 0.032)  # ~3 units reach
            ),
            # 3. Point Light #2 (fill light)
            PointLight(
                position=(-2.0, 1.5, 0.5),
                color=(0.8, 0.85, 1.0),
                intensity=0.6,
                attenuation=(1.0, 0.14, 0.07)  # ~2.5 units reach
            ),
            # 4. Spotlight (foco en Pikmin)
            SpotLight(
                position=(0, 3.0, 2.0),
                direction=(0, -0.9, -0.4),  # Hacia (0, 0.3, 0)
                cutoff_angle=30,
                color=(1.0, 1.0, 1.0),
                intensity=0.8,
                attenuation=(1.0, 0.05, 0.02),
                falloff=2.0  # Smooth edges
            ),
        ]
    }
