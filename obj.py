
import os


class Obj(object):
	def __init__(self, filename):
		# Asumiendo que el archivo es un formato .obj
		with open(filename, "r") as file:
			lines = file.read().splitlines()

		self.vertices = []
		self.texCoords = []
		self.normals = []
		self.faces = []
		# material name per face (None if no material)
		self.faceMaterials = []
		# materials parsed from .mtl (name -> dict of properties)
		self.materials = {}

		currentMat = None

		for line in lines:
			# Si la linea no cuenta con un prefijo y un valor,
			# seguimos a la siguiente la linea

			line = line.rstrip()

			try:
				prefix, value = line.split(" ", 1)
			except:
				continue

			# Dependiendo del prefijo, parseamos y guardamos
			# la informacion en el contenedor correcto

			if prefix == "v": # Vertices
				vert = list(map(float,value.split(" ")))
				self.vertices.append(vert)

			elif prefix == "vt": # Coordenadas de textura
				vts = list(map(float,value.split(" ")))
				self.texCoords.append([vts[0],vts[1]])

			elif prefix == "vn": # Normales
				norm = list(map(float,value.split(" ")))
				self.normals.append(norm)

			elif prefix == "mtllib":
				# load .mtl file referenced by this obj (path is relative to obj)
				mtl_file = value.strip()
				mtl_path = os.path.join(os.path.dirname(filename), mtl_file)
				self.materials = self._parse_mtl(mtl_path)

			elif prefix == "usemtl":
				currentMat = value.strip()

			elif prefix == "f": # Caras
				face = []
				verts = value.split(" ")
				for vert in verts:
					vert = list(map(int, vert.split("/")))
					face.append(vert)
				self.faces.append(face)
				self.faceMaterials.append(currentMat)


	def _parse_mtl(self, mtlPath):
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
				# ignore other MTL properties for now
		return mats