import pygame, math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0,0,0)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,angle):
        # call the parent constructor
        super().__init__()
        # load image
        self.image = pygame.image.load("bullet.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # declare the position of the bullet to the middle of the screen
        self.rect.topleft = (SCREEN_WIDTH//2 - 9,SCREEN_HEIGHT//2 - 9)
        # declare change_x and change_y
        self.change_x, self.change_y = self.get_direction(angle)
        
    def get_direction(self,angle):
        change_x = int(math.cos(math.radians(angle)) * 10)
        change_y = int(math.sin(math.radians(angle)) * 10) * -1
        
        return change_x,change_y
        
    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        