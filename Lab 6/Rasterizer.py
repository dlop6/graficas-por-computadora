import pygame
import numpy as np

WIDTH = 800
HEIGHT = 600

# Inicializar Pygame y la ventana
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Framebuffer como array numpy para manipulación directa
framebuffer = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

# Color de fondo (negro)
def clear(color=(0,0,0)):
    framebuffer[:,:,:] = color

# Mostrar el framebuffer en la ventana
def draw_framebuffer():
    surf = pygame.surfarray.make_surface(np.transpose(framebuffer, (1,0,2)))
    screen.blit(surf, (0,0))
    pygame.display.flip()

# --- Fase 2: Definición de Material y Esfera ---

class Material:
    def __init__(self, color, mat_type='opaque', ior=1.0, reflectivity=0.0):
        self.color = np.array(color, dtype=float)  # RGB [0,1]
        self.type = mat_type  # 'opaque', 'reflective', 'transparent'
        self.ior = ior        # Índice de refracción (solo para transparentes)
        self.reflectivity = reflectivity  # 0=mate, 1=espejo

class Sphere:
    def __init__(self, center, radius, material):
        self.center = np.array(center, dtype=float)
        self.radius = radius
        self.material = material

    def intersect(self, ray_origin, ray_dir):
        # Intersección rayo-esfera: retorna distancia o None
        L = self.center - ray_origin
        tca = np.dot(L, ray_dir)
        d2 = np.dot(L, L) - tca * tca
        r2 = self.radius * self.radius
        if d2 > r2:
            return None
        thc = np.sqrt(r2 - d2)
        t0 = tca - thc
        t1 = tca + thc
        if t0 > 0:
            return t0
        if t1 > 0:
            return t1
        return None

    def get_normal(self, point):
        return (point - self.center) / self.radius

# --- Fase 3: Raytracer básico ---

def trace_ray(ray_origin, ray_dir, spheres):
    closest_t = float('inf')
    hit_sphere = None
    for sphere in spheres:
        t = sphere.intersect(ray_origin, ray_dir)
        if t is not None and t < closest_t:
            closest_t = t
            hit_sphere = sphere
    if hit_sphere is not None:
        hit_point = ray_origin + closest_t * ray_dir
        normal = hit_sphere.get_normal(hit_point)
        return hit_sphere, hit_point, normal, closest_t
    return None, None, None, None

# --- Fase 4: Iluminación difusa y ambiente para materiales opacos ---

# Luz puntual sencilla
light_pos = np.array([5, 5, -3], dtype=float)
light_color = np.array([1, 1, 1], dtype=float)
ambient = 0.15

# --- Fase 5: Carga de Environment Map y materiales reflectivos ---

import struct

