import math

class Interval:
	def __init__(self, min, max):
		self.min = min
		self.max = max

	def size(self):
		return self.max - self.min

	def contains(self, x):
		return self.min <= x and x <= self.max

	def surrounds(self, x):
		return self.min < x and x < self.max

empty = Interval(math.inf, math.inf * -1)
universe = Interval(-1 * math.inf, math.inf)
