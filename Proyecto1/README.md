# Proyecto 1 - Rasterizador 3D
**Diego López 23747**

## Lo que hace

Un rasterizador que carga modelos OBJ y los renderiza con diferentes shaders. La escena tiene 4 modelos (gato, perro, caballo, vaca) cada uno con su propio shader.

## Modelos y shaders

- **Gato**: Shader con textura y normal mapping (usa Cat_diffuse.jpg)
- **Perro**: Shader fresnel con efectos de borde brillante (usa Australian_Cattle_Dog_dif.jpg)  
- **Caballo**: Toon shading estilo cartoon (usa Horse_v01.jpg)
- **Vaca**: Shader metálico con reflejos especulares

## Cómo usar

```bash
python main.py --preview    # Renderizado rápido para testing
python main.py             # Renderizado completo con shaders
```

## Archivos importantes

- `main.py` - Script principal
- `Shaders.py` - Todos los shaders implementados
- `Model.py` - Carga de OBJ y texturas
- `renders/` - Aquí van a estar las escenas con los 4 modelos cada uno

Los modelos se cargan automáticamente con sus texturas y cada uno usa un shader diferente. La escena se renderiza en perspectiva con una cámara posicionada para ver todos los modelos.