def load_hdr(filename):
    """Cargar HDR mejorado con soporte para múltiples formatos"""
    try:
        # Intentar cargar con OpenCV si está disponible
        import cv2
        img = cv2.imread(filename, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            print(f"HDR cargado exitosamente: {filename}")
            return img.astype(np.float32)
    except ImportError:
        print("OpenCV no disponible, usando environment map procedural")
    except Exception as e:
        print(f"Error cargando HDR {filename}: {e}")
    
    # Fallback mejorado
    print(f"Usando environment map procedural en lugar de {filename}")
    return create_procedural_skybox()

def create_procedural_skybox():
    """Crear un skybox procedural más realista con sol y gradientes"""
    size = 512
    env_map = np.zeros((size, size, 3))
    
    for i in range(size):
        for j in range(size):
            # Coordenadas normalizadas [-1, 1]
            u = (j / size) * 2 - 1
            v = (i / size) * 2 - 1
            
            # Convertir a coordenadas esféricas
            phi = np.arctan2(v, u)  # Ángulo azimutal
            theta = np.pi * np.sqrt(u*u + v*v)  # Ángulo polar
            
            # Simular cielo realista con gradiente vertical
            if theta < np.pi/2:  # Hemisferio superior (cielo)
                # Gradiente del cielo: más brillante en horizonte, más oscuro en cenit
                sky_intensity = 0.3 + 0.7 * (1.0 - theta / (np.pi/2))
                base_sky = np.array([0.4, 0.6, 1.0]) * sky_intensity
                
                # Añadir "sol" brillante
                sun_direction = np.array([0.5, 0.6, 0.6])  # Posición del sol
                sun_direction = sun_direction / np.linalg.norm(sun_direction)
                
                # Dirección del rayo para este pixel
                ray_dir = np.array([np.sin(theta) * np.cos(phi), 
                                  np.cos(theta), 
                                  np.sin(theta) * np.sin(phi)])
                
                sun_dot = np.dot(sun_direction, ray_dir)
                
                if sun_dot > 0.998:  # Núcleo del sol
                    env_map[i, j] = np.array([3.0, 2.5, 2.0])  # Muy brillante y cálido
                elif sun_dot > 0.995:  # Halo interior del sol
                    env_map[i, j] = np.array([2.0, 1.8, 1.5]) * (sun_dot - 0.995) / 0.003
                elif sun_dot > 0.98:  # Halo exterior del sol
                    glow = (sun_dot - 0.98) / 0.015
                    env_map[i, j] = base_sky + np.array([1.5, 1.2, 0.8]) * glow
                else:
                    env_map[i, j] = base_sky
                    
            else:  # Hemisferio inferior (suelo/horizonte)
                # Gradiente del suelo
                ground_intensity = 0.2 + 0.1 * (1.0 - (theta - np.pi/2) / (np.pi/2))
                env_map[i, j] = np.array([0.6, 0.5, 0.4]) * ground_intensity
    
    return env_map

def sample_environment(direction, env_map):
    # Convertir dirección 3D a coordenadas UV esféricas
    x, y, z = direction
    u = 0.5 + np.arctan2(x, z) / (2 * np.pi)
    v = 0.5 - np.arcsin(y) / np.pi
    u = np.clip(u, 0, 0.999)
    v = np.clip(v, 0, 0.999)
    
    h, w = env_map.shape[:2]
    i = int(v * h)
    j = int(u * w)
    return env_map[i, j]

def reflect_vector(incident, normal):
    return incident - 2 * np.dot(incident, normal) * normal

# Cargar environment map
env_map = load_hdr("rogland_clear_night_4k.hdr")

# --- Fase 6: Materiales transparentes con refracción y Fresnel ---

from refractionFunctions import refractVector, totalInternalReflection, fresnel

def lambert_diffuse(normal, light_dir):
    return max(0, np.dot(normal, light_dir))

# --- Fase 8: Escena final con 6 esferas (2 opacas, 2 reflectivas, 2 transparentes) ---

spheres = [
    # 2 Esferas opacas con diferentes colores (más separadas)
    Sphere(center=[-4.5, 1.5, -8], radius=1.2, 
        material=Material([0.8, 0.2, 0.2], 'opaque')),  # Roja
    Sphere(center=[4.5, -1.5, -8], radius=1.0, 
        material=Material([0.2, 0.8, 0.3], 'opaque')),  # Verde

    # 2 Esferas reflectivas con diferentes niveles de reflectividad (más separadas)
    Sphere(center=[-2, -2.5, -6], radius=0.8, 
        material=Material([0.9, 0.9, 0.9], 'reflective', reflectivity=0.9)),  # Casi espejo
    Sphere(center=[2, 2.5, -10], radius=1.1, 
        material=Material([0.8, 0.7, 0.5], 'reflective', reflectivity=0.7)),  # Reflectiva dorada

    # 2 Esferas transparentes con diferentes índices de refracción (más separadas)
    Sphere(center=[0, 0, -5.5], radius=0.9, 
        material=Material([0.9, 0.95, 1.0], 'transparent', ior=1.5)),  # Vidrio
    Sphere(center=[-3.5, 3, -12], radius=1.3, 
        material=Material([1.0, 0.9, 0.9], 'transparent', ior=2.4))   # Diamante (alto IOR)
]

# Cámara sencilla
camera_pos = np.array([0,0,0], dtype=float)

# --- Fase 9: Renderizado final optimizado ---

print("Iniciando renderizado de 6 esferas...")

# Render loop mejorado con indicador de progreso
for y in range(HEIGHT):
    if y % 50 == 0:  # Mostrar progreso cada 50 líneas
        print(f"Renderizando línea {y}/{HEIGHT}")
    
    for x in range(WIDTH):
        # Normalizar coordenadas de pixel a [-1,1]
        px = (2 * (x + 0.5) / WIDTH - 1) * (WIDTH/HEIGHT)
        py = 1 - 2 * (y + 0.5) / HEIGHT
        ray_dir = np.array([px, py, -1])
        ray_dir = ray_dir / np.linalg.norm(ray_dir)
        
        sphere, hit, normal, t = trace_ray(camera_pos, ray_dir, spheres)
        
        if sphere is not None:
            if sphere.material.type == 'opaque':
                # Iluminación difusa + ambiente mejorada
                to_light = light_pos - hit
                light_distance = np.linalg.norm(to_light)
                to_light = to_light / light_distance
                
                # Atenuación por distancia
                attenuation = 1.0 / (1.0 + 0.1 * light_distance + 0.01 * light_distance * light_distance)
                
                diff = lambert_diffuse(normal, to_light) * attenuation
                color = ambient * sphere.material.color + diff * sphere.material.color * light_color
                color = np.clip(color, 0, 1)
                framebuffer[y, x] = (color * 255).astype(np.uint8)
                
            elif sphere.material.type == 'reflective':
                # Material reflectivo: usar environment map
                reflected_ray = reflect_vector(ray_dir, normal)
                env_color = sample_environment(reflected_ray, env_map)
                # Mezclar con color base del material
                color = sphere.material.reflectivity * env_color + (1 - sphere.material.reflectivity) * sphere.material.color
                color = np.clip(color, 0, 1)
                framebuffer[y, x] = (color * 255).astype(np.uint8)
                
            elif sphere.material.type == 'transparent':
                # Material transparente: refracción + reflexión (Fresnel)
                n1 = 1.0  # Aire
                n2 = sphere.material.ior  # Material
                
                # Verificar reflexión total interna
                if totalInternalReflection(normal, ray_dir, n1, n2):
                    # Solo reflexión
                    reflected_ray = reflect_vector(ray_dir, normal)
                    color = sample_environment(reflected_ray, env_map)
                else:
                    # Calcular Fresnel para mezclar reflexión y refracción
                    kr, kt = fresnel(normal, ray_dir, n1, n2)
                    
                    # Componente reflejada
                    reflected_ray = reflect_vector(ray_dir, normal)
                    reflected_color = sample_environment(reflected_ray, env_map)
                    
                    # Componente refractada
                    refracted_ray = refractVector(normal, ray_dir, n1, n2)
                    refracted_color = sample_environment(refracted_ray, env_map)
                    
                    # Combinar con coeficientes de Fresnel
                    color = kr * reflected_color + kt * refracted_color
                
                # Aplicar tinte del material
                color = color * sphere.material.color
                color = np.clip(color, 0, 1)
                framebuffer[y, x] = (color * 255).astype(np.uint8)
            else:
                framebuffer[y, x] = (sphere.material.color * 255).astype(np.uint8)
        else:
            # Fondo: samplear environment map
            env_color = sample_environment(ray_dir, env_map)
            framebuffer[y, x] = (np.clip(env_color, 0, 1) * 255).astype(np.uint8)

print("Renderizado completo!")

# Guardar imagen como BMP
def save_as_bmp(filename="lab6_render.bmp"):
    # Convertir framebuffer a superficie de pygame y guardar
    surf = pygame.surfarray.make_surface(np.transpose(framebuffer, (1,0,2)))
    pygame.image.save(surf, filename)
    print(f"Imagen guardada como: {filename}")

# Mostrar resultado y guardar
draw_framebuffer()
save_as_bmp("lab6_6_spheres.bmp")
pygame.time.wait(3000)  # Mostrar resultado por 3 segundos

# Loop principal vacío (por ahora)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clear((10,10,30))  # Fondo azul oscuro
    draw_framebuffer()
    clock.tick(60)

pygame.quit()
