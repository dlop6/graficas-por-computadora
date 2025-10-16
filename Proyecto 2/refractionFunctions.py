import numpy as np
from math import acos, asin, pi

def refractVector(normal, incident, n1, n2):
	# Snell's Law		
	c1 = np.dot(normal, incident)
	
	if c1 < 0:
		c1 = -c1
	else:
		normal = np.array(normal) * -1
		n1, n2 = n2, n1

	n = n1 / n2
	
	# Verificar reflexión total interna
	discriminant = 1 - n**2 * (1 - c1**2)
	if discriminant < 0:
		# Reflexión total interna - no hay refracción
		return None
	
	T = n * (incident + c1 * normal) - normal * np.sqrt(discriminant)
	
	norm = np.linalg.norm(T)
	if norm < 1e-10:
		return None
	
	return T / norm


def totalInternalReflection(normal, incident, n1, n2):
	c1 = np.dot(normal, incident)
	if c1 < 0:
		c1 = -c1
	else:
		n1, n2 = n2, n1
		
	if n1 < n2:
		return False
	
	theta1 = acos(c1)
	thetaC = asin(n2/n1)
	
	return theta1 >= thetaC


def fresnel(normal, incident, n1, n2):
	c1 = np.dot(normal, incident)
	if c1 < 0:
		c1 = -c1
	else:
		n1, n2 = n2, n1

	s2 = (n1 * np.sqrt(max(0, 1 - c1**2))) / n2
	
	# Verificar reflexión total interna
	if s2 > 1.0:
		# Reflexión total - Kr = 1, Kt = 0
		return 1.0, 0.0
	
	c2 = np.sqrt(max(0, 1 - s2 ** 2))
	
	# Evitar división por cero
	denom1 = (n2 * c1) + (n1 * c2)
	denom2 = (n1 * c2) + (n2 * c1)
	
	if abs(denom1) < 1e-10 or abs(denom2) < 1e-10:
		return 1.0, 0.0
	
	F1 = (((n2 * c1) - (n1 * c2)) / denom1) ** 2
	F2 = (((n1 * c2) - (n2 * c1)) / denom2) ** 2

	Kr = (F1 + F2) / 2
	Kt = 1 - Kr
	return Kr, Kt
