"""
Comparador de modelos - Genera renders de todos los modelos disponibles
"""

import os
import pygame
from main import find_obj_file, render_shot
from Model import Model
from Camera import CameraController
from Renderer import Renderer

def compare_models():
    """Genera renders de comparación de todos los modelos"""
    print("🔍 Comparador de Modelos OBJ")
    print("=" * 40)
    
    # Buscar todos los modelos
    search_paths = [
        "obj",
        "models", 
        "../Lab 2/Rasterizer2025/Rasterizer2025/Rasterizer2025/obj",
        "../Lab 2/Rasterizer2025/Rasterizer2025/Rasterizer2025/models"
    ]
    
    models = []
    for path in search_paths:
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.lower().endswith('.obj'):
                    full_path = os.path.join(path, file)
                    if full_path not in models:  # Evitar duplicados
                        models.append(full_path)
    
    if not models:
        print("❌ No se encontraron modelos OBJ")
        return
    
    print(f"📄 Encontrados {len(models)} modelos:")
    for i, model_path in enumerate(models):
        print(f"  {i+1}. {os.path.basename(model_path)}")
    
    # Configuración
    width, height = 400, 300
    
    pygame.init()
    
    # Renderizar cada modelo
    surfaces = []
    model_names = []
    
    for model_path in models:
        model_name = os.path.splitext(os.path.basename(model_path))[0]
        print(f"\n🔄 Procesando {model_name}...")
        
        try:
            # Cargar modelo
            model = Model()
            if not model.load_obj(model_path):
                print(f"❌ Error cargando {model_name}")
                continue
            
            model.auto_center_and_scale(1.5)
            
            # Crear renderizador
            renderer = Renderer(width, height)
            renderer.add_model(model)
            renderer.set_light_direction(1.0, 1.0, 0.5)
            renderer.ambient_strength = 0.2
            
            # Crear cámara
            camera_controller = CameraController(width / height)
            camera_controller.set_distance(3.0)
            camera = camera_controller.get_medium_shot_camera()
            
            # Renderizar
            surface = render_shot(renderer, model, camera, f"{model_name} - Medium Shot", save_bmp=False)
            surfaces.append(surface)
            model_names.append(model_name)
            
            print(f"✓ {model_name} renderizado ({len(model.vertices)//3} vértices)")
            
        except Exception as e:
            print(f"❌ Error con {model_name}: {e}")
            continue
    
    if not surfaces:
        print("❌ No se pudo renderizar ningún modelo")
        return
    
    # Crear ventana de comparación
    cols = min(3, len(surfaces))  # Máximo 3 columnas
    rows = (len(surfaces) + cols - 1) // cols  # Calcular filas necesarias
    
    screen_width = width * cols
    screen_height = height * rows
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(f"Comparación de Modelos ({len(surfaces)} modelos)")
    
    # Dibujar modelos en grid
    screen.fill((20, 20, 20))
    
    for i, (surface, name) in enumerate(zip(surfaces, model_names)):
        row = i // cols
        col = i % cols
        
        x = col * width
        y = row * height
        
        # Dibujar superficie
        screen.blit(surface, (x, y))
        
        # Añadir etiqueta
        font = pygame.font.Font(None, 24)
        text = font.render(name, True, (255, 255, 255))
        screen.blit(text, (x + 10, y + 10))
        
        # Añadir borde
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 2)
    
    pygame.display.flip()
    
    print(f"\n✅ Comparación completa!")
    print(f"🖥️  Mostrando {len(surfaces)} modelos en ventana {screen_width}x{screen_height}")
    print("Presiona cualquier tecla o cierra la ventana para salir")
    
    # Loop de eventos
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False
        clock.tick(60)
    
    pygame.quit()
    print("👋 ¡Gracias por usar el comparador!")

if __name__ == "__main__":
    try:
        compare_models()
    except KeyboardInterrupt:
        print("\n👋 Saliendo...")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")
