import pygame.key

from Model.PokemonBDD import PokemonBDD

'''Méthode pour le sac du joueur'''
class Sac:

    '''Constructeur de la classe'''
    def __init__(self, leJeu):
        self.leJeu = leJeu
        self.laBdd = PokemonBDD()
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 15)  # Initialiser la police pour le texte

        self.lesObjets = []
        self.selecObj = 0
        self.yTxt = 96
        self.continuer = True
        self.carte ="jeu"

    '''Affichage du sac du joueur'''
    def affichage(self):
        if self.leJeu.mettre_a_jour:
            self.lesObjets = []
            self.recupObjs()
            self.leJeu.mettre_a_jour = False

        imgSac = pygame.image.load("Map/Images/sac.png") #Image à charger

        self.leJeu.screen.blit(imgSac, (0, 0))

        for obj in self.lesObjets: #Afficher tous les objets et mettre en évidence celui sélectionnée
            if self.lesObjets[self.selecObj] == obj:
                self.leJeu.screen.blit(self.text.render(" > " + obj[0] + " x" + str(obj[2]), True, (0, 0, 0)), (284, self.yTxt))
            else:
                self.leJeu.screen.blit(self.text.render(obj[0] + " x" + str(obj[2]), True, (0, 0, 0)), (284, self.yTxt))
            self.yTxt += 50

        self.yTxt = 96 #Distance entre deux affichages en Y

        pygame.display.flip()

    '''Récupréer les objets dans la BDD du joueur'''
    def recupObjs(self):
        tempObj= self.laBdd.getObjSac()

        for obj in tempObj: #Boucler sur tous les objets
            self.lesObjets.append(obj) #Ajouter dans la liste locale

    '''Ajouter un objet dans le sac du joueur (Et dans la BDD)'''
    def addObj(self,qte,desc,image,typeObj):
        self.laBdd.addObjSac(qte, desc, image, typeObj) #Add dansl a BDD

    '''Gestion des touches du SAC du joueur'''
    def gestion_touches(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE] and self.continuer: #ECHAP
            if self.carte == "jeu":
                self.leJeu.ecran_affiche = "jeu"
                self.leJeu.mettre_a_jour = True
            elif self.carte == "fight":
                self.leJeu.ecran_affiche = "fightP"
                self.leJeu.mettre_a_jour = True
        elif pygame.key.get_pressed()[pygame.K_DOWN] and self.continuer: #FLECHE BAS
            if self.selecObj < len(self.lesObjets) - 1:
                self.selecObj += 1
            self.continuer = False
        elif pygame.key.get_pressed()[pygame.K_UP] and self.continuer: #FLECHE HAUT
            if self.selecObj > 0:
                self.selecObj -= 1
            self.continuer = False
        elif pygame.key.get_pressed()[pygame.K_RETURN] and self.continuer:
            objSelec = self.lesObjets[self.selecObj]

            if self.carte == "fight":
                self.leJeu.ecran_affiche = "fightP"
                self.leJeu.mettre_a_jour
                self.laBdd.majNbOjet(objSelec[3], objSelec[2] - 1)
        elif not pygame.key.get_pressed()[pygame.K_ESCAPE] and not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[pygame.K_DOWN] and not self.continuer: #SPAM TOUCHE
            self.continuer = True

    '''MAJ de la carte'''
    def update_map(self, map):
        self.carte = map


