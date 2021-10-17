import pygame
import pytmx
import pyscroll

from Classes.Carte import Carte
from Classes.Joueur import Joueur

pygame.init()


class Jeu:
    def __init__(self):

        # créer la fenêtre du jeu

        self.screen = pygame.display.set_mode((700, 600))
        pygame.display.set_caption("Powebmon")

    def lancement(self):

        # Variables
        jeu = True
        cartes = Carte()
        joueur = Joueur(500, 500)
        clock = pygame.time.Clock()

        # Variables pour les cartes
        carte_principale = cartes.carte_princiaple(self.screen.get_size())
        magasin = cartes.carte_magasin(self.screen.get_size())

        # dessiner le groupe de calsques
        self.group = pyscroll.PyscrollGroup(map_layer=carte_principale, default_layer=1)
        self.group.add(joueur)

        # boucle du jeu
        while jeu:

            # A faire à chaque tour de boucle
            joueur.gestion_touches()
            self.group.update()
            self.group.center(joueur.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            # Récupérer les évènements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jeu = False

            clock.tick(60) # Définir le jeu à 30 FPS

        pygame.quit()
