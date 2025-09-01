import numpy as np

class Shape(object):
    def __init__(self, position, material=None) -> None:
        self.position = np.array(position, dtype=float)
        self.material = material
        self.type = "None"
    
    def ray_intersect(self, orig, dir):
        return False, None
    
    
class Sphere(Shape):
    def __init__(self, position, radius, material=None) -> None:
        super().__init__(position, material)
        self.radius = radius
        self.type = "Sphere"

    def ray_intersect(self, orig, dir):
        """
        Implementa la intersección rayo-esfera usando la ecuación cuadrática
        Retorna (hit, distance) donde hit es bool y distance es float
        """
        # Vector del origen del rayo al centro de la esfera
        L = self.position - orig
        
        # Proyección de L sobre la dirección del rayo
        tca = np.dot(L, dir)
        
        # Si tca < 0, la esfera está detrás del origen del rayo
        if tca < 0:
            return False, None
        
        # Distancia cuadrada del centro de la esfera al rayo
        d2 = np.dot(L, L) - tca * tca
        
        # Si d2 > radius^2, el rayo no intersecta la esfera
        if d2 > self.radius * self.radius:
            return False, None
        
        # Distancia desde el punto de proyección a los puntos de intersección
        thc = np.sqrt(self.radius * self.radius - d2)
        
        # Las dos soluciones de la ecuación cuadrática
        t0 = tca - thc  # Intersección más cercana
        t1 = tca + thc  # Intersección más lejana
        
        # Tomamos la intersección más cercana que sea positiva
        if t0 > 0:
            return True, t0
        elif t1 > 0:
            return True, t1
        else:
            return False, None
    
    def get_normal(self, point):
        """
        Calcula la normal en un punto de la superficie de la esfera
        """
        normal = point - self.position
        return normal / np.linalg.norm(normal)            