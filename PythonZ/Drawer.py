import pygame
class Drawer:    
    """Drawer class that acts as a wrapper for code to draw shapes/text onto pygame display for user
    """
    def __init__(self, game_surface):
        """Initializes Drawer object
        
        Args:
            pygame.Surface: Main game surface that the player sees
        """
        # Set colours
        self.RED = pygame.Color(255, 0, 0) # Colour of the option "False"
        self.GREEN = pygame.Color(0, 255, 0) # Colour of the option "True"
        self.BLUE = pygame.Color(0, 0, 255) # Colour of the python
        self.BLACK = pygame.Color(0, 0, 0) # Colour of texts
        self.WHITE = pygame.Color(211, 211, 211) # Background colour
        self.gs = game_surface
  
    def border(self):
        """Draws the fix bottom border that separates the game area and text area that displays the questions
        """
        pygame.draw.rect(self.gs, self.BLACK, (0, 510, 500, 10))
        
    def reset_surface(self):
        """Resets the main game surface by painting over all content on the surface with white
        """
        self.gs.fill(self.WHITE)
        
    def draw(self, text, x, y, print_score = False, small_text = False):
        """Draws either the score, question, or instructions based on the arguments
        
        Args:
            str: text to be displayed
            int: horizontal axis coordinates
            int: vertical axis coordinates
            boolean: True to print score, False to print text
            boolean: Print smaller text
        """
        text_font = "impact" if print_score else "arial"
        text_font_size = 24 if print_score else 20
        if small_text: 
            text_font_size = round(text_font_size * 0.7)
        if print_score:
            text_colour = self.RED
        else:
            text_colour = self.BLACK
            
        # Initialize to-be-displayed text's font and font size
        display_text_font = pygame.font.SysFont(text_font, text_font_size)
        
        # Create pygame.Surface object for text to appear on while assigning text colour
        display_surface = display_text_font.render(text, True, text_colour)
        
        # Create pygame.Rect object from Surface
        display_rectangle = display_surface.get_rect()
        
        if print_score:
            display_rectangle.midtop = (x, y)
        else:
            display_rectangle.midbottom = (x, y)
        
        # Update new surface and rectangle onto main game surface
        self.gs.blit(display_surface, display_rectangle)
    
    def end_remarks(self, text):
        """Draws the ending remarks for the user after Python has did
        
        Args:
            str: Remarks
        """
        text_font = "impact"
        text_font_size = 22
        text_colour = self.RED
        
        display_text_font = pygame.font.SysFont(text_font, text_font_size)
        display_surface = display_text_font.render(text, True, text_colour)
        display_rectangle = display_surface.get_rect()
        display_rectangle.midtop = (250, 100)
        
        self.gs.blit(display_surface, display_rectangle)
        
    def snake(self, python):
        """Draws the python onto the game surface
        
        Args:
            list: Python's body
        """
        for python_block in python:
            pygame.draw.rect(self.gs, self.BLUE, pygame.Rect(python_block[0],python_block[1],10,10))
        
    def text(self, text, small_text = False):
        """Draws text onto the game surface
        
        Args:
            str: text
            boolean: make text smaller
        """
        self.draw(text, 250, 600, False, small_text)
    
    def score(self, score):
        """Draws users score onto the game surface
        
        Args:
            int: score
        """
        self.draw("Score: {0}".format(score), 390, 50, True)
        
    def answers(self, false_pos, true_pos):
        """Draws game's answer options onto game surface
        
        Args:
            list: false option's position
            list: true option's position
        """
        pygame.draw.rect(self.gs, self.RED, pygame.Rect(false_pos[0],false_pos[1],10,10))
        pygame.draw.rect(self.gs, self.GREEN, pygame.Rect(true_pos[0],true_pos[1],10,10))