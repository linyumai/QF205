# Import statements
import pandas as pd, time, contextlib, sys, random, os
# Disable pygame in-built welcome message after importing
with contextlib.redirect_stdout(None):
    import pygame

DIFFICULTY = {
    "easy" : 10,
    "medium" : 20,
    "hard" : 35,
    "extreme" : 50
}
"""The difficulty of the game is directly related to the number of frame refreshes per second, which affects the speed of the Python character
"""

INPUT_DIFFICULTY = {
    "right" : "medium",
    "down" : "easy",
    "left" : "hard",
    "up" : "extreme"
}
"""Input control for user to select their desired difficulty
"""

USER_INPUT = {
    pygame.K_RIGHT : "right",
    pygame.K_LEFT : "left",
    pygame.K_UP : "up",
    pygame.K_DOWN : "down",
}
"""Mapping to translate user input events (keyboard presses) into directions
"""

# Classes
class Loops:
    """Parent object to call specific game loop logics
    """
    
    def __init__(self, drawer):
        """Initializes Loops object
        
        Args:
            Drawer: Drawer object that is responsible for displaying graphics to users
        """
        # Drawer: Drawer object that is responsible for updating graphics on user's interface
        self.drawer = drawer
        
        # pygame.time.Clock: a Clock object that controls the game's framerate and can track in-game time
        self.fps_controller = pygame.time.Clock()


    def user_input_checker(self):
        """ Get's the user's input through processing all pygame.events recorded
        
        Returns:
            str: Returns user's input based on USER_INPUT's values. 
            None: Returns when no valid user input is found
        """
        # Initialize direction variable with default value
        direction = None
        
        # Iterate through all posted pygame.events
        for event in pygame.event.get():
            
            # Get value of user input based on USER_INPUT dictionary
            user_input = self.event_checker(event)
            
            # Get the latest user inpur
            if user_input is not None:
                direction = user_input
        
        # By not returning in the for loop, it allows code to continue even after finding a user input direction in the event of an "esc" command
        return direction
    
    def event_checker(self, event):
        """ Translates the user's pygame.event into a direction
        
        Args:
            pygame.event: Python object that represents an event such as a key press
        
        Returns:
            str: Returns user's input based on USER_INPUT's values. 
            None: Returns when the event is not an arrow key press
        """ 
        # Quit pygame if pygame.QUIT event is queued
        if event.type == pygame.QUIT:
            pygame.quit()
            # Raises SystemExit Exception
            sys.exit()
            
        # Returns user input
        elif event.type == pygame.KEYDOWN:
            
            # Post pygame.QUIT event if user presses the "esc" key
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                
            # Returns str direction if user presses any arrow keys
            elif event.key in USER_INPUT:
                return USER_INPUT[event.key]
        # Return None if event is not an arrow key press
        return None

                
    def menu_loop(self):
        """ Loops continuously until a user presses an arrow key to select difficulty or "esc" to quit game
        
        Returns:
            int: Frames Per Second (FPS) that is used to control game's framerate (speed of Python)
        """
        # Clear pygame event queue
        pygame.event.clear()
        
        # Resets user interface
        self.drawer.reset_surface()
        
        # Posts instructional text to pygame
        self.drawer.text("R key: Medium, D key: Easy, L key: Hard, U key: Extreme", True)
        
        # Update any changes in pygame to user's display 
        pygame.display.flip()
        
        # Continuous loop until return statement or pygame.QUIT command
        while True:

            # Wait and listen for an event
            result = self.event_checker(pygame.event.poll())
            
            # If user has pressed on any of the arrow keys, return FPS
            if result is not None:
                return DIFFICULTY[INPUT_DIFFICULTY[result]]
            
    def dead_loop(self, score, max_score):
        """ Loops continuously until a user presses any arrow key to return to menu or "esc" to quit game
        
        Args:
            int: Final score of player
            int: Maximum score of game (number of questions in question bank)
        """        
        # Clear pygame event queue
        pygame.event.clear()
        
        # Resets user interface
        self.drawer.reset_surface()
        
        # Posts instructional text to pygame
        self.drawer.text("Press any arrow key to play again. Press ESC to quit.", True)
        
        # Posts user display score to pygame
        self.drawer.score(score)
        
        # Set game remarks to users based on user's performance
        if score == max_score:
            result_remarks = "Max Score! Double Confirm QF205 get A+"
        else:
            result_remarks = "Game over! The max score is: {0}".format(max_score)
        # Posts game remarks to users to pygame
        self.drawer.end_remarks(result_remarks)
        
        # Update any changes in pygame to user's display 
        pygame.display.flip()
        
        # Pause momentarily to give user time to react
        time.sleep(1)
        
        # Continuous loop until return statement or pygame.QUIT command
        while True:
            
            # Wait and listen for an event
            result = self.event_checker(pygame.event.poll())
            
            # If user has pressed on any of the arrow keys, break out of loop where the parent loop returns to menu_loop()
            if result is not None:
                break
            
    def game_loop(self, fps):
        """Main game loop 
        
        Args:
            int: Frames Per Second
            
        Returns: 
            int: Player's final score
            int: Game's maximum attainable score
        """
        
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
        
        # Continuous loop until player's python dies
        while alive: 
            
            # Get question and answer values
            answer, question = qb.get_answer_and_question_values(score)
            
            # Iterate through pygame events
            movement = self.user_input_checker()
            
            # If player has pressed any of the directional arrow keys, check and update Python's movement direction
            if movement is not None:
                self.python.update_direction(movement)

            # Update python based on it's movement direction attribute
            new_head_pos = self.python.move()

            # New python head position is None if it is beyond game boundaries or in its body
            if new_head_pos is None:
                alive = False

            # Check if new head position has reached either of the answers
            if new_head_pos in [false_pos, true_pos]:

                # Check if answer is correct
                if (answer == 1 and new_head_pos == true_pos) or (answer == 0 and new_head_pos == false_pos):
                    # If correct, add to score
                    score += 1

                    # If player has reached max score, kill the python to end the game
                    if score == qb.max_score:
                        alive = False

                    # Prepares to reset next question and answer for next iteration of the loop
                    else:
                        qb.next_question = True

                # If wrong answer, kill the Python
                else:
                    alive = False
                    
            # If python head not in any of the answers, remove last block position from python
            elif alive:
                self.python.pop()
              
            # Generate new answer position if user answered correctly
            if qb.next_question:
                # Get new random positions
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
        
            # Set game fps. Number of times the loop runs per second
            self.fps_controller.tick(fps)
        
        return score, qb.max_score
        

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
        self.WHITE = pygame.Color(211, 211, 211) # Background colour
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
    
    def end_remarks(self, text):
        
        text_font = "impact"
        text_font_size = 22
        text_colour = self.RED
        
        display_text_font = pygame.font.SysFont(text_font, text_font_size)
        display_surface = display_text_font.render(text, True, text_colour)
        display_rectangle = display_surface.get_rect()
        display_rectangle.midtop = (250, 100)
        
        self.gs.blit(display_surface, display_rectangle)
        
    def snake(self, python):
        for python_block in python:
            pygame.draw.rect(self.gs, self.BLUE, pygame.Rect(python_block[0],python_block[1],10,10))
        
    def text(self, text, small_text = False):
        self.draw(text, 250, 600, False, small_text)
    
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