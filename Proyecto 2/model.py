
import os
import numpy as np
from MathLib import *
from primitives import Triangle

class OBJModel:
    def __init__(self, filename):
        self.vertices = []
        self.normals = []
        self.uvs = []
        self.faces = []  # Each face: [(v_idx, vt_idx, vn_idx), ...]
        self.materials = {}
        self.usemtl = None
        self.load(filename)

    def load(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    parts = line.strip().split()
                    self.vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif line.startswith('vn '):
                    parts = line.strip().split()
                    self.normals.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif line.startswith('vt '):
                    parts = line.strip().split()
                    self.uvs.append([float(parts[1]), float(parts[2])])
                elif line.startswith('f '):
                    parts = line.strip().split()[1:]
                    # Triangulate if face has >3 vertices
                    idxs = [self.parse_face_vertex(p) for p in parts]
                    if len(idxs) == 3:
                        self.faces.append(idxs)
                    elif len(idxs) > 3:
                        # Fan triangulation
                        for i in range(1, len(idxs)-1):
                            self.faces.append([idxs[0], idxs[i], idxs[i+1]])
                elif line.startswith('usemtl '):
                    self.usemtl = line.strip().split()[1]
                elif line.startswith('mtllib '):
                    mtlfile = line.strip().split()[1]
                    self.load_mtl(os.path.join(os.path.dirname(filename), mtlfile))

    def parse_face_vertex(self, s):
        # Format: v/vt/vn or v//vn or v/vt or v
        vals = s.split('/')
        v_idx = int(vals[0]) - 1 if vals[0] else None
        vt_idx = int(vals[1]) - 1 if len(vals) > 1 and vals[1] else None
        vn_idx = int(vals[2]) - 1 if len(vals) > 2 and vals[2] else None
        return (v_idx, vt_idx, vn_idx)

    def load_mtl(self, mtl_path):
        if not os.path.exists(mtl_path):
            return
        current = None
        with open(mtl_path, 'r') as f:
            for line in f:
                if line.startswith('newmtl '):
                    current = line.strip().split()[1]
                    self.materials[current] = {}
                elif current:
                    if line.startswith('Kd '):
                        parts = line.strip().split()
                        self.materials[current]['Kd'] = [float(parts[1]), float(parts[2]), float(parts[3])]
                    elif line.startswith('map_Kd '):
                        tex = line.strip().split()[1]
                        self.materials[current]['map_Kd'] = tex
    
    def to_triangles(self, material, transform_matrix=None):
        """Convierte el modelo OBJ en una lista de primitivas Triangle.
        
        Args:
            material: Material a aplicar a todos los triángulos
            transform_matrix: Matriz 4x4 opcional para transformar el modelo
        
        Returns:
            Lista de objetos Triangle listos para raytracing
        """
        triangles = []
        
        for face in self.faces:
            # Extraer índices (recordar que OBJ usa indexado 1-based)
            v0_idx, vt0_idx, vn0_idx = face[0]
            v1_idx, vt1_idx, vn1_idx = face[1]
            v2_idx, vt2_idx, vn2_idx = face[2]
            
            # Obtener vértices
            v0 = self.vertices[v0_idx]
            v1 = self.vertices[v1_idx]
            v2 = self.vertices[v2_idx]
            
            # Aplicar transformación si existe
            if transform_matrix is not None:
                v0 = self._transform_point(v0, transform_matrix)
                v1 = self._transform_point(v1, transform_matrix)
                v2 = self._transform_point(v2, transform_matrix)
            
            # Obtener normales (si existen)
            n0 = self.normals[vn0_idx] if vn0_idx is not None and vn0_idx < len(self.normals) else None
            n1 = self.normals[vn1_idx] if vn1_idx is not None and vn1_idx < len(self.normals) else None
            n2 = self.normals[vn2_idx] if vn2_idx is not None and vn2_idx < len(self.normals) else None
            
            # Transformar normales (solo rotación, sin traslación)
            if transform_matrix is not None:
                if n0 is not None:
                    n0 = self._transform_normal(n0, transform_matrix)
                if n1 is not None:
                    n1 = self._transform_normal(n1, transform_matrix)
                if n2 is not None:
                    n2 = self._transform_normal(n2, transform_matrix)
            
            # Obtener UVs (si existen)
            uv0 = tuple(self.uvs[vt0_idx]) if vt0_idx is not None and vt0_idx < len(self.uvs) else None
            uv1 = tuple(self.uvs[vt1_idx]) if vt1_idx is not None and vt1_idx < len(self.uvs) else None
            uv2 = tuple(self.uvs[vt2_idx]) if vt2_idx is not None and vt2_idx < len(self.uvs) else None
            
            # Crear triángulo
            triangle = Triangle(v0, v1, v2, material, n0, n1, n2, uv0, uv1, uv2)
            triangles.append(triangle)
        
        return triangles
    
    def _transform_point(self, point, matrix):
        """Transforma un punto 3D por una matriz 4x4."""
        p = np.array([point[0], point[1], point[2], 1.0])
        p_transformed = matrix @ p
        # Normalizar por w
        return [p_transformed[0, 0] / p_transformed[0, 3],
                p_transformed[0, 1] / p_transformed[0, 3],
                p_transformed[0, 2] / p_transformed[0, 3]]
    
    def _transform_normal(self, normal, matrix):
        """Transforma una normal por una matriz 4x4 (solo rotación/escala)."""
        # Para normales, usar la inversa transpuesta (o solo la parte superior 3x3)
        n = np.array([normal[0], normal[1], normal[2], 0.0])
        n_transformed = matrix @ n
        result = np.array([n_transformed[0, 0], n_transformed[0, 1], n_transformed[0, 2]])
        norm = np.linalg.norm(result)
        if norm > 1e-6:
            result = result / norm
        return result


# Ejemplo de uso:
# from materials import Lambertian
# mat = Lambertian((0.8, 0.5, 0.3))
# obj = OBJModel('Proyecto 2/assets/model.obj')
# triangles = obj.to_triangles(mat)
# # Agregar triangles a scene['objects']
