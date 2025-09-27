

# Render loop

# --- INICIO DE CÓDIGO MEJORADO Y EXPLÍCITO ---
import numpy as np
import pygame
from gl import Material, Sphere, Plane, Disk, Triangle, Cube, Cylinder, Ellipsoid

# Configuración de la imagen
WIDTH = 800
HEIGHT = 600

# Inicializar Pygame y framebuffer
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
framebuffer = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

# Definir materiales (colores vivos y reflectividad)
mat_wall = Material([0.95, 0.95, 0.95], 'opaque')
mat_floor = Material([0.8, 0.8, 0.85], 'reflective', reflectivity=0.18)
mat_cube1 = Material([0.1, 0.5, 1.0], 'reflective', reflectivity=0.7)
mat_cube2 = Material([1.0, 0.2, 0.2], 'reflective', reflectivity=0.55)
mat_triangle = Material([0.85, 0.85, 0.85], 'reflective', reflectivity=0.85)
mat_disk = Material([1.0, 1.0, 0.7], 'opaque')
# Materiales para cilindros
mat_cyl_opaque = Material([0.2, 0.8, 0.3], 'opaque')
mat_cyl_reflect = Material([0.9, 0.7, 0.1], 'reflective', reflectivity=0.7)
mat_cyl_transp = Material([0.3, 0.7, 1.0], 'transparent', ior=1.4)
# Materiales para elipsoides
mat_ell_opaque = Material([0.8, 0.2, 0.7], 'opaque')
mat_ell_reflect = Material([0.2, 0.9, 0.9], 'reflective', reflectivity=0.7)
mat_ell_transp = Material([0.9, 0.9, 0.3], 'transparent', ior=1.3)

# Crear figuras del cuarto (objetos centrados y visibles, mejor composición)
scene = [
    # Pared trasera
    Plane([0, 0, -10], [0, 0, 1], mat_wall),
    # Piso
    Plane([0, -3, 0], [0, 1, 0], mat_floor),
    # Techo
    Plane([0, 3, 0], [0, -1, 0], mat_wall),
    # Pared izquierda
    Plane([-5, 0, 0], [1, 0, 0], mat_wall),
    # Pared derecha
    Plane([5, 0, 0], [-1, 0, 0], mat_wall),
    # Cubos
    Cube([-2.2, -2.2, -7.5], 1.5, mat_cube1),
    Cube([2.2, -2.0, -6.5], 1.2, mat_cube2),
    # Triángulo (más cerca del centro)
    Triangle([0, -2.5, -5.2], [1.5, -1, -5.2], [-1.5, -1, -5.2], mat_triangle),
    # Disco (luz)
    Disk([0, 2.7, -7], [0, -1, 0], 1.1, mat_disk),
    # Cilindros
    Cylinder([-1.5, -2.5, -8], [0, 1, 0], 0.5, 2.0, mat_cyl_opaque),
    Cylinder([0.5, -2.5, -6.5], [0, 1, 1], 0.4, 1.5, mat_cyl_reflect),
    Cylinder([2.0, -2.5, -8.5], [1, 1, 0], 0.3, 2.2, mat_cyl_transp),
    # Elipsoides (posiciones y tamaños ajustados para mejor visibilidad)
    Ellipsoid([-2.5, 0.4, -3.8], [0.5, 0.3, 0.3], mat_ell_opaque),      # Más cerca, arriba, izquierda
    Ellipsoid([0.0, -1.2, -4.2], [0.6, 0.4, 0.7], mat_ell_reflect),     # Más cerca y abajo, centro
    Ellipsoid([2.5, 0.0, -3.7], [0.4, 0.6, 0.4], mat_ell_transp),       # Más cerca, medio, derecha
]

# Luz y cámara mejoradas
light_pos = np.array([0, 2.7, -7], dtype=float)  # Coincide con el disco
light_color = np.array([1.8, 1.7, 1.3], dtype=float)  # Luz intensa y cálida
ambient = 0.22  # Luz ambiental balanceada
shadow_diffuse_factor = 0.13  # Sombra más marcada
camera_pos = np.array([0, 0.5, 2.5], dtype=float)  # Más cerca y centrada

def lambert_diffuse(normal, light_dir):
    return max(0, np.dot(normal, light_dir))

def phong_specular(normal, light_dir, view_dir, shininess=32):
    reflect_dir = 2 * np.dot(normal, light_dir) * normal - light_dir
    spec = max(0, np.dot(view_dir, reflect_dir)) ** shininess
    return spec

