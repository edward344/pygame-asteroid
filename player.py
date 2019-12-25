import pygame, math
import game_functions

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0,0,0)

class Player(pygame.sprite.Sprite):
    def __init__(self,filename,width,height):
        # call the parent class constructor
        super().__init__()
        # load images from sprite sheet
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.image_list = self.load_images(width,height)
        # set the image 
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        # put the player in the middle of the screen
        self.rect.topleft = (SCREEN_WIDTH//2 - 50,SCREEN_HEIGHT//2 - 50)
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        angle = game_functions.get_degrees(mouse_pos)
        index = int(len(self.image_list) / 360 * angle)
        self.image = self.image_list[index]
        
        
    def load_images(self,width,height):
        """ This method will return a list with the images """
        # Create a list that will contain the images
        image_list = []
        # Go through every single image in the sprite sheet
        for y in range(0,self.sprite_sheet.get_height(),height):
            for x in range(0,self.sprite_sheet.get_width(),width): 
                # load images into a list
                img = self.get_image(x,y,width,height)
                image_list.append(img)
        return image_list
        
    def get_image(self,x,y,width,height):
        """ This method will cut an image and return it """
        # Create a new blank image
        image = pygame.Surface([width,height]).convert()
        # Copy the sprite from the large sheet onto the smaller
        image.blit(self.sprite_sheet,(0,0),(x,y,width,height))
        # Assuming black works as the transparent color
        image.set_colorkey(BLACK)
        # Return the image
        return image
        
        