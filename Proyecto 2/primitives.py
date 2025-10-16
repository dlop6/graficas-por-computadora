import math
import numpy as np


class Ray:
    """Representa un rayo en 3D."""
    def __init__(self, origin, direction):
        self.origin = np.array(origin, dtype=float)
        dir_norm = np.linalg.norm(direction)
        if dir_norm < 1e-10:
            raise ValueError("Ray direction cannot be zero vector")
        self.direction = np.array(direction, dtype=float) / dir_norm
    
    def at(self, t):
        """Retorna el punto en el rayo a distancia t."""
        return self.origin + t * self.direction


class HitInfo:
    """Información de intersección rayo-objeto."""
    def __init__(self, t, point, normal, material, uv=(0, 0)):
        self.t = t
        self.point = point
        self.normal = np.array(normal, dtype=float)
        norm_len = np.linalg.norm(self.normal)
        if norm_len < 1e-10:
            self.normal = np.array([0, 1, 0], dtype=float)  # Fallback seguro
        else:
            self.normal = self.normal / norm_len
        self.material = material
        self.uv = uv


class Sphere:
    """Esfera con centro y radio."""
    def __init__(self, center, radius, material):
        self.center = np.array(center, dtype=float)
        self.radius = float(radius)
        self.material = material
    
    def intersect(self, ray):
        """Ray-sphere intersection usando ecuación cuadrática."""
        oc = ray.origin - self.center
        a = np.dot(ray.direction, ray.direction)
        b = 2.0 * np.dot(oc, ray.direction)
        c = np.dot(oc, oc) - self.radius ** 2
        discriminant = b * b - 4 * a * c
        
        if discriminant < 0:
            return None
        
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        
        t = t1 if t1 > 0.001 else t2
        if t <= 0.001:
            return None
        
        point = ray.at(t)
        normal = (point - self.center) / self.radius
        # UV spherical (con protección de dominio)
        phi = math.atan2(normal[2], normal[0])
        # Clamp normal[1] al rango [-1, 1] para evitar domain errors
        normal_y_clamped = max(-1.0, min(1.0, normal[1]))
        theta = math.acos(normal_y_clamped)
        u = (phi + math.pi) / (2 * math.pi)
        v = theta / math.pi
        
        return HitInfo(t, point, normal, self.material, (u, v))


class Plane:
    """Plano definido por punto y normal."""
    def __init__(self, point, normal, material, scale=10.0):
        self.point = np.array(point, dtype=float)
        self.normal = np.array(normal, dtype=float) / np.linalg.norm(normal)
        self.material = material
        self.scale = scale
    
    def intersect(self, ray):
        """Ray-plane intersection."""
        denom = np.dot(ray.direction, self.normal)
        if abs(denom) < 1e-6:
            return None
        
        t = np.dot(self.point - ray.origin, self.normal) / denom
        if t <= 0.001:
            return None
        
        point = ray.at(t)
        
        # Calcular UV usando proyección
        v_right = np.array([-self.normal[1], self.normal[0], 0], dtype=float)
        if np.linalg.norm(v_right) < 1e-6:
            v_right = np.array([1, 0, 0], dtype=float)
        v_right = v_right / np.linalg.norm(v_right)
        v_up = np.cross(self.normal, v_right)
        
        offset = point - self.point
        u = (np.dot(offset, v_right) / self.scale) % 1.0
        v = (np.dot(offset, v_up) / self.scale) % 1.0
        
        return HitInfo(t, point, self.normal, self.material, (u, v))


