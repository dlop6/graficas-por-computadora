POINTS = 0
LINES = 1
TRIANGLES = 2

# --- Figuras y materiales para Raytracer ---
import numpy as np

class Material:
    def __init__(self, color, mat_type='opaque', ior=1.0, reflectivity=0.0):
        self.color = np.array(color, dtype=float)  # RGB [0,1]
        self.type = mat_type  # 'opaque', 'reflective', 'transparent'
        self.ior = ior        # Índice de refracción (solo para transparentes)
        self.reflectivity = reflectivity  # 0=mate, 1=espejo

class Sphere:
    def __init__(self, center, radius, material):
        self.center = np.array(center, dtype=float)
        self.radius = radius
        self.material = material

    def intersect(self, ray_origin, ray_dir):
        L = self.center - ray_origin
        tca = np.dot(L, ray_dir)
        d2 = np.dot(L, L) - tca * tca
        r2 = self.radius * self.radius
        if d2 > r2:
            return None
        thc = np.sqrt(r2 - d2)
        t0 = tca - thc
        t1 = tca + thc
        if t0 > 0:
            return t0
        if t1 > 0:
            return t1
        return None

    def get_normal(self, point):
        return (point - self.center) / self.radius

class Plane:
    def __init__(self, point, normal, material):
        self.point = np.array(point, dtype=float)
        self.normal = np.array(normal, dtype=float) / np.linalg.norm(normal)
        self.material = material

    def intersect(self, ray_origin, ray_dir):
        denom = np.dot(self.normal, ray_dir)
        if np.abs(denom) < 1e-6:
            return None
        t = np.dot(self.point - ray_origin, self.normal) / denom
        if t > 0:
            return t
        return None

    def get_normal(self, point):
        return self.normal

class Disk:
    def __init__(self, center, normal, radius, material):
        self.center = np.array(center, dtype=float)
        self.normal = np.array(normal, dtype=float) / np.linalg.norm(normal)
        self.radius = radius
        self.material = material

    def intersect(self, ray_origin, ray_dir):
        denom = np.dot(self.normal, ray_dir)
        if np.abs(denom) < 1e-6:
            return None
        t = np.dot(self.center - ray_origin, self.normal) / denom
        if t < 0:
            return None
        hit = ray_origin + t * ray_dir
        if np.linalg.norm(hit - self.center) <= self.radius:
            return t
        return None

    def get_normal(self, point):
        return self.normal

class Triangle:
    def __init__(self, v0, v1, v2, material):
        self.v0 = np.array(v0, dtype=float)
        self.v1 = np.array(v1, dtype=float)
        self.v2 = np.array(v2, dtype=float)
        self.material = material

    def intersect(self, ray_origin, ray_dir):
        eps = 1e-6
        edge1 = self.v1 - self.v0
        edge2 = self.v2 - self.v0
        h = np.cross(ray_dir, edge2)
        a = np.dot(edge1, h)
        if -eps < a < eps:
            return None
        f = 1.0 / a
        s = ray_origin - self.v0
        u = f * np.dot(s, h)
        if u < 0.0 or u > 1.0:
            return None
        q = np.cross(s, edge1)
        v = f * np.dot(ray_dir, q)
        if v < 0.0 or u + v > 1.0:
            return None
        t = f * np.dot(edge2, q)
        if t > eps:
            return t
        return None

    def get_normal(self, point):
        return np.cross(self.v1 - self.v0, self.v2 - self.v0) / np.linalg.norm(np.cross(self.v1 - self.v0, self.v2 - self.v0))

class Cube:
    def __init__(self, center, size, material):
        self.center = np.array(center, dtype=float)
        self.size = size
        self.material = material
        self.bounds_min = self.center - size/2
        self.bounds_max = self.center + size/2

    def intersect(self, ray_origin, ray_dir):
        tmin = (self.bounds_min - ray_origin) / (ray_dir + 1e-8)
        tmax = (self.bounds_max - ray_origin) / (ray_dir + 1e-8)
        t1 = np.minimum(tmin, tmax)
        t2 = np.maximum(tmin, tmax)
        t_near = np.max(t1)
        t_far = np.min(t2)
        if t_near > t_far or t_far < 0:
            return None
        if t_near < 0:
            return t_far
        return t_near

    def get_normal(self, point):
        p = point - self.center
        half = self.size / 2
        for i in range(3):
            if np.isclose(p[i], half):
                n = np.zeros(3)
                n[i] = 1
                return n
            if np.isclose(p[i], -half):
                n = np.zeros(3)
                n[i] = -1
                return n
        return np.zeros(3)

