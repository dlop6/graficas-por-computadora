# Plan por fases — Diorama Lab 10

Basado en `docs/instrucciones.txt` y la rúbrica (modelos, shaders, skybox, movimientos de cámara y controles documentados).

**CAMBIO DE DISEÑO**: En lugar de Amaryllis City (muy grande), se usa plataforma procedural simple (stage.py) como base + pokébola + 4 pokémon (bulbasur, charizard, eevee, umbreon) como protagonistas visibles, cada uno con shaders distintos.

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

## Fase 4: Montaje de la plataforma base ✅

- [x] Crear plataforma procedural simple (stage.py) de 60x60 unidades.
- [x] Posicionar en origen para servir de base al diorama.
- [x] Validar dimensiones para alojar los 5 modelos pokémon.

## Fase 5: Colocación de modelos interactivos (pokebola + 4 pokémon) ✅

- [x] Instanciar pokeball, bulbasaur, charizard, eevee, umbreon (5 modelos).
- [x] Asignar `position/rotation/scale` específicas en las 4 esquinas + centro de la plataforma.
- [x] Verificar visibilidad inicial desde cámara orbital.

## Fase 6: Shaders por modelo (requisito rúbrica) ✅

- [x] Seleccionar combinación única (vertex + fragment) para cada modelo usando shaders existentes.
- [x] Compilar y asignar shaderProgram único a cada objeto (plataforma + 5 pokémon).
- [x] Uniforms comunes (luz, time, value) se pasan automáticamente por el renderer.

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
