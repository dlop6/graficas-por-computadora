from MathLib import *
from typing import List, Callable, Dict, Any, Optional, Union

class Model(object):
    def __init__(self):
        self.vertices: List[float] = []
        self.translation = [0.0, 0.0, 0.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.scale = [1.0, 1.0, 1.0]
        self.vertexShader: Optional[Callable[[List[float], Dict[str, Any]], List[float]]] = None

    def GetModelMatrix(self):
        translateMat = TranslationMatrix(self.translation[0],
                                         self.translation[1],
                                         self.translation[2])

        rotateMat = RotationMatrix(self.rotation[0],
                                   self.rotation[1],
                                   self.rotation[2])

        scaleMat = ScaleMatrix(self.scale[0],
                               self.scale[1],
                               self.scale[2])

        return translateMat * rotateMat * scaleMat

    def load_from_obj(self, path: str):
        verts_raw = []
        faces = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("v "):  # Solo vértices, no normales o UVs
                        _, x, y, z = line.split()
                        verts_raw.append([float(x), float(y), float(z)])
                    elif line.startswith("f "):
                        _, *idx = line.split()
                        i = [int(i.split('/')[0]) - 1 for i in idx]
                        if len(i) == 3:
                            faces.append(i)
                        elif len(i) == 4:
                            faces += [[i[0], i[1], i[2]],
                                      [i[0], i[2], i[3]]]
        except FileNotFoundError:
            print(f"Error: Archivo OBJ no encontrado: {path}")
            raise
        except Exception as e:
            print(f"Error leyendo archivo OBJ {path}: {e}")
            raise

        self.vertices = []
        for a, b, c in faces:
            self.vertices += verts_raw[a][:3] + verts_raw[b][:3] + verts_raw[c][:3]
