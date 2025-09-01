"""
Lights module for the raytracer
"""

import numpy as np

class Light:
    """
    Clase para representar una fuente de luz puntual
    """
    def __init__(self, position, color, intensity=1.0):
        self.position = np.array(position, dtype=float)
        self.color = np.array(color, dtype=float)
        self.intensity = intensity
    
    def get_light_direction(self, point):
        """
        Obtiene la dirección de la luz desde un punto dado
        """
        direction = self.position - point
        return direction / np.linalg.norm(direction)
    
    def get_distance_to(self, point):
        """
        Obtiene la distancia de la luz a un punto
        """
        return np.linalg.norm(self.position - point)
