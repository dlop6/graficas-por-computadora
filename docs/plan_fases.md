# Plan por fases — Diorama Lab 10

Basado en `docs/instrucciones.txt` y la rúbrica (modelos, shaders, skybox, movimientos de cámara y controles documentados). Escena objetivo: `models/Amaryllis City/OBJ/Amaryllis City.obj` como entorno base + pokébola + pokémon de `models/` (bulbasur, charizard, eve, umbreon), todos visibles dentro de la ciudad y con combinaciones de shaders distintas para cada modelo.

## Fase 1: Inspección de assets
- [ ] Listar assets y rutas finales: ciudad (`Amaryllis City/OBJ/Amaryllis City.obj`), pokeball, bulbasur, charizard, eve, umbreon.
- [ ] Revisar `.mtl` de cada modelo y confirmar texturas referenciadas existen (o anotar faltantes).
- [ ] Notar orientación y escala aproximada de cada modelo (bounds estimados) para preparar transformaciones.

## Fase 2: Limpieza del código legado (lab anterior) ✅

- [x] Remover lógica de "un solo modelo activo" y el ciclo de cambio M/N/B.
- [x] Quitar rotación automática global si no aporta a la escena final (dejar opcional para debug).
- [x] Eliminar dependencias de cámara al "modelo activo"; dejar cámara independiente con target configurable.
- [x] Depurar prints/boilerplate del montaje viejo.

## Fase 3: Configuración base del renderer ✅

- [x] Mantener resolución inicial (960x540) y estados GL necesarios (depth, culling desactivado si lo requiere la visibilidad).
- [x] Revisar y ajustar luz puntual y luz ambiente para buena lectura de la ciudad y los modelos.
- [x] Confirmar skybox se crea y dibuja antes de los modelos sin escribir al depth buffer (ya soportado).

## Fase 4: Montaje de la ciudad (entorno) ✅

- [x] Cargar `Amaryllis City.obj` con sus materiales/texturas.
- [x] Ajustar `position/rotation/scale` para centrar la ciudad en torno al origen y apoyar el piso en Y≈0.
- [x] Validar que el origin y la escala permiten alojar los otros modelos dentro de calles/plazas.

## Fase 5: Colocación de modelos interactivos (pokebola + 4 pokémon)
- [ ] Instanciar pokeball, bulbasur, charizard, eve, umbreon (5 modelos contabilizables; la ciudad cuenta como base).
- [ ] Asignar `position/rotation/scale` específicas para ubicarlos dentro de la ciudad, evitando solapes y hundimiento.
- [ ] Verificar visibilidad inicial desde una cámara general (sin depender de saltos de vista).

## Fase 6: Shaders por modelo (requisito rúbrica)
- [ ] Seleccionar combinación única (vertex + fragment) para cada modelo (ciudad incluida) usando los shaders existentes.
- [ ] Setear uniforms comunes (luz puntual, ambient, `time`, `value`) y, si es necesario, parámetros por modelo sin romper la regla de “shader distinto”.
- [ ] Opcional: exponer teclas para ciclar shaders de un modelo solo si ayuda a demostrar; por defecto cada modelo queda con su shader asignado.

## Fase 7: Cámara y controles (teclado + mouse)
- [ ] Orbitar/circular: A/D (y mouse drag) alrededor del `cameraTarget`.
- [ ] Zoom in/out: Q/E y rueda del mouse; clamp de distancias.
- [ ] Movimiento vertical: W/S para pitch vertical (clamp de ángulo).
- [ ] Saltos de vista: hotkeys (p.ej. 1-5) que ponen `cameraTarget` en cada modelo/punto de interés de la escena.
- [ ] Confirmar que los tres movimientos funcionan tanto con mouse (rotación + rueda) como con teclado (A/D, W/S, Q/E).

## Fase 8: Postprocesos y extras (solo si aportan y cumplen instrucciones)
- [ ] Decidir si activar un postproceso ligero (fog/DOF/outline) sin comprometer visibilidad; si no es necesario, dejar desactivado.
- [ ] Dejar el toggle documentado si se usa.

## Fase 9: Documentación y controles
- [ ] Actualizar README con: lista de modelos usados, shaders asignados por modelo, controles de cámara (teclado + mouse), teclas de saltos de vista, y cualquier toggle extra.
- [ ] Incluir nota de input requerido por la rúbrica y breve descripción estética/creativa del diorama.
- [ ] Anotar uso de IA y esta conversación según instrucciones.

## Fase 10: Pruebas y verificación final
- [ ] Smoke test: arrancar app, cargar 6 objetos (ciudad + 5 modelos), sin errores de texturas/paths.
- [ ] Verificar que todos los modelos son visibles dentro de la ciudad con sus escalas y shaders correctos.
- [ ] Probar controles: orbit, zoom, vertical, rueda, mouse drag, hotkeys de salto de vista.
- [ ] Validar skybox visible y no interfiere con depth; confirmar rendimiento aceptable en 960x540.
- [ ] Ajustes finales de posición/luz si algún modelo queda fuera de vista o clippea.
