import pygame

from math import sqrt

from ray import Ray
from utility import calculate_normal, colors, random_hemisphere


class Object:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		self.vector = pygame.math.Vector3(self.x, self.y, self.z)
		self.type = "unknown"

	def hit(self, ray, interval=0.001):
		return False

	def calculate_surf_color(self, ray, vec):
		return (0,0,0)

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

	def calculate_surf_color(self, ray, vec):
		if ray.hit_limit():
			return (0,0,0)

		result = self.hit(ray)

		if result is None:
			direction = ray.direction
			dy = direction.y
			if dy < 0:
				dy = 0
			cvec = dy * pygame.math.Vector3(255,255,255)
			return (cvec.x, cvec.y, cvec.z)

		# Calculate reflection vector direction
		normal = calculate_normal(ray, result)
		normalvec = (normal - self.vector).normalize()

		# Determine if we hit a front-face
		fface = ray.direction.dot(normalvec) < 0
		normalvec = normalvec if fface else normalvec * -1

		# Calculate the reflection direction based on faces/scatter direction
		random_dir = normalvec + random_hemisphere(vec)

		ray = Ray(normal, random_dir, ray.bounces + 1)
		scol = self.calculate_surf_color(ray, normalvec)

		x = scol[0] * 0.5
		y = scol[1] * 0.5
		z = scol[2] * 0.5

		return (x,y,z)
