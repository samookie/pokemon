import pygame

class Joueur(pygame.sprite.Sprite):

    def __init__(this, x, y):
        super().__init__() #Initialiser le constructeur parent (Sprite)

        #Varibales
        this.sprite_sheet = pygame.image.load("Map/Images/joueur_fille.png") #Définir l'image à aller chercher
        this.image = this.get_image(0, 0) #Appeler la méthode permettant de découper le sprite sheet
        this.rect = this.image.get_rect() #Récupérer le rectangle de collision de l'image
        this.images = {
            'bas': this.get_image(0, 0),
            'haut': this.get_image(0, 20),
            'gauche': this.get_image(0, 40),
            'droite': this.get_image(0, 60)
        }

        #Correction de l'image
        this.image.set_colorkey([36, 255, 0]) #Supprimer le fond noir de l'image
        this.position = [x, y] #Définir la position de l'image

    '''Méthode permettant de changer l'animation du joueur (Mettre l'image haut, bas, gauche, droite) en fonction du nom définis en paramètre'''
    def changer_animation(this, nom):
        this.image = this.images[nom]
        this.image.set_colorkey([36, 255, 0])

    '''Méthode permettant d'efectuer des actions sur le joueur en foction de la touche appuyé'''
    def gestion_touches(this):
        touche = pygame.key.get_pressed() #Récupérer la touche

        if touche[pygame.K_UP]:
            this.position[1] -= 2
            this.changer_animation('haut')
        elif touche[pygame.K_DOWN]:
            this.position[1] += 2
            this.changer_animation('bas')
        elif touche[pygame.K_LEFT]:
            this.position[0] -= 2
            this.changer_animation('gauche')
        elif touche[pygame.K_RIGHT]:
            this.position[0] += 2
            this.changer_animation('droite')

    '''Méthode permettant de mettre à jour la position du joueur sur la carte'''
    def update(this):
        this.rect.topleft = this.position #Définir la position du rectagle par rapport à la position défini en paramètre

    '''Méthode permettant de couper le sprite sheet à la bonne dimension pour n'afficher que le joueur'''
    def get_image(this, x, y):
        image = pygame.Surface([16, 20]) #Définir la surface de l'image
        image.blit(this.sprite_sheet, (0, 0), (x, y, 16, 20)) #Récupérer du spritesheet une seule image d'action
        return image #Retourner l'image coupé

