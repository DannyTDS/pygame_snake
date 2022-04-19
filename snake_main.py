'''
written by Ziang Tong
This file contains the main() function for the project. Run this file 
to start the game.
'''

import sys, pygame
from snake import Snake
import game_manager as gm
# TODO: keep track of rects in Snake, instead of re-drawing every frame

# color syntax sugars
BLACK 	= (0, 0, 0)
WHITE 	= (255, 255, 255)
RED 	= (255, 0, 0)
GREEN	= (0, 255, 0)
BLUE	= (0, 0, 255)


# prefab paths
prefab_paths = {
	"head"		: "./Assets/test_square.png",
	"body" 		: "./Assets/test_square.png",
	"gd_fruit"	: "./Assets/test_square.png",
	"bd_fruit"	: "./Assets/test_square.png",
}


# turning keys
turning_keys = [
	pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s,
	pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN,
]


# GLOBALS
width 		= 800							# size of the window
height 		= 800
speed 		= 20							# player speed
direction 	= 'r'							# player direction
bg_color 	= BLACK							# background color, in RGB
frame_time 	= 50							# wait time between frames, in ms
	

def main():
	# initialize screen and load prefabs
	screen 	= gm.setup((width, height))
	prefabs = gm.load_prefabs(prefab_paths)
	
	# TODO: test player only. combine with Snake class
	the_snake = Snake((width/2, height/2))
	
	# Testing only: added some body segments
	for i in range(10):
		the_snake.add_body()
	
	# initialize screen color and score
	score = 0
	global direction
	screen.fill(BLACK)
	pygame.display.update()
	
	while 1:
		# event control
		for event in pygame.event.get():
			# quit game
			if event.type == pygame.QUIT:
				sys.exit()
			# player turning
			elif event.type == pygame.KEYDOWN:
				if event.key in turning_keys:
					if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
						direction = 'r'
					elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
						direction = 'l'
					elif event.key == pygame.K_w or event.key == pygame.K_UP:
						direction = 'u'
					elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
						direction = 'd'
					if direction in the_snake.get_eligible_moves():
						the_snake.set_head_dir(direction)
				elif event.key == pygame.K_q:
					sys.exit()
				elif event.key == pygame.K_p:
					gm.pause(screen)

		# character control
		the_snake.update_body(speed)
		
		# update screen
		gm.update(screen, score, the_snake, prefabs, bg_color)
		pygame.time.wait(frame_time)


if __name__ == "__main__":
	main()
