import pygame

class Pnj():

    def __init__(self, leJeu, name, x, y, orientation="bas"):
        self.leJeu = leJeu
        self.imgPnj = pygame.image.load(f"Map/Images/{name}.png")

        self.leJeu.screen.blit(self.imgPnj, (x, y))
