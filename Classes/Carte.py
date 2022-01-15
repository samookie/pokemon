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
from Classes.ActionEndroit import ActionEndroit

class Carte:

    def __init__(self, leJeu, joueur):
        self.jeu = leJeu
        self.bdd = PokemonBDD()
        self.joueur = joueur
        self.lesPnj = ["pnj_centre","pnj_magasin","pnj_professeur"]
        self.menuInGame = MenuInGame(self.jeu)
        self.cinematiques = Cinematiques(self)
        self.enCinematique = False
        self.auCentre = False
        self.listePokemon = joueur.getLesPokemons()
        self.laListePokemon = []
        self.actionEndroit = ActionEndroit(self)
        print("Liste carte",self.listePokemon)
        self.cptPoke = 0
        self.bulbizarre  = Pokemon(self.jeu,"Bulbizarre","None","Herbizarre",1,45,45,49,65,49,65,"bulbizarre","d_bulbizarre","f_bulbizarre","Plante")
        for poke in self.listePokemon:
            unPokemon = Pokemon(self.jeu, poke[0],poke[1],poke[2],1,poke[4],poke[5],poke[6],poke[7],poke[8],poke[9],poke[10],poke[11],poke[12],poke[13])
            self.laListePokemon.append(unPokemon)
            self.laListePokemon[self.cptPoke].setLevelPokemon(poke[3])
            self.cptPoke += 1


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
        self.action=[]
        self.dresseur=[]

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
            elif obj.type == "action":
                self.action.append(obj)
            elif obj.type == "dresseur":
                self.dresseur.append(obj)

    def affichage_carte(self):
        self.joueur.ancienne_position()
        if self.jeu.dansMenu and not self.enCinematique and not self.auCentre:
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
            elif self.cinematiqueObj.name == "3" and str(self.idCine) == "3":
                self.cinematiques.cine3()
            elif self.cinematiqueObj.name == "4" and str(self.idCine) == "4":
                self.cinematiques.cine4()
            else:
                self.enCinematique = False
            self.cinematiques.gestion_touches()

        if self.auCentre:
            self.actionEndroit.affichage()
            self.actionEndroit.gestion_touches()
            self.actionEndroit.soigner()

        pygame.display.flip()


    '''Méthode permettant de mettre à jour le groupe de calques et si un des sprite (élément du jeu type joueur) est dans un objet de type colission faire revenir le joueur en arrière'''
    def update(self):
        self.idCine = self.bdd.getCurrentCinematique()[0]
        proba = random.randint(1,100)
        leNb = random.randint(1,100)
        position = [0,0]


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
            if self.joueur.pieds.colliderect(pygame.Rect(obj.x, obj.y, obj.width, obj.height)): # si le joueur tombe dans une zone de combat
                if proba == leNb: # si le nombre de proba aléatoire et le nombre sont égales
                    if obj.name == "zone1": # cela correspond à la zone 1
                        self.choixPokemon("zone1", leNb) #fonction de choix du pokemon et tp dans le fight pokemon
                    elif obj.name == "zone2":
                        self.choixPokemon("zone2", leNb)  # fonction de choix du pokemon et tp dans le fight pokemon
                    elif obj.name == "zone3":
                        self.choixPokemon("zone3", leNb)  # fonction de choix du pokemon et tp dans le fight pokemon

        for obj in self.action:
            if self.joueur.pieds.colliderect(pygame.Rect(obj.x, obj.y, obj.width, obj.height)): # si le joueur tombe dans une zone de combat
                if obj.name == "centre": # cela correspond à la zone 1
                    if pygame.key.get_pressed()[pygame.K_SPACE] and not self.auCentre:
                        self.auCentre = True

        for obj in self.dresseur:
            if self.joueur.pieds.colliderect(pygame.Rect(obj.x, obj.y, obj.width, obj.height)): # si le joueur tombe dans une zone de combat
                if obj.name == "Omar": # cela correspond à la zone 1
                    self.attaqueDresseur("Omar") #fonction de choix du pokemon et tp dans le fight pokemon




        for sprite in self.group.sprites():  # Récupérer les sprites du groupe
            if sprite.pieds.collidelist(self.collision) > -1:  # Si le sprite pied est dans la zone de collision
                sprite.revenir_en_arriere()  # Faire revenir le sprite (Donc ici l'image du joueur) en arrière

    def getPNJ(self):

        for pnj in self.objPnj:
            temp = Pnj(pnj.name)
            temp.modifPosition([pnj.x, pnj.y])
            self.group.add(temp)

    def attaqueDresseur(self, nomDresseur):
        liste_PokemonE =[]
        if nomDresseur == "Omar":

            infoChenipan = self.bdd.searchPokemon("Chenipan")  # chercher dans la base de donnée le pokémon
            chenipan = Pokemon(self.jeu, infoChenipan[0], "ASPICOT", infoChenipan[1], infoChenipan[2], infoChenipan[3],
                                infoChenipan[4], infoChenipan[5], infoChenipan[6], infoChenipan[7], infoChenipan[8],
                                infoChenipan[9], infoChenipan[10], infoChenipan[11],
                                infoChenipan[12])  # initialisation du pokémon
            chenipan.setLevelPokemon(6)  # Mettre le pokemon au niveau adaptée

            infoAspicot = self.bdd.searchPokemon("Aspicot")  # chercher dans la base de donnée le pokémon
            aspicot = Pokemon(self.jeu, infoAspicot[0], "ASPICOT", infoAspicot[1], infoAspicot[2], infoAspicot[3],
                               infoAspicot[4], infoAspicot[5], infoAspicot[6], infoAspicot[7], infoAspicot[8],
                               infoAspicot[9], infoAspicot[10], infoAspicot[11],
                               infoAspicot[12])  # initialisation du pokémon
            aspicot.setLevelPokemon(6)  # Mettre le pokemon au niveau adaptée

            liste_PokemonE = [chenipan,aspicot]

            self.jeu.fightD.changerPokemon(liste_PokemonE,self.laListePokemon)  # passer les informations à FightPokemon
            self.jeu.ecran_affiche = "fightD"  # Change l'écran d'affichage au fightPokemon
            self.jeu.mettre_a_jour = True

    def choixPokemon(self, zone , leNb):
        print(leNb)
        '''
        Fonction permettant d'avoir l'apparition des pokemons dans une zones et les pourcentages d'apparition, avec le noombre dans une zone
        :param zone: zone d'apparition des pokemons (zone1 , 2 , 3, ...)
        :param leNb: le nombre aléatoire tombé (pour faire le choix du pokémon
        '''

        if zone == "zone1":
            rattata = {"nom": "Rattata",
                       "level": [2, 3, 4],
                       "pourcentage": 45
                       }

            roucool = {"nom": "Roucool",
                       "level": [2, 3, 4, 5],
                       "pourcentage": 50
                       }

            if leNb < 50: # si nombre en dessous de 50 alors apparition de rattata
                niveau = random.randint(2, 5) # niveau du pokemon aléatoirement
                infoPokemon = self.bdd.searchPokemon(rattata.get("nom")) # chercher dans la base de donnée le pokémon
                lePokemon = Pokemon(self.jeu, infoPokemon[0],"RATTATA",infoPokemon[1],infoPokemon[2],infoPokemon[3],infoPokemon[4],infoPokemon[5],infoPokemon[6],infoPokemon[7],infoPokemon[8],infoPokemon[9],infoPokemon[10],infoPokemon[11],infoPokemon[12]) # initialisation du pokémon
                lePokemon.setLevelPokemon(niveau) # Mettre le pokemon au niveau adaptée
                self.jeu.fightP.changerPokemon(lePokemon.getPokemon(),self.laListePokemon) # passer les informations à FightPokemon
                self.jeu.ecran_affiche="fightP" # Change l'écran d'affichage au fightPokemon
                self.jeu.mettre_a_jour = True
            else:
                niveau = random.randint(3, 5)
                infoPokemon = self.bdd.searchPokemon(roucool.get("nom"))
                lePokemon = Pokemon(self.jeu, infoPokemon[0],"ROUCOOL", infoPokemon[1], infoPokemon[2], infoPokemon[3],
                                    infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7], infoPokemon[8],
                                    infoPokemon[9], infoPokemon[10], infoPokemon[11],infoPokemon[12])
                lePokemon.setLevelPokemon(niveau)

                self.jeu.fightP.changerPokemon(lePokemon.getPokemon(), self.laListePokemon)  # passer les informations à FightPokemon
                self.jeu.ecran_affiche = "fightP"
                self.jeu.mettre_a_jour = True
        elif zone == "zone2":
            rattata = {"nom": "Rattata",
                       "level": [2, 3, 4],
                       "pourcentage": 45
                       }

            roucool = {"nom": "Roucool",
                       "level": [2, 3, 4, 5],
                       "pourcentage": 50
                       }

            chenipan = {"nom": "Chenipan",
                       "level": [4, 5],
                       "pourcentage": 5
                       }

            aspicot = {"nom": "Aspicot",
                       "level": [4, 5],
                       "pourcentage": 5
                       }

            if leNb < 6 :
                niveau = random.randint(4, 5)  # niveau du pokemon aléatoirement
                infoPokemon = self.bdd.searchPokemon(chenipan.get("nom"))  # chercher dans la base de donnée le pokémon
                lePokemon = Pokemon(self.jeu, infoPokemon[0], "CHENIPAN", infoPokemon[1], infoPokemon[2], infoPokemon[3],
                                    infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7], infoPokemon[8],
                                    infoPokemon[9], infoPokemon[10], infoPokemon[11],
                                    infoPokemon[12])  # initialisation du pokémon
                lePokemon.setLevelPokemon(niveau)  # Mettre le pokemon au niveau adaptée
                self.jeu.fightP.changerPokemon(lePokemon.getPokemon(),
                                               self.laListePokemon)  # passer les informations à FightPokemon
                self.jeu.ecran_affiche = "fightP"  # Change l'écran d'affichage au fightPokemon
                self.jeu.mettre_a_jour = True

            elif leNb>=6 and leNb < 51 : # si nombre en dessous de 50 alors apparition de rattata
                niveau = random.randint(2, 5) # niveau du pokemon aléatoirement
                infoPokemon = self.bdd.searchPokemon(roucool.get("nom")) # chercher dans la base de donnée le pokémon
                lePokemon = Pokemon(self.jeu, infoPokemon[0],"ROUCOOL",infoPokemon[1],infoPokemon[2],infoPokemon[3],infoPokemon[4],infoPokemon[5],infoPokemon[6],infoPokemon[7],infoPokemon[8],infoPokemon[9],infoPokemon[10],infoPokemon[11],infoPokemon[12]) # initialisation du pokémon
                lePokemon.setLevelPokemon(niveau) # Mettre le pokemon au niveau adaptée
                self.jeu.fightP.changerPokemon(lePokemon.getPokemon(),self.laListePokemon) # passer les informations à FightPokemon
                self.jeu.ecran_affiche="fightP" # Change l'écran d'affichage au fightPokemon
                self.jeu.mettre_a_jour = True
            elif leNb>=51 and leNb <56:
                niveau = random.randint(4, 5)
                infoPokemon = self.bdd.searchPokemon(aspicot.get("nom"))
                lePokemon = Pokemon(self.jeu, infoPokemon[0],"ASPICOT", infoPokemon[1], infoPokemon[2], infoPokemon[3],
                                    infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7], infoPokemon[8],
                                    infoPokemon[9], infoPokemon[10], infoPokemon[11],infoPokemon[12])
                lePokemon.setLevelPokemon(niveau)

                self.jeu.fightP.changerPokemon(lePokemon.getPokemon(), self.laListePokemon)  # passer les informations à FightPokemon
                self.jeu.ecran_affiche = "fightP"
                self.jeu.mettre_a_jour = True

            elif leNb >= 56:
                niveau = random.randint(2, 5)
                infoPokemon = self.bdd.searchPokemon(rattata.get("nom"))
                lePokemon = Pokemon(self.jeu, infoPokemon[0],"RATTATA", infoPokemon[1], infoPokemon[2], infoPokemon[3],
                                    infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7], infoPokemon[8],
                                    infoPokemon[9], infoPokemon[10], infoPokemon[11],infoPokemon[12])
                lePokemon.setLevelPokemon(niveau)

                self.jeu.fightP.changerPokemon(lePokemon.getPokemon(), self.laListePokemon)  # passer les informations à FightPokemon
                self.jeu.ecran_affiche = "fightP"
                self.jeu.mettre_a_jour = True

        elif zone == "zone3":

            chenipan = {"nom": "Chenipan",
                       "level": [3, 4, 5],
                       "pourcentage": 40
                       }

            aspicot = {"nom": "Aspicot",
                       "level": [3, 4, 5],
                       "pourcentage": 40
                       }

            chrysacier = {"nom": "Chrysacier",
                       "level": [5],
                       "pourcentage": 5
                       }

            coconfort = {"nom": "Coconfort",
                       "level": [4, 5, 6],
                       "pourcentage": 10
                       }

            pikachu = {"nom": "Pikachu",
                       "level": [3, 4, 5],
                       "pourcentage": 5
                       }

            if leNb < 6 :
                niveau = random.randint(3, 5) # niveau du pokemon aléatoirement
                infoPokemon = self.bdd.searchPokemon(pikachu.get("nom"))  # chercher dans la base de donnée le pokémon
                lePokemon = Pokemon(self.jeu, infoPokemon[0], "PIKACHU", infoPokemon[1], infoPokemon[2], infoPokemon[3],
                                    infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7], infoPokemon[8],
                                    infoPokemon[9], infoPokemon[10], infoPokemon[11],
                                    infoPokemon[12])  # initialisation du pokémon
                lePokemon.setLevelPokemon(niveau)  # Mettre le pokemon au niveau adaptée
                self.jeu.fightP.changerPokemon(lePokemon.getPokemon(),
                                               self.laListePokemon)  # passer les informations à FightPokemon
                self.jeu.ecran_affiche = "fightP"  # Change l'écran d'affichage au fightPokemon
                self.jeu.mettre_a_jour = True

            elif leNb>=6 and leNb < 46 : # si nombre en dessous de 50 alors apparition de rattata
                niveau = random.randint(3, 5) # niveau du pokemon aléatoirement
                infoPokemon = self.bdd.searchPokemon(chenipan.get("nom")) # chercher dans la base de donnée le pokémon
                lePokemon = Pokemon(self.jeu, infoPokemon[0],"CHENIPAN",infoPokemon[1],infoPokemon[2],infoPokemon[3],infoPokemon[4],infoPokemon[5],infoPokemon[6],infoPokemon[7],infoPokemon[8],infoPokemon[9],infoPokemon[10],infoPokemon[11],infoPokemon[12]) # initialisation du pokémon
                lePokemon.setLevelPokemon(niveau) # Mettre le pokemon au niveau adaptée
                self.jeu.fightP.changerPokemon(lePokemon.getPokemon(),self.laListePokemon) # passer les informations à FightPokemon
                self.jeu.ecran_affiche="fightP" # Change l'écran d'affichage au fightPokemon
                self.jeu.mettre_a_jour = True
            elif leNb>=46 and leNb <51:
                niveau = 5
                infoPokemon = self.bdd.searchPokemon(chrysacier.get("nom"))
                lePokemon = Pokemon(self.jeu, infoPokemon[0],"CHRYSACIER", infoPokemon[1], infoPokemon[2], infoPokemon[3],
                                    infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7], infoPokemon[8],
                                    infoPokemon[9], infoPokemon[10], infoPokemon[11],infoPokemon[12])
                lePokemon.setLevelPokemon(niveau)

                self.jeu.fightP.changerPokemon(lePokemon.getPokemon(), self.laListePokemon)  # passer les informations à FightPokemon
                self.jeu.ecran_affiche = "fightP"
                self.jeu.mettre_a_jour = True

            elif leNb >= 51 and leNb<61:
                niveau = random.randint(4, 6)
                infoPokemon = self.bdd.searchPokemon(coconfort.get("nom"))
                lePokemon = Pokemon(self.jeu, infoPokemon[0],"COCONFORT", infoPokemon[1], infoPokemon[2], infoPokemon[3],
                                    infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7], infoPokemon[8],
                                    infoPokemon[9], infoPokemon[10], infoPokemon[11],infoPokemon[12])
                lePokemon.setLevelPokemon(niveau)

                self.jeu.fightP.changerPokemon(lePokemon.getPokemon(), self.laListePokemon)  # passer les informations à FightPokemon
                self.jeu.ecran_affiche = "fightP"
                self.jeu.mettre_a_jour = True

            elif leNb >= 61:
                niveau = random.randint(3, 5)
                infoPokemon = self.bdd.searchPokemon(aspicot.get("nom"))
                lePokemon = Pokemon(self.jeu, infoPokemon[0],"ASPICOT", infoPokemon[1], infoPokemon[2], infoPokemon[3],
                                    infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7], infoPokemon[8],
                                    infoPokemon[9], infoPokemon[10], infoPokemon[11],infoPokemon[12])
                lePokemon.setLevelPokemon(niveau)

                self.jeu.fightP.changerPokemon(lePokemon.getPokemon(), self.laListePokemon)  # passer les informations à FightPokemon
                self.jeu.ecran_affiche = "fightP"
                self.jeu.mettre_a_jour = True
