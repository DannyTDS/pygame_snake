import sys, pygame

# default button sizes
btn_width = 700
btn_height = 300

# Button Class
class Button():
    def __init__(self, color, x, y, text_color, text=''):
        # Button Characteristics
        self.color = color
        self.x = x
        self.y = y
        self.text = text
        self.text_color = text_color
        self.rect = None

    #Method to draw the button
    def draw(self,win):
        # pygame.draw.rect(win, True, (self.x, self.y, self.x+btn_width, self.y+btn_height))
            
        # pygame.draw.rect(win, self.color, (self.x, self.y, self.x+btn_width, self.y+btn_height),0)
        
        font_path = "./Assets/Fonts/Monaco.ttf"
        font = pygame.font.Font(font_path, 32)
        font.set_bold(True)
        
        text = font.render(self.text, True, self.text_color)
        btn_rect = text.get_rect(topleft=(self.x, self.y))
        
        win.blit(text, btn_rect)
        self.rect = btn_rect
