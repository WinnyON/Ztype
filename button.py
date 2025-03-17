import pygame


WHITE = (255,255,255)
ORANGE = (255,156,4)

class Button():
    def __init__(self, x, y, text, size):
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        font = pygame.font.SysFont("trebuchetms", size)
        self.text_surf = font.render(text, True, WHITE)
        self.text_surf2 = font.render(text, True, ORANGE)
        self.rect = self.text_surf.get_rect()
        self.rect.center = (x, y)
        self.click = False
        #self.draw()
    
    def draw(self, screen):
        action = False
        #screen.blit(self.text_surf, (self.rect.x, self.rect.y))

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            self.rect = self.text_surf2.get_rect()
            self.rect.center = (self.x,self.y)
            screen.blit(self.text_surf2, (self.rect.x, self.rect.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
               self.click = True
               action = True
        
        else:
            self.rect = self.text_surf.get_rect()
            self.rect.center = (self.x,self.y)
            screen.blit(self.text_surf, (self.rect.x, self.rect.y))

        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False
        
        

        return action
            #     self.text_surf = font.render(self.text, True, ORANGE)
        #     self.rect = self.text_surf.get_rect()
        #     self.rect.topleft = (self.x, self.y)
        # else:
        #     self.text_surf = font.render(self.text, True, WHITE)
        #     self.rect = self.text_surf.get_rect()
        #     self.rect.topleft = (self.x, self.y)


#When changing the color of the text-button, you don't have to rerender it, but you should create another font with orange color,
#and display that when hover and click.