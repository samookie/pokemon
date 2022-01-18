import pygame.key

from Model.PokemonBDD import PokemonBDD

'''Classe permettant d'afficer les pokémon du joueur'''
class PokemonView:

    def __init__(self, leJeu):
        self.leJeu = leJeu
        self.laBdd = PokemonBDD()
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 15)  # Initialiser la police pour le texte

        self.lesPokemons = []
        self.premierPoke = True
        self.carte = "jeu"
        self.nbrPokeSelecActuellement = 0
        self.passer = True
        self.bougerpoke = False

    '''Méthode pour afficher la liste du joueur'''
    def affichage(self):
        if self.leJeu.mettre_a_jour: #Actions à faire qu'une fois
            self.getPokemons()
            self.leJeu.mettre_a_jour = False

        #Chargement des sprites
        interface = pygame.image.load("Map/Images/poke.png")
        premierPokAct = pygame.transform.scale(pygame.image.load("Map/Images/pokePrincipalAct.png"), (250,170))
        premierPok = pygame.transform.scale(pygame.image.load("Map/Images/pokePrincipalInac.png"), (250, 170))
        pok = pygame.transform.scale(pygame.image.load("Map/Images/pokeInac.png"), (424, 62))
        pokAct = pygame.transform.scale(pygame.image.load("Map/Images/pokeAct.png"), (424, 62))

        self.leJeu.screen.blit(interface, (0, 0)) #Afficher l'interface

        addTxt = 0
        nbrPokeSelec = 0

        #Afficher les pokémon succintement
        for pokemon in self.lesPokemons:

            if self.premierPoke:
                if self.nbrPokeSelecActuellement == 0: #Si le pokémon actuel est sélectionné
                    self.leJeu.screen.blit(premierPokAct, (7, 110))
                else:
                    self.leJeu.screen.blit(premierPok, (7, 110))
                self.leJeu.screen.blit(self.text.render(f"{pokemon[0]}", 1, (0, 0, 0)), (78, 150))
                self.leJeu.screen.blit(self.text.render(f"{pokemon[3]}", 1, (0, 0, 0)), (149, 200))
                self.leJeu.screen.blit(self.text.render(f"{pokemon[4]}", 1, (0, 0, 0)), (206, 245))
                self.premierPoke = False
            else:
                if nbrPokeSelec == self.nbrPokeSelecActuellement: #Si le pokémon actuel est sélectionné
                    self.leJeu.screen.blit(pokAct, (274, 93 + addTxt))
                else:
                    self.leJeu.screen.blit(pok, (274, 93 + addTxt))
                self.leJeu.screen.blit(self.text.render(f"{pokemon[0]}", 1, (0, 0, 0)), (340, 98 + addTxt))
                self.leJeu.screen.blit(self.text.render(f"{pokemon[3]}", 1, (0, 0, 0)), (417, 130 + addTxt))
                self.leJeu.screen.blit(self.text.render(f"{pokemon[4]}", 1, (0, 0, 0)), (588, 130 + addTxt))
                addTxt += 73

            nbrPokeSelec += 1

        self.premierPoke = True

        if self.carte == "jeu": #En fonction de la carte qui à chargé la vue adapter
            self.leJeu.screen.blit(self.text.render(f"Jeu", 1, (0, 0, 0)), (25, 468))
        elif self.carte == "fight":
            self.leJeu.screen.blit(self.text.render(f"Fight", 1, (0, 0, 0)), (25, 468))

        pygame.display.flip()

    '''Méthode pour récupérer les pokémons de la BDD'''
    def getPokemons(self):
        temp = self.laBdd.getPokemonHero()
        self.lesPokemons = []

        for pokemon in temp:
            self.lesPokemons.append(pokemon)

    '''Gestion des touches de la classe'''
    def gestion_touches(self):

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            if self.carte == "jeu":
                self.leJeu.ecran_affiche = "jeu"
                self.leJeu.mettre_a_jour = True
            elif self.carte == "fightP":
                self.leJeu.ecran_affiche = "fightP"
                self.leJeu.mettre_a_jour = True
            elif self.carte == "fightD":
                self.leJeu.ecran_affiche = "fightD"
                self.leJeu.mettre_a_jour = True
        elif pygame.key.get_pressed()[pygame.K_DOWN] and self.passer:
            if self.nbrPokeSelecActuellement < len(self.lesPokemons) - 1:
                self.nbrPokeSelecActuellement += 1
            self.passer = False
        elif pygame.key.get_pressed()[pygame.K_UP] and self.passer:
            if self.nbrPokeSelecActuellement > 0:
                self.nbrPokeSelecActuellement -= 1
            self.passer = False
        elif pygame.key.get_pressed()[pygame.K_RETURN] and self.passer:
            if self.bougerpoke:
                self.bougerpoke = False
            else:
                self.bougerpoke = True
        elif not pygame.key.get_pressed()[pygame.K_DOWN] and not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[pygame.K_RETURN] and not self.passer:
            self.passer = True

    '''Mettre à jour la carte affiché'''
    def update_map(self, map):
        self.carte = map
