import math
import numpy as np


class Ray:
    """Representa un rayo en 3D."""
    def __init__(self, origin, direction):
        self.origin = np.array(origin, dtype=float)
        self.direction = np.array(direction, dtype=float) / np.linalg.norm(direction)
    
    def at(self, t):
        """Retorna el punto en el rayo a distancia t."""
        return self.origin + t * self.direction


class HitInfo:
    """Información de intersección rayo-objeto."""
    def __init__(self, t, point, normal, material, uv=(0, 0)):
        self.t = t
        self.point = point
        self.normal = np.array(normal, dtype=float)
        self.normal = self.normal / np.linalg.norm(self.normal)
        self.material = material
        self.uv = uv


class Sphere:
    """Esfera con centro y radio."""
    def __init__(self, center, radius, material):
        self.center = np.array(center, dtype=float)
        self.radius = float(radius)
        self.material = material
    
    def intersect(self, ray):
        """Ray-sphere intersection usando ecuación cuadrática."""
        oc = ray.origin - self.center
        a = np.dot(ray.direction, ray.direction)
        b = 2.0 * np.dot(oc, ray.direction)
        c = np.dot(oc, oc) - self.radius ** 2
        discriminant = b * b - 4 * a * c
        
        if discriminant < 0:
            return None
        
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        
        t = t1 if t1 > 0.001 else t2
        if t <= 0.001:
            return None
        
        point = ray.at(t)
        normal = (point - self.center) / self.radius
        # UV spherical
        phi = math.atan2(normal[2], normal[0])
        theta = math.acos(normal[1])
        u = (phi + math.pi) / (2 * math.pi)
        v = theta / math.pi
        
        return HitInfo(t, point, normal, self.material, (u, v))


class Plane:
    """Plano definido por punto y normal."""
    def __init__(self, point, normal, material, scale=10.0):
        self.point = np.array(point, dtype=float)
        self.normal = np.array(normal, dtype=float) / np.linalg.norm(normal)
        self.material = material
        self.scale = scale
    
    def intersect(self, ray):
        """Ray-plane intersection."""
        denom = np.dot(ray.direction, self.normal)
        if abs(denom) < 1e-6:
            return None
        
        t = np.dot(self.point - ray.origin, self.normal) / denom
        if t <= 0.001:
            return None
        
        point = ray.at(t)
        
        # Calcular UV usando proyección
        v_right = np.array([-self.normal[1], self.normal[0], 0], dtype=float)
        if np.linalg.norm(v_right) < 1e-6:
            v_right = np.array([1, 0, 0], dtype=float)
        v_right = v_right / np.linalg.norm(v_right)
        v_up = np.cross(self.normal, v_right)
        
        offset = point - self.point
        u = (np.dot(offset, v_right) / self.scale) % 1.0
        v = (np.dot(offset, v_up) / self.scale) % 1.0
        
        return HitInfo(t, point, self.normal, self.material, (u, v))


class Cylinder:
    """Cilindro vertical con centro en la base, radio y altura."""
    def __init__(self, center, radius, height, material):
        self.center = np.array(center, dtype=float)
        self.radius = float(radius)
        self.height = float(height)
        self.material = material
    
    def intersect(self, ray):
        """Ray-cylinder intersection (aproximado con dos capas y lateral)."""
        # Intersección con el cilindro lateral
        oc = ray.origin - self.center
        oc_xz = np.array([oc[0], 0, oc[2]])
        dir_xz = np.array([ray.direction[0], 0, ray.direction[2]])
        
        a = np.dot(dir_xz, dir_xz)
        b = 2.0 * np.dot(oc_xz, dir_xz)
        c = np.dot(oc_xz, oc_xz) - self.radius ** 2
        
        discriminant = b * b - 4 * a * c
        if discriminant >= 0:
            t1 = (-b - math.sqrt(discriminant)) / (2 * a)
            t2 = (-b + math.sqrt(discriminant)) / (2 * a)
            
            for t in sorted([t1, t2]):
                if t > 0.001:
                    point = ray.at(t)
                    if 0 <= point[1] - self.center[1] <= self.height:
                        normal = (point - self.center) * np.array([1, 0, 1])
                        normal = normal / np.linalg.norm(normal)
                        phi = math.atan2(point[2] - self.center[2], point[0] - self.center[0])
                        u = (phi + math.pi) / (2 * math.pi)
                        v = (point[1] - self.center[1]) / self.height
                        return HitInfo(t, point, normal, self.material, (u, v))
        
        # Intersección con tapa superior e inferior
        for y_target in [self.center[1], self.center[1] + self.height]:
            if abs(ray.direction[1]) > 1e-6:
                t = (y_target - ray.origin[1]) / ray.direction[1]
                if t > 0.001:
                    point = ray.at(t)
                    dist_sq = (point[0] - self.center[0]) ** 2 + (point[2] - self.center[2]) ** 2
                    if dist_sq <= self.radius ** 2:
                        normal = np.array([0, 1 if y_target > self.center[1] else -1, 0], dtype=float)
                        u = (point[0] - self.center[0] + self.radius) / (2 * self.radius)
                        v = (point[2] - self.center[2] + self.radius) / (2 * self.radius)
                        return HitInfo(t, point, normal, self.material, (u, v))
        
        return None
