
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


# Materiales estratégicos para demostración clara de algoritmos
mat_wall = Material([0.70, 0.70, 0.72], 'opaque')  # Gris neutro
mat_floor_pattern1 = Material([0.95, 0.95, 0.95], 'opaque')  # Blanco para patrón
mat_floor_pattern2 = Material([0.15, 0.15, 0.15], 'opaque')  # Negro para patrón
mat_disk = Material([1.0, 0.95, 0.70], 'opaque')

# Esferas de referencia para efectos de materiales
mat_ref_white = Material([0.95, 0.95, 0.95], 'opaque')  # Esfera blanca de referencia
mat_ref_black = Material([0.05, 0.05, 0.05], 'opaque')  # Esfera negra de referencia
mat_ref_color = Material([0.90, 0.20, 0.20], 'opaque')  # Esfera roja de referencia

# Cilindros con materiales optimizados para demostración
mat_cyl_opaque = Material([0.10, 0.80, 0.10], 'opaque')         # Verde puro opaco
mat_cyl_reflect = Material([0.90, 0.90, 0.95], 'reflective', reflectivity=0.85) # Plateado altamente reflectivo
mat_cyl_transp = Material([0.95, 0.95, 0.95], 'transparent', ior=1.60)          # Cristal claro con alta refracción

# Elipsoides con materiales optimizados para demostración  
mat_ell_opaque = Material([0.85, 0.10, 0.10], 'opaque')         # Rojo puro opaco
mat_ell_reflect = Material([0.95, 0.85, 0.10], 'reflective', reflectivity=0.80) # Dorado altamente reflectivo
mat_ell_transp = Material([0.10, 0.90, 0.95], 'transparent', ior=1.55)          # Cristal azul con alta refracción



scene = [
    # Paredes del cuarto
    Plane([0, 0, -10], [0, 0, 1], mat_wall),   # Pared trasera
    Plane([0, 3, 0], [0, -1, 0], mat_wall),    # Techo
    Plane([-5, 0, 0], [1, 0, 0], mat_wall),    # Pared izquierda
    Plane([5, 0, 0], [-1, 0, 0], mat_wall),    # Pared derecha
    
    # Piso con patrón de damero para mostrar reflejos y refracciones
    Plane([0, -3, 0], [0, 1, 0], mat_floor_pattern1),  # Base blanca
    
    # Esferas de referencia para demostrar efectos de materiales
    Sphere([0, -1.5, -6], 0.8, mat_ref_white),      # Esfera blanca central grande
    Sphere([-3, -2, -7], 0.5, mat_ref_black),       # Esfera negra izquierda
    Sphere([3, -2, -7], 0.5, mat_ref_color),        # Esfera roja derecha
    
    # CILINDROS: Posicionados estratégicamente para mostrar cada material
    # Cilindro OPACO (izquierda) - aislado para mostrar opacidad pura
    Cylinder([-3.5, -1.5, -4.5], [0, 1, 0], 0.6, 2.0, mat_cyl_opaque),
    
    # Cilindro REFLECTIVO (centro) - junto a esferas para mostrar reflejos claros
    Cylinder([0, -1.5, -4.0], [0, 1, 0], 0.6, 2.0, mat_cyl_reflect),
    
    # Cilindro TRANSPARENTE (derecha) - delante de esfera para mostrar refracción
    Cylinder([2.5, -1.5, -5.5], [0, 1, 0], 0.6, 2.0, mat_cyl_transp),
    
    # ELIPSOIDES: Elevados y distribuidos para mostrar cada material
    # Elipsoide OPACO (izquierda-atrás) - aislado para mostrar opacidad
    Ellipsoid([-2.5, 0.8, -3.5], [0.6, 0.4, 0.5], mat_ell_opaque),
    
    # Elipsoide REFLECTIVO (centro-elevado) - para mostrar reflejos del entorno
    Ellipsoid([0, 1.2, -3.0], [0.5, 0.7, 0.4], mat_ell_reflect),
    
    # Elipsoide TRANSPARENTE (derecha-adelante) - delante de elementos para mostrar refracción
    Ellipsoid([1.8, 0.8, -2.8], [0.4, 0.5, 0.6], mat_ell_transp),
    
    # Disco de luz principal
    Disk([0, 2.7, -7], [0, -1, 0], 1.1, mat_disk),
]

# Luz y cámara mejoradas

# Iluminación profesional optimizada para demostración de materiales
light_pos = np.array([1.5, 2.5, -5], dtype=float)    # Luz principal lateral-superior
light_color = np.array([1.2, 1.1, 1.0], dtype=float)  # Luz cálida intensa
light_pos2 = np.array([-2.0, 1.8, -4.0], dtype=float) # Luz de relleno lateral
light_color2 = np.array([0.6, 0.7, 0.9], dtype=float) # Luz fría de relleno
ambient = 0.08  # Muy bajo para máximo contraste
shadow_diffuse_factor = 0.25  # Sombras profundas
camera_pos = np.array([0, 0.5, 2.5], dtype=float)  # Cámara frontal para ver todos los efectos

def lambert_diffuse(normal, light_dir):
    return max(0, np.dot(normal, light_dir))

def phong_specular(normal, light_dir, view_dir, shininess=32):
    reflect_dir = 2 * np.dot(normal, light_dir) * normal - light_dir
    spec = max(0, np.dot(view_dir, reflect_dir)) ** shininess
    return spec


