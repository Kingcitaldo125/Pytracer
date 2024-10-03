import pygame

from math import sqrt

from ray import Ray
from utility import colors


class Object:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		self.position = pygame.math.Vector3(self.x, self.y, self.z)
		self.type = "unknown"
		self.item_id = -1

	def hit(self, ray, ray_interval):
		return False

class Sphere(Object):
	def __init__(self, x, y, z, rad, mat):
		super().__init__(x, y, z)
		self.radius = rad
		self.radius_squared = self.radius * self.radius
		self.color = colors["red"]
		self.type = "sphere"
		self.material = mat

	def __str__(self):
		return str(self.item_id) + ":" + str(self.x) + "," + str(self.y) + "," + str(self.z)

	def set_id(self,nid):
		self.item_id = nid

	def hit(self, ray, ray_interval, record):
		# References:
		# https://kylehalladay.com/blog/tutorial/math/2013/12/24/Ray-Sphere-Intersection.html
		# https://youtu.be/HFPlKQGChpE?si=YXX-EGaqQijDr4oE
		# https://raytracing.github.io/books/RayTracingInOneWeekend.html

		L = self.position - ray.origin
		L_len = L.length()
		tc = L.dot(ray.direction)

		if tc < 0 or L_len < tc:
			return False

		L_squared = L.length_squared()
		perp = sqrt(L_squared - tc*tc)

		if self.radius < perp:
			return False

		t1c = sqrt(self.radius_squared - perp*perp)
		t1 = tc - t1c
		t2 = tc + t1c

		root = ray.get_p(t1)
		chosen_t = t1
		if ray_interval.surrounds(t1) == False:
			root = ray.get_p(t2)
			chosen_t = t2
			if ray_interval.surrounds(t2) == False:
				return False

		record.p = root
		record.t = chosen_t
		normalvec = (root - self.position) / self.radius
		record.set_face_normal(ray, normalvec)
		record.material = self.material

		return True
