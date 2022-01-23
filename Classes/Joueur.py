import pygame

from Classes.Animation import Animation

from Model.PokemonBDD import PokemonBDD


class Joueur(Animation):

    def __init__(self, name):
        super().__init__(name) #Initialiser le constructeur parent (Sprite)

        #Varibales
        self.image = self.get_image(0, 0) #Appeler la méthode permettant de découper le sprite sheet
        self.rect = self.image.get_rect() #Récupérer le rectangle de collision de l'image
        self.pieds = pygame.Rect(0, 0, self.rect.width * 0.5, 6)
        self.position = [0, 0]  # Définir la position de l'image
        self.old_position = self.position.copy()
        self.bdd = PokemonBDD()

        #Correction de l'image
        self.image.set_colorkey([36, 255, 0]) #Supprimer le fond noir de l'image

        self.liste_pokemon=[] #Liste pokemon

    '''Enregistre la dernière position du joueur sur la carte'''
    def ancienne_position(self):
        self.old_position = self.position.copy()

    '''Méthode permettant d'efectuer des actions sur le joueur en foction de la touche appuyé'''
    def gestion_touches(self):
        touche = pygame.key.get_pressed() #Récupérer la touche

        if touche[pygame.K_UP]:
            self.position[1] -= 2
            self.changer_animation('haut')
        elif touche[pygame.K_DOWN]:
            self.position[1] += 2
            self.changer_animation('bas')
        elif touche[pygame.K_LEFT]:
            self.position[0] -= 2
            self.changer_animation('gauche')
        elif touche[pygame.K_RIGHT]:
            self.position[0] += 2
            self.changer_animation('droite')

    '''Méthode permettant de mettre à jour la position du joueur sur la carte'''
    def update(self):
        self.rect.topleft = self.position #Définir la position du rectagle par rapport à la position défini en paramètre
        self.pieds.midbottom = self.rect.midbottom #Définis la position des pieds

    '''Méthode permettant de remettre le joueur à l'ancienne position'''
    def revenir_en_arriere(self):
        self.position = self.old_position #Remettre le joueur à l'ancienne position
        self.rect.topleft = self.position  # Définir la position du rectagle par rapport à la position défini en paramètre
        self.pieds.midbottom = self.rect.midbottom #Définis la position des pieds

    '''Méthode pour permettre de modifier la position du joueur'''
    def modifPosition(self, pos):
        self.old_position = pos
        self.position = pos

    '''Méthode pour permettre d'avoir la liste de pokémon du joueur '''
    def getLesPokemons(self):
        for poke in self.bdd.getPokemonHero():
            self.liste_pokemon.append(poke)
        return self.liste_pokemon

    '''Méthode pour permettre d'ajouter un pokemon dans la liste'''
    def addPokemon(self, pokemon, niv):
        self.bdd.ajouterPokemonJoueur(pokemon, niv)

    def addPoke(self, pokemon, niv):
        self.bdd.ajouterPokemon(pokemon,niv)

