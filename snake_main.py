'''
written by Ziang Tong
This file contains the main() function for the project. Run this file 
to start the game.
'''

import sys, pygame
from snake import Snake
from fruit import Fruit
import game_manager as gm


# color syntax sugars
BLACK 	= (0, 0, 0)
WHITE 	= (255, 255, 255)
RED 	= (255, 0, 0)
GREEN	= (0, 255, 0)
BLUE	= (0, 0, 255)


# prefab paths
prefab_paths = {
	"head"		: "./Assets/sg_player_head.png",
	"body" 		: "./Assets/sg_player_body.png",
	"gd_fruit"	: "./Assets/gd_fruit.png",
	"bd_fruit"	: "./Assets/bd_fruit.png",
}


# turning keys
turning_keys = [
	pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s,
	pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN,
]


# GLOBALS
width 		= 1200							# size of the window
height 		= 800
speed 		= 20							# player speed
direction 	= 'r'							# player direction
bg_color 	= BLACK							# background color, in RGB
frame_time 	= 50							# wait time between frames, in ms
fruit_interval = 1500						# wait time between generation of fruits, in ms
	

def main():
	# initialize screen and load prefabs
	screen 	= gm.setup((width, height))
	prefabs = gm.load_prefabs(prefab_paths)
	
	start_classic(screen, prefabs)



# Single player mode
def start_classic(screen, prefabs):
	# initialize player
	the_snake = Snake((width/2, height/2))
	for i in range(2):
		the_snake.add_body()
	
	# initialize screen color and score
	score = 0
	fruit_cooldown = 0
	active_fruits = []
	occupied_slots = gm.update_occupancy(the_snake, active_fruits)
	global direction
	screen.fill(bg_color)
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
				elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
					sys.exit()
				elif event.key == pygame.K_p or event.key == pygame.K_SPACE:
					gm.pause(screen)

		# character control
		the_snake.update_body(speed)
		
		# check if player ate fruit
		score += gm.update_eat_fruit(the_snake, active_fruits)
		
		# check if new fruit needs to be generated
		if(fruit_cooldown >= fruit_interval/frame_time):
			active_fruits.append(Fruit(occupied_slots))
			fruit_cooldown = 0

		# update screen
		gm.update(screen, score, the_snake, active_fruits, prefabs, bg_color)
		
		# check if game over
		if (not the_snake.is_alive() or gm.self_collision(the_snake)):
			gm.game_over(screen, the_snake, prefabs, ("classic", score))
		
		pygame.time.wait(frame_time)
		
		# increment fruit_cooldown and update occupied_slots
		fruit_cooldown += 1
		occupied_slots = gm.update_occupancy(the_snake, active_fruits)
		active_fruits = gm.decay_fruits(active_fruits)


# Two players mode
def start_combat(screen, prefabs):
	pass


if __name__ == "__main__":
	main()
