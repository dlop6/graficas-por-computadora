import numpy as np
from math import pi, sin, cos, tan

def TranslationMatrix(x, y, z):
    """Crea una matriz de traslación 4x4"""
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def ScaleMatrix(x, y, z):
    """Crea una matriz de escala 4x4"""
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def RotationMatrix(pitch, yaw, roll):
    """Crea una matriz de rotación 4x4 combinando pitch, yaw y roll"""
    pitch = np.radians(pitch)
    yaw = np.radians(yaw)
    roll = np.radians(roll)

    # Rotación en X (pitch)
    pitchMat = np.array([
        [1, 0, 0, 0],
        [0, cos(pitch), -sin(pitch), 0],
        [0, sin(pitch), cos(pitch), 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

    # Rotación en Y (yaw)
    yawMat = np.array([
        [cos(yaw), 0, sin(yaw), 0],
        [0, 1, 0, 0],
        [-sin(yaw), 0, cos(yaw), 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

    # Rotación en Z (roll)
    rollMat = np.array([
        [cos(roll), -sin(roll), 0, 0],
        [sin(roll), cos(roll), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

    return pitchMat @ yawMat @ rollMat

def LookAtMatrix(eye, target, up):
    """Crea una matriz de vista (View Matrix) usando look-at"""
    eye = np.array(eye, dtype=np.float32)
    target = np.array(target, dtype=np.float32)
    up = np.array(up, dtype=np.float32)
    
    # Calcular vectores de la cámara
    forward = target - eye
    forward = forward / np.linalg.norm(forward)
    
    right = np.cross(forward, up)
    right = right / np.linalg.norm(right)
    
    up = np.cross(right, forward)
    
    # Crear matriz de vista
    viewMatrix = np.array([
        [right[0], right[1], right[2], -np.dot(right, eye)],
        [up[0], up[1], up[2], -np.dot(up, eye)],
        [-forward[0], -forward[1], -forward[2], np.dot(forward, eye)],
        [0, 0, 0, 1]
    ], dtype=np.float32)
    
    return viewMatrix

def PerspectiveMatrix(fov, aspect, near, far):
    """Crea una matriz de proyección en perspectiva"""
    fov_rad = np.radians(fov)
    f = 1.0 / tan(fov_rad / 2.0)
    
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ], dtype=np.float32)

def ViewportMatrix(x, y, width, height):
    """Crea una matriz de viewport para transformar NDC a coordenadas de pantalla"""
    return np.array([
        [width/2, 0, 0, x + width/2],
        [0, height/2, 0, y + height/2],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def barycentric_coordinates(p1, p2, p3, p):
    """Calcula las coordenadas baricéntricas de un punto p dentro del triángulo p1-p2-p3"""
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    x3, y3 = p3[0], p3[1]
    x, y = p[0], p[1]
    
    denominator = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    if abs(denominator) < 1e-6:
        return None  # Triángulo degenerado
    
    a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominator
    b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominator
    c = 1 - a - b
    
    return (a, b, c)

def cross_product_2d(v1, v2):
    """Producto cruz en 2D (devuelve escalar)"""
    return v1[0] * v2[1] - v1[1] * v2[0]

def normalize(v):
    """Normaliza un vector"""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm
