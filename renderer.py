import pygame

from ray import Ray
from utility import calculate_normal, colors

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

		a = (ray.direction.y + 1.0) / 2

		xchan = 127
		ychan = 178
		zchan = 255

		x = (1.0-a)*255 + a*xchan
		y = (1.0-a)*255 + a*ychan
		z = (1.0-a)*255 + a*zchan

		return (x, y, z)

	def render(self, screen, window, coord, debug=False):
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

		# Render objects
		for object in self.objects:
			result = object.hit(ray)

			if result is None:
				continue

			nvec = calculate_normal(ray, result)
			normalvec = (nvec - object.vector).normalize()

			if debug:
				screen.set_at((i,j), (255,255,255))
				return

			surf_col = object.calculate_surf_color(ray, normalvec)
			#print(f"surf_col {surf_col}")
			screen.set_at((i,j), surf_col)
			return

		# Drop out of the geometry collision calculations
		# if we didn't hit any objects of interest
		screen.set_at((i,j), self.calculate_background_color(ray))
