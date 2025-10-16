
import os
from MathLib import *

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

# Ejemplo de uso:
# obj = OBJModel('Proyecto 2/assets/model.obj')
# for face in obj.faces:
#     v0 = obj.vertices[face[0][0]]
#     ...
