import pygame

class Ray:
	def __init__(self, origin, direction):
		self.origin = origin
		self.direction = direction

	def get_p(self, t):
		xpart = self.origin.x + self.direction.x * t
		ypart = self.origin.y + self.direction.y * t
		zpart = self.origin.z + self.direction.z * t

		return pygame.math.Vector3(xpart, ypart, zpart)
