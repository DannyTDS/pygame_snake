'''
written by Ziang Tong
This file contains the main() function for the project. Run this file 
to start the game.
'''

import sys, pygame
from snake import Snake
from fruit import Fruit
from button import Button
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
	"playerA_head"	: "./Assets/db_playerA_head.png",
	"playerA_body"	: "./Assets/db_playerA_body.png",
	"playerB_head"	: "./Assets/db_playerB_head.png",
	"playerB_body"	: "./Assets/db_playerB_body.png",
	"gd_fruit"	: "./Assets/gd_fruit.png",
	"bd_fruit"	: "./Assets/bd_fruit.png",
}


# turning keys
turning_keys = [
	pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s,
	pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN,
]

# for competition mode
playerA_turning_keys = [
	pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s,
]

playerB_turning_keys = [
	pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN,
]


# GLOBALS
width 		= 1200							# size of the window
height 		= 800 
speed 		= 20							# player speed
direction 	= 'r'							# player direction
bg_color 	= BLACK							# background color, in RGB
frame_time 	= 80							# wait time between frames, in ms
fruit_interval = 1500						# wait time between generation of fruits, in ms
	

def main():
	# initialize screen and load prefabs
	screen 	= gm.setup((width, height))
	prefabs = gm.load_prefabs(prefab_paths)
	next_step = "menu"
	
	while 1:
		if next_step == "menu":
			game_mode = gm.load_homescreen(screen)
			if game_mode == "single":
				next_step = start_classic(screen, prefabs)
			elif game_mode == "double":
				next_step = start_combat(screen, prefabs)
		elif next_step == "restart":
			if game_mode == "single":
				next_step = start_classic(screen, prefabs)
			elif game_mode == "double":
				next_step = start_combat(screen, prefabs)
		elif next_step == "quit":
			sys.exit()


# Single player mode
def start_classic(screen, prefabs):
	# initialize player
	the_snake = Snake((width/2, height/2), 'r')
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
			next_step = gm.classic_game_over(screen, the_snake, score, prefabs)
			return next_step
		
		pygame.time.wait(frame_time)
		
		# increment fruit_cooldown and update occupied_slots
		fruit_cooldown += 1
		occupied_slots = gm.update_occupancy(the_snake, active_fruits)
		active_fruits = gm.decay_fruits(active_fruits)


# Two players mode
def start_combat(screen, prefabs):
	'''
	special rules:
	1. can cross the snake itself
	2. try to surround the other snake
	3. die when crash into the other snake
	4. faster fruit generation
	'''
	player_A = Snake((120, 120), 'r')
	player_B = Snake((width-120, height-120), 'l')
	for i in range(2):
		player_A.add_body()
		player_B.add_body()

	# initialize screen color and score
	fruit_interval = 500
	fruit_cooldown = 0
	active_fruits = []
	occupied_slots = gm.update_occupancy(player_A, active_fruits, player_B)
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
				if event.key in playerA_turning_keys:
					if event.key == pygame.K_d:
						tmp_A_dir = 'r'
					elif event.key == pygame.K_a:
						tmp_A_dir = 'l'
					elif event.key == pygame.K_w:
						tmp_A_dir = 'u'
					elif event.key == pygame.K_s:
						tmp_A_dir = 'd'
					if tmp_A_dir in player_A.get_eligible_moves():
						player_A.set_head_dir(tmp_A_dir)
				elif event.key in playerB_turning_keys:
					if event.key == pygame.K_RIGHT:
						tmp_B_dir = 'r'
					elif event.key == pygame.K_LEFT:
						tmp_B_dir = 'l'
					elif event.key == pygame.K_UP:
						tmp_B_dir = 'u'
					elif event.key == pygame.K_DOWN:
						tmp_B_dir = 'd'
					if tmp_B_dir in player_B.get_eligible_moves():
						player_B.set_head_dir(tmp_B_dir)
				elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
					sys.exit()
				elif event.key == pygame.K_p or event.key == pygame.K_SPACE:
					gm.pause(screen)

		# character control
		player_A.update_body(speed)
		player_B.update_body(speed)
		
		# check if player ate fruit
		gm.update_eat_fruit(player_A, active_fruits)
		gm.update_eat_fruit(player_B, active_fruits)
		
		# check if new fruit needs to be generated
		if(fruit_cooldown >= fruit_interval/frame_time):
			active_fruits.append(Fruit(occupied_slots))
			fruit_cooldown = 0

		# update screen
		gm.update_two_players(screen, player_A, player_B, active_fruits, prefabs, bg_color)
		
		# check if game over
		if (not player_A.is_alive() or gm.collide_into(player_A, player_B)):
			next_step = gm.combat_game_over(screen, player_A, player_B, prefabs, "B")
			return next_step
		if (not player_B.is_alive() or gm.collide_into(player_B, player_A)):
			next_step = gm.combat_game_over(screen, player_A, player_B, prefabs, "A")
			return next_step
		
		pygame.time.wait(frame_time)
		
		# increment fruit_cooldown and update occupied_slots
		fruit_cooldown += 1
		occupied_slots = gm.update_occupancy(player_A, active_fruits, player_B)
		active_fruits = gm.decay_fruits(active_fruits)


if __name__ == "__main__":
	main()