class Cylinder:
    """Cilindro vertical con centro en la base, radio y altura."""
    def __init__(self, center, radius, height, material):
        self.center = np.array(center, dtype=float)
        self.radius = float(radius)
        self.height = float(height)
        self.material = material
    
    def intersect(self, ray):
        """Ray-cylinder intersection (aproximado con dos capas y lateral)."""
        # Intersección con el cilindro lateral
        oc = ray.origin - self.center
        oc_xz = np.array([oc[0], 0, oc[2]])
        dir_xz = np.array([ray.direction[0], 0, ray.direction[2]])
        
        a = np.dot(dir_xz, dir_xz)
        
        # Proteger contra división por cero (rayo vertical)
        if a < 1e-10:
            # Rayo casi vertical, saltear intersección lateral
            pass
        else:
            b = 2.0 * np.dot(oc_xz, dir_xz)
            c = np.dot(oc_xz, oc_xz) - self.radius ** 2
            
            discriminant = b * b - 4 * a * c
            if discriminant >= 0:
                sqrt_disc = math.sqrt(max(0, discriminant))
                t1 = (-b - sqrt_disc) / (2 * a)
                t2 = (-b + sqrt_disc) / (2 * a)
            
                for t in sorted([t1, t2]):
                    if t > 0.001:
                        point = ray.at(t)
                        if 0 <= point[1] - self.center[1] <= self.height:
                            normal = (point - self.center) * np.array([1, 0, 1])
                            norm_len = np.linalg.norm(normal)
                            if norm_len < 1e-10:
                                continue  # Skip invalid normal
                            normal = normal / norm_len
                            phi = math.atan2(point[2] - self.center[2], point[0] - self.center[0])
                            u = (phi + math.pi) / (2 * math.pi)
                            v = (point[1] - self.center[1]) / self.height
                            return HitInfo(t, point, normal, self.material, (u, v))
        
        # Intersección con tapa superior e inferior
        for y_target in [self.center[1], self.center[1] + self.height]:
            if abs(ray.direction[1]) > 1e-6:
                t = (y_target - ray.origin[1]) / ray.direction[1]
                if t > 0.001:
                    point = ray.at(t)
                    dist_sq = (point[0] - self.center[0]) ** 2 + (point[2] - self.center[2]) ** 2
                    if dist_sq <= self.radius ** 2:
                        normal = np.array([0, 1 if y_target > self.center[1] else -1, 0], dtype=float)
                        u = (point[0] - self.center[0] + self.radius) / (2 * self.radius)
                        v = (point[2] - self.center[2] + self.radius) / (2 * self.radius)
                        return HitInfo(t, point, normal, self.material, (u, v))
        
        return None


class Capsule:
    """Cápsula: cilindro con hemisferios en los extremos.
    Útil para cuerpos de personajes tipo Pikmin."""
    def __init__(self, center, radius, height, material):
        self.center = np.array(center, dtype=float)
        self.radius = float(radius)
        self.height = float(height)  # altura del cilindro central
        self.material = material
    
    def intersect(self, ray):
        """Ray-capsule intersection: cilindro + 2 hemisferios."""
        best_hit = None
        min_t = float('inf')
        
        # 1. Intersección con cilindro central (sin tapas)
        oc = ray.origin - self.center
        oc_xz = np.array([oc[0], 0, oc[2]])
        dir_xz = np.array([ray.direction[0], 0, ray.direction[2]])
        
        a = np.dot(dir_xz, dir_xz)
        if a > 1e-6:  # Evitar división por cero
            b = 2.0 * np.dot(oc_xz, dir_xz)
            c = np.dot(oc_xz, oc_xz) - self.radius ** 2
            
            discriminant = b * b - 4 * a * c
            if discriminant >= 0:
                t1 = (-b - math.sqrt(discriminant)) / (2 * a)
                t2 = (-b + math.sqrt(discriminant)) / (2 * a)
                
                for t in [t1, t2]:
                    if t > 0.001 and t < min_t:
                        point = ray.at(t)
                        y_local = point[1] - self.center[1]
                        # Solo cuenta si está en la región del cilindro
                        if 0 <= y_local <= self.height:
                            normal = (point - self.center) * np.array([1, 0, 1])
                            norm_len = np.linalg.norm(normal)
                            if norm_len < 1e-10:
                                continue  # Skip invalid normal
                            normal = normal / norm_len
                            phi = math.atan2(point[2] - self.center[2], point[0] - self.center[0])
                            u = (phi + math.pi) / (2 * math.pi)
                            v = y_local / (self.height + 2 * self.radius)
                            best_hit = HitInfo(t, point, normal, self.material, (u, v))
                            min_t = t
        
        # 2. Hemisferio inferior (centro en base)
        sphere_bottom = Sphere(self.center, self.radius, self.material)
        hit_bottom = sphere_bottom.intersect(ray)
        if hit_bottom and hit_bottom.t < min_t:
            # Solo cuenta si está en la mitad inferior
            if hit_bottom.point[1] <= self.center[1]:
                best_hit = hit_bottom
                min_t = hit_bottom.t
        
        # 3. Hemisferio superior (centro en tope)
        top_center = self.center + np.array([0, self.height, 0])
        sphere_top = Sphere(top_center, self.radius, self.material)
        hit_top = sphere_top.intersect(ray)
        if hit_top and hit_top.t < min_t:
            # Solo cuenta si está en la mitad superior
            if hit_top.point[1] >= top_center[1]:
                best_hit = hit_top
                min_t = hit_top.t
        
        return best_hit


