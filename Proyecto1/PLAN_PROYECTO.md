# Plan Estratégico y Detallado para el Proyecto de Rasterizador

## Objetivo
Desarrollar un rasterizador en Python capaz de cargar y renderizar múltiples modelos `.obj` texturizados, aplicando diferentes shaders avanzados, y generando una escena final en formato BMP, cumpliendo todos los criterios de evaluación del curso.

---

## Fase 1: Preparación y Organización

1. **Revisión de requisitos y criterios de evaluación**
   - Analizar cada punto de la rúbrica para no dejar ningún objetivo sin cubrir.
2. **Organización de carpetas y archivos**
   - Estructura clara: `Proyecto1/` con subcarpetas `obj/`, `render/`, y archivos de código.
   - Eliminar archivos y carpetas innecesarias (`__pycache__`, backups, etc.).
3. **Control de versiones**
   - Confirmar que el repositorio está limpio y sincronizado con remoto.
   - Hacer commits frecuentes y descriptivos.

---

## Fase 2: Modelos y Recursos

1. **Selección de modelos**
   - Descargar 4 modelos `.obj` distintos (no usados en clase, al menos uno complejo).
   - Verificar que cada modelo tenga su archivo `.mtl` y texturas asociadas.
   - Probar que los modelos abran correctamente en un visualizador externo (Blender, MeshLab).
2. **Ubicación de modelos**
   - Colocar todos los modelos y texturas en `Proyecto1/obj/`.
   - Renombrar archivos para evitar espacios y caracteres raros.

---

## Fase 3: Carga y Transformación de Modelos

1. **Carga robusta de modelos**
   - Probar la función de carga de `.obj` con cada modelo.
   - Manejar errores comunes: rutas incorrectas, texturas faltantes, UVs fuera de rango.
2. **Transformaciones individuales**
   - Aplicar traslación, rotación y escala a cada modelo para que no se encimen.
   - Verificar que todos los modelos sean visibles en la escena.

---

## Fase 4: Shaders y Texturizado

1. **Implementación de shaders**
   - Tener al menos 4 shaders distintos y no triviales (toon, checkerboard, fresnel, multi-light, etc.).
   - Implementar normal mapping o bump mapping y aplicarlo a un modelo no trivial.
2. **Asignación de shaders**
   - Asignar un shader diferente a cada modelo.
   - Verificar que cada shader funcione correctamente y que no haya duplicidad de efectos.
3. **Texturizado**
   - Asegurarse de que todos los modelos usen texturas y que se mapeen correctamente.

---

## Fase 5: Cámara, Iluminación y Escena

1. **Configuración de cámara**
   - Usar proyección en perspectiva.
   - Ajustar la posición y orientación para que todos los modelos sean visibles y la escena sea estética.
2. **Iluminación**
   - Definir al menos una luz direccional.
   - Ajustar intensidades y colores para resaltar los efectos de los shaders.

---

## Fase 6: Renderizado y Exportación

1. **Render final**
   - Renderizar la escena completa y guardar el resultado en `Proyecto1/render/escena_final.bmp`.
   - Verificar que la imagen tenga buena resolución y todos los modelos sean visibles.
2. **Pruebas de robustez**
   - Probar con modelos/texturas faltantes para asegurar que el programa no crashee.
   - Validar que los shaders no generen artefactos visuales.

---

## Fase 7: Documentación y Entrega

1. **README.md**
   - Explicar cómo correr el proyecto, qué modelos y shaders se usaron, y cómo se cumplen los criterios de la rúbrica.
   - Incluir capturas del render final y, si es posible, un análisis breve de los resultados.
2. **Checklist de entrega**
   - Confirmar que todos los archivos necesarios están en el repositorio.
   - Eliminar archivos temporales y limpiar el proyecto.
   - Subir el render final al canal ShowOff de Discord.

---

## Fase 8: Prevención de Errores y Buenas Prácticas

- **Validar rutas y nombres de archivos** para evitar errores de carga.
- **Hacer pruebas incrementales**: después de cada fase, probar el sistema antes de avanzar.
- **Control de versiones**: commits frecuentes y claros, especialmente antes de cambios grandes.
- **Revisar dependencias**: asegurar que `numpy`, `pygame` y cualquier otra librería estén instaladas y documentadas.
- **Evitar hardcodear rutas absolutas**: usar rutas relativas para portabilidad.
- **Manejo de errores**: capturar y mostrar mensajes claros si falta un archivo o textura.
- **Revisar la estética**: ajustar cámara, luces y colores para que la escena sea atractiva.
- **No dejar para el final la documentación ni la limpieza del código**.

---

## Fase 9: Revisión Final y Backup

- Hacer una última revisión de todo el proyecto.
- Probar el render en otra máquina si es posible.
- Hacer un backup del proyecto antes de la entrega.

---

**Con este plan, se cubren todos los criterios de la rúbrica, se minimizan riesgos y se asegura una entrega profesional y funcional.**
