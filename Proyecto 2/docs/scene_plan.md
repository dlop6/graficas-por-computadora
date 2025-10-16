# Plan de escena — Proyecto 2: Pikmin Scene (Versión Simplificada)

## Referencia
Imagen de Pikmin sobre rama con vegetación y fondo bokeh.  
Guardar como `Proyecto 2/assets/reference.jpg`.

## Objetivo
Recrear versión simplificada usando figuras geométricas primitivas y cumplir exactamente con los requisitos:
- **30 pts**: >10 figuras
- **20 pts**: 4 materiales (1 texturado)
- **5 pts**: Environment map
- **20 pts**: 4 primitivas nuevas
- **20 pts**: 1 modelo OBJ
- **20 pts**: Estética
- **10 pts**: Iluminación múltiple

**Total objetivo: 100 puntos**

---

## Configuración de cámara
- **Posición**: `(0, 0.8, 3.5)`
- **Look-at**: `(0, 0.5, 0)` (centro de la rama)
- **FOV**: `45°`
- **Aspecto**: `16:9` (1920x1080 final, 960x540 preview)
- **Near/Far**: `0.1 / 100`

---

## Lista de objetos (14 figuras = 30 pts)

### Personajes Pikmin (primitivas combinadas)
1. **Pikmin Azul** (izquierda)
   - Cuerpo: Cápsula (nueva primitiva #1) vertical, radio 0.12, altura 0.5
   - Cabeza: Esfera, radio 0.15
   - Tallo: Cilindro delgado + esfera pequeña (flor/hoja)
   - Posición base: `(-0.8, 0.1, -0.3)`
   - Color: `(0.2, 0.5, 0.9)` azul

2. **Pikmin Amarillo** (centro-izquierda)
   - Cuerpo: Cápsula vertical, radio 0.12, altura 0.5
   - Cabeza: Esfera, radio 0.15
   - Orejas: 2 pequeñas esferas laterales
   - Tallo: Cilindro + esfera
   - Posición: `(-0.3, 0.1, -0.2)`
   - Color: `(0.95, 0.85, 0.2)` amarillo

3. **Pikmin Rojo** (centro-derecha)
   - Cuerpo: Cápsula vertical, radio 0.12, altura 0.5
   - Cabeza: Esfera, radio 0.15
   - Nariz: Cono pequeño (nueva primitiva #2)
   - Tallo: Cilindro + esfera
   - Posición: `(0.3, 0.1, -0.25)`
   - Color: `(0.9, 0.2, 0.2)` rojo

4. **Bulborb (enemigo robot derecha)**
   - Cuerpo: Elipsoide/esfera achatada, radio 0.25
   - Ojos: 2 esferas grandes blancas + pupilas negras
   - Detalles: Cilindros pequeños (patas/antenas)
   - Posición: `(1.2, 0.2, -0.5)`
   - Color: `(0.3, 0.4, 0.6)` azul metálico

### Objetos de escena
5. **Rama/tronco principal**
   - Cilindro horizontal grueso, radio 0.3, longitud 3.5
   - Textura: madera (material texturado)
   - Posición: `(0, 0, 0)` rotado horizontalmente
   - Color base: `(0.6, 0.45, 0.3)` marrón

6. **Tomate/fruta roja (izquierda)**
   - Esfera, radio 0.22
   - Material: lambertiano brillante
   - Posición: `(-1.3, 0.35, -0.4)`
   - Color: `(0.85, 0.15, 0.1)` rojo tomate

7. **Botella transparente (fondo izquierda)**
   - Cilindro alto + toro en la base (nueva primitiva #3)
   - Material: refractivo (vidrio, IOR 1.5)
   - Posición: `(-1.5, 0, -1.2)`
   - Escala: radio 0.15, altura 0.8

8. **Esfera metálica/burbuja (superior derecha)**
   - Esfera, radio 0.25
   - Material: metálico reflectivo (alta reflectividad)
   - Posición: `(1.5, 1.2, -0.8)`
   - Color: `(0.9, 0.9, 0.95)` plateado

9. **Hoja/pétalo grande (izquierda superior)**
   - Disco o anillo parcial (nueva primitiva #4)
   - Material: lambertiano texturado (verde)
   - Posición: `(-1.8, 1.0, -1.0)`
   - Rotación para simular hoja

10. **Flor violeta (derecha inferior)**
    - Disco plano, radio 0.3
    - Material: lambertiano
    - Posición: `(1.8, -0.3, 0.5)`
    - Color: `(0.6, 0.4, 0.8)` violeta

11. **Plano suelo (invisible/fondo)**
    - Plano en y = -0.5
    - Material: difuso oscuro o envmap reflejado
    - Color: `(0.3, 0.35, 0.3)` verde oscuro

12. **Elemento decorativo OBJ (taza/vaso)**
    - Modelo OBJ simple (20 pts)
    - Posición: `(0.8, 0.1, -0.6)`
    - Material: lambertiano o texturado

13. **Hoja adicional (derecha)**
    - Disco rotado, radio 0.25
    - Posición: `(1.5, 0.8, -0.3)`
    - Color verde: `(0.4, 0.7, 0.3)`

14. **Elemento ambiental (burbuja/orbe fondo)**
    - Esfera pequeña, radio 0.18
    - Material: refractivo o translúcido
    - Posición: `(-1.0, 1.5, -2.0)`

---

## Primitivas nuevas (20 pts = 4 primitivas × 5 pts)

### 1. Cápsula
- Cilindro con hemisferios en los extremos
- Ray-intersect: combinar cilindro + 2 esferas
- Uso: cuerpos de Pikmin

### 2. Cono
- Base circular, punta en vértice
- Ray-intersect: ecuación cuadrática en coordenadas cilíndricas
- Uso: nariz de Pikmin rojo, detalles

### 3. Toro
- Superficie de revolución (donut)
- Ray-intersect: ecuación cuártica reducida
- Uso: base de botella, anillos decorativos

### 4. Disco
- Círculo plano en 3D
- Ray-intersect: intersección con plano + distancia radial
- Uso: hojas, pétalos, flores

---

## Materiales (20 pts = 4 materiales × 5 pts)

### 1. Lambertiano texturado (rama)
- Difuso con textura de madera
- Archivo: `assets/wood_bark.jpg`
- Muestreo UV por coordenadas cilíndricas
- Shading: Lambertian + ambient

### 2. Metálico reflectivo (esfera plateada)
- Alta reflectividad (0.85)
- Color base: `(0.9, 0.9, 0.95)`
- Shading: Phong especular + rayos reflejados
- Toma en cuenta envmap en reflexiones

### 3. Refractivo vidrio (botella)
- IOR: 1.5
- Transparencia: 0.9
- Color tinte: `(0.95, 0.98, 1.0)` azul muy claro
- Usa funciones de `refractionFunctions.py`
- Toma en cuenta envmap en refracciones

### 4. Lambertiano difuso (Pikmin)
- Difuso simple sin textura
- Colores variados por objeto
- Shading: Lambert + ambient + especular suave

---

## Environment Map (5 pts)

### Configuración
- Formato: equirectangular (2:1)
- Archivo: `assets/envmap_outdoor.jpg` (jardín/naturaleza)
- Resolución recomendada: 2048×1024 o 1024×512

### Implementación
- Añadir método `sampleEnvMap(direction)` en `BMPTexture.py`
- Convertir dirección 3D a UV: 
  - `u = 0.5 + atan2(dir.z, dir.x) / (2π)`
  - `v = 0.5 - asin(dir.y) / π`
- Usar en:
  - **Fondo**: cuando rayo no interseca nada
  - **Reflexiones**: material metálico
  - **Refracciones**: material vidrio

---

## Iluminación (10 pts)

### 1. Directional Light (sol suave)
- Dirección: `normalize((-0.3, -0.5, -0.4))`
- Color: `(1.0, 0.98, 0.92)` blanco cálido
- Intensidad: 0.7
- Simula luz del sol filtrada

### 2. Point Light #1 (luz principal)
- Posición: `(1.5, 2.0, 1.0)`
- Color: `(1.0, 0.95, 0.85)` amarillo suave
- Intensidad: 1.2
- Atenuación cuadrática

### 3. Point Light #2 (fill light)
- Posición: `(-2.0, 1.5, 0.5)`
- Color: `(0.8, 0.85, 1.0)` azul frío
- Intensidad: 0.6
- Luz de relleno para sombras

### 4. Spotlight (foco en Pikmin)
- Posición: `(0, 3.0, 2.0)`
- Dirección: hacia `(0, 0.3, 0)`
- Ángulo: 30° cono
- Color: `(1.0, 1.0, 1.0)` blanco
- Intensidad: 0.8
- Enfoca el centro de la escena

### Ambient
- Intensidad: 0.15
- Color: `(0.7, 0.75, 0.8)` azul-gris suave

---

## Parámetros de render

### Preview (rápido)
- Resolución: 960×540
- Muestras por píxel: 1
- Profundidad de rayo: 3
- Tiempo estimado: 30-60 seg

### Final (calidad)
- Resolución: 1920×1080
- Muestras por píxel: 4 (si hay tiempo, sino 1)
- Profundidad de rayo: 5
- Antialiasing: jitter de subpíxeles (opcional)
- Tiempo estimado: 5-15 min

---

## Archivos requeridos

### Assets necesarios
```
Proyecto 2/assets/
├── reference.jpg          (imagen de referencia Pikmin)
├── envmap_outdoor.jpg     (envmap equirectangular)
├── wood_bark.jpg          (textura madera para rama)
├── model_decorative.obj   (modelo OBJ decorativo)
└── model_decorative.mtl   (opcional)
```

### Outputs esperados
```
Proyecto 2/outputs/
├── preview.bmp            (render rápido 960×540)
├── final.bmp              (render final 1920×1080)
└── comparison.jpg         (referencia + final lado a lado)
```

---

## Checklist de implementación

- [ ] Implementar 4 primitivas nuevas en archivo `primitives.py`
- [ ] Extender `BMPTexture.py` con soporte envmap equirectangular
- [ ] Crear 4 clases de materiales en `materials.py`
- [ ] Implementar sistema de iluminación múltiple en `lighting.py`
- [ ] Crear escena en `scene.py` con los 14 objetos
- [ ] Loader OBJ funcional en `model.py`
- [ ] Ray tracer con reflexión/refracción en `raytracer.py`
- [ ] Script principal `render_scene.py`
- [ ] Probar preview y ajustar posiciones
- [ ] Render final y comparar con referencia

---

## Notas técnicas

### Optimización
- Limitar profundidad de rayo a 5 (evitar recursión infinita)
- Usar bounding boxes si OBJ tiene >1000 triángulos
- Preview en baja resolución primero
- Considerar solo sombras duras (más rápido que soft shadows)

### Simplificaciones permitidas
- Pikmin sin articulaciones (pose fija)
- Texturas procedurales si no hay archivos
- Envmap de baja resolución (512×256) para velocidad
- Fondo desenfocado = solo envmap (sin path tracing)

### Extras opcionales (no necesarios para 100 pts)
- Depth of field
- Soft shadows
- Ambient occlusion
- Muestreo Monte Carlo
- BVH/aceleración espacial
