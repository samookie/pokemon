import pygame

class Animation(pygame.sprite.Sprite):

    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"Map/Images/{name}.png")
        self.animation_index = 0 #index permettant de savoir sur quel images d'animation on est
        self.clock = 0
        self.images = {
            'bas': self.get_images(0),
            'haut': self.get_images(20),
            'gauche': self.get_images(40),
            'droite': self.get_images(60)
        }
        self.speed = 2

    def chgSexePerso(self, name):
        if name == "g":
            self.sprite_sheet = pygame.image.load(f"Map/Images/joueur_garcon.png")
        else:
            self.sprite_sheet = pygame.image.load(f"Map/Images/joueur_fille.png")

    def get_image(self, x, y):
        image = pygame.Surface([16, 20])  # Définir la surface de l'image
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 20))  # Récupérer du spritesheet une seule image d'action
        return image  # Retourner l'image coupé

    def get_images(self , y):
        images = []
        for i in range(0 , 3):
            x = i * 16
            image = self.get_image( x, y)
            images.append(image)

        return images

    '''Méthode permettant de changer l'animation du joueur (Mettre l'image haut, bas, gauche, droite) en fonction du nom définis en paramètre'''

    def changer_animation(self, nom):
        self.image = self.images[nom][self.animation_index]
        self.image.set_colorkey([36, 255, 0])
        self.clock += self.speed * 8

        if self.clock >= 100:

            self.animation_index += 1 #passer à l'image suivante

            if self.animation_index >= len(self.images[nom]): # verifier si on arrive à la derniere image
                self.animation_index = 0

            self.clock = 0