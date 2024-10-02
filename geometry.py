import pygame

from math import sqrt

from ray import Ray
from utility import colors


class Object:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		self.vector = pygame.math.Vector3(self.x, self.y, self.z)
		self.type = "unknown"

	def hit(self, ray, interval=0.001):
		return False

class Sphere(Object):
	def __init__(self, x, y, z, rad):
		super().__init__(x, y, z)
		self.radius = rad
		self.radius_squared = self.radius * self.radius
		self.color = colors["red"]
		self.type = "sphere"

	def hit(self, ray, interval=0.001):
		# References:
		# https://kylehalladay.com/blog/tutorial/math/2013/12/24/Ray-Sphere-Intersection.html
		# https://youtu.be/HFPlKQGChpE?si=YXX-EGaqQijDr4oE

		L = self.vector - ray.origin
		L_squared = L*L
		tc = L.dot(ray.direction)

		if tc < interval or L_squared < tc:
			return None

		perp = sqrt(L_squared - tc*tc)

		if self.radius < perp:
			return None

		t1c = sqrt(self.radius_squared - perp*perp)
		t1 = tc - t1c
		t2 = tc + t1c

		return [ray.get_p(t1), ray.get_p(t2)]
