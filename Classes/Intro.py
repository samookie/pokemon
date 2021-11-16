import datetime
import random

import pygame

from Classes.Keyboard import KeyboardUser
from Model.PokemonBDD import PokemonBDD


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
        self.passer = True
        self.ecran = "dialogue"
        self.sexe = "g"
        self.bdd = PokemonBDD()
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 11)  # Initialiser la police pour le texte

        self.clavier = KeyboardUser(self.leJeu, "Heu... C'est quoi ton nom ?")

    def affichageTxtProfesseur(self):
        imgProfesseur = pygame.image.load("Map/Images/professeur.png")
        dialogBox = pygame.image.load("Map/Images/dialogBox.png")

        imgProfesseurScale = pygame.transform.scale(imgProfesseur, (171, 273))

        if self.ecran == "dialogue":
            pygame.draw.rect(self.leJeu.screen, (0, 0, 0), pygame.Rect(0, 0, 700, 600))
            self.leJeu.screen.blit(imgProfesseurScale, (random.randint(0, 700), random.randint(0, 600)))
            self.leJeu.screen.blit(dialogBox, (0, 0))
            self.leJeu.screen.blit(self.text.render(self.txtIntro[self.txtNum], True, (0, 0, 0)), (45, 490))

            if self.txtNum == 8:
                self.clavier.affichage()
                self.clavier.gestionTouches()
                self.nomJoueur = self.clavier.inputUser
            elif self.txtNum == 9:
                self.leJeu.screen.blit(dialogBox, (0, 0))
                self.leJeu.screen.blit(self.text.render(self.nomJoueur + self.txtIntro[self.txtNum], True, (0, 0, 0)), (45, 490))

                # Pouvoir changer de nom si il aime pas du coup je pense qu c'est un do While ou while stv 
                # self.leJeu.screen.blit(self.text.render("Est-tu sûr de t'appeler " + self.nomJoueur + " ?", True, (255, 255, 255)),(45, 200))
                # if self.sexe == "oui":
                #    self.leJeu.screen.blit(self.text.render("> Oui <", True, (255, 255, 255)), (45, 250))
                #    self.leJeu.screen.blit(self.text.render("Non", True, (255, 255, 255)), (45, 270))
                # else:
                #    self.leJeu.screen.blit(self.text.render("Oui", True, (255, 255, 255)), (45, 250))
                #    self.leJeu.screen.blit(self.text.render("> Non <", True, (255, 255, 255)), (45, 270))

            else:
                self.leJeu.screen.blit(self.text.render(self.txtIntro[self.txtNum], True, (0, 0, 0)), (45, 490))
        else:
            pygame.draw.rect(self.leJeu.screen, (0, 0, 0), pygame.Rect(0, 0, 700, 600))
            self.leJeu.screen.blit(self.text.render("Est-tu un garçon ou une fille ?", True, (255, 255, 255)), (45, 200))
            if self.sexe == "g":
                self.leJeu.screen.blit(self.text.render("> Garçon <", True, (255, 255, 255)), (45, 250))
                self.leJeu.screen.blit(self.text.render("Fille", True, (255, 255, 255)), (45, 270))
            else:
                self.leJeu.screen.blit(self.text.render("Garçon", True, (255, 255, 255)), (45, 250))
                self.leJeu.screen.blit(self.text.render("> Fille <", True, (255, 255, 255)), (45, 270))


        pygame.display.flip()

        if self.leJeu.mettre_a_jour: #Si la variable mettre à jour dans la classe jeu est à True
            pygame.mixer.init() #Initialiser le mixeur musique
            self.musique = pygame.mixer.Sound("Map/Musiques/03-Professor Oak.wav" )#Lancer la musique de fond
            self.musique.play()
            self.leJeu.mettre_a_jour = False #Passer la variable à faux

    '''Méthode permettant de vérifier la frappe des touches sur cette classe'''
    def gestion_touches(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.txtNum < len(self.txtIntro) - 1 and self.passer:
            self.txtNum = self.txtNum + 1
            self.passer = False
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.txtNum == len(self.txtIntro) - 1 and self.passer and self.ecran == "dialogue":
            self.ecran = "choix"
            self.passer = False
        elif pygame.key.get_pressed()[pygame.K_UP] and self.passer:
            self.sexe = "g"
            self.passer = False
        elif pygame.key.get_pressed()[pygame.K_DOWN] and self.passer:
            self.sexe = "f"
            self.passer = False
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.txtNum == len(self.txtIntro) - 1 and self.passer and self.ecran == "choix":
            self.bdd.creationPersonnage(self.nomJoueur, self.sexe)
            self.leJeu.ecran_affiche = "jeu"
            self.leJeu.mettre_a_jour = True
            self.musique.fadeout(2000)
        elif not pygame.key.get_pressed()[pygame.K_SPACE] and not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[pygame.K_DOWN]:
            self.passer = True