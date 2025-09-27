import numpy as np

class RectPlane:
    def __init__(self, center, normal, width, height, material=None):
        self.center = np.array(center)
        self.normal = np.array(normal) / np.linalg.norm(normal)
        self.width = width
        self.height = height
        self.material = material
        # Generate two orthogonal vectors in the plane
        if abs(self.normal[0]) > abs(self.normal[1]):
            self.u = np.cross(self.normal, [0,1,0])
        else:
            self.u = np.cross(self.normal, [1,0,0])
        self.u = self.u / np.linalg.norm(self.u)
        self.v = np.cross(self.normal, self.u)

    def intersect(self, ray_origin, ray_dir):
        # Ray-plane intersection
        denom = np.dot(self.normal, ray_dir)
        if abs(denom) < 1e-6:
            return None  # Parallel, no intersection
        t = np.dot(self.center - ray_origin, self.normal) / denom
        if t < 0:
            return None  # Intersection behind ray
        hit_point = ray_origin + t * ray_dir
        # Project hit_point onto plane axes to check bounds
        rel = hit_point - self.center
        u_dist = np.dot(rel, self.u)
        v_dist = np.dot(rel, self.v)
        if abs(u_dist) > self.width/2 or abs(v_dist) > self.height/2:
            return None  # Outside rectangle
        return {
            't': t,
            'point': hit_point,
            'normal': self.normal,
            'material': self.material
        }
