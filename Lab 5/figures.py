import numpy as np

class Shape:
    def __init__(self, position, material=None):
        self.position = np.array(position, dtype=float)
        self.material = material
        self.type = "None"
    
    def ray_intersect(self, orig, dir):
        return False, None
    
    
class Sphere(Shape):
    def __init__(self, position, radius, material=None):
        super().__init__(position, material)
        self.radius = radius
        self.type = "Sphere"

    def ray_intersect(self, orig, dir):
        # Ray-sphere intersection
        L = self.position - orig
        
        tca = np.dot(L, dir)
        
        if tca < 0:
            return False, None
        
        d2 = np.dot(L, L) - tca * tca
        
        if d2 > self.radius * self.radius:
            return False, None
        
        thc = np.sqrt(self.radius * self.radius - d2)
        
        t0 = tca - thc
        t1 = tca + thc
        
        if t0 > 0:
            return True, t0
        elif t1 > 0:
            return True, t1
        else:
            return False, None
    
    def get_normal(self, point):
        normal = point - self.position
        return normal / np.linalg.norm(normal)            