import math

class Interval:
	def __init__(self, min, max):
		self.min = min
		self.max = max

	def size(self):
		return max - min

	def contains(self, x):
		return min <= x and x <= max

	def surrounds(self, x):
		return min < x and x < max

empty = Interval(math.inf, math.inf * -1)
universe = Interval(-1 * math.inf, math.inf)
