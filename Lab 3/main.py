"""
Renderizador de Modelos OBJ con Texturas - Lab 3
Universidad del Valle de Guatemala
Gráficas por Computadora 2025

Este programa renderiza un modelo OBJ con textura desde 4 ángulos diferentes:
1. Medium shot - Vista frontal normal
2. Low angle - Vista desde abajo
3. High angle - Vista desde arriba  
4. Dutch angle - Vista inclinada

Implementa las 4 transformaciones requeridas:
- Model Matrix
- View Matrix  
- Projection Matrix
- Viewport Matrix
"""

import os
import pygame
import sys
from typing import List
from Model import Model
from Camera import Camera, CameraController
from Renderer import Renderer
from BMP_Writer import GenerateBMP

# Configuración
WIDTH, HEIGHT = 800, 600
ASPECT_RATIO = WIDTH / HEIGHT

def find_obj_file() -> str:
    """Busca archivos OBJ en las carpetas del proyecto"""
    search_paths = [
        "obj",
        "models", 
        "../Lab 2/Rasterizer2025/Rasterizer2025/Rasterizer2025/obj",
        "../Lab 2/Rasterizer2025/Rasterizer2025/Rasterizer2025/models"
    ]
    
    obj_extensions = ['.obj']
    
    for search_path in search_paths:
        if os.path.exists(search_path):
            for file in os.listdir(search_path):
                if any(file.lower().endswith(ext) for ext in obj_extensions):
                    return os.path.join(search_path, file)
    
    return None # type: ignore

def find_texture_file(obj_path: str) -> str:
    """Busca archivos de textura relacionados con el modelo OBJ"""
    if not obj_path:
        return None # type: ignore
    
    obj_dir = os.path.dirname(obj_path)
    obj_name = os.path.splitext(os.path.basename(obj_path))[0]
    
    texture_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tga']
    
    # Buscar texturas con el mismo nombre base
    for ext in texture_extensions:
        texture_path = os.path.join(obj_dir, obj_name + ext)
        if os.path.exists(texture_path):
            return texture_path
    
    # Buscar cualquier archivo de textura en el directorio
    for file in os.listdir(obj_dir):
        if any(file.lower().endswith(ext) for ext in texture_extensions):
            return os.path.join(obj_dir, file)
    
    return None # type: ignore

def render_shot(renderer: Renderer, model: Model, camera: Camera, 
               shot_name: str, save_bmp: bool = True) -> pygame.Surface:
    """Renderiza una toma específica"""
    print(f"Renderizando {shot_name}...")
    
    # Configurar cámara
    renderer.set_camera(camera)
    
    # Limpiar buffers
    renderer.clear((50, 50, 80))  # Color de fondo azul oscuro
    
    # Renderizar
    renderer.render()
    
    # Guardar como BMP si se solicita
    if save_bmp:
        # Crear carpeta renders si no existe
        renders_dir = "renders"
        if not os.path.exists(renders_dir):
            os.makedirs(renders_dir)
        
        filename = f"{shot_name.lower().replace(' ', '_')}.bmp"
        filepath = os.path.join(renders_dir, filename)
        GenerateBMP(filepath, WIDTH, HEIGHT, 3, renderer.frame_buffer)
        print(f"{shot_name} guardado como {filepath}")
    
    return renderer.get_framebuffer_as_surface()

def main():
    """Función principal"""
    print(" Renderizador de Modelos OBJ con Texturas")
    print("=" * 50)
    
    # Inicializar pygame
    pygame.init()
    
    # Buscar archivo OBJ
    obj_path = find_obj_file()
    if not obj_path:
        print(" Error: No se encontró ningún archivo OBJ")
        print("Por favor, coloca un archivo .obj en una de estas carpetas:")
        print("- obj/")
        print("- models/")
        print("- ../Lab 2/Rasterizer2025/Rasterizer2025/Rasterizer2025/obj/")
        return
    
    print(f"Modelo encontrado: {obj_path}")
    
    # Buscar textura
    texture_path = find_texture_file(obj_path)
    if texture_path:
        print(f"  Textura encontrada: {texture_path}")
    else:
        print("No se encontró textura, usando color sólido")
    
    # Cargar modelo
    model = Model()
    if not model.load_obj(obj_path, texture_path):
        print(" Error cargando el modelo")
        return
    
    # Auto-centrar y escalar modelo
    model.auto_center_and_scale(1.5)  # Hacer el modelo un poco más pequeño para mejor visibilidad
    print(f"Modelo centrado y escalado")
    
    # Crear renderizador
    renderer = Renderer(WIDTH, HEIGHT)
    renderer.add_model(model)
    
    # Configurar iluminación más dramática
    renderer.set_light_direction(1.0, 1.0, 0.5)
    renderer.ambient_strength = 0.2  # Menos luz ambiente para más contraste
    
    # Crear controlador de cámara
    camera_controller = CameraController(ASPECT_RATIO)
    camera_controller.set_distance(3.0)  # Distancia más cercana para mejor detalle
    
    print("\n Generando las 4 tomas...")
    print("-" * 30)
    
    # Crear ventana para mostrar resultados
    screen = pygame.display.set_mode((WIDTH * 2, HEIGHT * 2))
    pygame.display.set_caption("Renderizador OBJ - 4 Tomas")
    
    # Renderizar las 4 tomas
    shots = []
    
    # 1. Medium Shot
    medium_camera = camera_controller.get_medium_shot_camera()
    medium_surface = render_shot(renderer, model, medium_camera, "Medium Shot")
    shots.append(("Medium Shot", medium_surface))
    
    # 2. Low Angle
    low_camera = camera_controller.get_low_angle_camera()
    low_surface = render_shot(renderer, model, low_camera, "Low Angle")
    shots.append(("Low Angle", low_surface))
    
    # 3. High Angle  
    high_camera = camera_controller.get_high_angle_camera()
    high_surface = render_shot(renderer, model, high_camera, "High Angle")
    shots.append(("High Angle", high_surface))
    
    # 4. Dutch Angle
    dutch_camera = camera_controller.get_dutch_angle_camera()
    dutch_surface = render_shot(renderer, model, dutch_camera, "Dutch Angle")
    shots.append(("Dutch Angle", dutch_surface))
    
    print("\nTodas las tomas generadas exitosamente!")
    print("\n Archivos generados en la carpeta 'renders':")
    print("- renders/medium_shot.bmp")
    print("- renders/low_angle.bmp") 
    print("- renders/high_angle.bmp")
    print("- renders/dutch_angle.bmp")
    
    # Mostrar las 4 tomas en una ventana 2x2
    screen.fill((20, 20, 20))
    
    # Posiciones para el grid 2x2
    positions = [
        (0, 0),           # Arriba izquierda
        (WIDTH, 0),       # Arriba derecha  
        (0, HEIGHT),      # Abajo izquierda
        (WIDTH, HEIGHT)   # Abajo derecha
    ]
    
    # Dibujar cada toma
    for i, (shot_name, surface) in enumerate(shots):
        screen.blit(surface, positions[i])
        
        # Añadir etiqueta
        font = pygame.font.Font(None, 36)
        text = font.render(shot_name, True, (255, 255, 255))
        text_pos = (positions[i][0] + 10, positions[i][1] + 10)
        screen.blit(text, text_pos)
    
    pygame.display.flip()
    
    print("\nMostrando resultados en ventana...")
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
    print("\n¡Gracias por usar el renderizador!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")
