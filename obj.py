import os


class Obj(object):
    def __init__(self, filename):
        # Listas para almacenar datos del archivo .obj
        self.vertices = []        # v
        self.texCoords = []       # vt
        self.normals = []         # vn
        self.faces = []           # f
        self.faceMaterials = []   # material usado en cada cara
        self.materials = {}       # materiales cargados desde .mtl

        # Leemos todas las líneas del archivo .obj
        with open(filename, "r") as file:
            lines = file.read().splitlines()

        currentMat = None

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Intentamos separar prefijo y valor
            try:
                prefix, value = line.split(None, 1)
            except ValueError:
                # Línea sin datos útiles
                continue

            # Vertices
            if prefix == "v":
                vert = [float(x) for x in value.split() if x]
                self.vertices.append(vert)

            # Coordenadas de textura
            elif prefix == "vt":
                vts = [float(x) for x in value.split() if x]
                if len(vts) >= 2:
                    self.texCoords.append([vts[0], vts[1]])

            # Normales
            elif prefix == "vn":
                norm = [float(x) for x in value.split() if x]
                self.normals.append(norm)

            # Archivo de materiales
            elif prefix == "mtllib":
                mtl_file = value.strip()
                mtl_path = os.path.join(os.path.dirname(filename), mtl_file)
                self.materials = self._parse_mtl(mtl_path)

            # Uso de material
            elif prefix == "usemtl":
                currentMat = value.strip()

            # Caras
            elif prefix == "f":
                face = []
                verts = [v for v in value.split() if v]

                for vert in verts:
                    # Formato típico: v/vt/vn (algunos pueden faltar)
                    indices = [int(x) if x else 0 for x in vert.split("/")]
                    face.append(indices)

                self.faces.append(face)
                self.faceMaterials.append(currentMat)

    def _parse_mtl(self, mtlPath):
        """Parsea un archivo .mtl y devuelve un dict:
        {
            'material_name': {
                'map_Kd': 'ruta_textura',
                ...
            },
            ...
        }
        """
        mats = {}

        if not os.path.exists(mtlPath):
            return mats

        with open(mtlPath, 'r') as f:
            current = None

            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split(None, 1)
                if len(parts) == 0:
                    continue

                key = parts[0]
                val = parts[1] if len(parts) > 1 else ''

                if key == 'newmtl':
                    current = val.strip()
                    mats[current] = {}
                elif key == 'map_Kd' and current is not None:
                    mats[current]['map_Kd'] = val.strip()
                # Aquí se podrían parsear más propiedades si las necesitas

        return mats
