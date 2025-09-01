"""
Material module for the raytracer
Implements material properties for Phong shading
"""

import numpy as np

class Material:
    def __init__(self, diffuse_color, specular_color, ambient_color, shininess=32):
        self.diffuse_color = np.array(diffuse_color, dtype=float)
        self.specular_color = np.array(specular_color, dtype=float) 
        self.ambient_color = np.array(ambient_color, dtype=float)
        self.shininess = shininess
    
    def get_color(self, ambient_light, lights, point, normal, view_direction):
        # Componente ambiental
        color = self.ambient_color * ambient_light
        
        for light in lights:
            # Dirección de la luz
            light_direction = light.get_light_direction(point)
            
            # Componente difusa (Lambert)
            diffuse_intensity = max(0, np.dot(normal, light_direction))
            diffuse = self.diffuse_color * light.color * diffuse_intensity * light.intensity
            
            # Componente especular (Phong)
            if diffuse_intensity > 0:
                # Vector de reflexión
                reflect_direction = 2 * np.dot(normal, light_direction) * normal - light_direction
                reflect_direction = reflect_direction / np.linalg.norm(reflect_direction)
                
                # Intensidad especular
                specular_intensity = max(0, np.dot(reflect_direction, view_direction))
                specular_intensity = pow(specular_intensity, self.shininess)
                specular = self.specular_color * light.color * specular_intensity * light.intensity
            else:
                specular = np.array([0.0, 0.0, 0.0])
            
            color += diffuse + specular
        
        return np.clip(color, 0.0, 1.0)