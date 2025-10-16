"""
Genera textura procedural de madera para la rama
Patrón: anillos concéntricos con variación de tono marrón
"""
import numpy as np
from PIL import Image

def generate_wood_texture(width=512, height=512):
    """
    Genera textura de madera con anillos concéntricos
    """
    # Crear arrays de coordenadas
    y, x = np.ogrid[:height, :width]
    
    # Centrar en mitad de la textura
    center_x, center_y = width // 2, height // 2
    
    # Calcular distancia desde el centro (anillos)
    distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    
    # Crear patrón de anillos con frecuencia variable
    ring_pattern = np.sin(distance * 0.15 + np.random.rand(height, width) * 0.5)
    
    # Normalizar a [0, 1]
    ring_pattern = (ring_pattern + 1.0) / 2.0
    
    # Colores base madera (marrón oscuro a claro)
    wood_dark = np.array([0.35, 0.25, 0.15])  # Marrón oscuro
    wood_light = np.array([0.65, 0.50, 0.35]) # Marrón claro
    
    # Interpolar colores según el patrón
    wood_color = np.zeros((height, width, 3))
    for i in range(3):
        wood_color[:, :, i] = wood_dark[i] + (wood_light[i] - wood_dark[i]) * ring_pattern
    
    # Añadir ruido para textura más orgánica
    noise = np.random.randn(height, width, 3) * 0.05
    wood_color = np.clip(wood_color + noise, 0, 1)
    
    # Convertir a uint8 (0-255)
    wood_texture = (wood_color * 255).astype(np.uint8)
    
    return wood_texture

if __name__ == "__main__":
    print("🎨 Generando textura de madera...")
    texture = generate_wood_texture(512, 512)
    
    # Guardar como BMP
    img = Image.fromarray(texture, mode='RGB')
    img.save("assets/wood_bark.bmp")
    
    print("✅ Textura guardada: assets/wood_bark.bmp")
    print(f"   Dimensiones: {texture.shape[1]}x{texture.shape[0]}")
