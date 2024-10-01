import pygame

from math import sqrt

from ray import Ray
from utility import colors

# References:
# https://raytracing.github.io/books/RayTracingInOneWeekend.html

class Viewport:
	def __init__(self, camerapos, window):
		focal_length = 1
		aspect_ratio = 16/16
		winx, winy = window

		self.image_width = winx
		self.image_height = winy / aspect_ratio
		self.image_height = 1 if self.image_height < 1 else self.image_height

		self.viewport_u = pygame.math.Vector3(2, 0, 0)
		self.viewport_v = pygame.math.Vector3(0, -2, 0)

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
		self.objects = []
		self.sphere_color = colors["red"]

	def add_object(self, object):
		self.objects.append(object)

	def calculate_normal_color(self, vec):
		xval = abs(255 * vec.x)
		yval = abs(255 * vec.y)
		zval = abs(255 * vec.z)

		return (int(xval), int(yval), int(zval))

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
			return None

		perp = sqrt(L_squared - tc*tc)

		if radius < perp:
			return None

		t1c = sqrt(radius*radius - perp*perp)
		t1 = tc - t1c
		t2 = tc + t1c

		return [ray.get_p(t1), ray.get_p(t2)]

	def aliase_help(self, screen, window, coord):
		color_vals = []
		winx,winy = window
		pixel_x,pixel_y = coord

		for j in range(pixel_y - 1, pixel_y + 2):
			for i in range(pixel_x - 1, pixel_x + 2):
				if i < 0 or i >= winx or j < 0 or j >= winy:
					continue
				color_vals.append(screen.get_at((i,j))[:-1])

		sumr = 0
		sumg = 0
		sumb = 0
		for i in color_vals:
			r,g,b = i
			sumr += r
			sumg += g
			sumb += b

		n_items = len(color_vals)
		n_colors = (sumr//n_items, sumg//n_items, sumb//n_items)

		return screen.set_at((pixel_x, pixel_y), n_colors)

	def aliase(self, screen, window, coord, cycles=1):
		for i in range(cycles):
			self.aliase_help(screen, window, coord)

	def render(self, screen, window, coord):
		i,j = coord

		# Calculate the position from the current viewport coord
		# to the origin of the casted ray
		pixel_location = self.viewport.pixel_location
		delta_u = self.viewport.delta_u
		delta_v = self.viewport.delta_v

		pixel_center = pixel_location + (i * delta_u) + (j * delta_v)

		# Create the ray
		ray_origin = self.camerapos
		ray_direction = pixel_center - ray_origin
		ray = Ray(ray_origin, ray_direction.normalize())

		# Render spheres
		for object in self.objects:
			if object.type != "sphere":
				continue

			result = self.sphere_calc(object, ray)
			if result is None:
				continue

			# Calculate normal
			res1,res2 = result
			nvec = None
			if ray.origin.distance_to(res1) < ray.origin.distance_to(res2):
				nvec = res1
			else:
				nvec = res2

			normalvec = (nvec - object.vector).normalize()

			# Calculate front-face
			front_face = True if ray.direction.dot(normalvec) < 0 else False
			if front_face == False:
				normalvec = normalvec * -1

			screen.set_at((i,j), self.calculate_normal_color(normalvec))
			return

		# Drop out of the geometry collision calculations
		# if we didn't hit any objects of interest
		screen.set_at((i,j), self.calculate_background_color(ray))
