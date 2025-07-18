import numpy as np
import random
from typing import List, Dict, Any

def vertexShader(vertex: List[float], kwargs: Dict[str, Any]) -> List[float]:
    modelMatrix = kwargs["modelMatrix"]
    width      = kwargs["width"]
    height     = kwargs["height"]

    # Convertir vértice a coordenadas homogéneas
    v = np.array([vertex[0], vertex[1], vertex[2], 1.0])
    
    # Transformar vértice (convertir matriz a array numpy primero)
    modelMatrix = np.array(modelMatrix)
    v = modelMatrix.dot(v)        # objeto → mundo
    
    # Proyección ortográfica (simplemente usar x,y)
    x_ndc = v[0]
    y_ndc = v[1]

    x_scr = (x_ndc + 1) * 0.5 * width
    y_scr = (y_ndc + 1) * 0.5 * height
    return [x_scr, y_scr, v[2]]    # z sin usar por ahora

def randomColor():
    return [random.random(), random.random(), random.random()]
