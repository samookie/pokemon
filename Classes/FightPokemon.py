import pygame

from Classes.Joueur import Joueur
from Model.PokemonBDD import PokemonBDD


class FightPokemon:

    def __init__(self, leJeu, nomPokemon = "", liste_pokemon = ""):
        self.leJeu = leJeu #cLasse jeu
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 15) #Initialiser la police pour le texte
        self.bdd = PokemonBDD()
        self.lePokemon = nomPokemon
        self.liste_pokemon = liste_pokemon


    '''Méthode permettant d'afficher l'écran d'accueil et d'appliquer les modifications dessus'''
    def affichage(self):
        pygame.draw.rect(self.leJeu.screen, (0, 0, 0),pygame.Rect(0, 0, 700, 600))  # Créer un fond noir sur tout l'écran

        fight_img = pygame.image.load("Map/Images/fight.png")
        self.leJeu.screen.blit(fight_img, (0, 0)) #Dessiner l'image de fond

        pokemonBas = pygame.image.load("Map/Images/d_pikachu.png")
        pokemonBasScale = pygame.transform.scale(pokemonBas, (200, 200))  # Redimensionner l'image du professeur
        self.leJeu.screen.blit(pokemonBasScale, (100, 287))  # Dessiner l'image du pokémon d'en bas

        pokemonHaut = pygame.image.load("Map/Images/f_rattata.png") # Dessiner l'image du pokémon d'en haut
        pokemonHautScale = pygame.transform.scale(pokemonHaut, (200, 200))  # Redimensionner l'image du professeur
        self.leJeu.screen.blit(pokemonHautScale, (409, 190))

        statPH = pygame.image.load("Map/Images/statPokemonEnnemy.png")
        self.leJeu.screen.blit(statPH, (0, 0))  # Dessiner l'image des stats du pokémon du haut

        statPB = pygame.image.load("Map/Images/statPokemonAlly.png")
        self.leJeu.screen.blit(statPB, (0, 0))  # Dessiner l'image des stats du pokémon du bas

        dialogueBleu = pygame.image.load("Map/Images/fightDia.png")
        self.leJeu.screen.blit(dialogueBleu, (0, 0))  # Dessiner l'image du dialogue bleu



        pygame.display.flip()  # MAJ de l'affichage

    '''Méthode permettant de vérifier la frappe des touches sur cette classe'''
    def gestion_touches(self):
        pass

    def afficher_Pokemon_bas(self, pokemon):
        lePokemonB = pygame.image.load("Map/Images/fight.png")

        self.leJeu.screen.blit(lePokemonB, (0, 0))  # Dessiner l'image de fond

    def afficher_Pokemon_haut(self, pokemon):
        lePokemonH = pygame.image.load("Map/Images/fight.png")

        self.leJeu.screen.blit(lePokemonH, (0, 0))  # Dessiner l'image de fond

