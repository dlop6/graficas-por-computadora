#!/usr/bin/env python3
"""
Proyecto 1 - Rasterizador 3D
Escena con múltiples modelos OBJ para pruebas de transformaciones

Uso:
    python main.py --preview    # Renderizado rápido para testing
    python main.py             # Renderizado completo con shaders
"""

import os
import sys
import argparse
import numpy as np
import pygame
from Model import Model
from Camera import Camera
from Renderer import Renderer
from BMP_Writer import GenerateBMP

def get_obj_paths():
    """Obtiene las rutas de los 4 modelos OBJ a cargar"""
    base = os.path.dirname(__file__)
    return [
        os.path.join(base, 'obj', 'cat', '12221_Cat_v1_l3.obj'),
        os.path.join(base, 'obj', 'dog', 'Australian_Cattle_Dog_v1_L3.123c9c6a5764-399b-4e86-9897-6bcb08b5e8ed', '13463_Australian_Cattle_Dog_v3.obj'),
        os.path.join(base, 'obj', 'horse', '10026_Horse_v01_L3.123cf7625b3f-e79f-4633-9dc6-46d06c7bb985', '10026_Horse_v01-it2.obj'),
        os.path.join(base, 'obj', 'cow', 'Cow_v4_L1.123cea571596-0bc6-4e67-be6c-f586c6fd6a16', '16434_Cow_v4_NEW.obj'),
    ]

