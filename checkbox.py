import pygame

class CheckBox():

    def __init__(self, x, y, width, height):

        self.checked = False
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):

        pygame.draw.rect(surface, (0,0,0), self.rect, 2)

        if self.checked:
            pygame.draw.rect(surface, (0,0,0), pygame.Rect((self.rect.left + 4), (self.rect.top + 4), (self.rect.width - 8), (self.rect.height - 8)))

    def toggle(self):
        if self.checked == False: self.checked = True
        else: self.checked = False