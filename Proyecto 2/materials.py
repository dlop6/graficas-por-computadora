import math
import numpy as np
from BMPTexture import BMPTexture
from refractionFunctions import refractVector, fresnel

# Utility functions

def normalize(v):
    v = np.array(v, dtype=float)
    n = np.linalg.norm(v)
    if n == 0:
        return v
    return v / n

def clamp01(c):
    return max(0.0, min(1.0, c))


def lambert_shade(color, normal, light_dir, light_color, ambient=0.15):
    n = normalize(normal)
    l = normalize(light_dir)
    ndotl = max(0.0, np.dot(n, l))
    diffuse = np.array(color) * ndotl
    ambient_col = np.array(color) * ambient
    return np.clip((ambient_col + diffuse) * np.array(light_color), 0.0, 1.0)


class Lambertian:
    """Diffuse material (Lambertian)."""
    def __init__(self, color=(0.8,0.8,0.8), ambient=0.15):
        self.color = tuple(color)
        self.ambient = ambient

    def shade(self, normal, light_dir, light_color):
        return tuple(lambert_shade(self.color, normal, light_dir, light_color, ambient=self.ambient))


class Metal:
    """Metallic material: mix of reflective component and Blinn-Phong local shading."""
    def __init__(self, color=(0.9,0.9,0.95), reflectivity=0.85, shininess=64):
        self.color = tuple(color)
        self.reflectivity = clamp01(reflectivity)
        self.shininess = shininess

    def local_shade(self, normal, view_dir, light_dir, light_color):
        n = normalize(normal)
        l = normalize(light_dir)
        v = normalize(view_dir)
        h = normalize(v + l)
        ndotl = max(0.0, np.dot(n, l))
        ndoth = max(0.0, np.dot(n, h))
        diffuse = np.array(self.color) * ndotl * 0.3
        spec = np.array(light_color) * (ndoth ** (self.shininess))
        return np.clip(diffuse + spec, 0.0, 1.0)

    def shade(self, normal, view_dir, light_dir, light_color):
        # returns (local_color, reflectivity)
        return tuple(self.local_shade(normal, view_dir, light_dir, light_color)), self.reflectivity


class Refractive:
    """Simple refractive material using Snell's law for transmitted direction and Fresnel for mix.
    For this helper we return (Kr, Kt, refracted_dir) where Kr is reflection ratio, Kt transmission ratio.
    """
    def __init__(self, ior=1.5, tint=(0.95,0.98,1.0), transparency=0.9):
        self.ior = ior
        self.tint = tuple(tint)
        self.transparency = clamp01(transparency)

    def shade(self, normal, incident, n1=1.0):
        n = normalize(normal)
        i = normalize(incident)
        Kr, Kt = fresnel(n, i, n1, self.ior)
        refracted = None
        try:
            refracted = refractVector(n, i, n1, self.ior)
        except Exception:
            refracted = None
        return Kr, Kt * self.transparency, refracted


class TexturedLambert:
    """Lambertian material that samples a BMP texture by UV coordinates."""
    def __init__(self, texture_path, wrap=True, ambient=0.12):
        self.tex = BMPTexture(texture_path)
        self.wrap = wrap
        self.ambient = ambient

    def shade_uv(self, uv, normal, light_dir, light_color):
        u, v = uv
        if self.wrap:
            u = u % 1.0
            v = v % 1.0
        c = self.tex.getColor(u, v)
        if c is None:
            base = (0.8, 0.8, 0.8)
        else:
            base = tuple(c)
        return tuple(lambert_shade(base, normal, light_dir, light_color, ambient=self.ambient))
