import pygame

from Classes.Carte import Carte
from Classes.Home_Screen import Home_Screen
from Classes.Intro import Intro
from Classes.Joueur import Joueur
from Classes.PokemonView import PokemonView
from Classes.Sac import Sac
from Classes.FightPokemon import FightPokemon
from Model.PokemonBDD import PokemonBDD
from Classes.FightDresseur import FightDresseur

pygame.init()

'''Classe jeu gérant le jeu complet'''
class Jeu:
    def __init__(self):

        # créer la fenêtre du jeu

        self.screen = pygame.display.set_mode((700, 600)) #Définir taille écran
        pygame.display.set_caption("Powebmon") #Définir titre fenêtre

        bdd = PokemonBDD()

        #Création de la bDD si erreur
        try:
            bdd.testBDDFonctionnelle()
        except:
            bdd.resetBDD()

    '''Méthode permettant de lancer les bonnes fenêtre au cours du jeu'''
    def lancement(self):

        # Variables
        self.ecran_affiche = "home"
        self.mettre_a_jour = True
        self.dansMenu = False

        jeu = True
        self.carte = Carte(self, Joueur("joueur_fille"))
        clock = pygame.time.Clock()

        # VARS ECRANS
        ecran_accueil = Home_Screen(self)
        intro = Intro(self)
        self.sac = Sac(self)
        self.pokemon_ecran = PokemonView(self)
        self.fightP = FightPokemon(self)
        self.fightD = FightDresseur(self)


        # boucle du jeu
        while jeu:

            if self.ecran_affiche == "home":
                ecran_accueil.afficher_ecran()
                ecran_accueil.gestion_touches()
            elif self.ecran_affiche == "intro":
                intro.affichageTxtProfesseur()
                intro.gestion_touches()
            elif self.ecran_affiche == "jeu":
                self.carte.affichage_carte()
            elif self.ecran_affiche == "sac":
                self.sac.affichage()
                self.sac.gestion_touches()
            elif self.ecran_affiche == "pokemons":
                self.pokemon_ecran.affichage()
                self.pokemon_ecran.gestion_touches()
            elif self.ecran_affiche == "fightP":
                self.fightP.affichage()
                self.fightP.gestion_touches()
            elif self.ecran_affiche == "fightD":
                self.fightD.affichage()
                self.fightD.gestion_touches()
            else:
                pass

            # Récupérer les évènements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jeu = False

            clock.tick(60) # Définir le jeu à 30 FPS

        pygame.quit()