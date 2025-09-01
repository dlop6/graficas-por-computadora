"""
Raytracer - Lab 5
Programa principal que crea una escena con múltiples esferas y diferentes materiales
"""

from raytracer import Raytracer
from figures import Sphere
from material import Material
from lights import Light
import numpy as np

def create_materials():
    """
    Crea diferentes materiales para las esferas
    """
    # Material rojo brillante (metal rojo)
    red_metal = Material(
        diffuse_color=[0.7, 0.1, 0.1],
        specular_color=[1.0, 0.8, 0.8],
        ambient_color=[0.1, 0.02, 0.02],
        shininess=100
    )
    
    # Material azul metálico
    blue_metal = Material(
        diffuse_color=[0.1, 0.1, 0.7],
        specular_color=[0.8, 0.8, 1.0],
        ambient_color=[0.02, 0.02, 0.1],
        shininess=80
    )
    
    # Material verde mate
    green_matte = Material(
        diffuse_color=[0.2, 0.8, 0.2],
        specular_color=[0.3, 0.5, 0.3],
        ambient_color=[0.05, 0.1, 0.05],
        shininess=20
    )
    
    # Material dorado
    gold = Material(
        diffuse_color=[0.8, 0.6, 0.2],
        specular_color=[1.0, 0.9, 0.6],
        ambient_color=[0.1, 0.08, 0.02],
        shininess=120
    )
    
    # Material plateado
    silver = Material(
        diffuse_color=[0.6, 0.6, 0.6],
        specular_color=[0.9, 0.9, 0.9],
        ambient_color=[0.1, 0.1, 0.1],
        shininess=150
    )
    
    return red_metal, blue_metal, green_matte, gold, silver

def create_scene():
    """
    Crea la escena principal con múltiples esferas
    """
    # Crear el raytracer
    width = 800
    height = 600
    raytracer = Raytracer(width, height)
    
    # Configurar cámara
    raytracer.set_camera([0, 0, 0])
    
    # Configurar color de fondo (gradiente azul oscuro)
    raytracer.set_background_color([0.05, 0.05, 0.2])
    
    # Crear materiales
    red_metal, blue_metal, green_matte, gold, silver = create_materials()
    
    # Crear esferas con diferentes posiciones y tamaños
    
    # Esfera central grande (dorada)
    sphere_center = Sphere([0, 0, -8], 1.5, gold)
    raytracer.add_object(sphere_center)
    
    # Esferas alrededor formando un patrón
    
    # Esfera izquierda (roja)
    sphere_left = Sphere([-3, 0, -6], 1.0, red_metal)
    raytracer.add_object(sphere_left)
    
    # Esfera derecha (azul)
    sphere_right = Sphere([3, 0, -6], 1.0, blue_metal)
    raytracer.add_object(sphere_right)
    
    # Esfera superior (verde)
    sphere_top = Sphere([0, 3, -7], 0.8, green_matte)
    raytracer.add_object(sphere_top)
    
    # Esfera inferior (plateada)
    sphere_bottom = Sphere([0, -2.5, -5], 0.8, silver)
    raytracer.add_object(sphere_bottom)
    
    # Esferas pequeñas adicionales
    sphere_small1 = Sphere([-1.5, 1.5, -4], 0.5, blue_metal)
    raytracer.add_object(sphere_small1)
    
    sphere_small2 = Sphere([1.5, 1.5, -4], 0.5, red_metal)
    raytracer.add_object(sphere_small2)
    
    sphere_small3 = Sphere([-2, -1, -9], 0.6, green_matte)
    raytracer.add_object(sphere_small3)
    
    sphere_small4 = Sphere([2, -1, -9], 0.6, silver)
    raytracer.add_object(sphere_small4)
    
    return raytracer

def create_lighting(raytracer):
    """
    Crea un sistema de iluminación interesante
    """
    # Luz principal (blanca, desde arriba y a la izquierda)
    main_light = Light([5, 8, 2], [1.0, 1.0, 1.0], 1.2)
    raytracer.add_light(main_light)
    
    # Luz de relleno (azul suave, desde la derecha)
    fill_light = Light([-4, 3, -1], [0.6, 0.7, 1.0], 0.6)
    raytracer.add_light(fill_light)
    
    # Luz trasera (cálida, para dar profundidad)
    back_light = Light([0, -2, -15], [1.0, 0.8, 0.6], 0.4)
    raytracer.add_light(back_light)

def main():
    """
    Función principal
    """
    print("=== RAYTRACER LAB 5 ===")
    print("Creando escena con múltiples esferas y materiales...")
    
    # Crear la escena
    raytracer = create_scene()
    
    # Configurar iluminación
    create_lighting(raytracer)
    
    print(f"Escena creada con {len(raytracer.objects)} esferas y {len(raytracer.lights)} luces")
    
    # Renderizar
    print("\nIniciando renderizado...")
    raytracer.render()
    
    # Guardar imagen en la carpeta Lab 5
    import os
    lab5_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(lab5_path, "raytraced_spheres.bmp")
    raytracer.save_image(filename)
    
    print(f"\n✅ Raytracing completado!")
    print(f"📁 Imagen guardada como: {filename}")
    print("🎨 La imagen muestra:")
    print("   - Esfera central dorada grande")
    print("   - Esferas rojas, azules, verdes y plateadas")
    print("   - Modelo de iluminación Phong")
    print("   - Múltiples fuentes de luz")
    print("   - Ray intersect algorithm implementado")
    print("   - Diferentes materiales con propiedades únicas")

if __name__ == "__main__":
    main()
