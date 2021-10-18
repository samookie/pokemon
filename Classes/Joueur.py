import pygame

class Joueur(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__() #Initialiser le constructeur parent (Sprite)

        #Varibales
        self.sprite_sheet = pygame.image.load("Map/Images/joueur_fille.png") #Définir l'image à aller chercher
        self.image = self.get_image(0, 0) #Appeler la méthode permettant de découper le sprite sheet
        self.rect = self.image.get_rect() #Récupérer le rectangle de collision de l'image
        self.pieds = pygame.Rect(0, 0, self.rect.width * 0.5, 6)
        self.position = [x, y]  # Définir la position de l'image
        self.old_position = self.position.copy()
        self.images = {
            'bas': self.get_image(0, 0),
            'haut': self.get_image(0, 20),
            'gauche': self.get_image(0, 40),
            'droite': self.get_image(0, 60)
        }

        #Correction de l'image
        self.image.set_colorkey([36, 255, 0]) #Supprimer le fond noir de l'image

    '''Enregistre la dernière position du joueur sur la carte'''
    def ancienne_position(self):
        self.old_position = self.position.copy()

    '''Méthode permettant de changer l'animation du joueur (Mettre l'image haut, bas, gauche, droite) en fonction du nom définis en paramètre'''
    def changer_animation(self, nom):
        self.image = self.images[nom]
        self.image.set_colorkey([36, 255, 0])

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


    '''Méthode permettant de couper le sprite sheet à la bonne dimension pour n'afficher que le joueur'''
    def get_image(self, x, y):
        image = pygame.Surface([16, 20]) #Définir la surface de l'image
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 20)) #Récupérer du spritesheet une seule image d'action
        return image #Retourner l'image coupé

