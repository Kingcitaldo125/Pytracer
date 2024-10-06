import pygame

from math import inf

from pytracer.interval import Interval
from pytracer.material import Material
from pytracer.ray import Ray
from pytracer.utility import colors, random_hemisphere

# References:
# https://raytracing.github.io/books/RayTracingInOneWeekend.html

class HitRecord:
	def __init__(self):
		self.front_face = False
		self.normal = pygame.math.Vector3(0,0,0)
		self.material = Material()
		self.p = None
		self.t = None

	def __str__(self):
		return "p: " + str(self.p) + " t: " + str(self.t)

	def set_face_normal(self, ray, outward_normal):
		self.front_face = ray.direction.dot(outward_normal) < 0
		self.normal = outward_normal if self.front_face else outward_normal * -1

class Renderer:
	def __init__(self, camera):
		self.camera = camera
		self.objects = []
		self.sphere_color = colors["red"]
		self.zero_color_vector = pygame.math.Vector3(0.0,0.0,0.0)
		self.base_color_vector = pygame.math.Vector3(1.0,1.0,1.0)
		self.samples_per_pixel = 10
		self.ray_interval = Interval(0.001,inf)

	def add_object(self, object):
		self.objects.append(object)

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

	def calculate_background_color(self, ray):
		white = colors["white"]
		blue = colors["blue"]

		ray_hat = ray.direction.normalize()

		a = (ray_hat.y + 1.0) / 2

		xchan = 0.5
		ychan = 0.7
		zchan = 1.0

		x = (1.0-a) + a*xchan
		y = (1.0-a) + a*ychan
		z = (1.0-a) + a*zchan

		return pygame.math.Vector3(x, y, z)

	def calculate_surf_color(self, ray, interval, debug=False):
		if ray.hit_limit():
			return self.zero_color_vector

		record = HitRecord()
		closest = interval.max
		base_material = Material()
		hit_something = False
		for obj in self.objects:
			ninterval = Interval(interval.min, closest)

			if obj.hit(ray, ninterval, record) == False:
				continue

			hit_something = True
			closest = min(closest, record.t)
			base_material = obj.material

		if not hit_something:
			return self.calculate_background_color(ray)

		# Calculate surface color based on the object's material
		scattered,attenuation = base_material.scatter(ray, record)

		scol = self.calculate_surf_color(scattered, interval)

		rx = round(attenuation.x * scol.x, 1)
		ry = round(attenuation.y * scol.y, 1)
		rz = round(attenuation.z * scol.z, 1)

		return pygame.math.Vector3(rx,ry,rz)

	def hit_anything(self, ray):
		for object in self.objects:
			result = object.hit(ray, self.ray_interval, HitRecord())

			if result:
				return True

		return False

	def render(self, screen, window, coord):
		i,j = coord

		# Calculate the position from the current coord
		# to the origin of the casted ray
		pixel_location = self.camera.pixel_location
		delta_u = self.camera.delta_u
		delta_v = self.camera.delta_v

		pixel_center = pixel_location + (i * delta_u) + (j * delta_v)

		# Create the ray
		ray_origin = self.camera.pos
		ray_direction = (pixel_center - ray_origin).normalize()
		ray = Ray(ray_origin, ray_direction, 0)

		# Drop out of the geometry collision calculations
		# if we didn't hit any objects of interest
		if self.hit_anything(ray) == False:
			bcol = self.calculate_background_color(ray)

			bc_x = bcol.x * 255
			bc_y = bcol.y * 255
			bc_z = bcol.z * 255

			screen.set_at((i,j), (bc_x, bc_y, bc_z))
			return

		# Render objects
		ray = Ray(ray_origin, ray_direction, 0)
		pixel_color = pygame.math.Vector3(0,0,0)
		for sample in range(self.samples_per_pixel):
			surf_col = self.calculate_surf_color(ray, self.ray_interval)
			surf_col = surf_col * 255

			surf_col.x = int(surf_col.x)
			surf_col.y = int(surf_col.y)
			surf_col.z = int(surf_col.z)

			pixel_color += surf_col

		fx = pixel_color.x // self.samples_per_pixel
		fy = pixel_color.y // self.samples_per_pixel
		fz = pixel_color.z // self.samples_per_pixel

		screen.set_at((i,j), (fx, fy, fz))
