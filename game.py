import pygame,random
from menu import Menu
from player import Player
from bullet import Bullet
from enemy import Meteor
import game_functions
from explosion import Explosion

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MAX_SCORE = 100

WHITE = (255,255,255)
BLACK = (0,0,0)

class Game:
    def __init__(self):
        self.background_image = pygame.image.load("background-image.png").convert()
        # create menu object
        self.menu = Menu(("start","credits","exit"))
        # create font
        self.font = pygame.font.Font("kenvector_future.ttf",35)
        self.show_menu = True # true: when we need to display the menu
        self.show_credits = False # true: when we need to display credits
        # create player
        self.player = Player("space.png",100,100)
        # create group of bullets
        self.bullet_group = pygame.sprite.Group()
        # create group for meteors
        self.meteor_group = pygame.sprite.Group()
        # load meteors images
        sprite_sheet = pygame.image.load("meteor.png").convert()
        self.meteor_list = game_functions.load_images(sprite_sheet,100,100)
        # set timer for wait two second (60 frames)
        self.timer = 60
        # load the sound effects...
        self.explosion_sound = pygame.mixer.Sound("explosion.ogg")
        self.laser_sound = pygame.mixer.Sound("laser.ogg")
        # set the score
        self.score = 0
        self.game_over = False # true: when the player loose
        self.show_player = True # false: when the player lost
        # create explosion animation
        self.explosion = Explosion("explosion.png",256,256)
        
        
    def process_events(self):
        for event in pygame.event.get(): # user did something
            if event.type == pygame.QUIT: # user clicked close
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_menu:
                    if self.menu.state == 0:
                        self.show_menu = False
                    elif self.menu.state == 1:
                        self.show_credits = True
                    elif self.menu.state == 2:
                        # user clicked exit
                        return True
                elif not self.game_over:
                    # fire bullets
                    mouse_pos = pygame.mouse.get_pos()
                    self.bullet_group.add(Bullet(game_functions.get_degrees(mouse_pos)))
                    # play laser sound
                    self.laser_sound.play()
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # reset the game 
                    self.show_menu = True
                    self.show_credits = False
                    self.score = 0
                    self.show_player = True
                    self.game_over = False
                    self.meteor_group.empty()
                    self.bullet_group.empty()
               
        return False
        
    def run_logic(self):
        if self.show_menu:
            self.menu.update()
        elif not self.game_over or not self.explosion.is_empty():
            self.player.update()
            self.bullet_group.update()
            # remove bullets that are outside the screen
            for bullet in self.bullet_group:
                if bullet.rect.x > SCREEN_WIDTH or bullet.rect.x < 0:
                    self.bullet_group.remove(bullet)
                elif bullet.rect.y > SCREEN_HEIGHT or bullet.rect.y < 0:
                    self.bullet_group.remove(bullet)
            # update meteor_group
            self.meteor_group.update()
            self.explosion.update()
            # substract 1 from timer
            if self.timer == 0:
                # add a new meteor to the group
                random_index = random.randint(0,3) # choose randomly between images
                self.meteor_group.add(Meteor(self.get_random_pos(),self.meteor_list[random_index]))
                self.timer = 60
            else:
                self.timer -= 1
            # check if the bullets collide with some meteor
            for bullet in self.bullet_group:
                meteor_hit_list = pygame.sprite.spritecollide(bullet,self.meteor_group,True)
                if len(meteor_hit_list) > 0:
                    for meteor in meteor_hit_list:
                        # create explosion animation
                        self.explosion.add_animation(meteor.rect.center)
                    # remove bullet from group
                    self.bullet_group.remove(bullet)
                    # play explosion sound
                    self.explosion_sound.play()
                    # increase score
                    self.score += 1
                    
            # check if the player collide with some meteor
            if not self.game_over:
                meteor_hit_list = pygame.sprite.spritecollide(self.player,self.meteor_group,True)
                if len(meteor_hit_list) > 0:
                    # add explosion animation
                    self.explosion.add_animation(self.player.rect.center)
                    # play explosion sound
                    self.explosion_sound.play()
                    self.game_over = True
                    self.show_player = False
                    
            # check if the score is equal to MAX_SCORE
            if self.score >= MAX_SCORE:
                self.game_over = True
                    
        
    def display_frame(self,screen):
        # first, clear the screen to the background image
        screen.blit(self.background_image,(0,0))
        # --- drawing code should go here
        if self.show_menu:
            # display the credits
            if self.show_credits:
                self.display_message(screen,"by edu grando")
            else:
                # display the menu
                self.display_title(screen,"asteroids")
                self.menu.display_frame(screen)
        elif self.score >= MAX_SCORE and self.explosion.is_empty():
            self.display_message(screen,"you won...")
        elif self.game_over and self.explosion.is_empty():
            self.display_message(screen,"you lost...")
        else:
            # display game
            self.bullet_group.draw(screen)
            self.meteor_group.draw(screen)
            if self.show_player:
                # when the player looses the player image is no longer showed.
                screen.blit(self.player.image,self.player.rect)
            self.display_score(screen,self.score)
            self.explosion.draw(screen)
        # --- go ahead and update the screen 
        pygame.display.flip()
        
    def display_score(self,screen,score):
        label = self.font.render("score: " + str(score),True,WHITE)
        # draw the label on the screen
        screen.blit(label,(20,20))
        
    def display_message(self,screen,message):
        label = self.font.render(message,True,WHITE)
        # get the width and height of the label
        width = label.get_width()
        height = label.get_height()
        # determine the position of the label
        posX = (SCREEN_WIDTH//2) - (width//2)
        posY = (SCREEN_HEIGHT//2) - (height//2)
        # draw the label on the screen
        screen.blit(label,(posX,posY))
        
    def display_title(self,screen,title):
        label = self.font.render(title,True,WHITE)
        # get the width of the label
        width = label.get_width()
        # determine the position of the label
        posX = (SCREEN_WIDTH//2) - (width//2)
        # draw the label on the screen
        screen.blit(label,(posX,100))
        
    def get_random_pos(self):
        options = ("top","bottom","left","right")
        random_choice = random.choice(options)
        if random_choice == "top":
            posX = random.randint(0,SCREEN_WIDTH)
            posY = 0
        elif random_choice == "bottom":
            posX = random.randint(0,SCREEN_WIDTH)
            posY = SCREEN_HEIGHT
        elif random_choice == "left":
            posX = 0
            posY = random.randint(0,SCREEN_HEIGHT)
        elif random_choice == "right":
            posX = SCREEN_WIDTH
            posY = random.randint(0,SCREEN_HEIGHT)
            
        return posX,posY
        