class Renderer(object):
	def __init__(self, screen):
		self.screen = screen
		_, _, self.width, self.height = self.screen.get_rect()

		self.glColor(1,1,1)
		self.glClearColor(0,0,0)

		self.glClear()

		self.primitiveType = TRIANGLES

		self.models = []

		self.activeModelMatrix = None
		self.activeVertexShader = None


	def glClearColor(self, r, g, b):
		# 0 - 1
		r = min(1, max(0,r))
		g = min(1, max(0,g))
		b = min(1, max(0,b))

		self.clearColor = [r,g,b]


	def glColor(self, r, g, b):
		# 0 - 1
		r = min(1, max(0,r))
		g = min(1, max(0,g))
		b = min(1, max(0,b))

		self.currColor = [r,g,b]

	def glClear(self):
		color = [int(i * 255) for i in self.clearColor]
		self.screen.fill(color)

		self.frameBuffer = [[color for y in range(self.height)]
							for x in range(self.width)]


	def glPoint(self, x, y, color = None):
		# Pygame empieza a renderizar desde la esquina
		# superior izquierda, hay que voltear la Y

		x = round(x)
		y = round(y)

		if (0 <= x < self.width) and (0 <= y < self.height):
			color = [int(i * 255) for i in (color or self.currColor) ]

			self.screen.set_at((x,self.height - 1 - y ), color)

			self.frameBuffer[x][y] = color


	def glLine(self, p0, p1, color = None):
		# Algoritmo de Lineas de Bresenham
		# y = mx + b

		x0 = p0[0]
		x1 = p1[0]
		y0 = p0[1]
		y1 = p1[1]

		# Si el punto 0 es igual que el punto 1, solamente dibujar un punto
		if x0 == x1 and y0 == y1:
			self.glPoint(x0, y0)
			return

		dy = abs(y1 - y0)
		dx = abs(x1 - x0)

		steep = dy > dx

		if steep:
			x0, y0 = y0, x0
			x1, y1 = y1, x1

		if x0 > x1:
			x0, x1 = x1, x0
			y0, y1 = y1, y0

		dy = abs(y1 - y0)
		dx = abs(x1 - x0)

		offset = 0
		limit = 0.75
		m = dy / dx
		y = y0

		for x in range(round(x0), round(x1) + 1):
			if steep:
				self.glPoint(y, x, color or self.currColor)
			else:
				self.glPoint(x, y, color or self.currColor)

			offset += m

			if offset >= limit:
				if y0 < y1:
					y += 1
				else:
					y -= 1

				limit += 1


	def glTriangle(self, A, B, C):
		# Hay que asegurarse que los vertices entran en orden
		# A.y > B.y > C.y
		if A[1] < B[1]:
			A, B = B, A
		if A[1] < C[1]:
			A, C = C, A
		if B[1] < C[1]:
			B, C = C, B


		def flatBottom(vA, vB, vC):

			try:
				mBA = (vB[0] - vA[0]) / (vB[1] - vA[1])
				mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
			except:
				pass
			else:

				if vB[0] > vC[0]:
					vB, vC = vC, vB
					mBA, mCA = mCA, mBA

				x0 = vB[0]
				x1 = vC[0]

				for y in range(round(vB[1]), round(vA[1] + 1)):
					for x in range(round(x0), round(x1 + 1)):
						self.glPoint(x,y)

					x0 += mBA
					x1 += mCA

		def flatTop(vA, vB, vC):
			try:
				mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
				mCB = (vC[0] - vB[0]) / (vC[1] - vB[1])

			except:
				pass
			else:

				if vA[0] > vB[0]:
					vA, vB = vB, vA
					mCA, mCB = mCB, mCA

				x0 = vA[0]
				x1 = vB[0]

				for y in range(round(vA[1]), round(vC[1] - 1), -1):
					for x in range(round(x0), round(x1 + 1)):
						self.glPoint(x,y)

					x0 -= mCA
					x1 -= mCB


		if B[1] == C[1]:
			# Plano abajo
			flatBottom(A,B,C)

		elif A[1] == B[1]:
			# Plano arriba
			flatTop(A,B,C)

		else:
			# Irregular
			# Hay que dibujar ambos casos
			# Teorema del intercepto

			D = [ A[0] + ((B[1] - A[1]) / (C[1] - A[1])) * (C[0] - A[0]), B[1] ]
			flatBottom(A, B, D)
			flatTop(B, D, C)


	def glRender(self):
		
		for model in self.models:
			# Por cada modelo en la lista, los dibujo
			# Agarrar su matriz modelo y vertexshader
			self.activeModelMatrix = model.GetModelMatrix()
			self.activeVertexShader = model.vertexShader

			# Aqui vamos a guardar todos los vertices y su info correspondiente
			vertexBuffer = []

			for i in range(0, len(model.vertices), 3):

				x = model.vertices[i]
				y = model.vertices[i + 1]
				z = model.vertices[i + 2]

				# Si contamos con un Vertex Shader, se manda cada vertice
				# para transformalos. Recordar pasar las matrices necesarias
				# para usarlas dentro del shader
				if self.activeVertexShader:
					x, y, z = self.activeVertexShader([x,y,z],
													  modelMatrix = self.activeModelMatrix)

				vertexBuffer.append(x)
				vertexBuffer.append(y)
				vertexBuffer.append(z)

			self.glDrawPrimitives(vertexBuffer, 3)



	def glDrawPrimitives(self, buffer, vertexOffset):
		# El buffer es un listado de valores que representan
		# toda la informacion de un vertice (posicion, coordenadas
		# de textura, normales, color, etc.). El VertexOffset se
		# refiere a cada cuantos valores empieza la informacion
		# de un vertice individual
		# Se asume que los primeros tres valores de un vertice
		# corresponden a Posicion.

		if self.primitiveType == POINTS:
			# Si son puntos, revisamos el buffer en saltos igual
			# al Vertex Offset. El valor X y Y de cada vertice
			# corresponden a los dos primeros valores.
			for i in range(0, len(buffer), vertexOffset):
				x = buffer[i]
				y = buffer[i + 1]
				self.glPoint(x,y)


		elif self.primitiveType == LINES:
			# Si son lineas, revisamos el buffer en saltos igual
			# a 3 veces el Vertex Offset, porque cada trio corresponde
			# a un triangulo. 
			for i in range(0, len(buffer), vertexOffset * 3):
				for j in range(3):
					# Hay que dibujar la linea de un vertice al siguiente
					x0 = buffer[i + vertexOffset * j + 0]
					y0 = buffer[i + vertexOffset * j + 1]

					# En caso de que sea el ultimo vertices, el siguiente
					# seria el primero
					x1 = buffer[i + vertexOffset * ((j + 1) % 3) + 0]
					y1 = buffer[i + vertexOffset * ((j + 1) % 3) + 1]

					self.glLine((x0,y0), (x1,y1) )

		elif self.primitiveType == TRIANGLES:
			# Si son triangulos revisamos el buffer en saltos igual
			# a 3 veces el Vertex Offset, porque cada trio corresponde
			# a un triangulo. 
			for i in range(0, len(buffer), vertexOffset * 3):
				# Necesitamos tres vertices para mandar a dibujar el triangulo.
				# Cada vertice necesita todos sus datos, la cantidad de estos
				# datos es igual a VertexOffset
				A = [ buffer[i + j + vertexOffset * 0] for j in range(vertexOffset) ]
				B = [ buffer[i + j + vertexOffset * 1] for j in range(vertexOffset) ]
				C = [ buffer[i + j + vertexOffset * 2] for j in range(vertexOffset) ]

				self.glTriangle(A,B,C)










