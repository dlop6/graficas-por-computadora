import numpy as np
import math
from primitives import Ray, Sphere, Plane, Cylinder, HitInfo
from materials import Lambertian, Metal, Refractive
from HDRTexture import HDRTexture


class Raytracer:
    """Motor de raytracing básico."""
    
    def __init__(self, envmap=None):
        self.envmap = envmap
    
    def trace(self, ray, scene, depth=0, max_depth=3):
        """Lanza un rayo y retorna color (0..1 RGB)."""
        if depth > max_depth:
            return self.sample_envmap_or_black(ray.direction)
        
        # Encontrar intersección más cercana
        hit = None
        min_t = float('inf')
        
        for obj in scene:
            h = obj.intersect(ray)
            if h and h.t < min_t:
                hit = h
                min_t = h.t
        
        if not hit:
            # No hay intersección: retorna envmap o negro
            return self.sample_envmap_or_black(ray.direction)
        
        # Shading local (ambient + directional light simple)
        color = self.shade_hit(hit, ray)
        
        # Reflexión si es Metal
        if isinstance(hit.material, Metal):
            reflected_dir = ray.direction - 2 * np.dot(ray.direction, hit.normal) * hit.normal
            reflected_ray = Ray(hit.point, reflected_dir)
            reflected_color = self.trace(reflected_ray, scene, depth + 1, max_depth)
            color = tuple(np.array(color) * (1 - hit.material.reflectivity) + 
                         np.array(reflected_color) * hit.material.reflectivity)
        
        # Refracción si es Refractive
        elif isinstance(hit.material, Refractive):
            Kr, Kt, refracted_dir = hit.material.shade(hit.normal, ray.direction)
            if refracted_dir is not None:
                refracted_ray = Ray(hit.point, refracted_dir)
                refracted_color = self.trace(refracted_ray, scene, depth + 1, max_depth)
                reflected_dir = ray.direction - 2 * np.dot(ray.direction, hit.normal) * hit.normal
                reflected_ray = Ray(hit.point, reflected_dir)
                reflected_color = self.trace(reflected_ray, scene, depth + 1, max_depth)
                
                color = tuple(np.array(reflected_color) * Kr + 
                             np.array(refracted_color) * Kt * np.array(hit.material.tint))
        
        return color
    
    def shade_hit(self, hit, view_ray):
        """Retorna color de shading local (Lambert + directional light)."""
        # Luz directional simple
        light_dir = np.array([-0.3, -0.5, -0.4])
        light_dir = light_dir / np.linalg.norm(light_dir)
        light_color = (0.9, 0.9, 0.85)
        
        if isinstance(hit.material, Lambertian):
            color = hit.material.shade(hit.normal, light_dir, light_color)
        else:
            # Fallback: Lambert simple
            color = (0.8, 0.8, 0.8)
        
        return color
    
    def sample_envmap_or_black(self, direction):
        """Muestrea envmap o retorna negro."""
        if self.envmap:
            r, g, b = self.envmap.sample_equirect(direction)
            # NO clampear aquí - dejar que el tonemapping maneje HDR
            return (r, g, b)
        return (0.0, 0.0, 0.0)


def render(scene_dict, width, height, max_depth=3):
    """Renderiza escena retornando colorBuffer."""
    scene = scene_dict['objects']
    envmap = scene_dict['envmap']
    camera = scene_dict['camera']
    
    raytracer = Raytracer(envmap=envmap)
    
    # Construir base ortonormal de cámara
    cam_pos = np.array(camera['pos'])
    look_at = np.array(camera.get('look_at', (0, 0, 0)))
    up = np.array([0, 1, 0])
    
    # Forward (hacia donde mira la cámara)
    forward = look_at - cam_pos
    forward = forward / np.linalg.norm(forward)
    
    # Right (producto cruz up × forward)
    right = np.cross(up, forward)
    right = right / np.linalg.norm(right)
    
    # Up real (forward × right)
    up_real = np.cross(forward, right)
    up_real = up_real / np.linalg.norm(up_real)
    
    # Parámetros de frustum
    aspect = width / height
    fov_rad = math.radians(camera['fov'])
    h = math.tan(fov_rad / 2.0)
    w = aspect * h
    
    color_buffer = []
    for x in range(width):
        row = []
        for y in range(height):
            # NDC coordinates
            u = (x + 0.5) / width
            v = (y + 0.5) / height
            
            # Screen space
            px = (2 * u - 1) * w
            py = (1 - 2 * v) * h
            
            # Ray direction en espacio de cámara, luego transformar a world
            ray_dir = forward + px * right + py * up_real
            ray_dir = ray_dir / np.linalg.norm(ray_dir)
            
            ray = Ray(cam_pos, ray_dir)
            
            # Trace
            color = raytracer.trace(ray, scene, depth=0, max_depth=max_depth)
            row.append(color)
        
        color_buffer.append(row)
    
    return color_buffer
