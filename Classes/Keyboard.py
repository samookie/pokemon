import datetime

import pygame

class KeyboardUser:

    def __init__(self, leJeu, txtInfo):
        self.leJeu = leJeu
        self.txtInfo = txtInfo
        self.inputUser = ""

        self.imgKeyboard = pygame.image.load("Map/Images/keyboard.png")
        self.selectKey = pygame.image.load("Map/Images/keyboardSelec.png")

        self.xSelec = 107
        self.ySelec = 276

        self.secInput = int(datetime.datetime.now().strftime("%S"))
        self.minInput = int(datetime.datetime.now().strftime("%M"))

        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 15)  # Initialiser la police pour le texte

    def affichage(self):

        self.leJeu.screen.blit(self.imgKeyboard, (0, 0))
        self.leJeu.screen.blit(self.text.render(self.txtInfo, True, (255, 255, 255)), (0, 100))
        self.leJeu.screen.blit(self.text.render(self.inputUser, True, (255, 255, 255)), (0, 150))
        self.leJeu.screen.blit(self.selectKey, (self.xSelec, self.ySelec))
        pygame.display.flip()

    def gestionTouches(self):
        if int(datetime.datetime.now().strftime("%S")) > self.secInput or (int(datetime.datetime.now().strftime("%M")) >= self.minInput and int(datetime.datetime.now().strftime("%S")) > self.secInput):
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self.modifPos("bas")
            elif pygame.key.get_pressed()[pygame.K_UP]:
                self.modifPos("haut")
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.modifPos("droite")
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                self.modifPos("gauche")
            elif pygame.key.get_pressed()[pygame.K_RETURN]:
                self.validEntree()

            self.secInput = int(datetime.datetime.now().strftime("%S"))
            self.minInput = int(datetime.datetime.now().strftime("%M"))

    def modifPos(self, direction):
        if direction == "haut":
            if self.ySelec > 276:
                self.ySelec -= 54
        elif direction == "bas":
            if self.ySelec < 438:
                self.ySelec += 54
        elif direction == "gauche":
            if self.xSelec > 107:
                self.xSelec -= 43
        elif direction == "droite":
            if self.xSelec < 536:
                self.xSelec += 43

    def validEntree(self):
        if self.xSelec < 150 and self.ySelec < 330:
            self.inputUser += "A"
        elif self.xSelec < 193 and self.ySelec < 330:
            self.inputUser += "B"
        elif self.xSelec < 236 and self.ySelec < 330:
            self.inputUser += "C"
        elif self.xSelec < 322 and self.ySelec < 330:
            self.inputUser += "D"
        elif self.xSelec < 365 and self.ySelec < 330:
            self.inputUser += "E"
        elif self.xSelec < 408 and self.ySelec < 330:
            self.inputUser += "F"
        elif self.xSelec < 536 and self.ySelec < 330:
            self.inputUser += "."

