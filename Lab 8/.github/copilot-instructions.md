# Copilot Instructions for Lab 8 Graphics Project

## Project Overview
This project is a simple 3D graphics rasterizer implemented in Python, using Pygame for rendering. It is structured around a minimal OpenGL-like pipeline, supporting basic model transformations, custom shaders, and BMP texture handling.

## Key Components
- **Rasterizer2025.py**: Main entry point. Sets up the Pygame window, initializes the renderer, loads models, and handles the main loop and user input.
- **gl.py**: Contains the `Renderer` class, which manages the framebuffer, drawing primitives (points, lines, triangles), and rendering logic.
- **model.py**: Defines the `Model` class, which holds vertex data and transformation parameters. Provides `GetModelMatrix()` for model transformation.
- **MathLib.py**: Provides matrix operations for translation, scaling, and rotation, used for model transformations.
- **shaders.py**: Contains shader functions (e.g., `vertexShader`) that operate on vertices, applying model transformations.
- **BMP_Writer.py**: Utility for writing BMP files from color buffers.
- **BMPTexture.py**: Loads BMP files and provides texture sampling.
- **refractionFunctions.py**: Implements refraction, reflection, and Fresnel equations for advanced shading.

## Developer Workflows
- **Run the project**: Execute `Rasterizer2025.py` to launch the Pygame window and start rendering.
- **Edit shaders**: Modify `shaders.py` to change vertex processing or add new effects.
- **Add models**: Create new `Model` instances in `Rasterizer2025.py` and append them to `rend.models`.
- **Transform models**: Adjust `translation`, `rotation`, and `scale` attributes on `Model` objects.
- **Export images**: Use `GenerateBMP` from `BMP_Writer.py` to save the framebuffer as a BMP file.

## Project-Specific Patterns
- **Vertex data**: Models store vertices as flat lists of floats (x, y, z, ...).
- **Shaders**: Vertex shaders are Python functions assigned to `Model.vertexShader`.
- **Frame buffer**: Managed as a 2D list of color values in `Renderer.frameBuffer`.
- **Color convention**: Colors are floats in [0,1] for internal logic, converted to [0,255] for display/output.
- **Texture sampling**: Use `BMPTexture.getColor(u, v)` for UV-mapped textures.

## Example: Adding a New Model
```python
from model import Model
triangle = Model()
triangle.vertices = [x1, y1, z1, x2, y2, z2, x3, y3, z3]
triangle.vertexShader = vertexShader
rend.models.append(triangle)
```

## External Dependencies
- **Pygame**: Required for windowing and rendering. Install with `pip install pygame`.
- **Numpy**: Used for matrix math. Install with `pip install numpy`.

## Notable Conventions
- All transformations use 4x4 matrices (homogeneous coordinates).
- The rendering pipeline is intentionally simple for educational purposes.
- Keyboard controls in `Rasterizer2025.py` allow interactive model manipulation (arrow keys, 1/2/3 for primitive type).

## See Also
- `Rasterizer2025.py` for main loop and input handling
- `gl.py` for rendering logic
- `shaders.py` for custom shader code
- `BMP_Writer.py` and `BMPTexture.py` for BMP file I/O
