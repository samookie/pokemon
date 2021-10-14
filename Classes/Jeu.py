import pygame
import pytmx
import pyscroll

pygame.init()


class Jeu:
    def __init__(self):

        # créer la fenêtre du jeu

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Powebmon")

        # charger la carte

        tmx_data = pytmx.util_pygame.load_pygame("Map/ville.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        # dessiner le groupe de calsques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

    def lancement(self):

        # boucle du jeu

        jeu = True
        while jeu:
            self.group.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jeu = False

        pygame.quit()
