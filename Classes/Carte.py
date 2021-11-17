import pygame
import pyscroll
import pytmx
from Classes.Joueur import Joueur
from Model.PokemonBDD import PokemonBDD


class Carte:

    def __init__(self, leJeu):
        self.jeu = leJeu
        self.bdd = PokemonBDD()
        self.joueur = Joueur("joueur_fille",500, 500)
        self.nom_carte = "carte"

    '''Méthode permettant de charger une carte spécifique'''
    def chargerCarte(self, nomCarte):
        self.tmx_data = pytmx.util_pygame.load_pygame(f"Map/{nomCarte}.tmx")
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.jeu.screen.get_size())
        self.map_layer.zoom = 3

        self.get_collisions(nomCarte)
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)
        self.group.add(self.joueur)


    def get_collisions(self, nomCarte):
        self.collision = []

        for obj in pytmx.util_pygame.load_pygame(f"Map/{nomCarte}.tmx").objects:
            if obj.type == "collision":
                self.collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    def affichage_carte(self):
        self.joueur.ancienne_position()
        self.joueur.gestion_touches()
        self.update()
        self.group.center(self.joueur.rect.center)
        self.group.draw(self.jeu.screen)
        pygame.display.flip()

    '''Méthode permettant de mettre à jour le groupe de calques et si un des sprite (élément du jeu type joueur) est dans un objet de type colission faire revenir le joueur en arrière'''
    def update(self):
        self.group.update()  # Faire les majs du groupe

        for sprite in self.group.sprites():  # Récupérer les sprites du groupe
            if sprite.pieds.collidelist(self.collision) > -1:  # Si le sprite pied est dans la zone de collision
                sprite.revenir_en_arriere()  # Faire revenir le sprite (Donc ici l'image du joueur) en arrière

    def majSexePerso(self):
        print(self.bdd.getSexePersonnage())
        self.joueur.chgSexePerso(self.bdd.getSexePersonnage())
