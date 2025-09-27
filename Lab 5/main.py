from raytracer import Raytracer
from figures import Sphere
from material import Material
from lights import Light
import numpy as np
import os

def setup_materials():
    # Materiales básicos para las esferas
    red_material = Material([0.7, 0.1, 0.1], [1.0, 0.8, 0.8], [0.1, 0.02, 0.02], 100)
    blue_material = Material([0.1, 0.1, 0.7], [0.8, 0.8, 1.0], [0.02, 0.02, 0.1], 80)
    green_material = Material([0.2, 0.8, 0.2], [0.3, 0.5, 0.3], [0.05, 0.1, 0.05], 20)
    gold_material = Material([0.8, 0.6, 0.2], [1.0, 0.9, 0.6], [0.1, 0.08, 0.02], 120)
    silver_material = Material([0.6, 0.6, 0.6], [0.9, 0.9, 0.9], [0.1, 0.1, 0.1], 150)
    
    return red_material, blue_material, green_material, gold_material, silver_material

def main():
    # Configuración básica
    rt = Raytracer(800, 600)
    rt.set_camera([0, 0, 0])
    rt.set_background_color([0.05, 0.05, 0.2])
    
    # Materiales
    red_mat, blue_mat, green_mat, gold_mat, silver_mat = setup_materials()
    
    # Esferas de la escena
    rt.add_object(Sphere([0, 0, -8], 1.5, gold_mat))        # centro
    rt.add_object(Sphere([-3, 0, -6], 1.0, red_mat))       # izquierda  
    rt.add_object(Sphere([3, 0, -6], 1.0, blue_mat))       # derecha
    rt.add_object(Sphere([0, 3, -7], 0.8, green_mat))      # arriba
    rt.add_object(Sphere([0, -2.5, -5], 0.8, silver_mat))  # abajo
    
    # Esferas adicionales
    rt.add_object(Sphere([-1.5, 1.5, -4], 0.5, blue_mat))
    rt.add_object(Sphere([1.5, 1.5, -4], 0.5, red_mat))
    rt.add_object(Sphere([-2, -1, -9], 0.6, green_mat))
    rt.add_object(Sphere([2, -1, -9], 0.6, silver_mat))
    
    # Setup de luces
    rt.add_light(Light([5, 8, 2], [1.0, 1.0, 1.0], 1.2))      # principal
    rt.add_light(Light([-4, 3, -1], [0.6, 0.7, 1.0], 0.6))   # relleno
    rt.add_light(Light([0, -2, -15], [1.0, 0.8, 0.6], 0.4))  # trasera
    
    print("Lab 5 - Raytracer con esferas")
    print(f"Renderizando {len(rt.objects)} esferas...")
    
    # Renderizar
    rt.render()
    
    # Guardar
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, "raytraced_scene.bmp")
    rt.save_image(output_file)
    
    print(f"Imagen guardada: {output_file}")

if __name__ == "__main__":
    main()
