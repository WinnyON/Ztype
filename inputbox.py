import pygame

WHITE = (255,255,255)
LIGHT_GREY = (148, 148, 148)

class InputBox():
    def __init__(self, x, y, w, h, text = ''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.text = text
        self.font_name = pygame.font.SysFont("segoeuisemilight", 25)
        self.txt_surface = self.font_name.render(text, True, self.color)
        self.active = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            #If the user clicked on the input box rect
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            #Change the color of the box
            if self.active:
                self.color = LIGHT_GREY
            else:
                self.color = WHITE
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.active = False
                    self.color = WHITE
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) <= 20:
                        self.text += event.unicode
                #Re-render the text
                self.txt_surface = self.font_name.render(self.text, True, self.color)

    def update(self):
        #Resize the box if the text is too long
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        #Display the text
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        #Display the rect
        pygame.draw.rect(screen, self.color, self.rect, 2)