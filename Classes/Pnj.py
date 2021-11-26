import pygame

class Pnj(pygame.sprite.Sprite):

    def __init__(self, leJeu, name, x, y, orientation="bas"):
        super().__init__()

        self.leJeu = leJeu
        self.image = pygame.image.load(f"Map/Images/{name}.png")
        self.rect = self.image.get_rect()

        self.position = [x, y]
        self.sprite_sheet = self.image
