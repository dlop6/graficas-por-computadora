# Ray Tracer Project — AI Agent Instructions

## Project Overview
This is an educational ray tracer implementing physically-based rendering with custom primitives, materials, and HDR environment maps. The goal is to recreate reference scenes using geometric primitives (30 pts for >10 objects, 20 pts for 4 materials, 5 pts for envmap, 20 pts for 4 new primitives, 20 pts for OBJ model, 20 pts for aesthetics, 10 pts for multi-light).

## Core Architecture

### Rendering Pipeline
1. **Scene Definition** (`scene.py`) → defines camera, objects, materials, lights
2. **Ray Tracer** (`raytracer.py`) → recursive ray tracing with reflection/refraction (max depth 3-5)
3. **Intersection Tests** (`primitives.py`) → ray-geometry intersection algorithms
4. **Material Shading** (`materials.py`) → BRDF evaluation (Lambertian, Metal, Refractive, TexturedLambert)
5. **Output** (`BMP_Writer.py`) → writes 24-bit BMP files from `colorBuffer[x][y]` tuples

### Critical Data Flows
- **Color Buffer Convention**: `colorBuffer[x][y]` indexed as `[WIDTH][HEIGHT]` containing `(r,g,b)` tuples where values are 0-255 integers
- **Ray Direction**: Always normalized in `Ray.__init__()` to prevent accumulated float errors
- **Hit Info**: `HitInfo(t, point, normal, material, uv)` carries all intersection data; normal is auto-normalized
- **Environment Map**: HDR files use equirectangular mapping → sample via `HDRTexture.sample_equirect(direction)` returning float RGB (no clamping until final output)

## Key Implementation Patterns

### Adding New Primitives
New primitives must implement the `intersect(ray)` method returning `HitInfo` or `None`:
```python
class NewPrimitive:
    def intersect(self, ray):
        # 1. Solve ray equation: origin + t * direction = surface
        # 2. Check t > 0.001 to avoid self-intersection
        # 3. Calculate surface normal (must point outward)
        # 4. Compute UV coordinates for texturing
        return HitInfo(t, point, normal, self.material, (u, v))
```
See `Sphere.intersect()` (quadratic equation) and `Cylinder.intersect()` (lateral + caps) for reference.

### Material System
Materials define `shade()` methods with type-specific signatures:
- **Lambertian**: `shade(normal, light_dir, light_color)` → RGB tuple (diffuse + ambient)
- **Metal**: `shade(normal, view_dir, light_dir, light_color)` → `(local_color, reflectivity)`
- **Refractive**: `shade(normal, incident)` → `(Kr, Kt, refracted_dir)` using Fresnel equations
- **TexturedLambert**: `shade_uv(uv, normal, light_dir, light_color)` → samples BMP texture

### Environment Map Integration
HDR envmaps must be sampled in three contexts:
1. **Background**: When `trace()` finds no intersection
2. **Reflections**: Metal materials trace reflected rays
3. **Refractions**: Refractive materials trace transmitted rays

Use `HDRTexture.sample_equirect(direction)` with normalized direction vectors. The class handles equirectangular UV mapping: `u = atan2(z,x)/(2π)+0.5`, `v = acos(y)/π`.

### OBJ Model Loading
`OBJModel` (in `model.py`) parses Wavefront OBJ with vertex/normal/UV indices:
- Stores `vertices`, `normals`, `uvs`, `faces` as lists
- `parse_face_vertex()` handles formats: `v/vt/vn`, `v//vn`, `v/vt`, `v`
- Faces with >3 vertices are fan-triangulated: `[v0, v1, v2], [v0, v2, v3], ...`
- MTL materials are loaded but must be manually mapped to internal material classes

**Important**: OBJ models are NOT automatically integrated into the ray tracer. You must:
1. Convert `OBJModel.faces` into triangle primitives (requires a `Triangle` class)
2. Implement `Triangle.intersect()` using barycentric coordinates or Möller-Trumbore algorithm
3. Add triangle instances to `scene['objects']` list

## Critical Developer Workflows

### Running a Render
```powershell
# Quick preview (low resolution for iteration)
python render_preview.py  # 160x120, ~5-10 seconds

# Scene render (defined in scene.py)
python raytracer_scene.py  # Resolution varies, check scene config

# Custom scene (edit first, then run)
python raytracer.py  # Main entry point
```

### Testing Environment Map Loading
```powershell
python render_preview.py  # Renders just the envmap as background
```
Output saved to `outputs/envmap_preview.bmp`. Verify HDR tone mapping is correct (bright areas shouldn't blow out).

### Phase-Based Development
Follow `plan_fases.md` strictly:
1. **Phase 1-2**: Setup assets and design scene in `docs/scene_plan.md`
2. **Phase 3-4**: Implement geometry and materials (test at 480x270 resolution)
3. **Phase 5-6**: Add envmap and new primitives
4. **Phase 7-8**: Multi-light system and final composition (>10 objects)
5. **Phase 9-10**: Optimization and documentation

Always render previews at low resolution (960x540 or lower) before final 1920x1080 renders.

## Project Conventions

### File Organization
- `assets/` → reference images, HDR envmaps (.hdr), textures (.bmp/.jpg), OBJ models
- `outputs/` → rendered images (.bmp), comparison images
- `docs/` → scene planning (scene_plan.md), project instructions

### Coordinate System
- Right-handed: +X right, +Y up, +Z toward camera
- Camera looks down -Z by default
- Surface normals point outward from objects

### Performance Considerations
- Limit ray depth to 3-5 to prevent stack overflow (controlled by `max_depth` in `raytracer.trace()`)
- Use `t > 0.001` in intersection tests to avoid self-intersection artifacts
- HDR envmaps at 1024×512 are sufficient (4K maps increase memory and sampling time)
- For >1000 triangles in OBJ models, consider spatial acceleration (BVH), but not required for grading

## Common Pitfalls
- **Color Buffer Indexing**: BMP_Writer expects `colorBuffer[x][y]`, not `[y][x]`
- **Normal Direction**: Always normalize and ensure they point outward; reversed normals cause black surfaces
- **HDR Clamping**: Don't clamp HDR values until final output; use tone mapping for realistic bright areas
- **Material Reflection**: Metal materials combine local shading with reflected rays; weigh by reflectivity
- **Refraction Edge Cases**: Handle total internal reflection (when `refractVector` fails, use pure reflection)

## External Dependencies
- `numpy` for vector math (all vectors are `np.array`)
- `struct` for BMP/HDR binary parsing
- No external rendering libraries (intentionally CPU-only educational project)

## Debugging Tips
- Print `hit.t`, `hit.point`, `hit.normal` when surfaces appear black
- Visualize normals as colors: `(normal + 1) * 0.5` maps [-1,1] to [0,1] RGB
- Test single rays: `ray = Ray((0,0,0), (0,0,-1))` and check `object.intersect(ray)`
- For texture issues, render UVs as colors: `(u, v, 0)` shows UV unwrapping

## Scene Requirements Checklist
- [ ] >10 objects (30 pts) — primitives + OBJ model
- [ ] 4 materials: Lambertian, Metal, Refractive, TexturedLambert (20 pts)
- [ ] HDR environment map loaded and sampled (5 pts)
- [ ] 4 new primitives beyond Sphere/Plane/Cylinder (20 pts)
- [ ] 1 OBJ model with ray-traced triangles (20 pts)
- [ ] Multiple lights: directional, point, spotlight (10 pts)
- [ ] Aesthetic composition matching reference image (20 pts)
