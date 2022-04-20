'''
written by Ziang Tong
This file contains the functions for game control and 
Pygame visualization.
'''

import sys, pygame
from snake import Snake

width 		= 1200							# size of the window
height 		= 800

# color syntax sugars
BLACK 	= (0, 0, 0)
WHITE 	= (255, 255, 255)
RED 	= (255, 0, 0)
GREEN	= (0, 255, 0)
BLUE	= (0, 0, 255)


def setup(sz):
	# initialize the game window, return a Surface object
	pygame.init()
	screen = pygame.display.set_mode(size=sz)
	pygame.display.set_caption("SnakeX")
	return screen


# Returns a dictionary containing the loaded prefabs
def load_prefabs(prefab_paths):
	head = pygame.image.load(prefab_paths["head"])
	head = pygame.transform.scale(head, (20, 20))
	body = pygame.image.load(prefab_paths["body"])
	body = pygame.transform.scale(body, (20, 20))
	gd_fruit = pygame.image.load(prefab_paths["gd_fruit"])
	gd_fruit = pygame.transform.scale(gd_fruit, (20, 20))
	bd_fruit = pygame.image.load(prefab_paths["bd_fruit"])
	bd_fruit = pygame.transform.scale(bd_fruit, (20, 20))
	prefabs = {
		"head"		: head,
		"body" 		: body,
		"gd_fruit"	: gd_fruit,
		"bd_fruit"	: bd_fruit,
	}
	return prefabs


def pause(screen):
	# pause the game until another key stroke
	paused = True
	
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				paused = False
		
		message_to_screen(screen, "Paused",
			WHITE, (width/2, height/2), "large", "center")
		message_to_screen(screen, "Press any key to resume",
			WHITE, (width/2, height/2 + 50), "small", "center")
		pygame.time.wait(5)
		pygame.display.update()


def message_to_screen(screen, msg, color,
	anchor, size, align):
	# display text on appropriate location
	# generate Font object
	font_path = "./Assets/Fonts/Monaco.ttf"
	if size == "large":
		font = pygame.font.Font(font_path, 32)
		font.set_bold(True)
	elif size == "medium":
		font = pygame.font.Font(font_path, 24)
		font.set_bold(False)
	else:
		font = pygame.font.Font(font_path, 12)
		font.set_bold(False)
	
	# render the text & get position Rect
	text = font.render(msg, True, color, None)
	
	if align == "center":
		text_rect = text.get_rect(center=anchor)
	else:
		text_rect = text.get_rect(topleft=anchor)
		
	screen.blit(text, text_rect)
	return text_rect


# Update the game screen in one game loop
def update(screen, score, the_snake, active_fruits, prefabs, bg_color=BLACK):
	'''
	screen		:	the game screen
	the_snake	:	the snake that needs to be drawn
	prefabs		:	a dictionary, containing the prefabs loaded for head, body, and fruit
	'''
	screen.fill(bg_color)
	
	for i, node in enumerate(the_snake.get_body()):
		if i == 0:
			# head
			head_rect = prefabs["head"].get_rect(center=node.get_pos())
			screen.blit(prefabs["head"], head_rect)
		else:
			# body
			body_rect = prefabs["body"].get_rect(center=node.get_pos())
			screen.blit(prefabs["body"], body_rect)
	
	for fruit in active_fruits:
		if(fruit.get_type() == "gd"):
			fruit_rect = prefabs["gd_fruit"].get_rect(center=fruit.get_pos())
			screen.blit(prefabs["gd_fruit"], fruit_rect)
		elif(fruit.get_type() == "bd"):
			fruit_rect = prefabs["bd_fruit"].get_rect(center=fruit.get_pos())
			screen.blit(prefabs["bd_fruit"], fruit_rect)
	
	message_to_screen(screen, f"Score: {score}",
		WHITE, (5, 10), "medium", "left")
	
	pygame.display.update()


def update_occupancy(the_snake, active_fruits):
	occupied = []
	for node in the_snake.get_body():
		occupied.append(node.get_pos())
	for fruit in active_fruits:
		occupied.append(fruit.get_pos())
	return occupied


def update_eat_fruit(the_snake, active_fruits):
	head_pos = the_snake.get_head_pos()
	for fruit in active_fruits:
		if head_pos == fruit.get_pos():
			if fruit.get_type() == "gd":
				active_fruits.remove(fruit)
				the_snake.add_body()
				return 10
			elif fruit.get_type() == "bd":
				active_fruits.remove(fruit)
				the_snake.rm_body()
				return -5
	return 0


# Collision logic: when player collide with wall or himself
def self_collision(the_snake):
	head_pos = the_snake.get_body()[0].get_pos()
	
	# check collsion with walls
	if head_pos[0] < 0 or head_pos[0] > width:
		return True
	if head_pos[1] < 0 or head_pos[1] > height:
		return True
	
	# check collision with body
	for (i, node) in enumerate(the_snake.get_body()):
		if i == 0:
			# head
			continue
		else:
			if node.get_pos() == head_pos:
				return True
	
	# no collision detected
	return False


# Fruits decay overtime
def decay_fruits(active_fruits):
	for fruit in active_fruits:
		fruit.decay()
		if fruit.get_life() <= 0:
			active_fruits.remove(fruit)
	return active_fruits


# Game over animation controller
def game_over(screen, the_snake, prefabs, mode, bg_color=BLACK):
	screen.fill(bg_color)
	
	# Gradually pops back from the snake
	while(the_snake.is_alive()):
		the_snake.rm_body()
	
		screen.fill(bg_color)	
		for i, node in enumerate(the_snake.get_body()):
			if i == 0:
				# head
				head_rect = prefabs["head"].get_rect(center=node.get_pos())
				screen.blit(prefabs["head"], head_rect)
			else:
				# body
				body_rect = prefabs["body"].get_rect(center=node.get_pos())
				screen.blit(prefabs["body"], body_rect)
	
		pygame.display.update()
		pygame.time.wait(25)

	if mode[0] == "classic":
		message_to_screen(screen, "Game Over",
			RED, (width/2, height/2 - 10), "large", "center")
		score = mode[1]
		message_to_screen(screen, f"You scored: {score}",
			WHITE, (width/2, height/2 + 20), "small", "center")
		message_to_screen(screen, "Press any key to quit",
			WHITE, (width/2, height/2 + 40), "small", "center")

		pygame.display.update()
		
		pygame.time.wait(1000)
		
		while True:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					sys.exit()
