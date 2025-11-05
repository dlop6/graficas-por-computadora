import osimport os





class Obj(object):

    def __init__(self, filename): 

        # Asumiendo que el archivo es un formato .obj

        with open(filename, "r") as file:class Obj(object):	def __init__(self, filename):

            lines = file.read().splitlines()

	def __init__(self, filename):		# Asumiendo que el archivo es un formato .obj

        self.vertices = []

        self.texCoords = []		# Asumiendo que el archivo es un formato .obj		with open(filename, "r") as file:

        self.normals = []

        self.faces = []		with open(filename, "r") as file:			lines = file.read().splitlines()

        self.faceMaterials = []

        self.materials = {}			lines = file.read().splitlines()<<<<<<< HEAD



        currentMat = None		self.normals = []



        for line in lines:		self.vertices = []		self.faces = []

            # Si la linea no cuenta con un prefijo y un valor,

            # seguimos a la siguiente la linea		self.texCoords = []<<<<<<< HEAD

            line = line.rstrip()

		self.normals = []		

            try:

                prefix, value = line.split(" ", 1)		self.faces = []		# materials parsed from .mtl (name -> dict of properties)

            except ValueError:

                continue		self.faceMaterials = []		self.materials = {}



            # Dependiendo del prefijo, parseamos y guardamos		self.materials = {}

            # la informacion en el contenedor correcto

		currentMat = None

            if prefix == "v":  # Vertices

                vert = [float(x) for x in value.split() if x]		currentMat = None

                self.vertices.append(vert)

>>>>>>> Lab-9

            elif prefix == "vt":  # Coordenadas de textura

                vts = [float(x) for x in value.split() if x]		for line in lines:			# seguimos a la siguiente la linea

                if len(vts) >= 2:

                    self.texCoords.append([vts[0], vts[1]])			# Si la linea no cuenta con un prefijo y un valor,



            elif prefix == "vn":  # Normales			# seguimos a la siguiente la linea			line = line.rstrip()

                norm = [float(x) for x in value.split() if x]

                self.normals.append(norm)			line = line.rstrip()



            elif prefix == "mtllib":			try:

                # load .mtl file referenced by this obj (path is relative to obj)

                mtl_file = value.strip()			try:				prefix, value = line.split(" ", 1)

                mtl_path = os.path.join(os.path.dirname(filename), mtl_file)

                self.materials = self._parse_mtl(mtl_path)				prefix, value = line.split(" ", 1)			except:



            elif prefix == "usemtl":			except ValueError:				continue

                currentMat = value.strip()

				continue

            elif prefix == "f":  # Caras

                face = []			# Dependiendo del prefijo, parseamos y guardamos

                verts = [v for v in value.split() if v]

                for vert in verts:			# Dependiendo del prefijo, parseamos y guardamos			# la informacion en el contenedor correcto

                    indices = [int(x) if x else 0 for x in vert.split("/")]

                    face.append(indices)			# la informacion en el contenedor correcto

                self.faces.append(face)

                self.faceMaterials.append(currentMat)			if prefix == "v": # Vertices



    def _parse_mtl(self, mtlPath):			if prefix == "v":  # Vertices				vert = [float(x) for x in value.split() if x]

        mats = {}

        if not os.path.exists(mtlPath):				vert = [float(x) for x in value.split() if x]				self.vertices.append(vert)

            return mats

        with open(mtlPath, 'r') as f:				self.vertices.append(vert)

            current = None

            for line in f:			elif prefix == "vt": # Coordenadas de textura

                line = line.strip()

                if not line or line.startswith('#'):			elif prefix == "vt":  # Coordenadas de textura				vts = [float(x) for x in value.split() if x]

                    continue

                parts = line.split(None, 1)				vts = [float(x) for x in value.split() if x]				self.texCoords.append([vts[0],vts[1]])

                if len(parts) == 0:

                    continue				if len(vts) >= 2:

                key = parts[0]

                val = parts[1] if len(parts) > 1 else ''					self.texCoords.append([vts[0], vts[1]])			elif prefix == "vn": # Normales

                if key == 'newmtl':

                    current = val.strip()				norm = [float(x) for x in value.split() if x]

                    mats[current] = {}

                elif key == 'map_Kd' and current is not None:			elif prefix == "vn":  # Normales				self.normals.append(norm)

                    mats[current]['map_Kd'] = val.strip()

                # ignore other MTL properties for now				norm = [float(x) for x in value.split() if x]

        return mats

				self.normals.append(norm)			elif prefix == "mtllib":

				# load .mtl file referenced by this obj (path is relative to obj)

			elif prefix == "mtllib":				mtl_file = value.strip()

				# load .mtl file referenced by this obj (path is relative to obj)				mtl_path = os.path.join(os.path.dirname(filename), mtl_file)

				mtl_file = value.strip()				self.materials = self._parse_mtl(mtl_path)

				mtl_path = os.path.join(os.path.dirname(filename), mtl_file)

				self.materials = self._parse_mtl(mtl_path)			elif prefix == "usemtl":

				currentMat = value.strip()

			elif prefix == "usemtl":			elif prefix == "f": # Caras

				currentMat = value.strip()				face = []

				verts = [v for v in value.split() if v]

			elif prefix == "f":  # Caras				for vert in verts:

				face = []					vert = [int(x) if x else 0 for x in vert.split("/")]

				verts = [v for v in value.split() if v]					face.append(vert)

				for vert in verts:				self.faces.append(face)

					indices = [int(x) if x else 0 for x in vert.split("/")]				self.faceMaterials.append(currentMat)

					face.append(indices)

				self.faces.append(face)

				self.faceMaterials.append(currentMat)	def _parse_mtl(self, mtlPath):

		mats = {}

		if not os.path.exists(mtlPath):

	def _parse_mtl(self, mtlPath):			return mats

		mats = {}		with open(mtlPath, 'r') as f:

		if not os.path.exists(mtlPath):			current = None

			return mats			for line in f:

		with open(mtlPath, 'r') as f:				line = line.strip()

			current = None				if not line or line.startswith('#'):

			for line in f:					continue

				line = line.strip()				parts = line.split(None, 1)

				if not line or line.startswith('#'):				if len(parts) == 0:

					continue					continue

				parts = line.split(None, 1)				key = parts[0]

				if len(parts) == 0:				val = parts[1] if len(parts) > 1 else ''

					continue				if key == 'newmtl':

				key = parts[0]					current = val.strip()

				val = parts[1] if len(parts) > 1 else ''					mats[current] = {}

				if key == 'newmtl':				elif key == 'map_Kd' and current is not None:

					current = val.strip()					mats[current]['map_Kd'] = val.strip()

					mats[current] = {}				# ignore other MTL properties for now

				elif key == 'map_Kd' and current is not None:		return mats

					mats[current]['map_Kd'] = val.strip()
				# ignore other MTL properties for now
		return mats
