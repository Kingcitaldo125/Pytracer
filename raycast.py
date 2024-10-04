import pygame
import math

from random import randrange as rr
from time import time
from threading import Thread

import material

from renderer import Renderer
from geometry import Sphere
from camera import Camera

done = False

def render_help(screen, window, scene_geometry):
	global done

	winx,winy = window
	#cam_pos = pygame.math.Vector3(0,0,0)
	cam_pos = pygame.math.Vector3(-2,2,1)
	cam_target = pygame.math.Vector3(0,0,-1)
	cam = Camera(cam_pos, cam_target, window)
	renderer = Renderer(cam)

	do_alaising = False

	# Add geometry to the scene
	for item in scene_geometry:
		renderer.add_object(item)

	start = time()
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

	end = time()
	elapsed = int(end - start)
	print(f"Took '{elapsed}' seconds to render.")

def main(winx=500, winy=500):
	global done

	pygame.display.init()
	screen = pygame.display.set_mode((winx,winy))
	clock = pygame.time.Clock()

	scene_geometry = []

	#'''
	# Materials
	ground_metal = material.Lambertian(pygame.math.Vector3(0.8,0.8,0.0))
	center_metal = material.Lambertian(pygame.math.Vector3(0.1,0.2,0.5))
	left_glass = material.Glass(1.5)
	right_metal = material.Metal(pygame.math.Vector3(0.8,0.6,0.2), fuzzy=True)
	bubble = material.Glass(1.0/1.5)

	s1 = Sphere(0.0, -100.5, -1.0, 100, ground_metal)
	s2 = Sphere(0.0, 0.0, -1.2, 0.5, center_metal)
	s3 = Sphere(-1.0, 0.0, -1.0, 0.5, left_glass)
	s4 = Sphere(1.0, 0.0, -1.0, 0.5, right_metal)
	s5 = Sphere(-1.0, 0.0, -1.0, 0.4, bubble)

	scene_geometry.extend([s1,s2,s3,s4,s5])
	#'''

	for id,item in enumerate(scene_geometry):
		item.set_id(id + 1)
		print(f"Set {item}")

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

if __name__ == "__main__":
	main()
	#scratch()
