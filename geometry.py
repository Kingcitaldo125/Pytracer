import pygame

from utility import colors

class Object:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		self.vector = pygame.math.Vector3(self.x, self.y, self.z)
		self.type = "unknown"

class Sphere(Object):
	def __init__(self, x, y, z, rad):
		super().__init__(x, y, z)
		self.radius = rad
		self.color = colors["red"]
		self.type = "sphere"
