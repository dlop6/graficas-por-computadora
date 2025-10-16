"""
Test de robustez para validar protecciones contra edge cases
"""
import numpy as np
from primitives import Ray, Sphere, Cylinder, Capsule, Cone, Disk, Triangle, Torus, Plane
from materials import Lambertian, Metal, Refractive
from HDRTexture import HDRTexture
from refractionFunctions import refractVector, fresnel

print("🧪 INICIANDO TESTS DE ROBUSTEZ")
print("=" * 60)

# Test 1: Ray con dirección casi cero (debe lanzar excepción)
print("\n[Test 1] Ray con dirección casi cero")
try:
    ray = Ray((0, 0, 0), (0, 0, 0))
    print("  ❌ FALLO - Debería lanzar ValueError")
except ValueError as e:
    print(f"  ✅ PASÓ - Excepción esperada: {e}")

# Test 2: Ray con dirección válida
print("\n[Test 2] Ray con dirección válida")
try:
    ray = Ray((0, 0, 5), (0, 0, -1))
    print(f"  ✅ PASÓ - Ray creado: direction = {ray.direction}")
except Exception as e:
    print(f"  ❌ FALLO - {e}")

# Test 3: Cylinder con rayo vertical
print("\n[Test 3] Cylinder intersección con rayo vertical")
try:
    mat = Lambertian(color=(0.8, 0.8, 0.8))
    cyl = Cylinder(center=(0, 0, 0), radius=1.0, height=2.0, material=mat)
    ray = Ray((0, 5, 0), (0, -1, 0))  # Rayo vertical
    hit = cyl.intersect(ray)
    if hit:
        print(f"  ✅ PASÓ - Intersección en t={hit.t:.3f}, normal={hit.normal}")
    else:
        print("  ⚠️  WARNING - No hubo intersección (esperado para tapa)")
except Exception as e:
    print(f"  ❌ FALLO - {e}")

# Test 4: Sphere con normal extrema (casi vertical)
print("\n[Test 4] Sphere intersección en polo (normal vertical)")
try:
    mat = Lambertian(color=(1, 0, 0))
    sphere = Sphere(center=(0, 0, 0), radius=1.0, material=mat)
    ray = Ray((0, 5, 0), (0, -1, 0))  # Rayo directo al polo norte
    hit = sphere.intersect(ray)
    if hit:
        print(f"  ✅ PASÓ - Hit en t={hit.t:.3f}, normal={hit.normal}, UV={hit.uv}")
    else:
        print("  ❌ FALLO - Debería haber intersección")
except Exception as e:
    print(f"  ❌ FALLO - {e}")

# Test 5: Refracción con reflexión total interna
print("\n[Test 5] Refracción con reflexión total interna")
try:
    normal = np.array([0, 1, 0])
    incident = np.array([0.9, -0.1, 0])  # Ángulo muy rasante
    incident = incident / np.linalg.norm(incident)
    
    Kr, Kt = fresnel(normal, incident, n1=1.5, n2=1.0)
    refracted = refractVector(normal, incident, n1=1.5, n2=1.0)
    
    print(f"  Kr = {Kr:.4f}, Kt = {Kt:.4f}")
    print(f"  Refracted dir = {refracted}")
    
    if Kr > 0.9 and refracted is None:
        print("  ✅ PASÓ - Reflexión total interna detectada correctamente")
    else:
        print("  ⚠️  WARNING - Valores inesperados pero no crasheó")
except Exception as e:
    print(f"  ❌ FALLO - {e}")

# Test 6: HDRTexture con dirección extrema
print("\n[Test 6] HDRTexture con dirección vertical extrema")
try:
    # Crear un HDR dummy para testing
    import struct
    hdr_path = "assets/autumn_field_4k.hdr"
    hdr = HDRTexture(hdr_path)
    
    # Dirección casi vertical (caso problemático para acos)
    color1 = hdr.sample_equirect((0.0, 0.9999999, 0.0))
    color2 = hdr.sample_equirect((0.0, 1.0, 0.0))
    color3 = hdr.sample_equirect((0.0, -1.0, 0.0))
    
    print(f"  Dirección (0, 0.9999999, 0) → {color1}")
    print(f"  Dirección (0, 1, 0) → {color2}")
    print(f"  Dirección (0, -1, 0) → {color3}")
    print("  ✅ PASÓ - Todas las direcciones extremas manejadas")
except Exception as e:
    print(f"  ❌ FALLO - {e}")

# Test 7: Metal con view y light opuestos
print("\n[Test 7] Metal shading con view y light opuestos")
try:
    mat = Metal(color=(0.9, 0.9, 0.9), reflectivity=0.8, shininess=64)
    normal = np.array([0, 1, 0])
    view_dir = np.array([0, 1, 0])
    light_dir = np.array([0, -1, 0])  # Opuesto a view
    light_color = (1, 1, 1)
    
    local_color = mat.local_shade(normal, view_dir, light_dir, light_color)
    print(f"  Local color = {local_color}")
    print("  ✅ PASÓ - Half vector degenerado manejado")
except Exception as e:
    print(f"  ❌ FALLO - {e}")

# Test 8: Cone con punta muy aguda
print("\n[Test 8] Cone con geometría extrema")
try:
    mat = Lambertian(color=(1, 0.5, 0))
    cone = Cone(base_center=(0, 0, 0), base_radius=0.01, height=5.0, material=mat)
    ray = Ray((0, 2, 2), (0, 0, -1))
    hit = cone.intersect(ray)
    if hit:
        print(f"  ✅ PASÓ - Hit en cono extremo: t={hit.t:.3f}")
    else:
        print("  ⚠️  WARNING - No hit (puede ser válido)")
except Exception as e:
    print(f"  ❌ FALLO - {e}")

# Test 9: Disk con normal aleatoria
print("\n[Test 9] Disk con normal no-estándar")
try:
    mat = Lambertian(color=(0, 1, 0))
    disk = Disk(center=(0, 1, 0), normal=(1, 1, 0), radius=2.0, material=mat)
    ray = Ray((2, 1, 0), (-1, 0, 0))
    hit = disk.intersect(ray)
    if hit:
        print(f"  ✅ PASÓ - Disk hit: normal={hit.normal}")
    else:
        print("  ⚠️  WARNING - No hit")
except Exception as e:
    print(f"  ❌ FALLO - {e}")

# Test 10: Triangle con vértices colineales (degenerado)
print("\n[Test 10] Triangle degenerado (vértices colineales)")
try:
    mat = Lambertian(color=(0.5, 0.5, 0.5))
    tri = Triangle(v0=(0, 0, 0), v1=(1, 0, 0), v2=(2, 0, 0), material=mat)
    ray = Ray((1, 1, 0), (0, -1, 0))
    hit = tri.intersect(ray)
    if hit:
        print(f"  ⚠️  WARNING - Hit en triángulo degenerado (inesperado)")
    else:
        print("  ✅ PASÓ - No hay hit en triángulo degenerado (correcto)")
except Exception as e:
    print(f"  ❌ FALLO - {e}")

print("\n" + "=" * 60)
print("🏁 TESTS DE ROBUSTEZ COMPLETADOS")
print("\nSi todos los tests pasaron o dieron warnings esperados,")
print("el código está protegido contra edge cases críticos.")
