import numpy as np
from typing import Tuple

class Camera:
    def __init__(self, position: Tuple[float, float, float] = (0, 0, 5),
                 target: Tuple[float, float, float] = (0, 0, 0),
                 up: Tuple[float, float, float] = (0, 1, 0),
                 fov: float = 60.0,
                 aspect: float = 1.0,
                 near: float = 0.1,
                 far: float = 100.0):
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.up = np.array(up, dtype=np.float32)
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far

    def get_view_matrix(self):
        """Calcula la matriz de vista (View Matrix)"""
        from MathLib import LookAtMatrix
        return LookAtMatrix(self.position, self.target, self.up)

    def get_projection_matrix(self):
        """Calcula la matriz de proyección (Projection Matrix)"""
        from MathLib import PerspectiveMatrix
        return PerspectiveMatrix(self.fov, self.aspect, self.near, self.far)

    def set_position(self, x: float, y: float, z: float):
        """Establece la posición de la cámara"""
        self.position = np.array([x, y, z], dtype=np.float32)

    def set_target(self, x: float, y: float, z: float):
        """Establece el objetivo de la cámara"""
        self.target = np.array([x, y, z], dtype=np.float32)

    def set_up(self, x: float, y: float, z: float):
        """Establece el vector up de la cámara"""
        self.up = np.array([x, y, z], dtype=np.float32)

    def rotate_around_target(self, yaw: float, pitch: float, distance: float):
        """Rota la cámara alrededor del objetivo"""
        import math
        
        yaw_rad = math.radians(yaw)
        pitch_rad = math.radians(pitch)
        
        # Calcular nueva posición
        x = self.target[0] + distance * math.cos(pitch_rad) * math.cos(yaw_rad)
        y = self.target[1] + distance * math.sin(pitch_rad)
        z = self.target[2] + distance * math.cos(pitch_rad) * math.sin(yaw_rad)
        
        self.position = np.array([x, y, z], dtype=np.float32)

class CameraController:
    """Controlador para manejar diferentes tipos de tomas de cámara"""
    
    def __init__(self, aspect_ratio: float = 4/3):
        self.aspect_ratio = aspect_ratio
        self.target = np.array([0, 0, 0], dtype=np.float32)
        self.distance = 5.0

    def get_medium_shot_camera(self) -> Camera:
        """Toma media: Vista frontal normal del modelo"""
        camera = Camera(
            position=(0, 0, self.distance),
            target=tuple(self.target),
            up=(0, 1, 0),
            fov=60.0,  # FOV más amplio para ver mejor el modelo
            aspect=self.aspect_ratio
        )
        return camera

    def get_low_angle_camera(self) -> Camera:
        """Toma en ángulo bajo: Cámara desde abajo mirando hacia arriba"""
        camera = Camera(
            position=(self.distance * 0.3, -self.distance * 0.8, self.distance * 0.6),
            target=tuple(self.target),
            up=(0, 1, 0),
            fov=65.0,
            aspect=self.aspect_ratio
        )
        return camera

    def get_high_angle_camera(self) -> Camera:
        """Toma en ángulo alto: Cámara desde arriba mirando hacia abajo"""
        camera = Camera(
            position=(-self.distance * 0.3, self.distance * 0.8, self.distance * 0.6),
            target=tuple(self.target),
            up=(0, 1, 0),
            fov=65.0,
            aspect=self.aspect_ratio
        )
        return camera

    def get_dutch_angle_camera(self) -> Camera:
        """Toma holandesa: Cámara inclinada lateralmente"""
        import math
        
        # Posición ligeramente lateral
        camera = Camera(
            position=(self.distance * 0.7, self.distance * 0.3, self.distance * 0.7),
            target=tuple(self.target),
            up=(-0.4, 0.9, 0.2),  # Vector up inclinado para crear el efecto dutch
            fov=70.0,
            aspect=self.aspect_ratio
        )
        return camera

    def set_target(self, x: float, y: float, z: float):
        """Establece el punto objetivo para todas las cámaras"""
        self.target = np.array([x, y, z], dtype=np.float32)

    def set_distance(self, distance: float):
        """Establece la distancia base para las cámaras"""
        self.distance = distance
