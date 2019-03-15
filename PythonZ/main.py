from pz_modules import *

# Initialize pygame
pygame_init = pygame.init()
pygame.display.set_caption("QF205 PythonZ Game")
game_surface = pygame.display.set_mode((500, 700))

# Initialize Drawer
drawer = Drawer(game_surface)

# Initialize Loops
loops = Loops(drawer)

while True: 
    
    try:
        # Get game's frame's per second through user's input
        fps = loops.menu_loop()
        final_score, max_score = loops.game_loop(fps)
        loops.dead_loop(final_score, max_score)
        
    # Catch user initiated SystemExit exception
    except SystemExit:
        print("User Initiated Exit... \nClosed Pythonz")
        break
    except ValueError as ve:
        print(ve)
        break
    except:
        print("Unexpected error:", sys.exc_info()[0])
        break
        