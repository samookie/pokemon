import re

import pygame
import pyscroll
import pytmx
import random

from Classes.Cinematiques import Cinematiques
from Classes.Joueur import Joueur
from Classes.MenuInGame import MenuInGame
from Model.PokemonBDD import PokemonBDD
from Classes.Pnj import Pnj
from Classes.FightPokemon import FightPokemon
from Classes.Pokemon import Pokemon

class Carte:

    def __init__(self, leJeu, joueur):
        self.jeu = leJeu
        self.bdd = PokemonBDD()
        self.joueur = joueur
        self.lesPnj = ["pnj_centre","pnj_magasin","pnj_professeur"]
        self.menuInGame = MenuInGame(self.jeu)
        self.cinematiques = Cinematiques(self)
        self.enCinematique = False

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
        self.getPNJ()
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
        self.getPNJ()

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
        self.cinematique = []
        self.fight=[]

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
            elif obj.type == "cine":
                self.cinematique.append(obj)
            elif obj.type == "fight":
                self.fight.append(obj)

    def affichage_carte(self):
        self.joueur.ancienne_position()
        if self.jeu.dansMenu and not self.enCinematique:
            self.joueur.gestion_touches()
        self.update()
        self.group.center(self.joueur.rect.center)
        self.group.draw(self.jeu.screen)
        self.menuInGame.affichage()
        if self.enCinematique:
            if self.cinematiqueObj.name == "1" and str(self.idCine) == "1":
                self.cinematiques.cine1()
            elif self.cinematiqueObj.name == "2" and str(self.idCine) == "2":
                self.cinematiques.cine2()
            else:
                self.enCinematique = False
            self.cinematiques.gestion_touches()
        pygame.display.flip()


    '''Méthode permettant de mettre à jour le groupe de calques et si un des sprite (élément du jeu type joueur) est dans un objet de type colission faire revenir le joueur en arrière'''
    def update(self):
        self.idCine = self.bdd.getCurrentCinematique()[0]
        proba = random.randint(1,100)
        leNb = random.randint(1,100)
        position = self.joueur.position


        self.group.update()  # Faire les majs du groupe

        for entreeObjKey, entreeObjValue in self.entreeDict.items():
            if self.joueur.pieds.colliderect(entreeObjValue):
                self.chargerCarte(re.sub("(^entree_|^sortie_)|(-\w+)|(#\w+)", "", entreeObjKey), (re.sub("(\w+)-|(#\w+)", "", entreeObjKey) + self.numberSpawnPoint))

                if "#" in entreeObjKey:
                    self.numberSpawnPoint = re.sub(".+#", "", entreeObjKey)
                else:
                    self.numberSpawnPoint = ""

        for obj in self.cinematique:
            if self.joueur.pieds.colliderect(pygame.Rect(obj.x, obj.y, obj.width, obj.height)):
                self.enCinematique = True
                self.cinematiqueObj = obj

        for obj in self.fight:
            if self.joueur.pieds.colliderect(pygame.Rect(obj.x, obj.y, obj.width, obj.height)):
                print(obj.name)
                if proba == leNb:
                    if obj.name == "zone1":
                        self.choixPokemon("zone1", leNb) #fonction de choix du pokemon et tp dans le fight pokemon



        for sprite in self.group.sprites():  # Récupérer les sprites du groupe
            if sprite.pieds.collidelist(self.collision) > -1:  # Si le sprite pied est dans la zone de collision
                sprite.revenir_en_arriere()  # Faire revenir le sprite (Donc ici l'image du joueur) en arrière

    def getPNJ(self):

        for pnj in self.objPnj:
            temp = Pnj(pnj.name)
            temp.modifPosition([pnj.x, pnj.y])
            self.group.add(temp)

    def choixPokemon(self, zone , leNb):
        if zone == "zone1":
            rattata = {"nom": "Rattata",
                       "level": [2, 3, 4],
                       "pourcentage": 45
                       }

            roucool = {"nom": "Roucool",
                       "level": [2, 3, 4, 5],
                       "pourcentage": 50
                       }

            if leNb < 50:
                niveau = random.randint(2, 5)
                infoPokemon = self.bdd.searchPokemon(rattata.get("nom"))
                lePokemon = Pokemon(self.jeu, infoPokemon[0],"RATTATA",infoPokemon[1],infoPokemon[2],infoPokemon[3],infoPokemon[4],infoPokemon[5],infoPokemon[6],infoPokemon[7],infoPokemon[8],infoPokemon[9],infoPokemon[10],infoPokemon[11])
                lePokemon.setLevelPokemon(niveau) # Mettre le pokemon à niveau adaptée
                self.jeu.fightP.changerPokemon(lePokemon.getPokemon(),self.joueur.getLesPokemons()) # passer les informations à FightPokemon
                self.jeu.ecran_affiche="fightP" # Change l'écran d'affichage au fightPokemon
                self.jeu.mettre_a_jour = True
            else:
                niveau = random.randint(3, 5)
                infoPokemon = self.bdd.searchPokemon(roucool.get("nom"))
                lePokemon = Pokemon(self.jeu, infoPokemon[0],"ROUCOOL", infoPokemon[1], infoPokemon[2], infoPokemon[3],
                                    infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7], infoPokemon[8],
                                    infoPokemon[9], infoPokemon[10], infoPokemon[11])
                lePokemon.setLevelPokemon(niveau)
                self.jeu.fightP.changerPokemon(lePokemon.getPokemon(), self.joueur.getLesPokemons())  # passer les informations à FightPokemon
                self.jeu.ecran_affiche = "fightP"
                self.jeu.mettre_a_jour = True
