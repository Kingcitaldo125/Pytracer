import pygame

from ray import Ray
from utility import near_zero, random_vec_sphere, random_vec3_clamp, reflect


class Material:
	def __init__(self):
		self.albedo = pygame.math.Vector3(1.0,1.0,1.0)
		self.type = "base"
		self.fuzzy_rad = 0.1

	def scatter(self, ray_in, record, fuzzy=False):
		return None

class Lambertian(Material):
	def __init__(self, albedo):
		super().__init__()
		self.albedo = albedo
		self.type = "lambertian"

	def scatter(self, ray_in, record, fuzzy=False):
		scatter_dir = record.normal + random_vec3_clamp(-1,1)

		# Catch edge case where random direction cancels-out normalvec
		while near_zero(scatter_dir):
			scatter_dir = record.normal + random_vec3_clamp(-1,1)

		ray = Ray(record.p, scatter_dir, ray_in.bounces + 1)

		return [ray, self.albedo]

class Metal(Material):
	def __init__(self, albedo):
		super().__init__()
		self.albedo = albedo
		self.type = "metal"

	def scatter(self, ray_in, record, fuzzy=False):
		ref_v = reflect(ray_in.direction, record.normal)

		if fuzzy:
			ref_v = ref_v + random_vec_sphere(ref_v,self.fuzzy_rad)
			ref_v.normalize_ip()

		return [Ray(record.p, ref_v, ray_in.bounces + 1), self.albedo]
