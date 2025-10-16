import numpy as np
import math
from primitives import Ray, Sphere, Plane, Cylinder, HitInfo
from materials import Lambertian, Metal, Refractive, TexturedLambert
from HDRTexture import HDRTexture
from lighting import AmbientLight, DirectionalLight, PointLight, SpotLight


class Raytracer:
    """Motor de raytracing con soporte para iluminación múltiple."""
    
    def __init__(self, envmap=None, lights=None, ambient=None):
        self.envmap = envmap
        self.lights = lights if lights is not None else []
        self.ambient = ambient if ambient is not None else AmbientLight()
    
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
        
        # Shading local con iluminación múltiple
        color = self.shade_hit(hit, ray, scene)
        
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
            
            # Calcular reflexión
            reflected_dir = ray.direction - 2 * np.dot(ray.direction, hit.normal) * hit.normal
            reflected_ray = Ray(hit.point, reflected_dir)
            reflected_color = self.trace(reflected_ray, scene, depth + 1, max_depth)
            
            if refracted_dir is not None and not np.any(np.isnan(refracted_dir)):
                # Hay refracción válida
                refracted_ray = Ray(hit.point, refracted_dir)
                refracted_color = self.trace(refracted_ray, scene, depth + 1, max_depth)
                
                color = tuple(np.array(reflected_color) * Kr + 
                             np.array(refracted_color) * Kt * np.array(hit.material.tint))
            else:
                # Reflexión total interna - solo reflexión
                color = tuple(np.array(reflected_color))
        
        return color
    
    def shade_hit(self, hit, view_ray, scene):
        """Calcula shading local con iluminación múltiple.
        
        Args:
            hit: HitInfo con información de intersección
            view_ray: Rayo desde la cámara
            scene: Lista de objetos (para shadow rays)
        
        Returns:
            Color RGB tuple (0-1 range)
        """
        # Iniciar con luz ambiental
        ambient_color = np.array(self.ambient.get_color())
        
        # Color base del material
        if isinstance(hit.material, Lambertian):
            base_color = np.array(hit.material.color)
        elif isinstance(hit.material, TexturedLambert):
            # Para texturas, necesitamos UV
            base_color = np.array(hit.material.tex.getColor(hit.uv[0], hit.uv[1]) or (0.8, 0.8, 0.8))
        else:
            base_color = np.array([0.8, 0.8, 0.8])
        
        # Acumular contribución de luz ambiental
        accumulated_color = base_color * ambient_color
        
        # Calcular contribución de cada luz
        for light in self.lights:
            # Obtener dirección y intensidad de la luz
            light_dir = light.get_light_direction(hit.point)
            light_intensity = light.get_intensity(hit.point)
            
            if light_intensity < 1e-6:
                continue
            
            # Shadow ray: verificar si hay objetos bloqueando la luz
            shadow_ray_origin = hit.point + hit.normal * 0.001  # Offset para evitar self-intersection
            shadow_ray = Ray(shadow_ray_origin, light_dir)
            
            in_shadow = False
            
            # Para luces infinitas (directional), no hay límite de distancia
            if isinstance(light, DirectionalLight):
                for obj in scene:
                    shadow_hit = obj.intersect(shadow_ray)
                    if shadow_hit and shadow_hit.t > 0.001:
                        in_shadow = True
                        break
            else:
                # Para point/spot lights, solo verificar hasta la distancia de la luz
                light_distance = light.get_distance_to_light(hit.point)
                for obj in scene:
                    shadow_hit = obj.intersect(shadow_ray)
                    if shadow_hit and 0.001 < shadow_hit.t < light_distance:
                        in_shadow = True
                        break
            
            if in_shadow:
                continue
            
            # Calcular shading según el tipo de material
            light_color = light.get_color()
            
            if isinstance(hit.material, Lambertian):
                # Lambertian diffuse
                ndotl = max(0.0, np.dot(hit.normal, light_dir))
                diffuse = base_color * ndotl * np.array(light_color) * light_intensity
                accumulated_color += diffuse
            
            elif isinstance(hit.material, TexturedLambert):
                # Textured Lambertian
                ndotl = max(0.0, np.dot(hit.normal, light_dir))
                diffuse = base_color * ndotl * np.array(light_color) * light_intensity
                accumulated_color += diffuse
            
            elif isinstance(hit.material, Metal):
                # Metal: local shading (diffuse + specular)
                view_dir = -view_ray.direction
                ndotl = max(0.0, np.dot(hit.normal, light_dir))
                
                # Diffuse component (reducido para metales)
                diffuse = np.array(hit.material.color) * ndotl * 0.3
                
                # Specular (Blinn-Phong)
                h = view_dir + light_dir
                h_len = np.linalg.norm(h)
                if h_len > 1e-10:
                    h = h / h_len
                    ndoth = max(0.0, np.dot(hit.normal, h))
                else:
                    ndoth = 0.0
                specular = np.array(light_color) * (ndoth ** hit.material.shininess)
                
                accumulated_color += (diffuse + specular) * light_intensity
            
            # Refractive materials usan principalmente luz ambiental + reflexión/refracción
            # (ya manejado en trace())
        
        # Clamp a [0, 1]
        return tuple(np.clip(accumulated_color, 0.0, 1.0))
    
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
    envmap = scene_dict.get('envmap', None)
    camera = scene_dict['camera']
    lights = scene_dict.get('lights', [])
    ambient = scene_dict.get('ambient', None)
    
    raytracer = Raytracer(envmap=envmap, lights=lights, ambient=ambient)
    
    # Construir base ortonormal de cámara
    cam_pos = np.array(camera['pos'])
    look_at = np.array(camera.get('look_at', (0, 0, 0)))
    up = np.array([0, 1, 0])
    
    # Forward (hacia donde mira la cámara)
    forward = look_at - cam_pos
    forward_len = np.linalg.norm(forward)
    if forward_len < 1e-10:
        forward = np.array([0, 0, -1], dtype=float)
    else:
        forward = forward / forward_len
    
    # Right (producto cruz forward × up para right-handed system)
    right = np.cross(forward, up)
    right_len = np.linalg.norm(right)
    if right_len < 1e-10:
        right = np.array([1, 0, 0], dtype=float)
    else:
        right = right / right_len
    
    # Up real (right × forward para mantener right-handed system)
    up_real = np.cross(right, forward)
    up_real_len = np.linalg.norm(up_real)
    if up_real_len < 1e-10:
        up_real = np.array([0, 1, 0], dtype=float)
    else:
        up_real = up_real / up_real_len
    
    # Parámetros de frustum
    aspect = width / height
    fov_rad = math.radians(camera['fov'])
    h = math.tan(fov_rad / 2.0)
    w = aspect * h
    
    import time
    color_buffer = []
    start_time = time.time()
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
        # Log de progreso cada 10 filas
        if (x+1) % 10 == 0 or (x+1) == width:
            elapsed = time.time() - start_time
            percent = int(100 * (x+1) / width)
            rows_left = width - (x+1)
            if x > 0:
                avg_row_time = elapsed / (x+1)
                eta = avg_row_time * rows_left
            else:
                eta = 0
            print(f"[Render] {x+1}/{width} filas ({percent}%) - {elapsed:.1f}s transcurridos - ETA: {eta:.1f}s")
    return color_buffer
