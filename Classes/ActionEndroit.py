import pygame.image

from Classes.Pokemon import Pokemon
from Model.PokemonBDD import PokemonBDD


class ActionEndroit:

    def __init__(self,carte):
        self.laBdd = PokemonBDD()
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 10)  # Initialiser la police pour le texte
        self.continuer = True
        self.carte = carte
        self.numDialogue = 0
        self.numMaxDialogue = 0
        self.choixCentre = False

        self.dialogueCentre = ["Bienvenue dans notre CENTRE POKéMON!",
                              "Je vais m'occuper de vos POKéMON, un instant",
                               "Merci d'avoir attendu.",
                               "Vos PokéMON sont en super forme.",
                               "A bientôt!"]

    def affichage(self):
        imgDialogue = pygame.image.load("Map/Images/dialogBox.png")
        self.carte.jeu.screen.blit(imgDialogue, (0, 0))
        self.carte.jeu.screen.blit(self.text.render(self.dialogueCentre[self.numDialogue], 1, (0, 0, 0)), (45, 500))

    def gestion_touches(self):
        print(self.numDialogue + 1)
        print(len(self.dialogueCentre))

        if pygame.key.get_pressed()[pygame.K_SPACE] and self.continuer:
            if self.numDialogue < len(self.dialogueCentre) - 1:
                self.numDialogue += 1
            else:
                self.carte.auCentre = False
                self.numDialogue = 0
            self.continuer = False
        elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.continuer:
            self.continuer = True
