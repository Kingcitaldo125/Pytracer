import pygame

from math import inf

import material

from ray import Ray
from interval import Interval
from utility import colors, random_hemisphere

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

class HitRecord:
	def __init__(self):
		self.front_face = False
		self.normal = pygame.math.Vector3(0,0,0)
		self.material = material.Material()
		self.p = None
		self.t = None

	def __str__(self):
		return "p: " + str(self.p) + " t: " + str(self.t)

	def set_face_normal(self, ray, outward_normal):
		self.front_face = ray.direction.dot(outward_normal) < 0
		self.normal = outward_normal if self.front_face else outward_normal * -1

class Renderer:
	def __init__(self, camerapos, viewport):
		self.camerapos = camerapos
		self.viewport = viewport
		self.objects = []
		self.sphere_color = colors["red"]
		self.zero_color_vector = pygame.math.Vector3(0,0,0)
		self.base_color_vector = pygame.math.Vector3(255,255,255)
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
			if debug:
				print('hit limit')
			return self.zero_color_vector

		record = HitRecord()
		closest = interval.max
		base_material = material.Material()
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
		retcol = pygame.math.Vector3(rx,ry,rz)

		if debug:
			print(f"attenuation {attenuation}")
			print(f"scol {scol}")
			print(f"retcol {retcol}")
			print('')

		return retcol

	def hit_anything(self, ray):
		for object in self.objects:
			result = object.hit(ray, self.ray_interval, HitRecord())

			if result:
				return True

		return False

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
		ray = Ray(ray_origin, ray_direction.normalize(), 0)

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
		ray = Ray(ray_origin, ray_direction.normalize(), 0)
		pixel_color = pygame.math.Vector3(0,0,0)
		for sample in range(self.samples_per_pixel):
			surf_col = self.calculate_surf_color(ray, self.ray_interval)
			surf_col = surf_col * 255

			surf_col.x = int(surf_col.x)
			surf_col.y = int(surf_col.y)
			surf_col.z = int(surf_col.z)

			#print(f"surf_col {surf_col}")
			pixel_color += surf_col

		fx = pixel_color.x // self.samples_per_pixel
		fy = pixel_color.y // self.samples_per_pixel
		fz = pixel_color.z // self.samples_per_pixel

		#print("fx", fx)
		#print("fy", fy)
		#print("fz", fz)

		screen.set_at((i,j), (fx, fy, fz))
