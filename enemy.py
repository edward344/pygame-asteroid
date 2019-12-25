import pygame, math
import game_functions

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Meteor(pygame.sprite.Sprite):
    def __init__(self,pos,image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.change_x, self.change_y = self.get_direction()
        
        
    def get_direction(self):
        angle = game_functions.get_degrees(self.rect.center)
        change_x = int(math.cos(math.radians(angle)) * 5) * -1
        change_y = int(math.sin(math.radians(angle)) * 5)
        
        return change_x,change_y
        
    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y