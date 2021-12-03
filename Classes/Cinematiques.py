import pygame.image

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
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if self.carte.joueur.position > [144, 94] and self.carte.joueur.position < [145, 94]:
                print("poke1")
            elif self.carte.joueur.position > [156, 94] and self.carte.joueur.position < [157, 94]:
                print("poke2")
            elif self.carte.joueur.position > [172, 94] and self.carte.joueur.position < [173, 94]:
                print("poke3")
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
        elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.continuer:
            self.continuer = True