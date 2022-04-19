'''
written by Ziang Tong
This file contains the functions for game control and 
Pygame visualization.
'''

import pygame
from snake import Snake

width 		= 800							# size of the window
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


# Update the game screen in one game loop
def update(screen, score, the_snake, prefabs, bg_color=BLACK):
	'''
	screen		:	the game screen
	the_snake	:	the snake that needs to be drawn
	prefabs		:	a dictionary, containing the prefabs loaded for head, body, and fruit
	'''
	screen.fill(bg_color)
	
	for i, node in enumerate(the_snake.get_body()):
		if i == 1:
			# head
			head_rect = prefabs["head"].get_rect(center=node.get_pos())
			screen.blit(prefabs["head"], head_rect)
		else:
			# body
			body_rect = prefabs["body"].get_rect(center=node.get_pos())
			screen.blit(prefabs["body"], body_rect)
		
		message_to_screen(screen, f"Score: {score}",
			WHITE, (5, 10), "medium", "left")
	
	pygame.display.update()


# Update the score
def update_score(screen, score):
	message_to_screen(screen, f"Score: {score}", 
		WHITE, score_pos, "medium", "left")
