import random

width 		= 1200							# size of the window
height 		= 800
types		= ("gd", "gd", "bd")
lifespan	= 10000							# lifetime of fruit, in ms

class Fruit:
	''' This class produces fruits to be displayed on the board'''
	
	def __init__(self, occupied_slots):
		'''
		occupied_slots is a list of tuples indicating which slots on 
		the board are already filled w/ snake or other fruit
		'''
		while True:
			x = random.randint(1, width/20 -1) * 20
			y = random.randint(1, height/20 -1) * 20
			
			if (x, y) in occupied_slots:
				continue
			else:
				break
		
		self._pos = (x, y)
		self._type = random.choice(types)
		self._life = lifespan
	
	
	def get_pos(self):
		return self._pos
	
	
	def get_type(self):
		return self._type


	def get_life(self):
		return self._life


	def decay(self):
		self._life -= 50