class Cone:
    """Cono con base circular en el origen y punta hacia arriba.
    Útil para narices, sombreros, detalles decorativos."""
    def __init__(self, base_center, base_radius, height, material):
        self.base_center = np.array(base_center, dtype=float)
        self.base_radius = float(base_radius)
        self.height = float(height)
        self.material = material
        self.apex = self.base_center + np.array([0, height, 0])
    
    def intersect(self, ray):
        """Ray-cone intersection usando ecuación cuadrática."""
        # Transformar rayo a espacio local del cono
        oc = ray.origin - self.base_center
        d = ray.direction
        
        # Parámetros del cono: x^2 + z^2 = (r * (h - y) / h)^2
        k = (self.base_radius / self.height) ** 2
        
        # Ecuación cuadrática: a*t^2 + b*t + c = 0
        a = d[0]**2 + d[2]**2 - k * d[1]**2
        b = 2 * (oc[0]*d[0] + oc[2]*d[2] - k*oc[1]*d[1] + k*self.height*d[1])
        c = oc[0]**2 + oc[2]**2 - k*(oc[1]**2 - 2*self.height*oc[1] + self.height**2)
        
        discriminant = b**2 - 4*a*c
        
        if discriminant < 0:
            return self._intersect_base(ray)
        
        # Encontrar la intersección más cercana
        sqrt_disc = math.sqrt(discriminant)
        t1 = (-b - sqrt_disc) / (2*a) if abs(a) > 1e-6 else float('inf')
        t2 = (-b + sqrt_disc) / (2*a) if abs(a) > 1e-6 else float('inf')
        
        for t in sorted([t1, t2]):
            if t > 0.001:
                point = ray.at(t)
                y_local = point[1] - self.base_center[1]
                
                # Verificar que está dentro de los límites del cono
                if 0 <= y_local <= self.height:
                    # Calcular normal
                    r = math.sqrt((point[0] - self.base_center[0])**2 + 
                                 (point[2] - self.base_center[2])**2)
                    # Normal del cono: perpendicular a la superficie
                    normal = np.array([
                        point[0] - self.base_center[0],
                        r * self.base_radius / self.height,
                        point[2] - self.base_center[2]
                    ], dtype=float)
                    norm_len = np.linalg.norm(normal)
                    if norm_len < 1e-10:
                        continue  # Skip invalid normal
                    normal = normal / norm_len
                    
                    # UV mapping
                    phi = math.atan2(point[2] - self.base_center[2], 
                                    point[0] - self.base_center[0])
                    u = (phi + math.pi) / (2 * math.pi)
                    v = y_local / self.height
                    
                    return HitInfo(t, point, normal, self.material, (u, v))
        
        # Si no hay hit en la superficie, probar la base
        return self._intersect_base(ray)
    
    def _intersect_base(self, ray):
        """Intersección con la base circular del cono."""
        if abs(ray.direction[1]) < 1e-6:
            return None
        
        t = (self.base_center[1] - ray.origin[1]) / ray.direction[1]
        if t <= 0.001:
            return None
        
        point = ray.at(t)
        dist_sq = (point[0] - self.base_center[0])**2 + (point[2] - self.base_center[2])**2
        
        if dist_sq <= self.base_radius**2:
            normal = np.array([0, -1, 0], dtype=float)
            u = (point[0] - self.base_center[0] + self.base_radius) / (2 * self.base_radius)
            v = (point[2] - self.base_center[2] + self.base_radius) / (2 * self.base_radius)
            return HitInfo(t, point, normal, self.material, (u, v))
        
        return None


