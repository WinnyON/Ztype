from locale import currency
from operator import indexOf
import pygame
import button
import inputbox
import json
import math
import random


#IMPORT WORDS
SHORT =  {}
MEDIUM = {}
LONG  = {}

with open("long.json", "r") as json_file:
    LONG = json.load(json_file)

with open("short.json", "r") as json_file:
    SHORT = json.load(json_file)

with open("medium.json", "r") as json_file:
    MEDIUM = json.load(json_file)

#PYGAME & WINDOW INITIALIZATION
pygame.init()
win = pygame.display.set_mode((420, 720))
pygame.display.set_caption("Ztype")
clock = pygame.time.Clock()

#COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
ORANGE = (255,156,4)
LIGHT_GREY = (148, 148, 148)
DARK_GREY = (23, 23, 23)
CIAN = (28,212,204)


#BULLET


class laser():
    def __init__(self, targx, targy, x, y, color):
        self.targx = targx
        self.targy = targy
        self.x = x
        self.y = y
        self.color = color
        self.counter = 0
    
    def draw(self, screen):
        pygame.draw.line(screen, self.color, (self.x, self.y), (self.targx, self.targy), 5)

#SHIP


class Type2():
    def __init__(self, x, y, angle, word):
        self.x = x
        self.y = y
        self.vel = 0.7
        self.angle = angle
        self.word = word
        self.lenght = len(word)
        self.color = WHITE
        self.img_cnt = 0
        self.arrow_counter = 0
        #self.img_counter = 0
        self.active = False
        self.over = False
        angle_in_radians = math.radians(self.angle)
        sin_of_angle = math.sin(angle_in_radians)
        cos_of_angle = math.cos(angle_in_radians)
        self.vel_x = cos_of_angle*self.vel
        self.vel_y = sin_of_angle*self.vel
        self.img_list = pygame.image.load("arrow.png").convert_alpha()

        self.expl_imgs = [pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (16,16)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (24,24)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (32,32)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (64,64))]        
        

    def draw(self, screen):
        

        ship_font = pygame.font.SysFont("consolas", 20)
        self.word_surf = ship_font.render(self.word,True, self.color)
        self.word_rect = self.word_surf.get_rect()
        self.word_rect.bottomright = (self.x+8, self.y+8)

       # self.img_counter += 1 I don't know why but I has a bug
        #if self.img_counter == 4:
           # self.img_counter = 0
        
        self.img_rect = self.img_list.get_rect()
        self.img_rect.topleft = (self.x, self.y)

        self.text_width = self.word_surf.get_width()
        self.text_height = self.word_surf.get_height()
        self.backg = pygame.Rect(self.x - self.text_width//1.05, self.y - self.text_height//1.5, self.text_width + 8, self.text_height)

        pygame.draw.rect(screen, DARK_GREY, self.backg)
        screen.blit(self.word_surf, (self.word_rect.x, self.word_rect.y))
        screen.blit(self.img_list, (self.img_rect.x, self.img_rect.y))
        
    
    def update(self):

        #
        #angle_in_radians = self.angle
        
        self.arrow_counter += 1
        #print(self.x, self.y)
        self.x += self.vel_x
        self.y += self.vel_y
       # print(self.x, self.y)

        if self.vel < 0.5:
            self.vel += 0.7

        if self.active:
            self.color = ORANGE
        else:
            self.color = WHITE
        
        return self.over
    #you have to change event to letter, and put the event handling inside the event loop, because if there are more words, then you have to do it differently
    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.active = False
            elif event.unicode == self.word[0]:
                if len(self.word) == 1:
                    self.active = True
                    self.word = ""
                    self.over = True #set this over if collides with Spaceship
                else:
                    self.word = self.word[1:]
                    self.active = True
                    # self.x -= 2
                    # self.y -= 2
                    self.vel = -2*self.vel
                return True #this too
            else:
                return False #for the purpose of vibration in case of wrong letter
    
    def explode(self, screen):

        
        if self.img_cnt == 4:
            return False
        else:
            ex_rect = self.expl_imgs[self.img_cnt].get_rect()
            ex_rect.topleft = (self.x + (2 - self.img_cnt)*8, self.y + (2 - self.img_cnt)*8)
            screen.blit(self.expl_imgs[self.img_cnt], (ex_rect.x, ex_rect.y))
            pygame.time.wait(50)
            self.img_cnt += 1
            return True

class Type4():
    def __init__(self, x, y, angle, word):
        self.x = x
        self.y = y
        self.vel = 0.25
        self.angle = angle
        self.word = word
        self.lenght = len(word)
        self.color = WHITE
        self.img_cnt = 0
        #self.img_counter = 0
        self.active = False
        self.over = False
        angle_in_radians = math.radians(self.angle)
        sin_of_angle = math.sin(angle_in_radians)
        cos_of_angle = math.cos(angle_in_radians)
        self.vel_x = cos_of_angle*self.vel
        self.vel_y = sin_of_angle*self.vel
        self.img_list = pygame.image.load("type4.png").convert_alpha()

        self.expl_imgs = [pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (16,16)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (24,24)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (32,32)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (64,64))]        
        

    def draw(self, screen):
        

        ship_font = pygame.font.SysFont("consolas", 20)
        self.word_surf = ship_font.render(self.word,True, self.color)
        self.word_rect = self.word_surf.get_rect()
        self.word_rect.bottomright = (self.x+8, self.y+8)

       # self.img_counter += 1 I don't know why but I has a bug
        #if self.img_counter == 4:
           # self.img_counter = 0
        
        self.img_rect = self.img_list.get_rect()
        self.img_rect.topleft = (self.x, self.y)

        self.text_width = self.word_surf.get_width()
        self.text_height = self.word_surf.get_height()
        self.backg = pygame.Rect(self.x - self.text_width//1.05, self.y - self.text_height//1.5, self.text_width + 8, self.text_height)

        pygame.draw.rect(screen, DARK_GREY, self.backg)
        screen.blit(self.word_surf, (self.word_rect.x, self.word_rect.y))
        screen.blit(self.img_list, (self.img_rect.x, self.img_rect.y))
        
    
    def update(self):

        #
        #angle_in_radians = self.angle
        

        #print(self.x, self.y)
        self.x += self.vel_x
        self.y += self.vel_y
       # print(self.x, self.y)

        if self.vel < 0.25:
            self.vel += 0.35

        if self.active:
            self.color = ORANGE
        else:
            self.color = WHITE
        
        return self.over
    #you have to change event to letter, and put the event handling inside the event loop, because if there are more words, then you have to do it differently
    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.active = False
            elif event.unicode == self.word[0]:
                if len(self.word) == 1:
                    self.active = True
                    self.word = ""
                    self.over = True 
                else:
                    self.word = self.word[1:]
                    self.active = True
                    # self.x -= 2
                    # self.y -= 2
                    self.vel = -2*self.vel
                return True 
            else:
                return False #for the purpose of vibration in case of wrong letter
    
    def explode(self, screen):

        
        if self.img_cnt == 4:
            return False
        else:
            ex_rect = self.expl_imgs[self.img_cnt].get_rect()
            ex_rect.topleft = (self.x + (2 - self.img_cnt)*8, self.y + (2 - self.img_cnt)*8)
            screen.blit(self.expl_imgs[self.img_cnt], (ex_rect.x, ex_rect.y))
            pygame.time.wait(50)
            self.img_cnt += 1
            return True


class Type3():
    def __init__(self, x, y, angle, word):
        self.x = x
        self.y = y
        self.vel = 0.35
        self.angle = angle
        self.word = word
        self.lenght = len(word)
        self.color = WHITE
        self.img_cnt = 0
        self.arrow_counter = 0
        #self.img_counter = 0
        self.active = False
        self.over = False
        angle_in_radians = math.radians(self.angle)
        sin_of_angle = math.sin(angle_in_radians)
        cos_of_angle = math.cos(angle_in_radians)
        self.vel_x = cos_of_angle*self.vel
        self.vel_y = sin_of_angle*self.vel
        self.img_list = pygame.image.load("type3.png").convert_alpha()

        self.expl_imgs = [pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (16,16)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (24,24)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (32,32)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (64,64))]        
        

    def draw(self, screen):
        

        ship_font = pygame.font.SysFont("consolas", 20)
        self.word_surf = ship_font.render(self.word,True, self.color)
        self.word_rect = self.word_surf.get_rect()
        self.word_rect.bottomright = (self.x+8, self.y+8)

        
        self.img_rect = self.img_list.get_rect()
        self.img_rect.topleft = (self.x, self.y)

        self.text_width = self.word_surf.get_width()
        self.text_height = self.word_surf.get_height()
        self.backg = pygame.Rect(self.x - self.text_width//1.05, self.y - self.text_height//1.5, self.text_width + 8, self.text_height)

        pygame.draw.rect(screen, DARK_GREY, self.backg)
        screen.blit(self.word_surf, (self.word_rect.x, self.word_rect.y))
        screen.blit(self.img_list, (self.img_rect.x, self.img_rect.y))
        
    
    def update(self):

        #

        
        self.arrow_counter += 1
        #print(self.x, self.y)
        self.x += self.vel_x
        self.y += self.vel_y
       # print(self.x, self.y)

        if self.vel < 0.35:
            self.vel += 0.35

        if self.active:
            self.color = ORANGE
        else:
            self.color = WHITE
        
        return self.over
    
    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.active = False
            elif event.unicode == self.word[0]:
                if len(self.word) == 1:
                    self.active = True
                    self.word = ""
                    self.over = True 
                else:
                    self.word = self.word[1:]
                    self.active = True
                    # self.x -= 2
                    # self.y -= 2
                    self.vel = -2*self.vel
                return True #
            else:
                return False 
    
    def explode(self, screen):

        
        if self.img_cnt == 4:
            return False
        else:
            ex_rect = self.expl_imgs[self.img_cnt].get_rect()
            ex_rect.topleft = (self.x + (2 - self.img_cnt)*8, self.y + (2 - self.img_cnt)*8)
            screen.blit(self.expl_imgs[self.img_cnt], (ex_rect.x, ex_rect.y))
            pygame.time.wait(50)
            self.img_cnt += 1
            return True
            

class Type1():
    def __init__(self, x, y, angle, word):
        self.x = x
        self.y = y
        self.vel = 0.5
        self.angle = angle
        self.word = word
        self.lenght = len(word)
        self.color = WHITE
        self.img_cnt = 0
        self.img_counter = 0
        self.active = False
        self.over = False
        angle_in_radians = math.radians(self.angle)
        sin_of_angle = math.sin(angle_in_radians)
        cos_of_angle = math.cos(angle_in_radians)
        self.vel_x = cos_of_angle*self.vel
        self.vel_y = sin_of_angle*self.vel
        self.img_list = [pygame.transform.rotate(pygame.image.load("circle2.2-32x32.png").convert_alpha(), 0),
                        pygame.transform.rotate(pygame.image.load("circle2.2-32x32.png").convert_alpha(), 45),
                        pygame.transform.rotate(pygame.image.load("circle2.2-32x32.png").convert_alpha(), 90),
                        pygame.transform.rotate(pygame.image.load("circle2.2-32x32.png").convert_alpha(), 135)]

        self.expl_imgs = [pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (16,16)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (24,24)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (32,32)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (64,64))]        
        

    def draw(self, screen):
        

        ship_font = pygame.font.SysFont("consolas", 20)
        self.word_surf = ship_font.render(self.word,True, self.color)
        self.word_rect = self.word_surf.get_rect()
        self.word_rect.bottomright = (self.x+8, self.y+8)

       # self.img_counter += 1 I don't know why but I has a bug
        if self.img_counter == 4:
            self.img_counter = 0
        
        self.img_rect = self.img_list[self.img_counter].get_rect()
        self.img_rect.topleft = (self.x, self.y)

        self.text_width = self.word_surf.get_width()
        self.text_height = self.word_surf.get_height()
        self.backg = pygame.Rect(self.x - self.text_width//1.05, self.y - self.text_height//1.5, self.text_width + 8, self.text_height)

        pygame.draw.rect(screen, DARK_GREY, self.backg)
        screen.blit(self.word_surf, (self.word_rect.x, self.word_rect.y))
        screen.blit(self.img_list[self.img_counter], (self.img_rect.x, self.img_rect.y))
        
    
    def update(self):

        #
        #angle_in_radians = self.angle
        

        #print(self.x, self.y)
        self.x += self.vel_x
        self.y += self.vel_y
       # print(self.x, self.y)

        if self.vel < 0.35:
            self.vel += 0.5

        if self.active:
            self.color = ORANGE
        else:
            self.color = WHITE
        
        return self.over
 
    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.active = False
            elif event.unicode == self.word[0]:
                if len(self.word) == 1:
                    self.active = True
                    self.word = ""
                    self.over = True #set this over if collides with Spaceship
                else:
                    self.word = self.word[1:]
                    self.active = True
                    # self.x -= 2
                    # self.y -= 2
                    self.vel = -100*self.vel
                    #print("-timess")
                return True #this too
            else:
                return False #for the purpose of vibration in case of wrong letter
    
    def explode(self, screen):

        
        if self.img_cnt == 4:
            return False
        else:
            ex_rect = self.expl_imgs[self.img_cnt].get_rect()
            ex_rect.topleft = (self.x + (2 - self.img_cnt)*8, self.y + (2 - self.img_cnt)*8)
            screen.blit(self.expl_imgs[self.img_cnt], (ex_rect.x, ex_rect.y))
            pygame.time.wait(50)
            self.img_cnt += 1
            return True
            


#ENEMY SHIPS





#FUNCTIONS
def draw_background():
    global BACKGROUND_Y
    global STARTED
    if BACKGROUND_Y >= 720:
        BACKGROUND_Y = 0
    if not STARTED:
        BACKGROUND_Y += 0.25
      #  print(BACKGROUND_Y)

        win.blit(bg, (0, BACKGROUND_Y))
        win.blit(bg, (0, BACKGROUND_Y - 720))
        
    else:
        BACKGROUND_Y += 0.25

        win.blit(bg, (0, BACKGROUND_Y))
        win.blit(bg, (0, BACKGROUND_Y - 720))

def draw_spaceship(angle, shoot_counter):
    global SpaceShip
    global spaceship_rect
    global EXPLODED
    new_surf = pygame.transform.rotate(SpaceShip[shoot_counter], -angle*1.15)
    spaceship_rect = new_surf.get_rect()
    spaceship_rect.center = (210, 600)
    if not EXPLODED:
        win.blit(new_surf, (spaceship_rect.x, spaceship_rect.y))


        
        

    #!solve shooting

def explode():

    global explosion
    global BOOM_COUNT
    if BOOM_COUNT == 4:
        return False
    else:
        ex_rect = explosion[BOOM_COUNT].get_rect()
        ex_rect.topleft = (210 - (1 + BOOM_COUNT)*8, 600 - (1 + BOOM_COUNT)*8)
        win.blit(explosion[BOOM_COUNT], (ex_rect.x, ex_rect.y))
        pygame.time.wait(50)
        BOOM_COUNT += 1
        return True


def generate_wave():
    global TYPE1
    global TYPE3
    global TYPE4
    global WAVE
    if WAVE % 3 == 0:
        TYPE3 += 1
    else:
        TYPE1 += 1
    if WAVE % 7 == 0:
        TYPE4 += 1
        TYPE1 -= 1

def generate_words():
    global TYPE1
    global TYPE3
    global TYPE4
    global NUMBER_OF_SHIPS
    global WAVE
    frec = []
    for i in range(TYPE1):
        x = random.randint(0, 420)
        y = random.randint(-10*WAVE, 20)
        #if y < 0:
            #angle_in_radians = math.atan((600+y)/(210 - x))
       # else:
        if x != 210:
            angle_in_radians = math.atan((600-y)/(210-x))
            angle = math.ceil(math.degrees(angle_in_radians))
        else:
            angle = 90
        #print(angle_in_radians, end = " ")
        
        if angle < 0:
            angle = 180+ angle
       # print(x, y, angle)
        start_letter = random.choice("abcdefghijklmnopqrstuvwxyz")
        while start_letter not in SHORT.keys() or start_letter in frec:
            start_letter = random.choice("abcdefghijklmnopqrstuvwxyz")
        frec.append(start_letter)
        text = random.choice(SHORT[start_letter])
        WORD_LIST.append(Type1(x, y, angle, text))
        NUMBER_OF_SHIPS += 1
    #print("Type 1 done")

    for i in range(TYPE3):
        x = random.randint(80, 340)
        y = random.randint(-15*WAVE, 15)
        angle = random.randint(80, 120)
        if x > 210 and angle <= 90:
            angle += 20
        elif x < 210 and angle > 100:
            angle -= 20
        start_letter = random.choice("abcdefghijklmnopqrstuvwxyz")
        while start_letter not in MEDIUM.keys() or start_letter in frec:
            start_letter = random.choice("abcdefghijklmnopqrstuvwxyz")
        text = random.choice(MEDIUM[start_letter])
        WORD_LIST.append(Type3(x, y, angle, text))
        NUMBER_OF_SHIPS += 1

    #print("Type 3 done")

    for i in range(TYPE4):  
        x = random.randint(80, 340)
        y = random.randint(-15*WAVE, 20)
        angle = random.randint(80, 120)
        if x > 210 and angle <= 90:
            angle += 20
        elif x < 210 and angle > 100:
            angle -= 20
        start_letter = random.choice("abcdefghijklmnopqrstuvwxyz")
        while start_letter not in LONG.keys() or start_letter in frec:
            start_letter = random.choice("abcdefghijklmnopqrstuvwxyz")
        text = random.choice(LONG[start_letter])
        WORD_LIST.append(Type4(x, y, angle, text))
        NUMBER_OF_SHIPS += 1

    #print("Type 4 done")




#INPUT BOX

#VARIABLES
RUN = True
FPS = 60
BACKGROUND_Y = 0
STARTED = False
SETTING = False
STATS = False
ON1 = True
OFF1 = False
ON2 = True
OFF2 = False
WAVE_ON = False
OVER = False
CURRENT_SCORE = 0
TYPE1 = 3
TYPE3 = 0
TYPE4 = 0
WAVE = 1
SHOOT_COUNT = 0
CURRENT_SHIP = -1
NUMBER_OF_SHIPS = 0
BOOM_COUNT = 0
EXPLODED = False
SCORE = 0

def null():
    global WAVE_ON
    global OVER
    global CURRENT_SCORE
    global TYPE1
    global TYPE3
    global TYPE4
    global WAVE
    global SHOOT_COUNT
    global CURRENT_SHIP 
    global NUMBER_OF_SHIPS 
    global BOOM_COUNT 
    global EXPLODED
    global SCORE
    WAVE_ON = False
    OVER = False
    CURRENT_SCORE = 0
    TYPE1 = 3
    TYPE3 = 0
    TYPE4 = 0
    WAVE = 1
    SHOOT_COUNT = 0
    CURRENT_SHIP = -1
    NUMBER_OF_SHIPS = 0
    BOOM_COUNT = 0
    EXPLODED = False
    SCORE = 0
    

# LIST OF DICTIONARIES FOR SAVING SCORE
scoreboard = []

WORD_LIST = []

BULLETS = []

#CREATE BUTTONS
new_game = button.Button(210, 500, "new game", 30)
settings = button.Button(210, 550, "settings", 30)
my_stats = button.Button(210, 600, "my stats", 30)
exit_game = button.Button(210, 650, "exit game", 30)
on1 = button.Button(245, 155, 'ON', 20)
off1 = button.Button(245, 155, 'OFF', 20)
on2 = button.Button(245, 195, 'ON', 20)
off2 = button.Button(245, 195, 'OFF', 20)
back_menu = button.Button(210, 600, 'back to menu', 30)
back_menu2 = button.Button(210, 680, 'back to menu', 30)
space_count = 0

#CREATE INPUT BOX
box = inputbox.InputBox(110, 300, 140, 40)

#FONT
font = pygame.font.SysFont("segoeuisemibold", 130)
ztype = font.render('ZTYPE', True, (255,255,255))

font2 = pygame.font.SysFont("segoeuisemilight", 50)
settings_head = font2.render('SETTINGS', True, WHITE)
stats_head = font2.render('STATISTICS', True, WHITE)

font3 = pygame.font.SysFont("segoeuisemilight", 20)
sound = font3.render('SOUND', True, LIGHT_GREY)
music = font3.render('MUSIC', True, LIGHT_GREY)
username = font3.render('NAME', True, WHITE)
score = font3.render('SCORE', True, WHITE)
nr = font3.render('NR.', True, WHITE)
no_records = font3.render('NO RECORDS YET', True, LIGHT_GREY)

font_name = pygame.font.SysFont("segoeuisemilight", 30)
name = font_name.render('NAME', True, WHITE)


font_wave = pygame.font.SysFont("myanmartext", 50)
score_surf = font_wave.render(str(SCORE), True, CIAN)
font_rect = score_surf.get_rect()
xx = len(str(SCORE))
#font_rect.center = (230 - (xx-1)*10, 670)




#IMAGES
bg = pygame.transform.scale(pygame.image.load("space1.jpg").convert_alpha(), (420, 720))
spaceship = [pygame.image.load("pixil-frame-0.png").convert_alpha(),
            pygame.image.load("pixil-frame-1.png").convert_alpha(),
            pygame.image.load("pixil-frame-2.png").convert_alpha(),
            pygame.image.load("pixil-frame-3.png").convert_alpha()]

SpaceShip = [pygame.image.load("Spaceship.png").convert_alpha(),
            pygame.image.load("Spaceship-fire.png").convert_alpha()]

explosion = [pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (16,16)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (24,24)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (32,32)),
                    pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (64,64))]

