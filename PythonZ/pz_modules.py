import pandas as pd, time, contextlib, sys, random, os
# Disable pygame inherent welcome message from importing
with contextlib.redirect_stdout(None):
    import pygame
    
DIFFICULTY = {
    "easy" : 10,
    "medium" : 20,
    "hard" : 35,
    "extreme" : 50
}

INPUT_DIFFICULTY = {
    "right" : "medium",
    "down" : "easy",
    "left" : "hard",
    "up" : "extreme"
}

USER_INPUT = {
    pygame.K_RIGHT : "right",
    pygame.K_LEFT : "left",
    pygame.K_UP : "up",
    pygame.K_DOWN : "down",
    pygame.K_ESCAPE : "esc"
}

class Loops:
    
    def __init__(self, drawer):
        self.drawer = drawer
        self.fps_controller = pygame.time.Clock()


    def user_input_checker(self):
        # Take the first direction in event
        direction = None
        
        for event in pygame.event.get():
            user_input = self.event_checker(event)
            # Allows cycle through rest of events in case for "esc" command
            if direction is None and user_input is not None:
                direction = user_input
                
        return direction
    
    def event_checker(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Get user input
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return None
            elif event.key in USER_INPUT:
                return USER_INPUT[event.key]
        else:
            return None

                
    def menu_loop(self):
        """ returns difficulty  
        """
        
        # Clear pygame event queue
        pygame.event.clear()
        
        while True:
            # draw menu
            self.drawer.reset_surface()
            self.drawer.text("R key: Medium, D key: Easy, L key: Hard, U key: Extreme")
            pygame.display.flip()
        
            # Wait and listen for an event
            result = self.event_checker(pygame.event.poll())
            
            if result is not None:
                return DIFFICULTY[INPUT_DIFFICULTY[result]]
            
    # returns final score
    def game_loop(self, fps):
        
        # Clear pygame event queue
        pygame.event.clear()
        
        # Reset Question Bank
        qb = QuestionBank()
        
        # Reset Python
        self.python = Python()
        
        # Reset score
        score = 0
        
        # Initialize answer positions
        false_pos, true_pos = qb.get_answer_and_question_position()
        
        # alive boolean
        alive = True

        while alive: 
            
            # Get question and answer values
            answer, question = qb.get_answer_and_question_values(score)
            
            # Iterate through pygame events
            movement = self.user_input_checker()
            if movement is not None:
                self.python.update_direction(movement)
            
            # Update python
            new_head_pos = self.python.move()
            if new_head_pos is None:
                alive = False
                
            # Check if new head position has reached either of the answers
            if new_head_pos in [false_pos, true_pos]:
                # Check if answer is correct
                if (answer == 1 and new_head_pos == true_pos) or (answer == 0 and new_head_pos == false_pos):
                    score += 1
                    if score == qb.max_score:
                        alive = False
                    else:
                        qb.next_question = True
                # If wrong answer
                else:
                    alive = False
            # If not, remove last block position from python
            elif alive:
                self.python.pop()
              
            # Generate new answer position if user answered correctly
            if qb.next_question:
                false_pos, true_pos = qb.generate_new_answer_position(self.python)
                qb.next_question = False
            
            # Reset game board
            self.drawer.reset_surface()
            
            # Draw python
            self.drawer.snake(self.python)
            
            # Draw answers
            self.drawer.answers(false_pos, true_pos)
            
            # Draw border
            self.drawer.border()
            
            # Draw score
            self.drawer.score(score)
            
            # Draw question
            self.drawer.text(question)
            
            # Update new drawings on player's interface
            pygame.display.flip()
        
            # Set game fps
            self.fps_controller.tick(fps)
        
        return score
        
    # end
    def dead_loop(score):
        print(score)
            
        
class QuestionBank:
               
    def __init__(self):
        # Call parent constructor
        try:
            path = os.getcwd() + "\\assets\\gamedata.xlsx"

            # Ensure that filename argument is a string and not empty
            if not isinstance(path, str) or not path:
                raise ValueError("No str argument found")

            # Read and load excel file from path
            self.dataframe = pd.read_excel(path)
            
            # Raise exception if file is empty or contains missing values
            if self.dataframe.empty or self.dataframe.isnull().values.any():
                raise ValueError("Invalid {0} excel file found!".format(path))
            
            # Shuffle order of questions
            self.dataframe = self.dataframe.sample(frac=1).reset_index(drop=True)
            
            # Initialize first question's option
            self.false_pos = [350,350]
            self.true_pos = [350,150]
            
            # Initialize question logic
            self.next_question = False
            
            # Get maximum score
            self.max_score = len(self.dataframe.index)
            
            # Get first answer and question
            self.answer, self.question = self.get_answer_and_question_values()
            
            
        except FileNotFoundError:
            raise FileNotFoundError("{0} file not found!".format(path))
    
    def get_answer_and_question_values(self, score=0):
        
        # Ensure that score argument is within the bounds
        if abs(score) >= self.max_score:
            raise IndexError("Index out of bounds! Max Index:{0}".format(self.max_score))
        else:
            return self.dataframe.iloc[score]
        
    def get_answer_and_question_position(self):
        return self.false_pos, self.true_pos
    
    def check_answer(self, head_pos):
        # User answered correctly
        if (self.answer == 1 and head_pos == self.true_pos) or (self.answer == 0 and head_pos == self.false_pos):
            self.next_question = True
            return True
        else:
            return False
        
    def generate_new_answer_position(self, python):
        self.false_pos = [random.randrange(1,50)*10,random.randrange(1,50)*10]
        while self.false_pos in python:
            self.false_pos = [random.randrange(1,50)*10,random.randrange(1,50)*10]
        self.true_pos = [random.randrange(1,50)*10,random.randrange(1,50)*10]
        while self.true_pos == self.false_pos or self.true_pos in python:
            self.true_pos = [random.randrange(1,50)*10,random.randrange(1,50)*10]
        return self.false_pos, self.true_pos


class Drawer:    
    
    def __init__(self, game_surface):
        # Set colours
        self.RED = pygame.Color(255, 0, 0) # Colour of the option "False"
        self.GREEN = pygame.Color(0, 255, 0) # Colour of the option "True"
        self.BLUE = pygame.Color(0, 0, 255) # Colour of the python
        self.BLACK = pygame.Color(0, 0, 0) # Colour of texts
        self.WHITE = pygame.Color(255, 255, 255) # Background colour
        self.gs = game_surface
  
    def border(self):
        pygame.draw.rect(self.gs, self.BLACK, (0, 510, 500, 10))
        
    def reset_surface(self):
        self.gs.fill(self.WHITE)
        
    def draw(self, text, x, y, print_score = False, small_text = False):
        
        text_font = "impact" if print_score else "arial"
        text_font_size = 24 if print_score else 20
        if small_text: 
            text_font_size = round(text_font_size * 0.7)
        if print_score:
            text_colour = self.RED
        else:
            text_colour = self.BLACK
            
        display_text_font = pygame.font.SysFont(text_font, text_font_size)
        display_surface = display_text_font.render(text, True, text_colour)
        display_rectangle = display_surface.get_rect()
        
        if print_score:
            display_rectangle.midtop = (x, y)
        else:
            display_rectangle.midbottom = (x, y)
        
        self.gs.blit(display_surface, display_rectangle)
        
        
    def snake(self, python):
        for python_block in python:
            pygame.draw.rect(self.gs, self.BLUE, pygame.Rect(python_block[0],python_block[1],10,10))
        
    def text(self, text):
        self.draw(text, 250, 600, False, True)
    
    def score(self, score):
        self.draw("Score: {0}".format(score), 390, 50, True)
        
    def answers(self, false_pos, true_pos):
        pygame.draw.rect(self.gs, self.RED, pygame.Rect(false_pos[0],false_pos[1],10,10))
        pygame.draw.rect(self.gs, self.GREEN, pygame.Rect(true_pos[0],true_pos[1],10,10))

class Python(list):
    
    def __init__(self,  length = 5):
        
        # Directions
        self.RIGHT = [10, 0]
        self.LEFT = [-10, 0]
        self.UP = [0, -10]
        self.DOWN = [0, 10]
        
        # User Input Mappings
        self.movement_to_direction = {
            "right" : self.RIGHT,
            "down" : self.DOWN,
            "left" : self.LEFT,
            "up" : self.UP
        }
        
        # Initialize directions
        self.current_direction = self.RIGHT

        # Initialize list
        super().__init__()
        for i in range(100, 10 * (10-length), -10):
            self.append([i,250])

    def update_direction(self, movement):
        change_to = self.movement_to_direction[movement]
        # Validate python is moving in accordance to the game's logic
        if change_to == self.RIGHT and self.current_direction != self.LEFT:
            self.current_direction = self.RIGHT
        elif change_to == self.LEFT and self.current_direction != self.RIGHT:
            self.current_direction = self.LEFT
        elif change_to == self.UP and self.current_direction != self.DOWN:
            self.current_direction = self.UP
        elif change_to == self.DOWN and self.current_direction != self.UP:
            self.current_direction = self.DOWN
    
    def get_head(self):
        return (self[0])
    
    def move(self):
        new_head_pos = [a + b for a, b in zip(self[0], self.current_direction)]
        # Check if python "ate itself" or is out of bounds
        self.insert(0, new_head_pos)
        if new_head_pos in self[1:]:
            return None
        elif new_head_pos[0] >= 500 or new_head_pos[0] <= 0:
            return None
        elif new_head_pos[1] >= 500 or new_head_pos[1] <= 0:
            return None

        return new_head_pos

    def update_body(self, new_head_pos):
        self.insert(0, new_head_pos)

if __name__ == '__main__':
    print("pz_modules loaded! Please run game.py to start the game...")