def tone_map(color):
    # ACES filmic approximation para preservar saturación y highlights
    a, b, c, d, e = 2.51, 0.03, 2.43, 0.59, 0.14
    x = np.clip(color, 0, None)
    mapped = (x * (a * x + b)) / (x * (c * x + d) + e)
    mapped = np.clip(mapped, 0, 1)
    gamma = 2.2
    mapped = np.power(mapped, 1.0 / gamma)
    return mapped

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
        if obj is not None and hit is not None and normal is not None:
            # Si el objeto es el disco de luz principal, hacerlo "emissive"
            if isinstance(obj, Disk) and np.allclose(obj.center, light_pos, atol=0.05):
                color = obj.material.color * 1.1
                color = tone_map(color)
                framebuffer[y, x] = (color * 255).astype(np.uint8)
                continue
            # Luz principal
            to_light = light_pos - hit
            light_distance = np.linalg.norm(to_light)
            to_light = to_light / light_distance
            # Atenuación suave tipo fotométrica
            attenuation = 1.0 / (1.0 + 0.07 * light_distance + 0.017 * light_distance * light_distance)
            view_dir = -ray_dir
            in_shadow = is_in_shadow(hit, light_pos, scene)
            if in_shadow:
                diff = shadow_diffuse_factor * attenuation
                spec = 0
            else:
                diff = lambert_diffuse(normal, to_light) * attenuation
                spec = phong_specular(normal, to_light, view_dir, shininess=48) * attenuation
            # Luz secundaria
            to_light2 = light_pos2 - hit
            light_distance2 = np.linalg.norm(to_light2)
            to_light2 = to_light2 / light_distance2
            attenuation2 = 1.0 / (1.2 + 0.09 * light_distance2 + 0.022 * light_distance2 * light_distance2)
            in_shadow2 = is_in_shadow(hit, light_pos2, scene)
            if in_shadow2:
                diff2 = shadow_diffuse_factor * attenuation2
                spec2 = 0
            else:
                diff2 = lambert_diffuse(normal, to_light2) * attenuation2
                spec2 = phong_specular(normal, to_light2, view_dir, shininess=36) * attenuation2
            base_color = ambient * obj.material.color \
                + diff * obj.material.color * light_color + spec * light_color * 0.35 \
                + diff2 * obj.material.color * light_color2 + spec2 * light_color2 * 0.20
            # Soporte para materiales reflectivos y transparentes
            final_color = base_color
            
            # Materiales reflectivos
            if hasattr(obj, 'material') and getattr(obj.material, 'reflectivity', 0) > 0:
                reflectivity = obj.material.reflectivity
                reflection_dir = get_reflection(ray_dir, normal)
                obj_r, hit_r, normal_r, t_r = trace_ray(hit + 1e-4 * reflection_dir, reflection_dir, scene)
                if obj_r is not None and hit_r is not None and normal_r is not None:
                    # Si el rayo reflejado pega en el disco de luz principal
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
                final_color = (1 - reflectivity) * base_color + reflectivity * color_r
            
            # Materiales transparentes (simplificado pero efectivo)
            if hasattr(obj, 'material') and obj.material.type == 'transparent':
                ior = getattr(obj.material, 'ior', 1.5)
                
                # Refracción simplificada: rayo ligeramente desviado
                refraction_dir = ray_dir + 0.1 * normal * (ior - 1.0) / ior
                refraction_dir = refraction_dir / np.linalg.norm(refraction_dir)
                
                obj_t, hit_t, normal_t, t_t = trace_ray(hit + 1e-4 * refraction_dir, refraction_dir, scene)
                if obj_t is not None and hit_t is not None and normal_t is not None:
                    to_light_t = light_pos - hit_t
                    light_distance_t = np.linalg.norm(to_light_t)
                    to_light_t = to_light_t / light_distance_t
                    in_shadow_t = is_in_shadow(hit_t, light_pos, scene)
                    if in_shadow_t:
                        diff_t = shadow_diffuse_factor
                    else:
                        diff_t = lambert_diffuse(normal_t, to_light_t)
                    color_t = ambient * obj_t.material.color + diff_t * obj_t.material.color * light_color
                    color_t = np.clip(color_t, 0, 1)
                else:
                    color_t = np.array([0.05, 0.05, 0.1])
                
                # Mezclar color base con color refractado (efecto de transparencia)
                transparency = 0.7  # 70% transparente
                final_color = (1 - transparency) * final_color + transparency * color_t * obj.material.color
            
            color = final_color
            color = tone_map(color)
            framebuffer[y, x] = (color * 255).astype(np.uint8)
        else:
            # Gradiente de fondo sutil
            bg = np.array([0.12, 0.12, 0.15]) + 0.03 * (y / HEIGHT)
            framebuffer[y, x] = (np.clip(bg, 0, 1) * 255).astype(np.uint8)

# Mostrar y guardar resultado
surf = pygame.surfarray.make_surface(np.transpose(framebuffer, (1,0,2)))
screen.blit(surf, (0,0))
pygame.display.flip()
pygame.image.save(surf, "lab7_room_render.bmp")
print("Imagen guardada como lab7_room_render.bmp")
pygame.time.wait(3500)
pygame.quit()
