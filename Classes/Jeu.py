import pygame

from Classes.Carte import Carte
from Classes.Home_Screen import Home_Screen

pygame.init()

class Jeu:
    def __init__(self):

        # créer la fenêtre du jeu

        self.screen = pygame.display.set_mode((700, 600))
        pygame.display.set_caption("Powebmon")

    def lancement(self):

        # Variables
        self.ecran_affiche = "home"
        self.mettre_a_jour = True

        jeu = True
        carte = Carte(self)
        clock = pygame.time.Clock()

        # Variables pour les cartes
        carte.chargerCarte("ville")

        # VARS ECRANS
        ecran_accueil = Home_Screen(self)

        # boucle du jeu
        while jeu:

            if self.ecran_affiche == "home":
                ecran_accueil.afficher_ecran()
                ecran_accueil.gestion_touches()
            elif self.ecran_affiche == "jeu":
                carte.affichage_carte()
            else:
                pass

            # Récupérer les évènements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jeu = False

            clock.tick(60) # Définir le jeu à 30 FPS

        pygame.quit()