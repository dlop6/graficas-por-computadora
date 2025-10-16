# Plan de escena — Proyecto 2

Referencia: coloca `reference.jpg` en `Proyecto 2/assets/` (imagen de los Pikmin/escena de estudio).

Resumen objetivo:
- Recrear una versión simplificada de la imagen de referencia usando primitivas y 1 OBJ.
- Enfocar en composición, 4 materiales (incluye textura), envmap y varias luces.

Cámara:
- Posición aproximada: (0, 1.2, 4.0)
- Objetivo (look-at): (0, 1.0, 0)
- FOV: 40°
- Profundidad de campo: opcional (pequeño blur usando jitter de lente si hay tiempo)

Lista de objetos (mínimo 11):
1. Suelo / plano (textura madera)
2. Pared de fondo (plano con textura / envmap visible)
3. Rama (varios cilindros conectados o un OBJ simple)
4. Botella/vaso de vidrio (primitiva cilíndrica con material refractivo)
5. Tarro metálico (esfera metálica)
6. Personaje 1 (combinación de esferas/cilindros)
7. Personaje 2 (esfera + cilindro)
8. Personaje 3
9. Personaje 4
10. Planta/hoja (plano con textura alpha)
11. OBJ decorativo (ej. taza/adorno) — cargar desde `assets/` (OBJ + texturas)

Materiales (4 ejemplos):
- Texturado difuso: madera (para mesa/suelo) — usa `assets/wood.jpg`.
- Metálico: alta reflexión, bajo roughness (para esfera metálica).
- Refractivo (vidrio): IOR ~1.5, transparencia y atenuación de color.
- Lambertiano simple: colores planos para algunos personajes.

Iluminación:
- 1 directional (simula luz ambiente/sol suave desde arriba-izquierda).
- 2 point lights (uno cerca de la cámara, otro detrás de la cámara o lateral).
- 1 spotlight (foco sobre la escena principal).

Environment map:
- Usa una imagen equirectangular en `assets/envmap.jpg` para background y reflejos.

Notas de implementación y prioridades:
- MVP: usar primitivas (esferas, cilindros, planos) para la mayoría de los objetos; agregar 1 OBJ.
- Asegurar soporte de UVs y normales en el loader OBJ.
- Usar mipmaps o muestreo bilinear si tu `BMPTexture.py` lo soporta (mejor apariencia).
- Si hay muchos triángulos, considerar no usar modelos pesados o implementar BVH más tarde.

Archivos y estructura esperada:
- `Proyecto 2/assets/reference.jpg` (imagen de referencia)
- `Proyecto 2/assets/envmap.jpg` (opcional)
- `Proyecto 2/assets/wood.jpg`, `.../leaf.png`, `.../label.jpg`
- `Proyecto 2/outputs/final.png` (render final)

Tareas siguientes inmediatas:
- Añadir assets en `Proyecto 2/assets/`.
- Verificar/implementar loader OBJ en `model.py`.
- Implementar materiales y envmap.
