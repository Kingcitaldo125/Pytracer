import pygame

from math import sqrt
from random import randrange as rr
from threading import Thread

from renderer import Renderer, Viewport
from ray import Ray

done = False

def render_help(screen, window):
	global done

	camerapos = pygame.math.Vector3(0,0,0)

	vport = Viewport(camerapos, window)
	renderer = Renderer(camerapos, vport)
	winx,winy = window

	for i in range(winx):
		if done:
			return
		for j in range(winy):
			if done:
				return
			#print(i,j,renderer.calculate_color(i,j))
			renderer.render(screen, (i,j), window)

def main(winx=600, winy=600):
	global done

	pygame.display.init()
	screen = pygame.display.set_mode((winx,winy))
	clock = pygame.time.Clock()

	render_thread = Thread(target=render_help, args=(screen, (winx,winy)))
	render_thread.start()
	while not done:
		clock.tick(60)

		events = pygame.event.get()
		for e in events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					done = True
					break

		pygame.display.flip()

	render_thread.join()
	pygame.display.quit()

def scratch():
	camerapos = pygame.math.Vector3(0,0,0)
	vport = Viewport(camerapos, (600,600))
	renderer = Renderer(camerapos, vport)

	ray_origin = camerapos
	ray_direction = pygame.math.Vector3(0,0,1) - ray_origin

	ray = Ray(ray_origin, ray_direction.normalize())

	for i in range(25):
		for j in range(25):
			print(i,j,renderer.calculate_color(ray))
			ray.direction.y += 0.1
		ray.direction.y = 0

if __name__ == "__main__":
	main()
