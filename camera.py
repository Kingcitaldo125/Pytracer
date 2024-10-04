import pygame

from math import radians, tan


class Camera:
	def __init__(self, pos, window, fov=57):
		self.pos = pos

		# fov in degrees
		self.samples_per_pixel = 10

		focal_length = 1.0
		aspect_ratio = 2
		winx,winy = window

		image_width = winx
		image_height = image_width // aspect_ratio
		#image_height = 1 if image_height < 1 else image_height
		
		theta = radians(fov)
		h = tan(theta / 2)
		viewport_height = 2 * h * focal_length
		viewport_width = viewport_height * (image_width / image_height)

		viewport_u = pygame.math.Vector3(viewport_width, 0, 0)
		viewport_v = pygame.math.Vector3(0, -viewport_height, 0)

		self.delta_u = viewport_u / image_width
		self.delta_v = viewport_v / image_height

		upper_left = self.pos - pygame.math.Vector3(0, 0, focal_length)
		upper_left = upper_left - viewport_u//2
		upper_left = upper_left - viewport_v//2

		self.pixel_location = upper_left + 0.5 * (self.delta_u + self.delta_v)
