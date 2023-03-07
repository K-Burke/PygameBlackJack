import pygame
import math
pygame.font.init()

class Button():

    def __init__(self, x, y, image, scale):

        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

    def set_position(self, x, y):

        self.rect.topleft = (x, y)

# Here is an example of initializing it, looks best with at least 50 for height, and more than that for width
# TEST = button.TextButton(100, 100, 500, 300, "Play", (0,255,255), (30, 30, 255))
class TextButton():

    def __init__(self, x, y, width, height, content, back, fore):
        
        self.text = content
        self.back = back
        self.fore = fore
        self.background = pygame.Rect(x, y, width, height)

        tempOff = math.floor((width + height)/30)
        tempX = x + tempOff
        tempY = y + tempOff
        tempW = width - (2 * tempOff)
        tempH = height - (2* tempOff)

        self.foreground = pygame.Rect(tempX, tempY, tempW, tempH)
        self.foreground_size = math.floor(tempOff/3)
        
        # This will make the size of the content make sense
        x = (width + height)/6
        self.content = pygame.font.SysFont('timesnewroman', math.floor(x)).render(content, False, fore)
        self.content_shadow = pygame.font.SysFont('timesnewroman', math.floor(x)).render(content, False, (0,0,0))
        while self.content.get_width() > (self.foreground.width - 10):
            x = (x * 0.85)
            self.content = pygame.font.SysFont('timesnewroman', math.floor(x)).render(content, False, fore)
            self.content_shadow = pygame.font.SysFont('timesnewroman', math.floor(x)).render(content, False, (0,0,0))
    
    def draw(self, surface, shadow):

        pygame.draw.rect(surface, self.back, self.background)
        if shadow:
            pygame.draw.rect(surface, (0,0,0), pygame.Rect((self.foreground.left + (math.floor(self.foreground_size))), (self.foreground.top + (math.floor(self.foreground_size))), self.foreground.width, self.foreground.height), self.foreground_size)
        pygame.draw.rect(surface, self.fore, self.foreground, self.foreground_size)

        if shadow:
            surface.blit(self.content_shadow, ((self.background.left + (self.background.width / 2) - (self.content.get_width() / 2) + math.floor(self.foreground_size/1.25), (self.background.top + (self.background.height / 2) - (self.content.get_height() / 2) + math.floor(self.foreground_size/1.25)))))
        surface.blit(self.content, ((self.background.left + (self.background.width / 2) - (self.content.get_width() / 2)), (self.background.top + (self.background.height / 2) - (self.content.get_height() / 2))))

    def set_position(self, x, y):

        delta_X = self.background.left - x
        delta_Y = self.background.top - y

        self.foreground.topleft = ((self.foreground.left - delta_X), (self.foreground.top - delta_Y))

        self.background.topleft = (x, y)