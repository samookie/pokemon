import random
import pygame

from Classes.Joueur import Joueur
from Classes.Keyboard import KeyboardUser
from Model.PokemonBDD import PokemonBDD

'''Classe Intro permettant de réaliser l"intro du jeu'''
class Intro:

    '''Classe Intro permettant de réaliser l"intro du jeu'''
    def __init__(self, leJeu):
        self.leJeu = leJeu #Classe le jeu

        self.nomJoueur = "" #Nom du joueur défini par l'utilisateur

        self.txtIntro = ["Bien le bonjour ! Bienvenue dans le monde magique des POKEMON",
                         "Mon nom est CHEN ! Les gens souvent m'appellent le PROF POKEMON",
                         "Ce monde est peuplé de créatures du nom de POKEMON",
                         "Humains et Pokémon vivent en parfaite harmonie...",
                         "Certains jouent avec les Pokémons, d'autres font des combats.",
                         "Mais il reste beaucoup à apprendre sur nos amis les Pokémons",
                         "De nombreux mystères planent sur le sujet.",
                         "Et c'est pourquoi j'étudie les Pokémon tous les jours",
                         "Heu... C'est quoi ton nom ?",
                         " ça te conviens ?",
                         ", est-tu prêt ?",
                         "Ta quête Pokémon est sur le point de commencer.",
                         "Joies et périls parveront ta route...",
                         "Un monde de rêve, de dangers et de Pokémon t'attend !",
                         "En avant !",
                         "... A plus tard."]


        self.txtNum = 0 #Ligne du dialogue actuel
        self.passer = True #Variable pour savoir si on peut passer au texte suivant
        self.ecran = "dialogue" #Ecran affiché actuellement (Dialogue ou choix)
        self.sexe = "g" #Sex du personnage
        self.okNom = False #Savoir si le nom défini par l'utilisateur est validé
        self.bdd = PokemonBDD() #Modèle

        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 11)  # Initialiser la police pour le texte

        self.clavier = KeyboardUser(self.leJeu, "Heu... C'est quoi ton nom ?") #Instancier la classe keyboard pour afficher le clavier à l'utiliser

    '''Méthode permettant d'afficher le dialogue d'intro'''
    def affichageTxtProfesseur(self):
        imgProfesseur = pygame.image.load("Map/Images/professeur.png") #Image du professeur
        dialogBox = pygame.image.load("Map/Images/dialogBox.png") #Image de la dialogBox

        imgProfesseurScale = pygame.transform.scale(imgProfesseur, (171, 273)) #Redimensionner l'image du professeur

        if self.ecran == "dialogue": #Si l'écran actuel est dialogue
            pygame.draw.rect(self.leJeu.screen, (0, 0, 0), pygame.Rect(0, 0, 700, 600)) #Créer un fond noir sur tout l'écran
            self.leJeu.screen.blit(imgProfesseurScale, (random.randint(0, 700), random.randint(0, 600))) #Insérer le professeur
            self.leJeu.screen.blit(dialogBox, (0, 0)) #Insérer la dialogBox
            self.leJeu.screen.blit(self.text.render(self.txtIntro[self.txtNum], True, (0, 0, 0)), (45, 490)) #Afficher le texte du dialogue

            if self.txtNum == 10 and not self.okNom: #Si on demande la validation du nom défini et que la réponse est non remttre le dialogue à la position 8
                self.txtNum = 8

            if self.txtNum == 8: #Si le dialogue est sur la demande du nom du perso afficher le clavier
                self.clavier.affichage()
                self.clavier.gestionTouches()
                self.nomJoueur = self.clavier.inputUser
            elif self.txtNum == 9: #Si le dialogue est sur l'affichage de la confirmation du nom du perso
                self.leJeu.screen.blit(dialogBox, (0, 0))
                self.leJeu.screen.blit(self.text.render(self.nomJoueur + self.txtIntro[self.txtNum], True, (0, 0, 0)), (45, 490))

                if self.okNom == True: #Si la confirmation du nom est à Oui
                    self.leJeu.screen.blit(self.text.render("> Oui <", True, (255, 255, 255)), (45, 250))
                    self.leJeu.screen.blit(self.text.render("Non", True, (255, 255, 255)), (45, 270))
                else: #Si la confirmation du nom est à Non
                    self.leJeu.screen.blit(self.text.render("Oui", True, (255, 255, 255)), (45, 250))
                    self.leJeu.screen.blit(self.text.render("> Non <", True, (255, 255, 255)), (45, 270))
            elif self.txtNum == 10: #Si le dialogue est sur l'affichage du pret avec nom perso
                self.leJeu.screen.blit(dialogBox, (0, 0))
                self.leJeu.screen.blit(self.text.render(self.nomJoueur + self.txtIntro[self.txtNum], True, (0, 0, 0)), (45, 490))
            else: #Sinon si c'est un dialogue sans conditions particulières

                self.leJeu.screen.blit(self.text.render(self.txtIntro[self.txtNum], True, (0, 0, 0)), (45, 490))
        else: #Si l'écran est l'écran de choix
            pygame.draw.rect(self.leJeu.screen, (0, 0, 0), pygame.Rect(0, 0, 700, 600))
            self.leJeu.screen.blit(self.text.render("Est-tu un garçon ou une fille ?", True, (255, 255, 255)), (45, 200))
            if self.sexe == "g": #Si le sexe choisis est garçon
                self.leJeu.screen.blit(self.text.render("> Garçon <", True, (255, 255, 255)), (45, 250))
                self.leJeu.screen.blit(self.text.render("Fille", True, (255, 255, 255)), (45, 270))
            else: #Si le sexe choisis est fille
                self.leJeu.screen.blit(self.text.render("Garçon", True, (255, 255, 255)), (45, 250))
                self.leJeu.screen.blit(self.text.render("> Fille <", True, (255, 255, 255)), (45, 270))

        pygame.display.flip() #Mettre à jour l'afficghage

        if self.leJeu.mettre_a_jour: #Si la variable mettre à jour dans la classe jeu est à True
            pygame.mixer.init() #Initialiser le mixeur musique
            self.musique = pygame.mixer.Sound("Map/Musiques/03-Professor Oak.wav" )#Lancer la musique de fond
            self.musique.play(-1)
            self.leJeu.mettre_a_jour = False #Passer la variable à faux

    '''Méthode permettant de vérifier la frappe des touches sur cette classe'''
    def gestion_touches(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.txtNum < len(self.txtIntro) - 1 and self.passer: #Si la touche est espace, que l'on peut encore naviguer dans le dialogue et que la variable passer est à True
            self.txtNum = self.txtNum + 1
            self.passer = False
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.txtNum == len(self.txtIntro) - 1 and self.passer and self.ecran == "dialogue": #Si la touche est espace, que l'on est à la fin du dialogue
            self.ecran = "choix"
            self.passer = False
        elif pygame.key.get_pressed()[pygame.K_UP] and self.passer: #Si la touche est flèche haut
            if self.ecran == "choix": #Si l'écran actuel est choix
                self.sexe = "g"
                self.passer = False
            else: #Si l'écran actuel est dialogue
                self.okNom = True
                self.passer = False
        elif pygame.key.get_pressed()[pygame.K_DOWN] and self.passer: #Si la touche est flèche bas
            if self.ecran == "choix": #Si l'écran actuel est choix
                self.sexe = "f"
                self.passer = False
            else: #Si l'écran actuel est dialogue
                self.okNom = False
                self.passer = False
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.txtNum == len(self.txtIntro) - 1 and self.passer and self.ecran == "choix": #Si la touche espace est appuyé, que l'on est à la fin du dialogue et que on est sur l'écran choix
            self.bdd.creationPersonnage(self.nomJoueur, self.sexe)  #Stocker le sexe du personnage dans la BDD
            if self.sexe == "g": # Si le sexe est garçon
                self.leJeu.carte.joueur = Joueur("joueur_garcon")
            else:  # Si le joueur est fille
                self.leJeu.carte.joueur = Joueur("joueur_fille")
            self.leJeu.carte.chargerCarte("maisonH2", "spawn_etage_maisonH") # Charger la carte pour d'arrivée
            self.leJeu.ecran_affiche = "jeu"
            self.leJeu.mettre_a_jour = True
            self.musique.fadeout(2000)
        elif not pygame.key.get_pressed()[pygame.K_SPACE] and not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[pygame.K_DOWN]: #Si aucune touche n'est enfoncé
            self.passer = True