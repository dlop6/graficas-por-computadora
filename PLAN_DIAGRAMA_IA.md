# Planificación exhaustiva para agente de IA: Diorama Pokémon + Amaryllis City

## Instrucciones generales
Este documento describe, paso a paso y por fases, todo lo que un agente de IA debe realizar para transformar el proyecto existente en un diorama 3D con Amaryllis City como fondo y modelos de Pokémon como objetos principales. **No omitir ni asumir nada.** Cada fase debe ser completada y reportada antes de pasar a la siguiente, esperando autorización explícita.

---

## Fase 1: Auditoría y limpieza del código
**Objetivo:** Eliminar toda referencia, lógica y assets de proyectos anteriores (Iron Golem, T-Rex, Titan, etc.) y dejar la base lista para el nuevo diorama.

### Pasos detallados:
1. Revisar todos los archivos `.py` del proyecto.
2. Identificar y eliminar:
   - Cualquier referencia a modelos antiguos (Iron Golem, T-Rex, Titan, etc.) en código, comentarios, variables, input, etc.
   - Lógica de cambio de modelo que no corresponda a los Pokémon o Amaryllis City.
   - Carga de texturas, posiciones, escalas, o shaders asociados a modelos antiguos.
   - Menús, mensajes, prints, o documentación interna que mencione los modelos antiguos.
3. Verificar que el código compile y corra (aunque no muestre modelos).
4. Reportar los archivos modificados y los cambios realizados.
5. Esperar autorización para continuar a la siguiente fase.

---

## Fase 2: Preparación y prueba de assets
**Objetivo:** Garantizar que todos los modelos y texturas a usar estén en formato correcto y se puedan cargar sin errores.

### Pasos detallados:
1. Listar todos los modelos de Pokémon y el modelo de Amaryllis City en la carpeta `models/`.
2. Verificar que cada modelo esté en formato `.obj` y tenga su(s) textura(s) asociada(s) en la carpeta correspondiente.
3. Probar la carga de cada modelo individualmente usando la clase `Model` y reportar si hay errores de parsing, texturas faltantes, o problemas de escala.
4. Documentar la ruta y nombre de cada modelo y textura que se usará.
5. Esperar autorización para continuar a la siguiente fase.

---

## Fase 3: Carga y posicionamiento de modelos en la escena
**Objetivo:** Cargar Amaryllis City como fondo y los Pokémon como objetos principales, todos visibles simultáneamente y bien posicionados.

### Pasos detallados:
1. Modificar el loop principal (`RendererOpenGL2025.py`) para:
   - Cargar el modelo de Amaryllis City y posicionarlo como fondo (ajustar escala y posición para que abarque la escena).
   - Cargar al menos 4-5 modelos de Pokémon y posicionarlos en lugares lógicos y variados dentro de la ciudad.
   - Ajustar la escala de cada Pokémon para que tenga proporciones creíbles respecto a la ciudad y entre sí.
   - Si es necesario, agregar un modelo de piso/base.
2. Asegurarse de que todos los modelos estén presentes en la lista `rend.scene` y se rendericen juntos.
3. Reportar la posición, escala y nombre de cada modelo en la escena.
4. Esperar autorización para continuar a la siguiente fase.

---

## Fase 4: Implementación de la cámara y cambio de foco
**Objetivo:** Implementar una cámara orbital completa, con la capacidad de cambiar el foco entre los Pokémon usando input.

### Pasos detallados:
1. Revisar y, si es necesario, modificar la clase `Camera` y el loop principal para:
   - Permitir orbitar, hacer zoom y desplazamiento vertical con teclado y mouse.
   - Implementar input (por ejemplo, teclas numéricas) para cambiar el foco de la cámara entre cada Pokémon.
   - Asegurarse de que la cámara nunca atraviese el modelo de la ciudad ni se aleje demasiado.
2. Documentar los controles de cámara y cambio de foco.
3. Reportar la implementación y controles definidos.
4. Esperar autorización para continuar a la siguiente fase.

---

## Fase 5: Asignación de shaders creativos por modelo
**Objetivo:** Cada Pokémon debe tener una combinación de shaders diferente y creativa.

### Pasos detallados:
1. Revisar los archivos `fragmentShaders.py` y `vertexShaders.py`.
2. Asignar un shader diferente a cada Pokémon (puede ser combinación de fragment y vertex shaders).
3. Permitir modificar parámetros de los shaders en tiempo real mediante input (por ejemplo, teclas para cambiar color, intensidad, efectos).
4. Si es posible, implementar algún geometry shader o efecto de deformación para algún modelo.
5. El modelo de la ciudad puede tener un shader más simple o uno que simule ambiente/iluminación global.
6. Documentar la asignación de shaders y los controles para modificarlos.
7. Reportar la implementación y combinaciones usadas.
8. Esperar autorización para continuar a la siguiente fase.

---

## Fase 6: Skybox y ambiente
**Objetivo:** Mejorar la inmersión visual con un skybox/cubemap y buena iluminación.

### Pasos detallados:
1. Asegurarse de que el skybox se muestre correctamente y combine con la escena.
2. Ajustar la iluminación global y la luz puntual para que los modelos se vean bien integrados.
3. Documentar la configuración del skybox y la iluminación.
4. Reportar la implementación.
5. Esperar autorización para continuar a la siguiente fase.

---

## Fase 7: Extras y pulido
**Objetivo:** Sumar puntos extra y mejorar la experiencia y estética.

### Pasos detallados:
1. Agregar música de fondo y/o efectos de sonido (al cambiar de modelo, por ejemplo).
2. Implementar un menú simple para seleccionar modelos o cambiar shaders.
3. Agregar post-processing si es posible (bloom, color grading, etc).
4. Mejorar la estética: detalles, texturas, composición visual.
5. Documentar todos los extras implementados y sus controles.
6. Reportar la implementación.
7. Esperar autorización para continuar a la siguiente fase.

---

## Fase 8: Documentación y entrega
**Objetivo:** Cumplir con los requisitos de entrega y claridad.

### Pasos detallados:
1. Documentar todos los controles y funcionalidades en el README.
2. Explicar cómo cambiar de modelo, de cámara, de shader, etc.
3. Si se usó IA, adjuntar la conversación y explicar cómo se usó.
4. Hacer pruebas finales y grabar un video o tomar capturas para mostrar el diorama.
5. Reportar la documentación final y los archivos de entrega.
6. Esperar confirmación final de cierre del proyecto.

---

**Nota:** No avanzar a la siguiente fase sin autorización explícita. Cada reporte debe ser claro, detallado y enumerar los cambios realizados.
