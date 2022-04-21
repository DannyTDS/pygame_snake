import sys, pygame

width 		= 1200							# size of the window
height 		= 800
types		= ("gd", "gd", "bd")

# Colors
BLACK 	= (0, 0, 0)
WHITE 	= (255, 255, 255)
RED 	= (255, 0, 0)
GREEN	= (0, 255, 0)
BLUE	= (0, 0, 255)

# Button Class
class Button():
    def __init__(self, color, x, y, text_color, text=''):
        # Button Characteristics
        self.color = color
        self.x = x
        self.y = y
        self.text = text
        self.text_color = text_color

    #Method to draw the button
    def draw(self,win):
        pygame.draw.rect(win, True, (self.x, self.y, self.x+700, self.y+300))
            
        pygame.draw.rect(win, self.color, (self.x, self.y, self.x + 700, self.y + 300),0)
        
        font = pygame.font.SysFont('arial', 60)
        
        text = font.render(self.text, 1, self.text_color)
        
        win.blit(text, (self.x + (350 - text.get_width()/2), self.y + (150 - text.get_height()/2)))

