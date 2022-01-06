import pygame.key

from Model.PokemonBDD import PokemonBDD


class Sac:

    def __init__(self, leJeu):
        self.leJeu = leJeu
        self.laBdd = PokemonBDD()
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 15)  # Initialiser la police pour le texte

        self.lesObjets = []
        self.selecObj = 0
        self.yTxt = 96
        self.continuer = True
        self.carte ="jeu"

    def affichage(self):
        if self.leJeu.mettre_a_jour:
            self.lesObjets = []
            self.recupObjs()
            self.leJeu.mettre_a_jour = False

        imgSac = pygame.image.load("Map/Images/sac.png")

        self.leJeu.screen.blit(imgSac, (0, 0))

        for obj in self.lesObjets:
            if self.lesObjets[self.selecObj] == obj:
                self.leJeu.screen.blit(self.text.render(" > " + obj[0] + " x" + str(obj[2]), True, (0, 0, 0)), (284, self.yTxt))
            else:
                self.leJeu.screen.blit(self.text.render(obj[0] + " x" + str(obj[2]), True, (0, 0, 0)), (284, self.yTxt))
            self.yTxt += 50

        self.yTxt = 96

        pygame.display.flip()

    def recupObjs(self):
        tempObj= self.laBdd.getObjSac()

        for obj in tempObj:
            self.lesObjets.append(obj)

    def addObj(self,qte,desc,image,typeObj):
        self.laBdd.addObjSac(qte, desc, image, typeObj)

    def gestion_touches(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE] and self.continuer:
            if self.carte == "jeu":
                self.leJeu.ecran_affiche = "jeu"
                self.leJeu.mettre_a_jour = True
            elif self.carte == "fight":
                self.leJeu.ecran_affiche = "fightP"
                self.leJeu.mettre_a_jour = True
        elif pygame.key.get_pressed()[pygame.K_DOWN] and self.continuer:
            if self.selecObj < len(self.lesObjets) - 1:
                self.selecObj += 1
            self.continuer = False
        elif pygame.key.get_pressed()[pygame.K_UP] and self.continuer:
            if self.selecObj > 0:
                self.selecObj -= 1
            self.continuer = False
        elif not pygame.key.get_pressed()[pygame.K_ESCAPE] and not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[pygame.K_DOWN] and not self.continuer:
            self.continuer = True

    def update_map(self, map):
        self.carte = map


