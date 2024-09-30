import pygame

from math import sqrt
from random import randrange as rr
from threading import Thread

from renderer import Renderer, Viewport
from geometry import Sphere
from ray import Ray

done = False

def render_help(screen, window, scene_geometry):
	global done

	camerapos = pygame.math.Vector3(0,0,0)

	vport = Viewport(camerapos, window)
	renderer = Renderer(camerapos, vport)
	winx,winy = window

	# Add geometry to the scene
	for item in scene_geometry:
		renderer.add_object(item)

	for i in range(winx):
		if done:
			return

		for j in range(winy):
			if done:
				return

			renderer.render(screen, (i,j), window)
		pygame.display.flip()

def main(winx=500, winy=500):
	global done

	pygame.display.init()
	screen = pygame.display.set_mode((winx,winy))
	clock = pygame.time.Clock()

	scene_geometry = [Sphere(0,0,-1,0.5)]
	thread_args = (screen, (winx,winy), scene_geometry)

	render_thread = Thread(target=render_help, args=thread_args)
	render_thread.start()
	while not done:
		clock.tick(30)

		events = pygame.event.get()
		for e in events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					done = True
					break

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
			print(i,j,renderer.calculate_background_color(ray))
			ray.direction.y += 0.1
		ray.direction.y = 0

if __name__ == "__main__":
	main()
