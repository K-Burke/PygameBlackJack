import pygame

class TextInput():

    def __init__(self, x, y, width, height, col, font, isPassword, max):
        
        self.active = False
        self.password = isPassword
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = col
        self.font = font
        self.max_length = max
        self.content = '' 

    def draw(self, surface):
        
        if self.active:
            pygame.draw.rect(surface, self.colour, self.rect)
            pygame.draw.rect(surface, (0,0,0), pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height), 2)

        else:
            pygame.draw.rect(surface, self.colour, self.rect)

        if self.password:
            output = ''
            for x in self.content:
                output += '*'
        else: output = self.content

        content_text = self.font.render(output, False, (0,0,0))
        surface.blit(content_text, (self.rect.x + 5, self.rect.y))


