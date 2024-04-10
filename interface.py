import pygame

class Interface():
    def __init__(self, surface):
        self.display_surface = surface
        self.viewRect = pygame.Rect(150, 30, 500, 400)
        self.inputRect = pygame.Rect(200, 500, 400, 50)

    def draw(self):
        self.box_input = pygame.draw.rect(self.display_surface, (255, 255, 255), self.inputRect, 0, 40)
        self.box_show = pygame.draw.rect(self.display_surface, (255, 255, 255), self.viewRect, 0, 20)