import datetime
import random

import pygame

from Classes.Keyboard import KeyboardUser


class Intro:

    def __init__(self, leJeu):
        self.leJeu = leJeu

        self.nomJoueur = ""

        self.txtIntro = ["Bien le bonjour ! Bienvenue dans le monde magique des POKEMON",
                         "Mon nom est CHEN ! Les gens souvent m'appellent le PROF POKEMON",
                         "Ce monde est peuplé de créatures du nom de POKEMON",
                         "Humains et Pokémon vivent en parfaite harmonie...",
                         "Certains jouent avec les Pokémons, d'autres font des combats.",
                         "Mais il reste beaucoup à apprendre sur nos amis les Pokémons",
                         "De nombreux mystères planent sur le sujet.",
                         "Et c'est pourquoi j'étudie les Pokémon tous les jours",
                         "Heu... C'est quoi ton nom ?",
                         ", est-tu prêt ?",
                         "Ta quête Pokémon est sur le point de commencer.",
                         "Joies et périls parveront ta route...",
                         "Un monde de rêve, de dangers et de Pokémon t'attend !",
                         "En avant !",
                         "... A plus tard."]

        self.txtNum = 0
        self.heureNext = int(datetime.datetime.now().strftime("%S")) #Récupérer la seconde ou le texte à été affiché
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 11)  # Initialiser la police pour le texte

        self.clavier = KeyboardUser(self.leJeu, "Quel est ton nom ?")

    def affichageTxtProfesseur(self):
        imgProfesseur = pygame.image.load("Map/Images/professeur.png")
        dialogBox = pygame.image.load("Map/Images/dialogBox.png")

        imgProfesseurScale = pygame.transform.scale(imgProfesseur, (171, 273))

        pygame.draw.rect(self.leJeu.screen, (0, 0, 0), pygame.Rect(0, 0, 700, 600))
        self.leJeu.screen.blit(imgProfesseurScale, (random.randint(0, 700), random.randint(0, 600)))
        self.leJeu.screen.blit(dialogBox, (0, 0))
        self.leJeu.screen.blit(self.text.render(self.txtIntro[self.txtNum], True, (0, 0, 0)), (45, 490))

        if self.txtNum == 8:
            self.clavier.affichage()
            self.clavier.gestionTouches()
            self.nomJoueur = self.clavier.inputUser
        elif self.txtNum == 9:
            self.leJeu.screen.blit(self.text.render(self.nomJoueur + self.txtIntro[self.txtNum], True, (0, 0, 0)), (45, 490))
        else:
            self.leJeu.screen.blit(self.text.render(self.txtIntro[self.txtNum], True, (0, 0, 0)), (45, 490))

        pygame.display.flip()

        if self.leJeu.mettre_a_jour: #Si la variable mettre à jour dans la classe jeu est à True
            pygame.mixer.init() #Initialiser le mixeur musique
            self.musique = pygame.mixer.Sound("Map/Musiques/03-Professor Oak.wav" )#Lancer la musique de fond
            self.musique.play()
            self.leJeu.mettre_a_jour = False #Passer la variable à faux

    '''Méthode permettant de vérifier la frappe des touches sur cette classe'''
    def gestion_touches(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.txtNum < len(self.txtIntro) - 1 and (self.heureNext < int(datetime.datetime.now().strftime("%S")) or int(datetime.datetime.now().strftime("%S")) == 0):
            self.txtNum = self.txtNum + 1
            self.heureNext = int(datetime.datetime.now().strftime("%S")) #Redéfinir la seconde ou le texte à été lu
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.txtNum == len(self.txtIntro) - 1:
            self.leJeu.ecran_affiche = "jeu"
            self.leJeu.mettre_a_jour = True
            self.musique.fadeout(2000)