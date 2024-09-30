import pygame

from math import sqrt

from ray import Ray
from utility import colors

# References:
# https://raytracing.github.io/books/RayTracingInOneWeekend.html

class Viewport:
	def __init__(self, camerapos, window):
		focal_length = 1
		winx, winy = window

		self.image_width = winx
		self.image_height = winy

		self.viewport_u = pygame.math.Vector3(self.image_width, 0, 0)
		self.viewport_v = pygame.math.Vector3(0, -self.image_width, 0)

		self.delta_u = self.viewport_u / self.image_width
		self.delta_v = self.viewport_v / self.image_height

		upper_left = camerapos - pygame.math.Vector3(0, 0, focal_length)
		upper_left = upper_left - self.viewport_u//2
		upper_left = upper_left - self.viewport_v//2

		self.pixel_location = upper_left + 0.5 * (self.delta_u + self.delta_v)

class Renderer:
	def __init__(self, camerapos, viewport):
		self.camerapos = camerapos
		self.viewport = viewport

	def calculate_background_color(self, ray):
		white = colors["white"]
		blue = colors["blue"]

		a = (ray.direction.y + 1.0) / 2

		xchan = 127
		ychan = 178
		zchan = 255

		x = (1.0-a)*255 + a*xchan
		y = (1.0-a)*255 + a*ychan
		z = (1.0-a)*255 + a*zchan

		return (x, y, z)

	def sphere_calc(self, sphere, ray):
		# References:
		# https://kylehalladay.com/blog/tutorial/math/2013/12/24/Ray-Sphere-Intersection.html
		# https://youtu.be/HFPlKQGChpE?si=YXX-EGaqQijDr4oE

		radius = sphere.radius
		L = sphere.vector - ray.origin
		L_squared = L*L
		tc = L.dot(ray.direction)

		if tc < 0 or L_squared < tc:
			return [-1,-1]

		perp = sqrt(L_squared - tc*tc)

		if radius < perp:
			return [-1,-1]

		t1c = sqrt(radius*radius - perp*perp)
		t1 = tc - t1c
		t2 = tc + t1c

		return [ray.get_p(t1), ray.get_p(t2)]

	def render(self, screen, coord, window):
		i,j = coord

		pixel_location = self.viewport.pixel_location
		delta_u = self.viewport.delta_u
		delta_v = self.viewport.delta_v

		pixel_center = pixel_location + (i * delta_u) + (j * delta_v)
		ray_origin = self.camerapos
		ray_direction = pixel_center - ray_origin

		ray = Ray(ray_origin, ray_direction.normalize())

		screen.set_at((i,j), self.calculate_background_color(ray))