#spaceship_rect
spaceship_rect = 0

#bg.set_alpha(10)
#MAINLOOP
while RUN:

     #set fps
    #win.fill(BLACK)
#    # win.blit(bg, (0, BACKGROUND_Y))
#     BACKGROUND_Y += 0.75
#     if BACKGROUND_Y >= 720:
#         BACKGROUND_Y = 0
    if STARTED:
        CURRENT_SCORE = 0
        draw_background()
        #win.blit(score_surf, (font_rect.x, font_rect.y))
        win.blit(score_surf, (210-xx*15, 640))
       #generate_wave()
        #generate_words()
        if not WAVE_ON and not OVER:
            WORD_LIST.clear()
              
            generate_wave()
            generate_words()
            #newword = Type1(100, 100, 50, "simplified")
            #newword = WORD_LIST[0]
            WAVE_ON = True
            OVER = False
        #elif not OVER:
            #newword.draw(win)
            #newword.update()
        else:
            pass

    elif STATS:
        win.fill(BLACK)
        win.blit(stats_head, (95,60))
        win.blit(nr, (50, 140))
        win.blit(username, (160, 140))
        win.blit(score, (300, 140))

        pygame.draw.line(win, LIGHT_GREY, (40,170), (370, 170), 2)

        if not scoreboard:
            win.blit(no_records, (125, 180))
        else:
            scoreboard = sorted(scoreboard, key=lambda d: d['score'], reverse=True)
            for i, record in enumerate(scoreboard):
                number = font3.render(str(i+1), True, LIGHT_GREY)
                num_rect = number.get_rect()
                num_rect.center = (60, 190 + i*25)
                user = font3.render(record["name"], True, LIGHT_GREY)
                user_rect = user.get_rect()
                user_rect.center = (185, 190 + i*25)
                scr = font3.render(str(record["score"]), True, LIGHT_GREY)
                scr_rect = scr.get_rect()
                scr_rect.center = (330, 190 + i*25)
                win.blit(number, (num_rect.x, num_rect.y))
                win.blit(user, (user_rect.x, user_rect.y))
                win.blit(scr, (scr_rect.x, scr_rect.y))
        
        if back_menu2.draw(win) == True:
            STATS = False
            pygame.time.wait(100)   



    elif SETTING:
        win.fill(BLACK)
        win.blit(settings_head, (105, 60))
        win.blit(sound, (150, 140))
        win.blit(music, (155, 180))
        win.blit(name, (160, 230))
        
        if ON1:
            if on1.draw(win):
                ON1 = False
                OFF1 = True
                #print("OFF")
        elif OFF1:
            if off1.draw(win):
                ON1 = True
                OFF1 = False
                #print("ON")
        if ON2:
            if on2.draw(win):
                ON2 = False
                OFF2 = True
                #print("OFF")
        elif OFF2:
            if off2.draw(win):
                ON2 = True
                OFF2 = False
                #print("ON")

        if back_menu.draw(win) == True:
                SETTING = False
                pygame.time.wait(100)

    else:
        draw_background()
        win.blit(ztype, (25, 20))   
        #win.blit(space1, (190, 400))

        #Display SpaceShip
        if space_count > 3:
            space_count = 0
        win.blit(spaceship[space_count], (182, 400))
        space_count += 1
        #DISPLAY BUTTONS
        if new_game.draw(win) == True and SETTING == False and STATS == False and RUN == True:
            STARTED = True
            OVER = False
            WAVE = 1
            WAVE_ON = False
        if settings.draw(win) == True:
            SETTING = True
        if my_stats.draw(win) == True:
            STATS = True
        if exit_game.draw(win) == True:
            RUN = False

        


    #eventloop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if SETTING:
            #handles text input    
            box.handle_event(event)
        elif STARTED and WAVE_ON and not OVER:
            if CURRENT_SHIP == -1:
                if event.type == pygame.KEYDOWN:
                    letter = event.unicode
                    #for loop to check all words
                    for classe in WORD_LIST:
                        if classe.word[0] == letter:
                            CURRENT_SHIP = WORD_LIST.index(classe)
                            classe.handle_event(event)
                            break
                    # if letter == newword.word[0]:

                    #     CURRENT_SHIP = 1
                    #     newword.handle_event(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    #newword.handle_event(event)
                    #if event.unicode == letter:
                        #bullet = projectile(210, 590, WHITE, )
                    WORD_LIST[CURRENT_SHIP].handle_event(event)
                    CURRENT_SHIP = -1
            
                # if newword.handle_event(event) == True:
                #     SHOOT_COUNT = 1
                if WORD_LIST[CURRENT_SHIP].over == False and WORD_LIST[CURRENT_SHIP].handle_event(event) == True:
                    SHOOT_COUNT = 1
    
    if SETTING:
        #updates box size, and displays box
        box.update()
        box.draw(win)
    elif STARTED and WAVE_ON and not OVER:
        if SHOOT_COUNT == 0:
            draw_spaceship(0, 0)
        else:
            #count angle
            #angle_in_radians = math.tan((newword.x - 210)/(600 - newword.y))
            angle_in_radians = math.tan((WORD_LIST[CURRENT_SHIP].x - 210)/(600 - WORD_LIST[CURRENT_SHIP].y))
            angle = math.ceil(math.degrees(angle_in_radians))
            #if angle > 0:
                #angle += 180
            BULLETS.append(laser(WORD_LIST[CURRENT_SHIP].x, WORD_LIST[CURRENT_SHIP].y, 210, 590, CIAN))
            #BULLETS.append(projectile(WORD_LIST[CURRENT_SHIP].x, WORD_LIST[CURRENT_SHIP].y, 210,590, WHITE, angle))
            draw_spaceship(angle, 1)
            #bullet.draw(win)
            SHOOT_COUNT -= 1 #shoot count = 0
        # if not newword.update():
        #     newword.draw(win)
        # if newword.over:
        #     #WAVE_ON = False
        #     newword.explode(win)
        #     CURRENT_SHIP = -1
        # if newword.img_cnt == 4:
        #    pass #check if there are any more ships, if not WAVE_ON = FALSE
        for (index, ship) in enumerate(WORD_LIST):
            if index != CURRENT_SHIP:
                ship.update()
                #print(ship.x, ship.y)
                ship.draw(win)
                
            elif not WORD_LIST[CURRENT_SHIP].update():
                #print(type(WORD_LIST[CURRENT_SHIP]))
                WORD_LIST[CURRENT_SHIP].draw(win)
                # if isinstance(ship, Type3) and ship.over == False:
                #     x = ship.x
                #     y = ship.y + 15
                #     if x != 210:
                #         angle_in_radians = math.atan((720-y)/(210-x))
                #         angle = math.ceil(math.degrees(angle_in_radians))
                #     else:
                #         angle = 90
                #     #print(angle_in_radians, end = " ")
                    
                #     if angle < 0:
                #         angle = 180+ angle
                #     start_letter = random.choice("abcdefghijklmnopqrstuvwxyz")
                #     while start_letter not in SHORT.keys():
                #         start_letter = random.choice("abcdefghijklmnopqrstuvwxyz")
                #     text = random.choice(SHORT[start_letter])
                #     WORD_LIST.append(Type2(x, y, angle, text))
                #     NUMBER_OF_SHIPS += 1
            
            # for ship in WORD_LIST:
            #     ship.draw(win)
        for index, bullet in enumerate(BULLETS):
            bullet.draw(win)
            bullet.counter += 1
            if bullet.counter == 10:
                del BULLETS[index]
        if WORD_LIST[CURRENT_SHIP].over:
            BULLETS.clear()
            SCORE += WORD_LIST[CURRENT_SHIP].lenght
            score_surf = font_wave.render(str(SCORE), True, CIAN)
            font_rect = score_surf.get_rect()
            xx = len(str(SCORE))
            #font_rect.center = (230 - (xx-1)*10, 670)
            if WORD_LIST[CURRENT_SHIP].img_cnt == 4:  
                del WORD_LIST[CURRENT_SHIP]
                CURRENT_SHIP = -1   
                if len(WORD_LIST) == 0:
                    WAVE_ON = False   
                    WAVE += 1
                    BULLETS.clear()
            else:
                WORD_LIST[CURRENT_SHIP].explode(win)

        for ship in WORD_LIST:
            #print(ship.word, ship.x, ship.y)
            if ship.img_rect.colliderect(spaceship_rect):
                
                if BOOM_COUNT == 4:
                    pygame.time.wait(100)
                    WAVE_ON = False
                    STARTED = False
                    if not box.text:
                        box.text = "unknown"
                    scoreboard.append({"name": box.text, "score": SCORE})
                    null()
                    
                else:
                    explode()
                    EXPLODED = True
                break
   
    pygame.display.update()
    clock.tick(FPS)


pygame.quit()