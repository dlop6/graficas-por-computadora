# Lab 10 - Diorama OpenGL

diorama 3d con modelos pokémon renderizados en opengl 3.3+. incluye shaders personalizados, post-processing, y sistema de cámara orbital.

## ejecución

```bash
python RendererOpenGL2025.py
```

## controles

### cámara orbital

| control | acción |
|---------|--------|
| **W/S** | rotar cámara arriba/abajo (pitch) |
| **A/D** | rotar cámara izquierda/derecha (yaw) |
| **Q/E** | alejar/acercar zoom |
| **mouse drag (click izq.)** | rotar cámara alrededor del target |
| **mouse wheel** | zoom |
| **C** | activar/desactivar rotación automática |

### cambio de vista

| tecla | objetivo |
|-------|----------|
| **0** | vista general |
| **1** | pokeball |
| **2** | charizard |
| **3** | eevee |
| **4** | umbreon |
| **5** | bulbasaur |

### visualización

| control | acción |
|---------|--------|
| **F** | alternar entre filled/wireframe |

## arquitectura

### modelos
- **plataforma procedural** (60x60 unidades)
- **charizard** - shader plasma multicolor
- **eevee** - shader patrones procedurales
- **umbreon** - shader psicodélico 10 capas
- **bulbasaur** - shader patrones ondulantes
- **pokeball** - shader glitch holográfico

### shaders creativos
cada modelo implementa un fragment shader único con efectos avanzados:
- kaleidoscope transforms
- fractal brownian motion
- voronoi cells
- chromatic aberration
- fresnel/rim lighting
- procedural noise

### post-processing
- bloom con kernel 5x5
- vignette dinámico
- ajuste de contraste y saturación

### iluminación
- point light elevada (0, 20, 0)
- ambient light 0.5
- phong shading en todos los modelos

## dependencias

```
pygame
PyOpenGL
PyGLM
numpy
```

