import pygame

from utility import colors

class Object:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		self.vector = pygame.math.Vector3(self.x, self.y, self.z)

class Sphere(Object):
	def __init__(self, x, y, rad):
		self.radius = rad
		self.color = colors["red"]
