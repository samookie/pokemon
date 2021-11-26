import pygame

from Classes.Animation import Animation


class Pnj(Animation):

    def __init__(self, name):
        super().__init__(name) #Initialiser le constructeur parent (Sprite)

        #Varibales
        self.image = self.get_image(0, 0) #Appeler la méthode permettant de découper le sprite sheet
        self.rect = self.image.get_rect() #Récupérer le rectangle de collision de l'image
        self.pieds = pygame.Rect(0, 0, self.rect.width * 0.5, 6)
        self.position = [0, 0]  # Définir la position de l'image
        self.old_position = self.position.copy()

        #Correction de l'image
        self.image.set_colorkey([36, 255, 0]) #Supprimer le fond noir de l'image

    '''Enregistre la dernière position du joueur sur la carte'''
    def ancienne_position(self):
        self.old_position = self.position.copy()

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

