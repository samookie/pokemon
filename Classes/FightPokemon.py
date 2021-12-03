import pygame

from Classes.Joueur import Joueur
from Model.PokemonBDD import PokemonBDD


class FightPokemon:

    def __init__(self, leJeu, nomPokemon = "", liste_pokemon = []):
        self.leJeu = leJeu #cLasse jeu
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 15) #Initialiser la police pour le texte
        self.bdd = PokemonBDD()
        self.lePokemon = nomPokemon
        self.liste_pokemon = liste_pokemon
        self.txtNum = 0
        self.passer = True


    '''Méthode permettant d'afficher l'écran d'accueil et d'appliquer les modifications dessus'''
    def affichage(self):
        pygame.draw.rect(self.leJeu.screen, (0, 0, 0),pygame.Rect(0, 0, 700, 600))  # Créer un fond noir sur tout l'écran

        fight_img = pygame.image.load("Map/Images/fight.png")
        self.leJeu.screen.blit(fight_img, (0, 0)) #Dessiner l'image de fond

        self.afficher_Pokemon_haut(self.lePokemon)
        self.afficher_Pokemon_bas("pikachu")

        self.afficher_stat_haut()
        self.afficher_stat_bas()

        dialogueBleu = pygame.image.load("Map/Images/fightDia.png")
        self.leJeu.screen.blit(dialogueBleu, (0, 0))  # Dessiner l'image du dialogue bleu

        if self.txtNum == 0:
            self.leJeu.screen.blit(self.text.render(f"Un {self.lePokemon[1]} sauvage apparaît!", True, (255,255,255)), (27, 495))
        elif self.txtNum == 1:
            self.leJeu.screen.blit(self.text.render('PIKACHOUM! GO!', True, (255, 255, 255)), (27, 495))
        elif self.txtNum == 2:
            self.afficher_choix_menu()

        pygame.display.flip()  # MAJ de l'affichage

    '''Méthode permettant de vérifier la frappe des touches sur cette classe'''
    def gestion_touches(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.passer: #Si la touche est espace, que l'on peut encore naviguer dans le dialogue et que la variable passer est à True
            self.txtNum = self.txtNum + 1
            self.passer = False
        elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.passer:
            self.passer = True

    def afficher_Pokemon_bas(self, pokemon):
        pokemonBas = pygame.image.load(f'Map/Images/d_{pokemon}.png')
        pokemonBasScale = pygame.transform.scale(pokemonBas, (200, 200))  # Redimensionner l'image du professeur
        self.leJeu.screen.blit(pokemonBasScale, (100, 287))  # Dessiner l'image du pokémon d'en bas

    def afficher_Pokemon_haut(self, pokemon):
        pokemonHaut = pygame.image.load(f'Map/Images/{pokemon[12]}.png')  # Dessiner l'image du pokémon d'en haut
        pokemonHautScale = pygame.transform.scale(pokemonHaut, (200, 200))  # Redimensionner l'image du professeur
        self.leJeu.screen.blit(pokemonHautScale, (409, 190))

    def changerPokemon(self, pokemon, liste_pokemon):
        self.lePokemon = pokemon
        self.liste_pokemon = liste_pokemon

    def afficher_stat_bas(self):
        statPB = pygame.image.load("Map/Images/statPokemonAlly.png")
        self.leJeu.screen.blit(statPB, (0, 0))  # Dessiner l'image des stats du pokémon du bas
        self.leJeu.screen.blit(self.text.render("PIKATCHOUM", 1, (0, 0, 0)), (445, 374))
        self.leJeu.screen.blit(self.text.render("5", 1, (0, 0, 0)), (642, 374))

    def afficher_stat_haut(self):
        statPH = pygame.image.load("Map/Images/statPokemonEnnemy.png")
        self.leJeu.screen.blit(statPH, (0, 0))  # Dessiner l'image des stats du pokémon du haut
        self.leJeu.screen.blit(self.text.render(str(self.lePokemon[1]), 1, (0, 0, 0)), (58 , 218))
        self.leJeu.screen.blit(self.text.render(str(self.lePokemon[3]), 1, (0, 0, 0)), (246 ,218))

    def afficher_choix_menu(self):
        self.menu_choix()
        self.leJeu.screen.blit(self.text.render("Que dois faire ", True,(255, 255, 255)), (29, 495))
        self.leJeu.screen.blit(self.text.render("PIKACHOUM ?", True, (255, 255, 255)), (29, 520))

    def menu_choix(self):
        menuChoix = pygame.image.load("Map/Images/choixFight.png")
        self.leJeu.screen.blit(menuChoix, (0, 0))
        self.leJeu.screen.blit(self.text.render("ATTAQUE ", True, (0, 0, 0)), (420,494))
        self.leJeu.screen.blit(self.text.render("SAC", True, (0, 0, 0)), (585,494))
        self.leJeu.screen.blit(self.text.render("POKEMON", True, (0, 0, 0)), (420,545))
        self.leJeu.screen.blit(self.text.render("FUITE", True, (0, 0, 0)), (585,545))






