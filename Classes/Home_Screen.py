import pygame

from Classes.Joueur import Joueur
from Model.PokemonBDD import PokemonBDD


class Home_Screen:

    def __init__(self, leJeu):
        self.leJeu = leJeu #CLasse jeu
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 15) #Initialiser la police pour le texte
        self.bdd = PokemonBDD()
        self.nbrSav = self.bdd.getSavExist()[0]

        if self.nbrSav == 0:
            self.curseur = "nouv"  # Variable pour savoir ou le curseur est situé
        else:
            self.curseur = "continuer"  # Variable pour savoir ou le curseur est situé


    '''Méthode permettant d'afficher l'écran d'accueil et d'appliquer les modifications dessus'''
    def afficher_ecran(self):
        home_screen_img = pygame.image.load("Map/Images/home_screen.png")

        self.leJeu.screen.blit(home_screen_img, (0, 0)) #Dessiner l'image de fond

        if self.curseur == "continuer": #En fonction du curseur changer la couleur du texte et ajouter ><
            self.leJeu.screen.blit(self.text.render("> Continuer <", 1, (255, 255, 255)), (285, 375))
            self.leJeu.screen.blit(self.text.render("Nouvelle Partie", 1, (209, 209, 209)), (260, 400))
        elif self.curseur == "nouv" and self.nbrSav == 0:
            self.leJeu.screen.blit(self.text.render("Continuer", 1, (150, 150, 150)), (285, 375))
            self.leJeu.screen.blit(self.text.render("> Nouvelle Partie <", 1, (255, 255, 255)), (260, 400))
        elif self.curseur == "nouv":
            self.leJeu.screen.blit(self.text.render("Continuer", 1, (209, 209, 209)), (285, 375))
            self.leJeu.screen.blit(self.text.render("> Nouvelle Partie <", 1, (255, 255, 255)), (260, 400))

        if self.leJeu.mettre_a_jour: #Si la variable mettre à jour dans la classe jeu est à True
            pygame.mixer.init() #Initialiser le mixeur musique
            self.musique = pygame.mixer.Sound("Map/Musiques/01-Opening.wav" )#Lancer la musique de fond
            self.musique.play(-1)
            self.leJeu.mettre_a_jour = False #Passer la variable à faux
            pygame.display.flip()  # MAJ de l'affichage

    '''Méthode permettant de vérifier la frappe des touches sur cette classe'''
    def gestion_touches(self):
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.curseur = "nouv"
            pygame.display.flip()  # MAJ de l'affichage
        elif pygame.key.get_pressed()[pygame.K_UP] and self.nbrSav != 0:
            self.curseur = "continuer"
            pygame.display.flip()  # MAJ de l'affichagez
        elif pygame.key.get_pressed()[pygame.K_RETURN] and self.curseur == "continuer":
            infos = self.bdd.getInfosChargerSav() #Récupérer les infos de la sauvegarde dans la BDD

            if infos[0] == "g": # Si le sexe est garçon
                joueurTemp = Joueur("joueur_garcon")
            else:  # Si le joueur est fille
                joueurTemp = Joueur("joueur_fille")
            joueurTemp.modifPosition([infos[1], infos[2]]) #Modifier la position du perso pour correspondre à celle de la sauvegarde
            self.leJeu.carte.joueur = joueurTemp #Changer le joueur sur la carte
            self.leJeu.carte.chargerCarteSansSpawn(infos[3]) # Charger la carte pour d'arrivée
            self.leJeu.ecran_affiche = "jeu"
            self.leJeu.mettre_a_jour = True
            self.musique.fadeout(2000)

        elif pygame.key.get_pressed()[pygame.K_RETURN] and self.curseur == "nouv":
            self.bdd.resetBDD()
            self.leJeu.mettre_a_jour = True
            self.leJeu.ecran_affiche = "intro"
            self.musique.fadeout(2000)
