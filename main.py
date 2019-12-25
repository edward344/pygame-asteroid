import pygame
from game import Game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    done = False
    clock = pygame.time.Clock()
    # create game object
    game = Game()
    # ---------- Main Program Loop ------ 
    while not done:
        # --- Process events
        done = game.process_events()
        # --- Game logic should go here
        game.run_logic()
        # --- Draw the current frame
        game.display_frame(screen)
        # --- Limit to 30 frames per second
        clock.tick(30)
        
    pygame.quit()

if __name__ == '__main__':
    main()