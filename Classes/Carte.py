import pygame
import pyscroll
import pytmx

class Carte:

    def __init__(self, leJeu):
        self.jeu = leJeu

    '''Méthode permettant de charger une carte spécifique'''
    def chargerCarte(self, nomCarte):
        self.tmx_data = pytmx.util_pygame.load_pygame(f"Map/{nomCarte}.tmx")
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.jeu.screen.get_size())
        self.map_layer.zoom = 3

        return self.map_layer

    def get_collisions(self, nomCarte):
        collision = []

        for obj in pytmx.util_pygame.load_pygame(f"Map/{nomCarte}.tmx").objects:
            if obj.type == "collision":
                collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        return collision
