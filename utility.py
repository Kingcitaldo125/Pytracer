import pygame

from random import randrange as rr
from random import uniform

colors = {
	"white": (255,255,255),
	"red": (255,0,0),
	"blue": (0,0,255),
	"black": (0,0,0)
}

def random_color():
	return (rr(0,255), rr(0,255), rr(0,255))

def random_vec3():
	return pygame.math.Vector3(uniform(-1,1), uniform(-1,1), uniform(-1,1))

def random_vec3_clamp(min, max):
	xval = max + 1
	yval = max + 1
	zval = max + 1

	while xval < min or xval > max:
		xval = uniform(-1,1)

	while yval < min or yval > max:
		yval = uniform(-1,1)

	while zval < min or zval > max:
		zval = uniform(-1,1)

	return pygame.math.Vector3(xval,yval,zval)

def random_hemisphere(normalvec):
	vec = random_vec3_clamp(-1,1)
	vec.scale_to_length(1.0)
	return vec if vec.dot(normalvec) > 0.0 else vec * -1

def near_zero(vec, scale=1e-8):
	vx = abs(vec.x)
	vy = abs(vec.y)
	vz = abs(vec.z)

	return vx < scale and vy < scale and vz < scale

def reflect(vec,normal):
	return vec - 2 * vec.dot(normal) * normal
