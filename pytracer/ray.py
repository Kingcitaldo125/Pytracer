from pygame.math import Vector3


class Ray:
	def __init__(self, origin, direction, bounces, bounce_limit=10):
		self.origin = origin
		self.direction = direction
		self.bounces = bounces
		self.bounce_limit = bounce_limit

	def hit_limit(self):
		return self.bounces >= self.bounce_limit

	def get_p(self, t):
		xpart = self.origin.x + self.direction.x * t
		ypart = self.origin.y + self.direction.y * t
		zpart = self.origin.z + self.direction.z * t

		return Vector3(xpart, ypart, zpart)
