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

        self.tableauTp = {}

    '''Méthode permettant de charger une carte spécifique'''
    def chargerCarte(self, nomCarte, spawn):
        self.tmx_data = pytmx.util_pygame.load_pygame(f"Map/{nomCarte}.tmx")
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.jeu.screen.get_size())
        self.map_layer.zoom = 3

        self.get_collisions(nomCarte) # prendre toutes les collisions de la map
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)
        self.group.add(self.joueur)
        self.joueur.position = self.getCoordonnee(spawn) # changer les coordonnées du joueurs par celui du spown
        self.tps() # chargement des entrées


    """ Méthode permettant de récupérer les coordonnées du spawn actuelle (récupéré dans la méthodes getCollision) """
    def getCoordonnee(self, spawn):
        result =[0,0]
        for obj in self.spawn:
            if obj.name == spawn:
                result = [obj.x , obj.y] # coordonnée x y du spawn

        return result



    def tps(self):
        # Maison du héro METTRE LES CONDITIONS
        """self.descendre_maisonH = self.tmx_data.get_object_by_name('descendre_maisonH')  # descendre les escaliers maison du héro
        self.tpDescendre_maisonH = pygame.Rect(self.descendre_maisonH.x, self.descendre_maisonH.y,self.descendre_maisonH.width, self.descendre_maisonH.height)

        self.monter_maisonH = self.tmx_data.get_object_by_name('monter_maisonH')  # monter les escaliers maison du héro
        self.tpMonter_maisonH = pygame.Rect(self.monter_maisonH.x, self.monter_maisonH.y, self.monter_maisonH.width,self.monter_maisonH.height)

        self.sortie_maisonH = self.tmx_data.get_object_by_name('sortie_maisonH')  # sortir de la maison du héro
        self.tpSortie_maisonH = pygame.Rect(self.sortie_maisonH.x, self.sortie_maisonH.y, self.sortie_maisonH.width,self.sortie_maisonH.height)"""

        self.entree_maisonH = self.tmx_data.get_object_by_name('entree_maisonH')  # entrer dans la maison du héro
        self.tpEntree_maisonH = pygame.Rect(self.entree_maisonH.x, self.entree_maisonH.y, self.entree_maisonH.width,self.entree_maisonH.height)


    def get_collisions(self, nomCarte):
        self.collision = []
        self.entree = []
        self.spawn = []

        for obj in pytmx.util_pygame.load_pygame(f"Map/{nomCarte}.tmx").objects:
            if obj.type == "collision":
                self.collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "entree": # Récupération de toutes les entrées de la map actuelle
                self.entree.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "spawn": # Récupération de tous les spawns de la map actuelle
                self.spawn.append(obj)


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

        # vérifier l'entré dans la maison METTRE LES CONDITIONS
        if self.joueur.pieds.colliderect(self.tpEntree_maisonH):
            self.chargerCarte('maisonH','entree_maisonH')


        for sprite in self.group.sprites():  # Récupérer les sprites du groupe
            if sprite.pieds.collidelist(self.collision) > -1:  # Si le sprite pied est dans la zone de collision
                sprite.revenir_en_arriere()  # Faire revenir le sprite (Donc ici l'image du joueur) en arrière

    def majSexePerso(self):
        print(self.bdd.getSexePersonnage())
        self.joueur.chgSexePerso(self.bdd.getSexePersonnage())
