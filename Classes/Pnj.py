import pygame

from Classes.Animation import Animation


class Pnj():

    def __init__(self, name, x, y, orientation="bas"):
        self.sprite_sheet = pygame.image.load(f"Map/Images/{name}.png")

        #Variables
        self.image = self.get_image(0, 0) #Appeler la méthode permettant de découper le sprite sheet
        self.position = [x, y]  # Définir la position de l'image
        #Correction de l'image
        self.image.set_colorkey([36, 255, 0]) #Supprimer le fond noir de l'image

        self.images = {
            'bas': self.get_image(0,0),
            'haut': self.get_image(0,20),
            'gauche': self.get_image(0,40),
            'droite': self.get_image(0,60)
        }
        self.orientation = orientation

    def imagePNJ(self):

        return self.images[self.orientation]

    def get_image(self, x, y):
        image = pygame.Surface([16, 20])  # Définir la surface de l'image
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 20))  # Récupérer du spritesheet une seule image d'action
        return image  # Retourner l'image coupé