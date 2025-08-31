import numpy as np

class Light:
    def __init__(self, position, color, intensity=1.0):
        self.position = np.array(position, dtype=float)
        self.color = np.array(color, dtype=float)
        self.intensity = intensity
    
    def get_light_direction(self, point):
        direction = self.position - point
        return direction / np.linalg.norm(direction)
    
    def get_distance_to(self, point):
        return np.linalg.norm(self.position - point)
