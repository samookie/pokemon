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
        self.collision = []
        #pygame.mixer.init()
        #musique = pygame.mixer.Sound("Map/Musiques/pokemon_main-theme.wav")
        #musique.play()

        # Variables pour les cartes
        carte_principale = cartes.carte_princiaple(self.screen.get_size())
        magasin = cartes.carte_magasin(self.screen.get_size())

        # Récupérer les objets de la carte
        for obj in pytmx.util_pygame.load_pygame("Map/ville.tmx").objects:
            if obj.type == "collision":
                self.collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calsques
        self.group = pyscroll.PyscrollGroup(map_layer=carte_principale, default_layer=1)
        self.group.add(joueur)

        # boucle du jeu
        while jeu:

            # A faire à chaque tour de boucle
            joueur.ancienne_position()
            joueur.gestion_touches()
            self.update()
            self.group.center(joueur.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            # Récupérer les évènements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jeu = False

            clock.tick(60) # Définir le jeu à 30 FPS

        pygame.quit()

    '''Méthode permettant de mettre à jour le groupe de calques et si un des sprite (élément du jeu type joueur) est dans un objet de type colission faire revenir le joueur en arrière'''
    def update(self):
        self.group.update()

        for sprite in self.group.sprites():
            if sprite.pieds.collidelist(self.collision) > -1:
                sprite.revenir_en_arriere()
