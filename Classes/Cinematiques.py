import pygame.image


class Cinematiques:

    def __init__(self, carte):
        self.carte = carte
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 10)  # Initialiser la police pour le texte
        self.continuer = True
        self.numDialogue = 0
        self.numMaxDialogue = 0
        self.numCine = 1

        self.dialogueMaman = ["Bon...",
                              "Tous les garçons quittent un jour la maison.. C'est la vie !",
                              "Le PROF. Chen te cherche. Il est dans la maison voisine."]

    def affichage(self):
        imgDialogue = pygame.image.load("Map/Images/dialogBox.png")
        self.carte.jeu.screen.blit(imgDialogue, (0, 0))

    def cine1(self):
        self.numCine = 1
        self.numMaxDialogue = len(self.dialogueMaman)
        self.affichage()

        self.carte.jeu.screen.blit(self.text.render(self.dialogueMaman[self.numDialogue], 1, (0, 0, 0)), (45, 500))

    def gestion_touches(self):

        if pygame.key.get_pressed()[pygame.K_SPACE] and self.numDialogue < self.numMaxDialogue - 1 and self.continuer:
            self.numDialogue += 1
            self.continuer = False
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.numDialogue == self.numMaxDialogue - 1 and self.continuer:
            self.carte.bdd.setCurrentCinematique(self.numCine + 1)
            self.carte.enCinematique = False
            self.numMaxDialogue = 0
            self.numDialogue = 0
            self.continuer = True
        elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.continuer:
            self.continuer = True