class Disk:
    """Disco circular plano en 3D.
    Útil para hojas, pétalos, flores."""
    def __init__(self, center, normal, radius, material):
        self.center = np.array(center, dtype=float)
        self.normal = np.array(normal, dtype=float) / np.linalg.norm(normal)
        self.radius = float(radius)
        self.material = material
        
        # Crear sistema de coordenadas local para UV mapping
        if abs(self.normal[1]) < 0.999:
            self.tangent = np.cross(self.normal, np.array([0, 1, 0]))
        else:
            self.tangent = np.cross(self.normal, np.array([1, 0, 0]))
        tangent_len = np.linalg.norm(self.tangent)
        if tangent_len < 1e-10:
            self.tangent = np.array([1, 0, 0], dtype=float)  # Fallback
        else:
            self.tangent = self.tangent / tangent_len
        self.bitangent = np.cross(self.normal, self.tangent)
    
    def intersect(self, ray):
        """Ray-disk intersection: plano + verificación de radio."""
        denom = np.dot(ray.direction, self.normal)
        
        if abs(denom) < 1e-6:
            return None
        
        t = np.dot(self.center - ray.origin, self.normal) / denom
        
        if t <= 0.001:
            return None
        
        point = ray.at(t)
        offset = point - self.center
        dist_sq = np.dot(offset, offset)
        
        if dist_sq <= self.radius**2:
            # UV mapping usando coordenadas polares
            dist = math.sqrt(dist_sq)
            u = 0.5 + np.dot(offset, self.tangent) / (2 * self.radius)
            v = 0.5 + np.dot(offset, self.bitangent) / (2 * self.radius)
            
            return HitInfo(t, point, self.normal, self.material, (u, v))
        
        return None


