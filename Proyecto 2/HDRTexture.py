import struct
import math
import os

class HDRTexture:
    """Simple loader for Radiance .hdr (RGBE) files.

    Provides: HDRTexture(path) -> object with width, height, data (float RGB tuples)
    and a sample(direction) helper that expects equirectangular coordinates.
    """

    def __init__(self, path):
        self.path = path
        self.width = 0
        self.height = 0
        self.data = []  # list of (r,g,b) floats row-major
        self._load_rgbe(path)

    def _read_line(self, f):
        line = b""
        while True:
            ch = f.read(1)
            if not ch:
                break
            line += ch
            if line.endswith(b"\n"):
                break
        return line.decode('ascii')

    def _load_rgbe(self, path):
        with open(path, 'rb') as f:
            # header
            line = self._read_line(f)
            if not line.startswith('#') and not line.startswith('\xff'):
                # Radiance hdr header usually starts with #?RADIANCE
                # If not present, still try to continue
                pass
            # read until blank line
            while True:
                line = self._read_line(f)
                if line.strip() == '':
                    break
            # dimensions line, e.g., -Y 512 +X 1024
            dims = self._read_line(f).strip()
            parts = dims.split()
            try:
                y_index = parts.index('-Y')
                h = int(parts[y_index+1])
                x_index = parts.index('+X')
                w = int(parts[x_index+1])
            except Exception:
                # fallback: try different ordering
                try:
                    y_index = parts.index('+Y')
                    h = int(parts[y_index+1])
                    x_index = parts.index('-X')
                    w = int(parts[x_index+1])
                except Exception as e:
                    raise ValueError('Unsupported HDR dimensions line: %r' % dims)
            self.width = w
            self.height = h
            # now read pixel data as RGBE
            pixels = []
            for y in range(h):
                # scanline read per Radiance format
                scanline = f.read(4)
                if len(scanline) < 4:
                    raise EOFError('Unexpected EOF reading HDR')
                if scanline[0] != 2 or scanline[1] != 2:
                    # old format: each pixel is 4 bytes RGBE
                    # fallback: unread and read whole image as flat RGBE
                    f.seek(-4, os.SEEK_CUR)
                    remaining = f.read()
                    # parse remaining as flat rgbe triplets
                    # each pixel is 4 bytes
                    count = len(remaining)//4
                    for i in range(count):
                        r,g,b,e = struct.unpack_from('4B', remaining, i*4)
                        pixels.append(self._rgbe_to_rgb(r,g,b,e))
                    break
                scanline_len = (scanline[2] << 8) | scanline[3]
                if scanline_len != w:
                    # not a RLE scanline; fallback
                    f.seek(-4, os.SEEK_CUR)
                    remaining = f.read()
                    count = len(remaining)//4
                    for i in range(count):
                        r,g,b,e = struct.unpack_from('4B', remaining, i*4)
                        pixels.append(self._rgbe_to_rgb(r,g,b,e))
                    break
                # read channels
                scan = [bytearray() for _ in range(4)]
                for ch in range(4):
                    i = 0
                    while i < w:
                        bval = ord(f.read(1))
                        if bval > 128:
                            run = bval - 128
                            val = ord(f.read(1))
                            scan[ch].extend([val]*run)
                            i += run
                        else:
                            run = bval
                            scan[ch].extend(f.read(run))
                            i += run
                for i in range(w):
                    r = scan[0][i]
                    g = scan[1][i]
                    b = scan[2][i]
                    e = scan[3][i]
                    pixels.append(self._rgbe_to_rgb(r,g,b,e))

            # store row-major top-to-bottom
            self.data = pixels

    def _rgbe_to_rgb(self, r,g,b,e):
        if e == 0:
            return (0.0,0.0,0.0)
        f = math.ldexp(1.0, e - (128+8))
        return (r * f, g * f, b * f)

    def sample_equirect(self, direction):
        """Sample envmap using 3D direction vector (x,y,z) -> returns (r,g,b)
        Equirectangular mapping: u = atan2(z,x)/(2pi)+0.5, v = acos(y)/pi
        """
        x, y, z = direction
        
        # Check for NaN values
        if math.isnan(x) or math.isnan(y) or math.isnan(z):
            return (0.5, 0.5, 0.5)  # Fallback gray
        
        # Clamp y to valid range for acos
        y = max(-1.0, min(1.0, y))
        
        # Calculate spherical coordinates
        u = (math.atan2(z, x) / (2.0 * math.pi)) + 0.5
        v = math.acos(y) / math.pi
        
        # Check for NaN in spherical coords
        if math.isnan(u) or math.isnan(v):
            return (0.5, 0.5, 0.5)  # Fallback gray
        
        # Clamp and wrap coordinates to [0, 1)
        u = u % 1.0
        v = max(0.0, min(1.0, v))
        
        # Convert to pixel coordinates
        px = int(u * (self.width - 1))
        py = int(v * (self.height - 1))
        
        # Safely index into data
        px = max(0, min(self.width - 1, px))
        py = max(0, min(self.height - 1, py))
        idx = py * self.width + px
        
        if idx < 0 or idx >= len(self.data):
            return (0.5, 0.5, 0.5)  # Fallback gray
        
        return self.data[idx]

    def sample_uv(self, u, v):
        u = u % 1.0
        v = max(0.0, min(1.0, v))
        px = int(u * self.width) % self.width
        py = int(v * self.height) % self.height
        return self.data[py*self.width + px]
