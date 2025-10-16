import os
from scene import build_scene
from raytracer import render
from BMP_Writer import GenerateBMP


def tonemap_and_convert(color_buffer, width, height, exposure=1.0, gamma=2.2):
    """Convierte buffer float (0..1) a uint8 con tonemapping."""
    output = []
    for x in range(width):
        row = []
        for y in range(height):
            r, g, b = color_buffer[x][y]
            # Exposure
            r, g, b = r * exposure, g * exposure, b * exposure
            # Tonemapping Reinhard simple
            r = r / (1.0 + r)
            g = g / (1.0 + g)
            b = b / (1.0 + b)
            # Gamma
            r = r ** (1.0 / gamma)
            g = g ** (1.0 / gamma)
            b = b ** (1.0 / gamma)
            # Clamp y convert
            r_int = int(max(0, min(255, r * 255)))
            g_int = int(max(0, min(255, g * 255)))
            b_int = int(max(0, min(255, b * 255)))
            row.append((r_int, g_int, b_int))
        output.append(row)
    return output


if __name__ == '__main__':
    print('Construyendo escena...')
    scene = build_scene()
    
    width, height = 320, 180
    print(f'Renderizando {width}x{height}...')
    
    color_buffer = render(scene, width, height, max_depth=3)
    
    print('Tonemapping...')
    output_buffer = tonemap_and_convert(color_buffer, width, height, exposure=1.2, gamma=2.2)
    
    base_dir = os.path.dirname(__file__)
    output_path = os.path.join(base_dir, 'outputs', 'render_preview.bmp')
    
    print(f'Guardando en {output_path}...')
    GenerateBMP(output_path, width, height, 3, output_buffer)
    print('Render completo!')