class Triangle:
    """Triángulo con 3 vértices y opcionalmente normales/UVs por vértice.
    Usa algoritmo de Möller-Trumbore para intersección rápida."""
    def __init__(self, v0, v1, v2, material, n0=None, n1=None, n2=None, uv0=None, uv1=None, uv2=None):
        self.v0 = np.array(v0, dtype=float)
        self.v1 = np.array(v1, dtype=float)
        self.v2 = np.array(v2, dtype=float)
        self.material = material
        
        # Normales por vértice (para smooth shading)
        self.n0 = np.array(n0, dtype=float) if n0 is not None else None
        self.n1 = np.array(n1, dtype=float) if n1 is not None else None
        self.n2 = np.array(n2, dtype=float) if n2 is not None else None
        
        # UVs por vértice
        self.uv0 = uv0 if uv0 is not None else (0, 0)
        self.uv1 = uv1 if uv1 is not None else (1, 0)
        self.uv2 = uv2 if uv2 is not None else (0, 1)
        
        # Precalcular normal del plano si no hay normales por vértice
        if self.n0 is None:
            edge1 = self.v1 - self.v0
            edge2 = self.v2 - self.v0
            self.face_normal = np.cross(edge1, edge2)
            norm = np.linalg.norm(self.face_normal)
            if norm > 1e-6:
                self.face_normal = self.face_normal / norm
            else:
                self.face_normal = np.array([0, 1, 0], dtype=float)
    
    def intersect(self, ray):
        """Ray-triangle intersection usando algoritmo de Möller-Trumbore.
        Retorna HitInfo con coordenadas baricéntricas interpoladas."""
        
        EPSILON = 1e-8
        
        edge1 = self.v1 - self.v0
        edge2 = self.v2 - self.v0
        
        # Calcular determinante
        h = np.cross(ray.direction, edge2)
        det = np.dot(edge1, h)
        
        # Si det está cerca de 0, el rayo es paralelo al triángulo
        if abs(det) < EPSILON:
            return None
        
        inv_det = 1.0 / det
        s = ray.origin - self.v0
        u = inv_det * np.dot(s, h)
        
        # Verificar coordenada baricéntrica u
        if u < 0.0 or u > 1.0:
            return None
        
        q = np.cross(s, edge1)
        v = inv_det * np.dot(ray.direction, q)
        
        # Verificar coordenada baricéntrica v
        if v < 0.0 or u + v > 1.0:
            return None
        
        # Calcular t para encontrar el punto de intersección
        t = inv_det * np.dot(edge2, q)
        
        if t <= 0.001:  # Evitar self-intersection
            return None
        
        # Calcular punto de intersección
        point = ray.at(t)
        
        # Interpolar normal (smooth shading si hay normales por vértice)
        w = 1.0 - u - v  # Tercera coordenada baricéntrica
        
        if self.n0 is not None and self.n1 is not None and self.n2 is not None:
            # Smooth shading
            normal = w * self.n0 + u * self.n1 + v * self.n2
            norm_len = np.linalg.norm(normal)
            if norm_len < 1e-10:
                normal = self.face_normal  # Fallback a flat shading
            else:
                normal = normal / norm_len
        else:
            # Flat shading
            normal = self.face_normal
        
        # Interpolar UVs
        uv = (
            w * self.uv0[0] + u * self.uv1[0] + v * self.uv2[0],
            w * self.uv0[1] + u * self.uv1[1] + v * self.uv2[1]
        )
        
        return HitInfo(t, point, normal, self.material, uv)


class Torus:
    """Toro (donut) - superficie de revolución.
    Útil para anillos, bases de botellas, decoraciones."""
    def __init__(self, center, major_radius, minor_radius, material):
        self.center = np.array(center, dtype=float)
        self.major_radius = float(major_radius)  # R: radio mayor (del centro al tubo)
        self.minor_radius = float(minor_radius)  # r: radio menor (del tubo)
        self.material = material
    
    def intersect(self, ray):
        """Ray-torus intersection usando ecuación cuártica.
        Basado en: (sqrt(x^2+z^2) - R)^2 + y^2 = r^2"""
        
        # Transformar rayo a espacio local
        origin = ray.origin - self.center
        direction = ray.direction
        
        # Precalcular términos
        ox, oy, oz = origin[0], origin[1], origin[2]
        dx, dy, dz = direction[0], direction[1], direction[2]
        
        R = self.major_radius
        r = self.minor_radius
        
        # Coeficientes de la ecuación cuártica
        sum_d_sqr = dx*dx + dy*dy + dz*dz
        sum_o_sqr = ox*ox + oy*oy + oz*oz
        e = sum_o_sqr - R*R - r*r
        f = ox*dx + oy*dy + oz*dz
        four_a_sqr = 4.0 * R * R
        
        # at^4 + bt^3 + ct^2 + dt + e = 0
        coeffs = [
            sum_d_sqr * sum_d_sqr,  # a: t^4
            4.0 * sum_d_sqr * f,    # b: t^3
            2.0 * sum_d_sqr * e + 4.0 * f * f + four_a_sqr * dy * dy,  # c: t^2
            4.0 * f * e + 2.0 * four_a_sqr * oy * dy,  # d: t^1
            e * e - four_a_sqr * (r * r - oy * oy)     # e: t^0
        ]
        
        # Resolver ecuación cuártica (usaremos método de Ferrari simplificado)
        roots = self._solve_quartic(coeffs)
        
        # Encontrar la raíz positiva más pequeña
        valid_roots = [t for t in roots if t > 0.001]
        
        if not valid_roots:
            return None
        
        t = min(valid_roots)
        point = ray.at(t)
        
        # Calcular normal
        local_point = point - self.center
        param_squared = local_point[0]**2 + local_point[2]**2
        
        if param_squared < 1e-6:
            return None
        
        param = math.sqrt(param_squared)
        normal = np.array([
            local_point[0] * (1.0 - R / param),
            local_point[1],
            local_point[2] * (1.0 - R / param)
        ], dtype=float)
        
        norm_len = np.linalg.norm(normal)
        if norm_len < 1e-6:
            return None
        
        normal = normal / norm_len
        
        # UV mapping
        phi = math.atan2(local_point[2], local_point[0])
        theta = math.atan2(local_point[1], param - R)
        u = (phi + math.pi) / (2 * math.pi)
        v = (theta + math.pi) / (2 * math.pi)
        
        return HitInfo(t, point, normal, self.material, (u, v))
    
    def _solve_quartic(self, coeffs):
        """Solver simplificado para ecuación cuártica.
        Retorna lista de raíces reales."""
        a, b, c, d, e = coeffs
        
        if abs(a) < 1e-10:
            # Degradar a cúbica
            return self._solve_cubic([b, c, d, e])
        
        # Normalizar
        b /= a
        c /= a
        d /= a
        e /= a
        
        # Usar método numérico simplificado (Ferrari)
        # Para raytracing, Newton-Raphson es suficiente
        roots = []
        
        # Buscar raíces en rango razonable
        for t0 in [0.01, 0.1, 1.0, 10.0, 100.0]:
            t = self._newton_raphson(lambda t: t**4 + b*t**3 + c*t**2 + d*t + e,
                                     lambda t: 4*t**3 + 3*b*t**2 + 2*c*t + d,
                                     t0)
            if t is not None and t > 0:
                # Verificar que es realmente una raíz
                val = t**4 + b*t**3 + c*t**2 + d*t + e
                if abs(val) < 1e-3:
                    # Evitar duplicados
                    is_duplicate = any(abs(t - r) < 1e-3 for r in roots)
                    if not is_duplicate:
                        roots.append(t)
        
        return roots
    
    def _solve_cubic(self, coeffs):
        """Solver para ecuación cúbica."""
        if len(coeffs) < 4:
            return []
        a, b, c, d = coeffs
        if abs(a) < 1e-10:
            return self._solve_quadratic([b, c, d])
        
        # Normalizar y usar fórmula de Cardano (simplificada)
        b /= a
        c /= a
        d /= a
        
        # Método numérico
        roots = []
        for t0 in [0.01, 1.0, 10.0]:
            t = self._newton_raphson(lambda t: t**3 + b*t**2 + c*t + d,
                                     lambda t: 3*t**2 + 2*b*t + c,
                                     t0)
            if t is not None:
                roots.append(t)
        
        return roots
    
    def _solve_quadratic(self, coeffs):
        """Solver para ecuación cuadrática."""
        if len(coeffs) < 3:
            return []
        a, b, c = coeffs
        if abs(a) < 1e-10:
            return [-c/b] if abs(b) > 1e-10 else []
        
        disc = b*b - 4*a*c
        if disc < 0:
            return []
        
        sqrt_disc = math.sqrt(disc)
        return [(-b - sqrt_disc)/(2*a), (-b + sqrt_disc)/(2*a)]
    
    def _newton_raphson(self, f, df, x0, max_iter=20, tol=1e-6):
        """Método de Newton-Raphson para encontrar raíces."""
        x = x0
        for _ in range(max_iter):
            fx = f(x)
            if abs(fx) < tol:
                return x
            
            dfx = df(x)
            if abs(dfx) < 1e-10:
                return None
            
            x_new = x - fx / dfx
            if abs(x_new - x) < tol:
                return x_new
            x = x_new
        
        return None
