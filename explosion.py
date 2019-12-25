import pygame
import game_functions

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

WHITE = (255,255,255)
BLACK = (0,0,0)

class Explosion:
    def __init__(self,filename,width,height):
        sprite_sheet = pygame.image.load(filename).convert()
        self.image_list = game_functions.load_images(sprite_sheet,width,height)
        self.animation_list = []
        self.width = width
        self.height = height
        
    def add_animation(self,pos):
        x = pos[0]
        y = pos[1]
        self.animation_list.append(Animation(self.image_list,x,y,self.width,self.height))
        
    def update(self):
        for index,animation in enumerate(self.animation_list):
            animation.update()
            if animation.finished:
                # delete the animation when it's finished
                del self.animation_list[index]
            
    def draw(self,screen):
        for animation in self.animation_list:
            animation.draw(screen)
            
    def is_empty(self):
        if len(self.animation_list) > 0:
            return False
        else:
            return True

class Animation:
    def __init__(self,image_list,x,y,width,height):
        self.image_list = image_list
        self.x = x - width // 2
        self.y = y - height // 2
        self.index = 0
        self.finished = False
        
    def update(self):
        if self.index == len(self.image_list) - 1:
            self.index = 0
            self.finished = True
        else:
            self.index += 1
            
            
    def draw(self,screen):
        # draw the image
        screen.blit(self.image_list[self.index],(self.x,self.y))