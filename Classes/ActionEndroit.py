import pygame.image

from Classes.Pokemon import Pokemon
from Model.PokemonBDD import PokemonBDD


class ActionEndroit:

    def __init__(self,carte):
        self.laBdd = PokemonBDD()
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 10)  # Initialiser la police pour le texte
        self.continuer = True
        self.carte = carte
        self.numDialogue = 0
        self.numMaxDialogue = 0
        self.choixCentre = False
        self.choix = "oui"

        self.dialogueCentre = ["Bienvenue dans notre CENTRE POKéMON!",
                              "Voulez-vous que je m'occupe de vos POKéMON?",
                              "OK, je prends vos POKéMON un instant.",
                               "Merci d'avoir attendu.",
                               "Vos PokéMON sont en super forme.",
                               "A bientôt!"]

    def affichage(self):
        imgDialogue = pygame.image.load("Map/Images/dialogBox.png")
        self.carte.jeu.screen.blit(imgDialogue, (0, 0))
        self.carte.jeu.screen.blit(self.text.render(self.dialogueCentre[self.numDialogue], 1, (0, 0, 0)), (45, 500))
    def gestion_touches(self):
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.choix= "oui"
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                pokemons = self.carte.laListePokemon
                for poke in pokemons:
                    poke.soignerPokemon()
                self.choixCentre = False

        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            self.choix= "non"
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.choixCentre = False

        elif pygame.key.get_pressed()[pygame.K_RETURN]:
            self.choixCentre= False

    def dialogue(self):
        if self.choixCentre:
            pygame.draw.rect(self.carte.jeu.screen, (255, 255, 255, 100), pygame.Rect(50, 400, 600, 150))
            pygame.draw.rect(self.carte.jeu.screen, (0, 0, 0), pygame.Rect(50, 400, 600, 150), 2)
            self.carte.jeu.screen.blit(self.text.render("Voulez vous soigner vos pokémon ?", True, (0, 0, 0)),(60, 425))
            if self.choix =="oui":
                self.carte.jeu.screen.blit(self.text.render("> Oui", True, (0, 0, 0)), (60, 450))
                self.carte.jeu.screen.blit(self.text.render("Non", True, (0, 0, 0)), (60, 475))
            else:
                self.carte.jeu.screen.blit(self.text.render("Oui", True, (0, 0, 0)), (60, 450))
                self.carte.jeu.screen.blit(self.text.render("> Non", True, (0, 0, 0)), (60, 475))
