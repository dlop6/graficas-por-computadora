
Proyecto 2 — Ray Tracer — Auditoría completa

Estructura relevante del proyecto (archivos consultados):
- `pikmin_scene.py` — definición completa de la escena (cámaras, materiales, objetos, luces, envmap, render pipeline).
- `raytracer.py` — núcleo del raytracer (construcción de rayos, NDC→screen mapping, loop de render, shading y trace).
- `primitives.py` — definición de primitivas geométricas (Sphere, Plane, Cylinder, Capsule, Cone, Disk, Torus, etc.).
- `materials.py` — implementaciones de materiales (Lambertian, TexturedLambert, Metal, Refractive).
- `BMP_Writer.py` — escritura de BMP final (rutina `GenerateBMP`).
- `HDRTexture.py` — loader/muestreo de HDR (envmap).
- `model.py` — loader y conversor de modelos OBJ (`OBJModel` y `to_triangles`).
- `assets/` — contiene `autumn_field_4k.hdr` (envmap) y `cube.obj` (modelo de prueba); rutas verificadas dentro del proyecto.

- Elementos usados:
	1) Cuatro materiales distintos implementados y usados en la escena.
	2) Environment map HDR cargado y usado (muestreo y reflejos).
	3) Cuatro primitivas nuevas implementadas: Capsule, Cone, Disk, Torus.
	4) Integración y uso de un modelo OBJ (loader y conversión a triángulos).
	5) Sistema de iluminación múltiple con 4 luces.
	6) Escena con más de 10 objetos.

Evidencia y referencias concretas
================================

1) Materiales (evidencia en `pikmin_scene.py`)
- `Lambertian` — múltiples instancias en `pikmin_scene.py` (por ejemplo `mat_blue_pikmin = Lambertian(color=(0.2, 0.5, 0.9), ambient=0.15)`) (línea ~22-31). Archivo: `pikmin_scene.py`.
- `Metal` — presencia en `pikmin_scene.py` (ej.: `mat_ground = Metal(color=(0.35, 0.38, 0.32), reflectivity=0.25, shininess=8)`) (línea ~69). Archivo: `pikmin_scene.py`.
- `Refractive` — presente (`mat_glass_orb = Refractive(ior=1.3, tint=(0.98, 0.96, 1.0), transparency=0.85)`) (línea ~84). Archivo: `pikmin_scene.py`.
- `TexturedLambert` — declared and used as `mat_wood = TexturedLambert(texture_path=wood_texture_path, ambient=0.15)` if `assets/wood_bark.bmp` exists; fallback to Lambertian otherwise (líneas ~56-66). Archivo: `pikmin_scene.py`.

2) Environment map HDR (evidencia en `pikmin_scene.py` y `HDRTexture.py`)
- `pikmin_scene.py` busca y carga `envmap_path = 'assets/autumn_field_4k.hdr'` y, si existe, instancia `HDRTexture(envmap_path)` (líneas ~644-647). Archivo: `pikmin_scene.py`.
- El archivo `assets/autumn_field_4k.hdr` existe en el directorio `assets/` (ruta verificada en repo: `Proyecto 2/assets/autumn_field_4k.hdr`).
- `HDRTexture.py` proporciona `HDRTexture(path)` con métodos para muestreo (equirectangular), usado por `raytracer` para `sample_envmap_or_black` (consultar `raytracer.py::sample_envmap_or_black`). Archivos: `HDRTexture.py`, `raytracer.py`.

3) Primitivas implementadas (evidencia en `primitives.py`)
- `Capsule` — clase `Capsule` definida en `primitives.py` (línea alrededor de 167). Archivo: `primitives.py`.
- `Cone` — clase `Cone` definida en `primitives.py` (línea alrededor de 235). Archivo: `primitives.py`.
- `Disk` — clase `Disk` definida en `primitives.py` (línea alrededor de 322). Archivo: `primitives.py`.
- `Torus` — clase `Torus` definida en `primitives.py` (línea alrededor de 465). Archivo: `primitives.py`.

4) Modelo OBJ integrado (evidencia en `pikmin_scene.py` y `model.py`)
- `model.py` exporta `OBJModel`, y `.github/copilot-instructions.md` documenta `OBJModel` parsing + `to_triangles(material, transform_matrix)` (ver `./.github/copilot-instructions.md`). Archivo: `model.py` y documentación auxiliar.
- En `pikmin_scene.py` hay código que comprueba `obj_path = "assets/cube.obj"`, carga `OBJModel(obj_path)`, aplica transform y hace `triangles = obj_model.to_triangles(mat_ceramic, transform)` y `objects.extend(triangles)` (líneas ~556-564). Ruta `assets/cube.obj` existe (ver repo). Archivo: `pikmin_scene.py`.

5) Iluminación múltiple (4 luces) (evidencia en `pikmin_scene.py`)
- Definición de 4 luces:
	* `light_sun` — `DirectionalLight(...)` (línea ~604)
	* `light_main` — `PointLight(position=(-2.0, 2.5, 1.5), ...)` (línea ~614)
	* `light_fill` — `PointLight(position=(2.5, 1.8, 0.5), ...)` (línea ~628)
	* `light_spot` — `SpotLight(position=(0.0, 2.0, 1.0), ...)` (línea ~642)
- Las luces se agregan a la lista `lights = [light_sun, light_main, light_fill, light_spot]` y se pasa a `raytracer` dentro de `scene_dict` (línea ~678). Archivo: `pikmin_scene.py`.

6) Escena con >10 objetos (evidencia en `pikmin_scene.py`)
- `pikmin_scene.py` hace múltiples `objects.append(...)` para componer la escena. 

Evidencia visual puntual (en la imagen proporcionada):

- Lambertian: cuerpos y caras de los 3 Pikmin (centro).
- Metal: esfera reflectante arriba-derecha; reflejos difusos en el suelo bajo la escena.
- Refractive: orbe transparente abajo-derecha; botella transparente izquierda.

- Envmap: cielo y horizonte en el fondo; reflejos en esfera metálica y en piso.
- Capsule: cuerpos alargados de los Pikmin (3 cápsulas en el centro).
- Cone: nariz del Pikmin rojo (centro-derecha).
- Disk: discos planos coloreados sobre el suelo (derecha e izquierda).
- Torus: anillo/toro bajo la esfera roja (izquierda).
- OBJ: pequeño cubo entre los Pikmin y la orbe plateada (centro-derecha) corresponde al `cube.obj` o su reemplazo.
- Iluminación múltiple: sombras y especulares en varias direcciones en el suelo y objetos (evidencia visual de múltiples fuentes).
- >10 objetos: más de 10 objetos visibles 

