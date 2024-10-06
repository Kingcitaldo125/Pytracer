import pygame

from math import radians, tan

class Camera:
	def __init__(self, pos, target, window, fov=90):
		self.pos = pos
		# fov in degrees
		self.fov = fov
		self.window = window
		self.aspect_ratio = 1.0

		# Defaults to be accessed by scene renderer
		self.delta_u = 0
		self.delta_v = 0
		self.pixel_location = 0

		# Establish camera/view frustrum reference frame
		# w = forward; u = right; v = up
		self.up_ref_vec = pygame.math.Vector3(0.0,1.0,0.0)
		self.forward = pygame.math.Vector3(0.0,0.0,-1.0)
		self.up = self.up_ref_vec
		self.right = pygame.math.Vector3(1.0,0.0,0.0)

		self.samples_per_pixel = 10

		self.look_at(target)

	def look_at(self, target):
		# w = forward; u = right; v = up
		self.forward = (self.pos - target).normalize()
		self.right = self.up_ref_vec.cross(self.forward).normalize()
		self.up = self.forward.cross(self.right)

		print(f"forward {self.forward}")
		print(f"right {self.right}")
		print(f"up {self.up}")

		self.render_viewport(target)

	def render_viewport(self, target):
		focal_length = (self.pos - target).length()
		winx,winy = self.window

		image_width = winx
		image_height = winx // self.aspect_ratio

		theta = radians(self.fov)
		h = tan(theta / 2)
		viewport_height = 2 * h * focal_length
		viewport_width = viewport_height

		viewport_u = viewport_width * self.right
		viewport_v = viewport_height * self.up * -1

		self.delta_u = viewport_u / image_width
		self.delta_v = viewport_v / image_height

		focal_forward = focal_length * self.forward

		upper_left = self.pos - focal_forward
		upper_left = upper_left - viewport_u/2
		upper_left = upper_left - viewport_v/2

		self.pixel_location = upper_left + 0.5 * (self.delta_u + self.delta_v)
