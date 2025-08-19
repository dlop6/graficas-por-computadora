"""
Lab 4 - Shaders Creativos
Universidad del Valle de Guatemala
Gráficas por Computadora 2025

Demostración de 2 shaders únicos:
🌊 Agua Animada - Ondas procedurales
🔥 Fuego/Plasma - Efectos de llama
"""

import os
import pygame
import sys
import time
from Model import Model
from Camera import Camera, CameraController
from Renderer import Renderer
from BMP_Writer import GenerateBMP
from Shaders import AVAILABLE_SHADERS

# Configuración
WIDTH, HEIGHT = 800, 600
ASPECT_RATIO = WIDTH / HEIGHT

def find_obj_file() -> str:
    """Busca archivos OBJ en las carpetas del proyecto"""
    search_paths = [
        "Lab 4/obj",
        "Lab 4/models",
        "Lab 3/obj"
    ]
    for search_path in search_paths:
        if os.path.exists(search_path):
            for file in os.listdir(search_path):
                if file.lower().endswith('.obj'):
                    return os.path.join(search_path, file)
    return None # type: ignore

def render_shader_demo(renderer: Renderer, model: Model, camera: Camera, 
                      shader_name: str, demo_name: str) -> pygame.Surface:
    """Renderiza una demostración de shader específico"""
    print(f"  Renderizando {demo_name}...")
    
    # Configurar el shader
    renderer.set_shader(shader_name)
    renderer.set_camera(camera)
    
    # Limpiar buffers
    renderer.clear((30, 30, 40))  # Fondo azul oscuro
    
    # Renderizar
    renderer.render()
    
    # Guardar como BMP
    renders_dir = os.path.join("Lab 4", "renders")
    if not os.path.exists(renders_dir):
        os.makedirs(renders_dir)
    filename = f"{shader_name}_shader.bmp"
    filepath = os.path.join(renders_dir, filename)
    GenerateBMP(filepath, WIDTH, HEIGHT, 3, renderer.frame_buffer)
    print(f"    ✓ Guardado: {filepath}")
    return renderer.get_framebuffer_as_surface()

def main():
    """Función principal del Lab 4"""
    print("╔" + "═" * 48 + "╗")
    print("║" + " " * 12 + "🎨 LAB 4: SHADERS CREATIVOS" + " " * 9 + "║")
    print("║" + " " * 10 + "Universidad del Valle de Guatemala" + " " * 4 + "║")
    print("╚" + "═" * 48 + "╝")
    
    # Inicializar pygame
    pygame.init()
    
    # Buscar archivo OBJ
    obj_path = find_obj_file()
    if not obj_path:
        print("\n❌ Error: No se encontró ningún archivo OBJ")
        print("Por favor, coloca un archivo .obj en la carpeta 'obj/'")
        return
    
    print(f"\n📁 Modelo encontrado: {obj_path}")
    
    # Cargar modelo
    model = Model()
    if not model.load_obj(obj_path):
        print("❌ Error cargando el modelo")
        return
    
    # Auto-centrar y escalar modelo
    model.auto_center_and_scale(2.0)
    # Rotar 180 grados en X para corregir orientación
    model.rotation[0] += 180.0
    print("✓ Modelo cargado, escalado y rotado 180° en X")
    
    # Crear renderizador
    renderer = Renderer(WIDTH, HEIGHT)
    renderer.add_model(model)
    
    # Configurar iluminación
    renderer.set_light_direction(1.0, 1.0, 0.5)
    renderer.ambient_strength = 0.2
    
    # Crear cámara
    camera_controller = CameraController(ASPECT_RATIO)
    camera_controller.set_distance(3.5)
    main_camera = camera_controller.get_medium_shot_camera()
    
    print(f"\n🎬 Generando {len(AVAILABLE_SHADERS)} shaders creativos...")
    print("=" * 50)
    
    # Crear ventana para mostrar resultados
    screen = pygame.display.set_mode((WIDTH * 2, HEIGHT))
    pygame.display.set_caption("Lab 4 - Shaders Creativos")
    
    # Renderizar cada shader
    shader_surfaces = []
    shader_names = list(AVAILABLE_SHADERS.keys())
    
    for i, shader_name in enumerate(shader_names):
        shader_info = AVAILABLE_SHADERS[shader_name]
        demo_name = shader_info['name']
        
        print(f"{i+1}. {demo_name}")
        print(f"   📝 {shader_info['description']}")
        
        surface = render_shader_demo(renderer, model, main_camera, shader_name, demo_name)
        shader_surfaces.append((shader_name, demo_name, surface))
        
        # Pausa para ver progreso
        time.sleep(1.0)
    
    print(f"\n✅ ¡Shaders generados exitosamente!")
    print(f"\n📂 Archivos BMP en carpeta 'renders/':")
    for shader_name in shader_names:
        print(f"   - renders/{shader_name}_shader.bmp")
    
    # Mostrar los 2 shaders lado a lado
    screen.fill((20, 20, 30))
    
    # Posiciones lado a lado
    positions = [
        (0, 0),      # Izquierda
        (WIDTH, 0)   # Derecha
    ]
    
    # Dibujar cada shader
    for i, (shader_name, demo_name, surface) in enumerate(shader_surfaces):
        if i < 2:  # Solo los primeros 2
            screen.blit(surface, positions[i])
            
            # Añadir etiqueta
            font = pygame.font.Font(None, 36)
            text = font.render(demo_name, True, (255, 255, 255))
            
            # Posición de la etiqueta
            text_rect = text.get_rect()
            text_rect.topleft = (positions[i][0] + 20, positions[i][1] + 20)
            
            # Dibujar sombra del texto
            shadow = font.render(demo_name, True, (0, 0, 0))
            screen.blit(shadow, (text_rect.x + 3, text_rect.y + 3))
            screen.blit(text, text_rect.topleft)
    
    pygame.display.flip()
    
    print(f"\n🖼️  Mostrando resultados en ventana...")
    print("⌨️  Presiona cualquier tecla o cierra la ventana para continuar")
    
    print(f"\n💡 Análisis de los Shaders Implementados:")
    print("=" * 50)
    
    print(f"\n🌊 Shader de Agua:")
    print("  • Usa funciones sin() y cos() para crear ondas")
    print("  • Combina 3 ondas diferentes (horizontal, vertical, diagonal)")
    print("  • Los brillos aparecen donde las ondas son más altas")
    print("  • Se anima usando el tiempo como parámetro")
    
    print(f"\n🔥 Shader de Fuego:")
    print("  • Crea turbulencia combinando múltiples frecuencias")
    print("  • El fuego 'sube' - más intenso abajo, menos arriba")
    print("  • Gradiente realista: rojo → naranja → amarillo → blanco")
    print("  • Usa ruido procedural para movimiento natural")
    
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
    print(f"\n🎉 ¡Gracias por explorar los shaders creativos!")
    print("💡 Estos 2 shaders demuestran técnicas avanzadas de programación gráfica")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")