def load_background_image(width, height):
    """Carga la imagen de fondo o crea uno por defecto"""
    bg_path = os.path.join(os.path.dirname(__file__), 'obj', 'super24.jpg')
    
    pygame.init()
    if os.path.exists(bg_path):
        try:
            print(f"Cargando fondo: {bg_path}")
            bg_img = pygame.image.load(bg_path)
            bg_img = pygame.transform.scale(bg_img, (width, height))
            bg_surface = pygame.surfarray.array3d(bg_img).transpose((1, 0, 2))
            return bg_surface
        except Exception as e:
            print(f"Error cargando fondo: {e}")
    
    print("Usando fondo degradado por defecto")
    # Crear fondo degradado azul
    bg_surface = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        intensity = int(100 + (155 * y / height))  # Degradado de 100 a 255
        bg_surface[y, :] = [intensity//3, intensity//2, intensity]  # Azul degradado
    
    return bg_surface

def setup_camera(width, height):
    """Configura la cámara para ver toda la escena"""
    aspect_ratio = width / height
    
    # Cámara posicionada para ver los 4 modelos
    camera = Camera(
        position=(0, 3, 12),     # Elevada y alejada
        target=(0, 0, 0),        # Mirando al centro
        up=(0, 1, 0),           # Vector up estándar
        fov=60,                 # Campo de visión cómodo
        aspect=aspect_ratio,
        near=0.1,
        far=100.0
    )
    
    return camera

def get_model_transformations():
    """Define las transformaciones para cada modelo (posición, rotación, escala)"""
    
    # ¡AQUÍ PUEDES AJUSTAR LAS TRANSFORMACIONES FÁCILMENTE!
    
    transformations = [
        # Gato - Izquierda frontal
        {
            "name": "cat",
            "translation": [-4.5, 5.2, 2.0],
            "rotation": [90.0, 0.0, 90.0],    # Rotado 45° en Y
            "scale": [2.0, 2.0, 2.0],        # Ligeramente más grande
            "shader": "textured_normal"       # Textura + Normal mapping
        },
        # Perro - Centro frontal
        {
            "name": "dog", 
            "translation": [3.0, 4.0, 2.0],
            "rotation": [90.0,0.0,250.0],    
            "scale": [1.4, 1.4, 1.4],        # Escala normal
            "shader": "fresnel"               # Fresnel para efectos brillantes
        },
        # Caballo - Derecha frontal
        {
            "name": "horse",
            "translation": [-5.3, -2.5, -1.0],
            "rotation": [90.0, 0.0, 90.0],   # Rotado -45° en Y
            "scale": [1.5, 1.5, 1.5],        # Más pequeño
            "shader": "toon"                  # Toon shading estilo cartoon
        },
        # Vaca - Centro trasero
        {
            "name": "cow",
            "translation": [1.0, 3.5, -2.0],
            "rotation": [90.0, 00.0, 90.0],   # Rotado 180° (mirando al frente)
            "scale": [2.0, 2.0, 2.0],        # Ligeramente más grande
            "shader": "metallic"              # Efecto metálico especial
        }
    ]
    
    return transformations

def load_models(obj_paths, transformations):
    """Carga todos los modelos y aplica sus transformaciones"""
    models = []
    
    for i, (path, transform) in enumerate(zip(obj_paths, transformations)):
        print(f"Cargando modelo {i+1}: {transform['name']}...", end=" ")
        
        # Verificar que el archivo existe
        if not os.path.exists(path):
            print(f"❌ Archivo no encontrado: {path}")
            continue
        
        # Crear y cargar modelo
        model = Model()
        if not model.load_obj(path):
            print(f"❌ Error cargando {path}")
            continue
        
        # Autocentrar y escalar el modelo base
        model.auto_center_and_scale(target_size=1.5)
        
        # Aplicar transformaciones específicas
        model.translation = transform["translation"]
        model.rotation = transform["rotation"]  
        model.scale = [
            model.scale[0] * transform["scale"][0],
            model.scale[1] * transform["scale"][1], 
            model.scale[2] * transform["scale"][2]
        ]
        
        # Guardar shader asignado
        model.assigned_shader = transform.get("shader", "plain")
        
        models.append(model)
        print("✅ Listo")
        print(f"   -> Posición: {model.translation}")
        print(f"   -> Rotación: {model.rotation}")
        print(f"   -> Escala: {model.scale}")
        print(f"   -> Shader: {model.assigned_shader}")
    
    return models

def render_simple_scene(renderer, models, preview_mode=False):
    """Renderiza la escena de forma simple para testing"""
    
    if preview_mode:
        print("\n🔍 MODO PREVIEW: Renderizado simple sin shaders")
        # Usar shader básico para preview rápido
        renderer.set_shader('plain')
        # Limpiar listas de modelos anteriores
        renderer.models.clear()
        # Agregar todos los modelos al renderer
        for model in models:
            renderer.add_model(model)
        # Renderizar la escena
        renderer.render()
    else:
        print("\n🎨 MODO COMPLETO: Renderizado con shaders específicos por modelo") 
        # Limpiar listas de modelos anteriores
        renderer.models.clear()
        
        # Renderizar cada modelo con su shader específico
        for i, model in enumerate(models):
            print(f"   📦 Renderizando {model.assigned_shader} en modelo {i+1}")
            
            # Cambiar al shader específico del modelo
            renderer.set_shader(model.assigned_shader)
            
            # Limpiar lista y agregar solo este modelo
            renderer.models.clear()
            renderer.add_model(model)
            
            # Renderizar este modelo
            renderer.render()
    
    print("✅ Renderizado completado")

def main():
    print("=" * 60)
    print("🎮 PROYECTO 1 - RASTERIZADOR 3D")
    print("🎯 Escena con múltiples modelos OBJ")
    print("=" * 60)
    
    # Parsear argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Rasterizador 3D con múltiples modelos')
    parser.add_argument('--preview', action='store_true', 
                       help='Modo preview: renderizado rápido para testing')
    parser.add_argument('--width', type=int, default=1000,
                       help='Ancho de la imagen (default: 1000)')
    parser.add_argument('--height', type=int, default=800, 
                       help='Alto de la imagen (default: 800)')
    args = parser.parse_args()
    
    # Configurar dimensiones
    if args.preview:
        WIDTH, HEIGHT = 600, 400  # Resolución más baja para preview
        print(f"📐 Modo PREVIEW: {WIDTH}x{HEIGHT}")
    else:
        WIDTH, HEIGHT = args.width, args.height
        print(f"📐 Modo COMPLETO: {WIDTH}x{HEIGHT}")
    
    # Obtener rutas de modelos
    obj_paths = get_obj_paths()
    transformations = get_model_transformations()
    
    print(f"\n📂 Modelos a cargar: {len(obj_paths)}")
    
    # Cargar imagen de fondo
    print("\n🖼️  Configurando fondo...")
    bg_surface = load_background_image(WIDTH, HEIGHT)
    
    # Configurar cámara
    print("📷 Configurando cámara...")
    camera = setup_camera(WIDTH, HEIGHT)
    
    # Crear renderer
    print("🎨 Inicializando renderer...")
    renderer = Renderer(WIDTH, HEIGHT)
    renderer.set_camera(camera)
    
    # Establecer fondo en el renderer
    if bg_surface is not None:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                renderer.frame_buffer[y][x] = tuple(bg_surface[y, x])
    else:
        renderer.clear((50, 100, 150))  # Azul por defecto
    
    # Cargar modelos
    print(f"\n📦 Cargando modelos...")
    models = load_models(obj_paths, transformations)
    
    if not models:
        print("❌ No se pudo cargar ningún modelo. Revisa las rutas.")
        print("🖼️  Guardando solo el fondo...")
        output_path = os.path.join(os.path.dirname(__file__), 'renders', 'solo_fondo.bmp')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        renderer.save_framebuffer(output_path)
        print(f"✅ Imagen guardada: {output_path}")
        return
    
    print(f"✅ Se cargaron {len(models)} modelos correctamente")
    
    # Renderizar escena
    render_simple_scene(renderer, models, preview_mode=args.preview)
    
    # Guardar resultado
    print("\n💾 Guardando imagen...")
    if args.preview:
        output_path = os.path.join(os.path.dirname(__file__), 'renders', 'preview_escena.bmp')
    else:
        output_path = os.path.join(os.path.dirname(__file__), 'renders', 'escena_completa.bmp')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    renderer.save_framebuffer(output_path)
    
    print(f"✅ Imagen guardada: {output_path}")
    print("\n🎉 ¡Renderizado completado con éxito!")
    print("\n💡 Para ajustar posiciones, edita la función 'get_model_transformations()' en main.py")

if __name__ == "__main__":
    main()
			
