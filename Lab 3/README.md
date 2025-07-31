# Lab 3 - Renderizador OBJ con 4 Tomas de Cámara

Renderizador 3D que carga modelos OBJ y los renderiza desde 4 ángulos diferentes.

## Qué hace

Carga un modelo 3D (formato .obj) y genera 4 imágenes desde diferentes ángulos:
- **Medium Shot** - Vista frontal normal
- **Low Angle** - Desde abajo (dramático)
- **High Angle** - Desde arriba 
- **Dutch Angle** - Inclinado (dinámico)

Usa las 4 transformaciones matriciales: Model, View, Projection y Viewport.

## Cómo usar

1. Pon tu archivo `.obj` en la carpeta `obj/`
2. Ejecuta: `python main.py`
3. Se generan 4 archivos `.bmp` en la carpeta `renders/`

También muestra una ventana con todas las tomas juntas.

## Archivos

```
Lab 3/
├── main.py         # Programa principal
├── Model.py        # Carga modelos OBJ
├── Camera.py       # Manejo de cámaras
├── Renderer.py     # Motor de renderizado
├── Shaders.py      # Efectos visuales
├── obj/           # Pon aquí tu modelo .obj
└── renders/       # Aquí salen las imágenes
```

## Requisitos

- Python 3.8+
- pygame
- numpy

Instalar: `pip install pygame numpy`

## Notas

- El programa busca automáticamente archivos .obj
- Soporta texturas si están en la misma carpeta
- Los modelos se auto-centran y escalan
- Usa z-buffer para profundidad correcta

---

**Diego López 23747**  
Gráficas por Computadora - UVG 2025
