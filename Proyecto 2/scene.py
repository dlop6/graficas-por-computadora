import os
from primitives import Sphere, Plane, Cylinder
from materials import Lambertian, Metal, Refractive
from HDRTexture import HDRTexture


def build_scene():
    """Construye una escena simple con 3 esferas, 1 plano y envmap."""
    
    # Cargar envmap
    base_dir = os.path.dirname(__file__)
    assets_dir = os.path.join(base_dir, 'assets')
    hdr_files = [f for f in os.listdir(assets_dir) if f.lower().endswith('.hdr')]
    envmap = None
    if hdr_files:
        # Preferir autumn_field_4k.hdr si existe
        preferred = 'autumn_field_4k.hdr'
        if preferred in hdr_files:
            envmap_path = os.path.join(assets_dir, preferred)
        else:
            envmap_path = os.path.join(assets_dir, hdr_files[0])
        envmap = HDRTexture(envmap_path)
        print(f'Envmap cargado: {envmap_path}')
    
    # Materiales
    mat_red_lambert = Lambertian((0.8, 0.2, 0.2), ambient=0.15)
    mat_blue_lambert = Lambertian((0.2, 0.5, 0.9), ambient=0.15)
    mat_metal = Metal((0.9, 0.9, 0.95), reflectivity=0.8, shininess=64)
    mat_glass = Refractive(ior=1.5, tint=(0.95, 0.98, 1.0), transparency=0.9)
    mat_ground = Lambertian((0.6, 0.6, 0.6), ambient=0.1)
    
    # Objetos
    objects = [
        # Esfera roja (izquierda)
        Sphere((-0.7, 0.3, -1.0), 0.3, mat_red_lambert),
        
        # Esfera azul (centro)
        Sphere((0.0, 0.3, -1.2), 0.35, mat_blue_lambert),
        
        # Esfera metálica (derecha)
        Sphere((0.7, 0.4, -0.8), 0.35, mat_metal),
        
    # Plano (suelo) -- bajado a y = -0.5 para no bloquear el cielo
    Plane((0, -0.5, -1.5), (0, 1, 0), mat_ground, scale=5.0),
    ]
    
    # Empaquetar escena
    return {
        'objects': objects,
        'envmap': envmap,
        'camera': {
            'pos': (0, 0.8, 3.5),
            'look_at': (0, 0.5, 0),
            'fov': 45,
        }
    }
