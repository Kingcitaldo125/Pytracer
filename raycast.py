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

	do_alaising = False

	# Add geometry to the scene
	for item in scene_geometry:
		renderer.add_object(item)

	print("Rendering...")
	for i in range(winx):
		if done:
			return

		for j in range(winy):
			if done:
				return

			renderer.render(screen, window, (i,j))
		pygame.display.flip()

	if do_alaising:
		print("Ailasing...")
		for i in range(winx):
			if done:
				return

			for j in range(winy):
				if done:
					return

				renderer.aliase(screen, window, (i,j), 2)
			pygame.display.flip()

	print("Done.")

def main(winx=500, winy=500):
	global done

	pygame.display.init()
	screen = pygame.display.set_mode((winx,winy))
	clock = pygame.time.Clock()

	# Base sphere, ground sphere
	scene_geometry = [Sphere(0,0,-1,0.5), Sphere(0,-100.5,-1,100)]
	thread_args = (screen, (winx,winy), scene_geometry)

	render_thread = Thread(target=render_help, args=thread_args)
	render_thread.start()
	repeat = False
	while not done:
		clock.tick(30)

		events = pygame.event.get()
		for e in events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE:
					repeat = True
					done = True
					break
				if e.key == pygame.K_ESCAPE:
					done = True
					break

	render_thread.join()
	pygame.display.quit()

	if repeat:
		done = False
		main(winx,winy)

def scratch():
	camerapos = pygame.math.Vector3(0,0,0)
	vport = Viewport(camerapos, (600,600))
	renderer = Renderer(camerapos, vport)

	ray_origin = camerapos
	ray_direction = pygame.math.Vector3(0,0,1) - ray_origin

	ray = Ray(ray_origin, ray_direction.normalize())
	
	for i in range(25):
		for j in range(25):
			ray.direction = pygame.math.Vector3(i,0,j) - ray.origin
			nc = None
			if ray.direction.length() != 0:
				ray.direction.normalize_ip()
				nc = renderer.calculate_normal_color(ray.direction)
			else:
				nc = (0,0,0)
			print(f"normal color: {nc}")

if __name__ == "__main__":
	main()
	#scratch()
