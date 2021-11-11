import random

import pygame

class Intro:

    def __init__(self, leJeu):
        self.leJeu = leJeu

        self.txtIntro = ["Bien le bonjour ! Bienvenue dans le monde magique des POKEMON",
                         "Mon nom est CHEN ! Les gens souvent m'appellent le PROF POKEMON"]

        self.txtNum = 0
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 10)  # Initialiser la police pour le texte


        pass

    def affichageTxtProfesseur(self):
        imgProfesseur = pygame.image.load("Map/Images/professeur.png")
        dialogBox = pygame.image.load("Map/Images/dialogBox.png")

        imgProfesseurScale = pygame.transform.scale(imgProfesseur, (171, 273))

        pygame.draw.rect(self.leJeu.screen, (0, 0, 0), pygame.Rect(0, 0, 700, 600))
        self.leJeu.screen.blit(imgProfesseurScale, (random.randint(0, 700), random.randint(0, 600)))
        self.leJeu.screen.blit(dialogBox, (0, 0))
        self.leJeu.screen.blit(self.text.render(self.txtIntro[self.txtNum], True, (0, 0, 0)), (45, 490))

        pygame.display.flip()

    '''Méthode permettant de vérifier la frappe des touches sur cette classe'''
    def gestion_touches(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.txtNum < len(self.txtIntro) - 1:
            self.txtNum = self.txtNum + 1