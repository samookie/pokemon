import pygame
import pyscroll

from Classes.Carte import Carte
from Classes.Home_Screen import Home_Screen
from Classes.Joueur import Joueur

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
        joueur = Joueur(500, 500)
        clock = pygame.time.Clock()
        self.collision = carte.get_collisions("ville")

        # Variables pour les cartes
        carte_principale = carte.chargerCarte("ville")

        # dessiner le groupe de calsques
        self.group = pyscroll.PyscrollGroup(map_layer=carte_principale, default_layer=1)
        self.group.add(joueur)

        # boucle du jeu
        while jeu:

            if self.ecran_affiche == "home":
                Home_Screen(self)
            elif self.ecran_affiche == "jeu":
                joueur.ancienne_position()
                joueur.gestion_touches()
                self.update()
                self.group.center(joueur.rect.center)
                self.group.draw(self.screen)
                pygame.display.flip()
            else:
                pass

            # Récupérer les évènements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jeu = False

            clock.tick(60) # Définir le jeu à 30 FPS

        pygame.quit()

    '''Méthode permettant de mettre à jour le groupe de calques et si un des sprite (élément du jeu type joueur) est dans un objet de type colission faire revenir le joueur en arrière'''
    def update(self):
        self.group.update() #Faire les majs du groupe

        for sprite in self.group.sprites(): #Récupérer les sprites du groupe
            if sprite.pieds.collidelist(self.collision) > -1: #Si le sprite pied est dans la zone de collision
                sprite.revenir_en_arriere() #Faire revenir le sprite (Donc ici l'image du joueur) en arrière
