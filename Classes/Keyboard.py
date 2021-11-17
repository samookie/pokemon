import datetime

import pygame

class KeyboardUser:

    '''Classe Keyboard permettant d'afficher un clavier pour permettre à l'utilisateur d'entrer des données'''
    def __init__(self, leJeu, txtInfo):
        self.leJeu = leJeu #La classe jeu
        self.txtInfo = txtInfo #Le texte d'info affiché à l'utilisateur
        self.inputUser = "" #Ce que l'utilisateur à entré

        self.imgKeyboard = pygame.image.load("Map/Images/keyboard.png") #Image du clavier
        self.selectKey = pygame.image.load("Map/Images/keyboardSelec.png") #Image du rectangle indiquant la lettre sélectionné

        self.xSelec = 107 #Cordonnée x de base
        self.ySelec = 276 #Cordonée y de base

        self.passer = True #Variable pour savoir si on peut valider l'entrée

        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 15)  # Initialiser la police pour le texte

    '''Méthode permettant d'afficher les éléments'''
    def affichage(self):

        self.leJeu.screen.blit(self.imgKeyboard, (0, 0)) #Afficher le clavier
        self.leJeu.screen.blit(self.text.render(self.txtInfo, True, (255, 255, 255)), (0, 100)) #Afficher le texte d'info
        self.leJeu.screen.blit(self.text.render(self.inputUser, True, (255, 255, 255)), (0, 150)) #Afficher l'entrée de l'utilisateur
        self.leJeu.screen.blit(self.selectKey, (self.xSelec, self.ySelec)) #Afficher le carée de sélection de la lettre
        pygame.display.flip() #MAJ affichage

    '''Méthode permettant de gérer les touches sur cet écran'''
    def gestionTouches(self):
        if self.passer: #Si la variable passer est à True
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self.modifPos("bas")
                self.passer = False
            elif pygame.key.get_pressed()[pygame.K_UP]:
                self.modifPos("haut")
                self.passer = False
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.modifPos("droite")
                self.passer = False
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                self.modifPos("gauche")
                self.passer = False
            elif pygame.key.get_pressed()[pygame.K_RETURN]:
                self.validEntree()
                self.passer = False
            elif pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                self.supprCrac()
                self.passer = False
        elif not pygame.key.get_pressed()[pygame.K_DOWN] and not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[pygame.K_RIGHT] and not pygame.key.get_pressed()[pygame.K_LEFT] and not pygame.key.get_pressed()[pygame.K_RETURN] and not pygame.key.get_pressed()[pygame.K_BACKSPACE]: #Si aucune touche n'est enfoncé
            self.passer = True

    '''Méthode permettant de supprimer le dernier caractère de l'enrtée utilisateur'''
    def supprCrac(self):
        self.inputUser = self.inputUser[:-1] #Supprimer le dernier caractère de la chaine

    '''Méthode permettant de bouger le carée de sélection de lettre'''
    def modifPos(self, direction):
        if direction == "haut": #Si la modification de la position est haut
            if self.ySelec > 276:
                self.ySelec -= 54
        elif direction == "bas":  #Si la modification de la position est bas
            if self.ySelec < 438:
                self.ySelec += 54
        elif direction == "gauche":  #Si la modification de la position est gauche
            if self.xSelec > 107:
                self.xSelec -= 55
        elif direction == "droite":  #Si la modification de la position est droite
            if self.xSelec < 492:
                self.xSelec += 55

    '''Méthode permettant d'insérer la lettre sélectionné par l'utilisateur'''
    def validEntree(self):
        if self.xSelec < 162 and self.ySelec < 330:
            self.inputUser += "A"
        elif self.xSelec < 217 and self.ySelec < 330:
            self.inputUser += "B"
        elif self.xSelec < 272 and self.ySelec < 330:
            self.inputUser += "C"
        elif self.xSelec < 327 and self.ySelec < 330:
            self.inputUser += "D"
        elif self.xSelec < 382 and self.ySelec < 330:
            self.inputUser += "E"
        elif self.xSelec < 437 and self.ySelec < 330:
            self.inputUser += "F"
        elif self.xSelec < 547 and self.ySelec < 330:
            self.inputUser += "."
        elif self.xSelec < 162 and self.ySelec < 384:
            self.inputUser += "G"
        elif self.xSelec < 217 and self.ySelec < 384:
            self.inputUser += "H"
        elif self.xSelec < 272 and self.ySelec < 384:
            self.inputUser += "I"
        elif self.xSelec < 327 and self.ySelec < 384:
            self.inputUser += "J"
        elif self.xSelec < 382 and self.ySelec < 384:
            self.inputUser += "K"
        elif self.xSelec < 437 and self.ySelec < 384:
            self.inputUser += "L"
        elif self.xSelec < 547 and self.ySelec < 384:
            self.inputUser += ","
        elif self.xSelec < 162 and self.ySelec < 438:
            self.inputUser += "M"
        elif self.xSelec < 217 and self.ySelec < 438:
            self.inputUser += "N"
        elif self.xSelec < 272 and self.ySelec < 438:
            self.inputUser += "O"
        elif self.xSelec < 327 and self.ySelec < 438:
            self.inputUser += "P"
        elif self.xSelec < 382 and self.ySelec < 438:
            self.inputUser += "Q"
        elif self.xSelec < 437 and self.ySelec < 438:
            self.inputUser += "R"
        elif self.xSelec < 547 and self.ySelec < 438:
            self.inputUser += "S"
        elif self.xSelec < 162 and self.ySelec < 492:
            self.inputUser += "T"
        elif self.xSelec < 217 and self.ySelec < 492:
            self.inputUser += "U"
        elif self.xSelec < 272 and self.ySelec < 492:
            self.inputUser += "V"
        elif self.xSelec < 327 and self.ySelec < 492:
            self.inputUser += "W"
        elif self.xSelec < 382 and self.ySelec < 492:
            self.inputUser += "X"
        elif self.xSelec < 437 and self.ySelec < 492:
            self.inputUser += "Y"
        elif self.xSelec < 547 and self.ySelec < 492:
            self.inputUser += "Z"

