import pygame.key

from Model.PokemonBDD import PokemonBDD


class PokemonView:

    def __init__(self, leJeu):
        self.leJeu = leJeu
        self.laBdd = PokemonBDD()

        self.lesPokemons = []
        self.premierPoke = True

    def affichage(self):
        if self.leJeu.mettre_a_jour:
            self.getPokemons()
            self.leJeu.mettre_a_jour = False

        interface = pygame.image.load("Map/Images/poke.png")
        premierPok = pygame.image.load("Map/Images/pokePrincipalAct.png")
        pok = pygame.image.load("Map/Images/pokeInac.png")

        self.leJeu.screen.blit(interface, (0, 0))

        for pokemon in self.lesPokemons:

            if self.premierPoke:
                self.leJeu.screen.blit(premierPok, (7, 121))

        pygame.display.flip()

    def getPokemons(self):
        temp = self.laBdd.getPokemonHero()

        for pokemon in temp:
            self.lesPokemons.append(pokemon)

    def gestion_touches(self):

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.leJeu.ecran_affiche = "jeu"
            self.leJeu.mettre_a_jour = True