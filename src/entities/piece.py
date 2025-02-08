import pygame
import os

dirname = os.path.dirname(__file__)

class Piece(pygame.sprite.Sprite):
    def __init__(self,x=0,y=0, name = "placeholder", color = "w"):
        self.color = color
        self.position = (x,y)
        super().__init__()

        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", name + color+".png")
        )

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y