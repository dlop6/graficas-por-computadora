import struct
from typing import List, Tuple

def GenerateBMP(filename: str, width: int, height: int, byteDepth: int, colorBuffer: List[List[Tuple[int, int, int]]]) -> None:
    """
    Genera un archivo BMP a partir de un buffer de colores
    
    Args:
        filename: Nombre del archivo de salida
        width: Ancho de la imagen
        height: Alto de la imagen  
        byteDepth: Profundidad de color en bytes (normalmente 3 para RGB)
        colorBuffer: Buffer de colores como lista 2D de tuplas RGB
    """
    def char(c: str) -> bytes:
        return struct.pack("<c", c.encode("ascii"))

    def word(w: int) -> bytes:
        return struct.pack("<H", w)

    def dword(d: int) -> bytes:
        return struct.pack("<L", d)

    with open(filename, "wb") as file:
        # BMP Header
        file.write(char("B"))
        file.write(char("M"))
        file.write(dword(14 + 40 + (width * height * byteDepth)))
        file.write(dword(0))
        file.write(dword(14 + 40))

        # Info Header
        file.write(dword(40))
        file.write(dword(width))
        file.write(dword(height))
        file.write(word(1))
        file.write(word(byteDepth * 8))
        file.write(dword(0))
        file.write(dword(width * height * byteDepth))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))

        # Pixel data (BMP stores pixels bottom to top)
        for y in range(height - 1, -1, -1):
            for x in range(width):
                color = colorBuffer[y][x]
                # color is a tuple (R, G, B), BMP wants BGR order
                # Convertir a int de Python para usar to_bytes
                file.write(int(color[2]).to_bytes(1, 'little'))
                file.write(int(color[1]).to_bytes(1, 'little'))
                file.write(int(color[0]).to_bytes(1, 'little'))