def trace_ray(ray_origin, ray_dir, objects):
    closest_t = float('inf')
    hit_obj = None
    for obj in objects:
        t = obj.intersect(ray_origin, ray_dir)
        if t is not None and t < closest_t:
            closest_t = t
            hit_obj = obj
    if hit_obj is not None:
        hit_point = ray_origin + closest_t * ray_dir
        normal = hit_obj.get_normal(hit_point)
        return hit_obj, hit_point, normal, closest_t
    return None, None, None, None

def get_reflection(ray_dir, normal):
    return ray_dir - 2 * np.dot(ray_dir, normal) * normal

def is_in_shadow(point, light_pos, scene):
    shadow_dir = light_pos - point
    shadow_dist = np.linalg.norm(shadow_dir)
    shadow_dir = shadow_dir / shadow_dist
    shadow_origin = point + 1e-4 * shadow_dir
    for obj in scene:
        t = obj.intersect(shadow_origin, shadow_dir)
        if t is not None and t < shadow_dist:
            return True
    return False

# Render loop
print("Renderizando escena del cuarto...")
for y in range(HEIGHT):
    if y % 50 == 0:
        print(f"Línea {y}/{HEIGHT}")
    for x in range(WIDTH):
        px = (2 * (x + 0.5) / WIDTH - 1) * (WIDTH/HEIGHT)
        py = 1 - 2 * (y + 0.5) / HEIGHT
        ray_dir = np.array([px, py, -1])
        ray_dir = ray_dir / np.linalg.norm(ray_dir)
        obj, hit, normal, t = trace_ray(camera_pos, ray_dir, scene)
        if obj is not None:
            # Si el objeto es el disco de luz, hacerlo "emissive" pero sin saturar
            if isinstance(obj, Disk) and np.allclose(obj.center, light_pos, atol=0.05):
                color = obj.material.color * 1.5  # Emisión más fuerte
                color = np.clip(color, 0, 1)
                framebuffer[y, x] = (color * 255).astype(np.uint8)
                continue
            to_light = light_pos - hit
            light_distance = np.linalg.norm(to_light)
            to_light = to_light / light_distance
            # Atenuación menos agresiva
            attenuation = 1.0 / (0.4 + 0.04 * light_distance + 0.008 * light_distance * light_distance)
            view_dir = -ray_dir
            in_shadow = is_in_shadow(hit, light_pos, scene)
            if in_shadow:
                diff = shadow_diffuse_factor * attenuation
                spec = 0
            else:
                diff = lambert_diffuse(normal, to_light) * attenuation
                spec = phong_specular(normal, to_light, view_dir, shininess=48) * attenuation
            base_color = ambient * obj.material.color + diff * obj.material.color * light_color + spec * light_color * 0.5
            # Soporte para materiales reflectivos
            if hasattr(obj, 'material') and getattr(obj.material, 'reflectivity', 0) > 0:
                reflectivity = obj.material.reflectivity
                reflection_dir = get_reflection(ray_dir, normal)
                obj_r, hit_r, normal_r, t_r = trace_ray(hit + 1e-4 * reflection_dir, reflection_dir, scene)
                if obj_r is not None:
                    # Si el rayo reflejado pega en el disco de luz, hacerlo "emissive"
                    if isinstance(obj_r, Disk) and np.allclose(obj_r.center, light_pos, atol=0.05):
                        color_r = obj_r.material.color * 2.5
                    else:
                        to_light_r = light_pos - hit_r
                        light_distance_r = np.linalg.norm(to_light_r)
                        to_light_r = to_light_r / light_distance_r
                        in_shadow_r = is_in_shadow(hit_r, light_pos, scene)
                        if in_shadow_r:
                            diff_r = shadow_diffuse_factor
                            spec_r = 0
                        else:
                            diff_r = lambert_diffuse(normal_r, to_light_r)
                            spec_r = phong_specular(normal_r, to_light_r, -reflection_dir, shininess=48)
                        color_r = ambient * obj_r.material.color + diff_r * obj_r.material.color * light_color + spec_r * light_color * 0.5
                    color_r = np.clip(color_r, 0, 1)
                else:
                    color_r = np.array([0.1, 0.1, 0.15])
                color = (1 - reflectivity) * base_color + reflectivity * color_r
            else:
                color = base_color
            color = np.clip(color, 0, 1)
            framebuffer[y, x] = (color * 255).astype(np.uint8)
        else:
            framebuffer[y, x] = (np.array([0.18, 0.18, 0.22]) * 255).astype(np.uint8)

# Mostrar y guardar resultado
surf = pygame.surfarray.make_surface(np.transpose(framebuffer, (1,0,2)))
screen.blit(surf, (0,0))
pygame.display.flip()
pygame.image.save(surf, "lab7_room_render.bmp")
print("Imagen guardada como lab7_room_render.bmp")
pygame.time.wait(3500)
pygame.quit()
# --- FIN DE CÓDIGO MEJORADO ---
