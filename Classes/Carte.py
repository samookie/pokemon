import re

import pygame
import pyscroll
import pytmx
from Classes.Joueur import Joueur
from Classes.MenuInGame import MenuInGame
from Model.PokemonBDD import PokemonBDD
from Classes.Pnj import Pnj

class Carte:

    def __init__(self, leJeu, joueur):
        self.jeu = leJeu
        self.bdd = PokemonBDD()
        self.joueur = joueur
        self.lesPnj = ["pnj_centre","pnj_magasin","pnj_professeur"]
        self.menuInGame = MenuInGame(self.jeu)

        self.nom_carte = "carte"
        self.numberSpawnPoint = ""

        self.tableauTp = {}

    '''Méthode permettant de charger une carte spécifique'''
    def chargerCarte(self, nomCarte, spawn):
        self.nom_carte = nomCarte

        self.tmx_data = pytmx.util_pygame.load_pygame(f"Map/{nomCarte}.tmx")
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.jeu.screen.get_size())
        self.map_layer.zoom = 3

        self.get_collisions(nomCarte) # prendre toutes les collisions de la map
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)
        self.group.add(self.joueur)
        self.joueur.modifPosition(self.getCoordonnee(spawn))# changer les coordonnées du joueurs par celui du spown

    '''Méthode permettant de charger une carte spécifique'''

    def chargerCarteSansSpawn(self, nomCarte):
        self.nom_carte = nomCarte

        self.tmx_data = pytmx.util_pygame.load_pygame(f"Map/{nomCarte}.tmx")
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.jeu.screen.get_size())
        self.map_layer.zoom = 3

        self.get_collisions(nomCarte)  # prendre toutes les collisions de la map
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)
        self.group.add(self.joueur)

    """ Méthode permettant de récupérer les coordonnées du spawn actuelle (récupéré dans la méthodes getCollision) """
    def getCoordonnee(self, spawn):
        result =[0,0]
        for obj in self.spawn:
            if obj.name == spawn:
                result = [obj.x , obj.y] # coordonnée x y du spawn

        return result

    def get_collisions(self, nomCarte):
        self.collision = []
        self.entree = []
        self.spawn = []
        self.entreeDict = {}
        self.objPnj = []

        for obj in pytmx.util_pygame.load_pygame(f"Map/{nomCarte}.tmx").objects:
            if obj.type == "collision":
                self.collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "entree": # Récupération de toutes les entrées de la map actuelle
                self.entree.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                self.entreeDict[obj.name] = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            elif obj.type == "spawn": # Récupération de tous les spawns de la map actuelle
                self.spawn.append(obj)
            elif obj.type == "pnj":
                self.objPnj.append(obj)

    def affichage_carte(self):
        self.joueur.ancienne_position()
        if self.jeu.dansMenu:
            self.joueur.gestion_touches()
        self.update()
        self.group.center(self.joueur.rect.center)
        self.group.draw(self.jeu.screen)
        self.getPNJ()
        self.menuInGame.affichage()
        pygame.display.flip()

    '''Méthode permettant de mettre à jour le groupe de calques et si un des sprite (élément du jeu type joueur) est dans un objet de type colission faire revenir le joueur en arrière'''
    def update(self):
        self.group.update()  # Faire les majs du groupe

        for entreeObjKey, entreeObjValue in self.entreeDict.items():
            if self.joueur.pieds.colliderect(entreeObjValue):
                self.chargerCarte(re.sub("(^entree_|^sortie_)|(-\w+)|(#\w+)", "", entreeObjKey), (re.sub("(\w+)-|(#\w+)", "", entreeObjKey) + self.numberSpawnPoint))

                if "#" in entreeObjKey:
                    self.numberSpawnPoint = re.sub(".+#", "", entreeObjKey)
                else:
                    self.numberSpawnPoint = ""


        for sprite in self.group.sprites():  # Récupérer les sprites du groupe
            if sprite.pieds.collidelist(self.collision) > -1:  # Si le sprite pied est dans la zone de collision
                sprite.revenir_en_arriere()  # Faire revenir le sprite (Donc ici l'image du joueur) en arrière

    def getPNJ(self):

        for pnj in self.objPnj:
            Pnj(self.jeu, pnj.name, pnj.x, pnj.y)

