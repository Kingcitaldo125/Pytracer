import pygame

from math import sqrt

from ray import Ray
from utility import near_zero, random_double, random_vec_sphere, random_vec3_clamp, reflect, refract


class Material:
	def __init__(self):
		self.albedo = pygame.math.Vector3(1.0,1.0,1.0)
		self.type = "base"

	def scatter(self, ray_in, record):
		return None

class Lambertian(Material):
	def __init__(self, albedo):
		super().__init__()
		self.albedo = albedo
		self.type = "lambertian"

	def scatter(self, ray_in, record):
		scatter_dir = record.normal + random_vec3_clamp(-1,1)

		# Catch edge case where random direction cancels-out normalvec
		while near_zero(scatter_dir):
			scatter_dir = record.normal + random_vec3_clamp(-1,1)

		ray = Ray(record.p, scatter_dir, ray_in.bounces + 1)

		return [ray, self.albedo]

class Metal(Material):
	def __init__(self, albedo, fuzzy=False):
		super().__init__()
		self.albedo = albedo
		self.fuzzy = fuzzy
		self.fuzzy_rad = 0.75
		self.type = "metal"

	def scatter(self, ray_in, record):
		ref_v = reflect(ray_in.direction, record.normal)

		if self.fuzzy:
			ref_v = ref_v + random_vec_sphere(ref_v, self.fuzzy_rad)
			ref_v.normalize_ip()

		return [Ray(record.p, ref_v, ray_in.bounces + 1), self.albedo]

class Glass(Material):
	def __init__(self, refraction_idx):
		super().__init__()
		self.refraction_idx = refraction_idx
		self.rf_idx_inv = (1.0 / self.refraction_idx)
		self.attenuation = pygame.math.Vector3(1.0,1.0,1.0)
		self.type = "glass"

	def reflectance(self, cos_theta, ri):
		rtheta = (1 - ri) / (1 + ri)
		rtheta_squared = rtheta * rtheta
		neg_cos = (1 - cos_theta)
		neg_theta = (1 - rtheta_squared)
		return rtheta_squared + neg_theta * neg_cos**5

	def scatter(self, ray_in, record):
		ri = self.rf_idx_inv if record.front_face else self.refraction_idx

		unit_dir = ray_in.direction.normalize()
		unit_dir_inv = unit_dir * -1

		cos_theta = min(unit_dir_inv.dot(record.normal), 1.0)
		sin_theta = sqrt(1.0 - cos_theta * cos_theta)

		cannot_refract = ri * sin_theta > 1.0
		direction = None

		if cannot_refract or self.reflectance(cos_theta, ri) > random_double(0,1):
			direction = reflect(unit_dir, record.normal)
		else:
			direction = refract(unit_dir, record.normal, ri)

		return [Ray(record.p, direction, ray_in.bounces + 1), self.attenuation]
