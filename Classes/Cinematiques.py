import pygame.image

from Classes.Pokemon import Pokemon
from Model.PokemonBDD import PokemonBDD


class Cinematiques:

    def __init__(self, carte):
        self.carte = carte
        self.laBdd = PokemonBDD()
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 10)  # Initialiser la police pour le texte
        self.continuer = True
        self.numDialogue = 0
        self.numMaxDialogue = 0
        self.numCine = 1
        self.tournerProf = 0
        self.dansChoixPokemon = False
        self.validationChoixPokemon = False
        self.pokemonChoisis = ""

        self.dialogueMaman = ["Bon...",
                              "Tous les garçons quittent un jour la maison.. C'est la vie !",
                              "Le PROF. Chen te cherche. Il est dans la maison voisine."]

        self.dialogueProfesseur2 = ["Hé, attends ! Ne pars pas",
                                    "C'est très dangereux ! Des pokémons sauvages infestent les hautes herbes !",
                                    "Il te faut un pokémon pour te protéger.. Je sais !",
                                    "Suis-moi !"]

        self.dialogueProfesseur3 = [f"{str(self.laBdd.chargerInfosHero()[1])} ? Heu...",
                                   "Ah, c'est vrai ! Je t'ai dit de venir...",
                                   "Tiens, NT ",
                                   "Il y a trois pokémon ici !",
                                   "Ils sont dans ces poké balls",
                                   "Plus jeune, j'étais sacré DRESSEUR DE POKEMON ! Eh oui",
                                   "Mais à cause de mon âge, je n'en ai gardé que trois!",
                                   "Il y en a un pour toi. Allez ! Choisis-en un !"]

    def affichage(self):
        imgDialogue = pygame.image.load("Map/Images/dialogBox.png")
        self.imgProfesseur = pygame.image.load("Map/Images/pnj_professeur.png")
        self.carte.jeu.screen.blit(imgDialogue, (0, 0))

    def cine1(self):
        self.numCine = 1
        self.numMaxDialogue = len(self.dialogueMaman)
        self.affichage()

        self.carte.jeu.screen.blit(self.text.render(self.dialogueMaman[self.numDialogue], 1, (0, 0, 0)), (45, 500))

    def cine2(self):
        self.numCine = 2
        self.numMaxDialogue = len(self.dialogueProfesseur2)
        self.affichage()

        self.carte.jeu.screen.blit(self.text.render(self.dialogueProfesseur2[self.numDialogue], 1, (0, 0, 0)), (45, 500))

        if self.numDialogue >= 1:
            cropped = pygame.Surface((48, 60))
            image = pygame.transform.scale(self.imgProfesseur, (48, 240))
            image.set_colorkey([36, 255, 0])
            cropped.blit(image, (0, 0), (0, 60, 48, 120))
            self.carte.jeu.screen.blit(pygame.transform.rotate(cropped, self.tournerProf), (239, 356))
            self.tournerProf += 5

    def cine3(self):
        self.numCine = 3
        self.numMaxDialogue = len(self.dialogueProfesseur3)
        self.affichage()

        self.carte.jeu.screen.blit(self.text.render(self.dialogueProfesseur3[self.numDialogue], 1, (0, 0, 0)), (45, 500))

    def cine4(self):
        self.numCine = 4

        if self.dansChoixPokemon:

            if self.carte.joueur.position > [144, 94] and self.carte.joueur.position < [156, 94]:
                self.pokemonChoisis = "bulbizarre"
                pygame.draw.rect(self.carte.jeu.screen, (255, 255, 255, 100), pygame.Rect(50, 400, 600, 150))
                pygame.draw.rect(self.carte.jeu.screen, (0, 0, 0), pygame.Rect(50, 400, 600, 150), 2)
                self.carte.jeu.screen.blit(self.text.render("Voulez vous choisir pokémon Bulbizarre ?", True, (0, 0, 0)), (60, 425))
                self.carte.jeu.screen.blit(pygame.image.load("Map/Images/bulbizarre.png"), (500, 350))
                if self.validationChoixPokemon:
                    self.carte.jeu.screen.blit(self.text.render("> Oui", True, (0, 0, 0)), (60, 450))
                    self.carte.jeu.screen.blit(self.text.render("Non", True, (0, 0, 0)), (60, 475))
                else:
                    self.carte.jeu.screen.blit(self.text.render("Oui", True, (0, 0, 0)), (60, 450))
                    self.carte.jeu.screen.blit(self.text.render("> Non", True, (0, 0, 0)), (60, 475))

            elif self.carte.joueur.position > [156, 94] and self.carte.joueur.position < [172, 94]:
                self.pokemonChoisis = "salameche"
                pygame.draw.rect(self.carte.jeu.screen, (255, 255, 255, 100), pygame.Rect(50, 400, 600, 150))
                pygame.draw.rect(self.carte.jeu.screen, (0, 0, 0), pygame.Rect(50, 400, 600, 150), 2)
                self.carte.jeu.screen.blit(self.text.render("Voulez vous choisir pokémon Salamèche ?", True, (0, 0, 0)), (60, 425))
                self.carte.jeu.screen.blit(pygame.image.load("Map/Images/salamèche.png"), (500, 350))
                if self.validationChoixPokemon:
                    self.carte.jeu.screen.blit(self.text.render("> Oui", True, (0, 0, 0)), (60, 450))
                    self.carte.jeu.screen.blit(self.text.render("Non", True, (0, 0, 0)), (60, 475))
                else:
                    self.carte.jeu.screen.blit(self.text.render("Oui", True, (0, 0, 0)), (60, 450))
                    self.carte.jeu.screen.blit(self.text.render("> Non", True, (0, 0, 0)), (60, 475))

            elif self.carte.joueur.position > [172, 94] and self.carte.joueur.position < [184, 94]:
                self.pokemonChoisis = "carapuce"
                pygame.draw.rect(self.carte.jeu.screen, (255, 255, 255, 100), pygame.Rect(50, 400, 600, 150))
                pygame.draw.rect(self.carte.jeu.screen, (0, 0, 0), pygame.Rect(50, 400, 600, 150), 2)
                self.carte.jeu.screen.blit(self.text.render("Voulez vous choisir pokémon Carapuce ?", True, (0, 0, 0)), (60, 425))
                self.carte.jeu.screen.blit(pygame.image.load("Map/Images/carapuce.png"), (500, 350))
                if self.validationChoixPokemon:
                    self.carte.jeu.screen.blit(self.text.render("> Oui", True, (0, 0, 0)), (60, 450))
                    self.carte.jeu.screen.blit(self.text.render("Non", True, (0, 0, 0)), (60, 475))
                else:
                    self.carte.jeu.screen.blit(self.text.render("Oui", True, (0, 0, 0)), (60, 450))
                    self.carte.jeu.screen.blit(self.text.render("> Non", True, (0, 0, 0)), (60, 475))

            if pygame.key.get_pressed()[pygame.K_RETURN] and self.validationChoixPokemon:
                if self.pokemonChoisis == "bulbizarre":

                    infoPokemon = self.laBdd.searchPokemon("Bulbizarre")  # chercher dans la base de donnée le pokémon
                    lePokemon = Pokemon(self.carte.jeu, infoPokemon[0], "Bulbizarre", infoPokemon[1], infoPokemon[2],
                                        infoPokemon[3], infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7],
                                        infoPokemon[8], infoPokemon[9], infoPokemon[10],
                                        infoPokemon[11],infoPokemon[12])  # initialisation du pokémon
                    lePokemon.setLevelPokemon(5)
                    self.carte.joueur.addPokemon(lePokemon,5)
                    self.laBdd.setCurrentCinematique(5)

                elif self.pokemonChoisis == "salameche":

                    infoPokemon = self.laBdd.searchPokemon("Salamèche")  # chercher dans la base de donnée le pokémon
                    lePokemon = Pokemon(self.carte.jeu, infoPokemon[0], "Salamèche", infoPokemon[1], infoPokemon[2],
                                        infoPokemon[3], infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7],
                                        infoPokemon[8], infoPokemon[9], infoPokemon[10],
                                        infoPokemon[11],infoPokemon[12])  # initialisation du pokémon
                    lePokemon.setLevelPokemon(5)
                    self.carte.joueur.addPokemon(lePokemon,5)
                    self.laBdd.setCurrentCinematique(5)

                elif self.pokemonChoisis == "carapuce":

                    infoPokemon = self.laBdd.searchPokemon("Carapuce")  # chercher dans la base de donnée le pokémon
                    lePokemon = Pokemon(self.carte.jeu, infoPokemon[0], "Carapuce", infoPokemon[1], infoPokemon[2],
                                        infoPokemon[3], infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7],
                                        infoPokemon[8], infoPokemon[9], infoPokemon[10],
                                        infoPokemon[11],infoPokemon[12])  # initialisation du pokémon
                    lePokemon.setLevelPokemon(5)
                    self.carte.joueur.addPokemon(lePokemon,5)
                    self.laBdd.setCurrentCinematique(5)

                #self.carte.jeu.ecran_affiche = "fightP"
                #self.carte.jeu.mettre_a_jour = True

        elif pygame.key.get_pressed()[pygame.K_SPACE]:
            if self.carte.joueur.position > [144, 94] and self.carte.joueur.position < [145, 94]:
                self.dansChoixPokemon = True
            elif self.carte.joueur.position > [156, 94] and self.carte.joueur.position < [157, 94]:
                self.dansChoixPokemon = True
            elif self.carte.joueur.position > [172, 94] and self.carte.joueur.position < [173, 94]:
                self.dansChoixPokemon = True
            else:
                self.carte.enCinematique = False
        else:
            self.carte.enCinematique = False

    def gestion_touches(self):

        if pygame.key.get_pressed()[pygame.K_SPACE] and self.numDialogue < self.numMaxDialogue - 1 and self.continuer:
            self.numDialogue += 1
            self.continuer = False
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.numDialogue == self.numMaxDialogue - 1 and self.numCine == 2 and self.continuer:
            self.carte.bdd.setCurrentCinematique(self.numCine + 1)
            self.carte.enCinematique = False
            self.numMaxDialogue = 0
            self.numDialogue = 0
            self.continuer = True
            self.carte.chargerCarte("laboratoire", "spawn_labo")
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.numDialogue == self.numMaxDialogue - 1 and self.continuer:
            self.carte.bdd.setCurrentCinematique(self.numCine + 1)
            self.carte.enCinematique = False
            self.numMaxDialogue = 0
            self.numDialogue = 0
            self.continuer = True
        elif pygame.key.get_pressed()[pygame.K_UP] and self.numCine == 4:
            self.validationChoixPokemon = True
        elif pygame.key.get_pressed()[pygame.K_DOWN] and self.numCine == 4:
            self.validationChoixPokemon = False
        elif pygame.key.get_pressed()[pygame.K_RETURN] and self.numCine == 4:
            if self.validationChoixPokemon:
                print("Validation")
                self.dansChoixPokemon = False
            else:
                self.dansChoixPokemon = False
        elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.continuer:
            self.continuer = True