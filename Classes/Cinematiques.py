import pygame.image

from Classes.Pokemon import Pokemon
from Model.PokemonBDD import PokemonBDD

'''Classe contenant les cinématiques du début de jeu'''
class Cinematiques:

    '''Constructeur de la classe cinématique'''
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
        self.infoHero = ""

        self.dialogueMaman = ["Bon...",
                              "Tous les garçons quittent un jour la maison.. C'est la vie !",
                              "Le PROF. Chen te cherche. Il est dans la maison voisine."]

        self.dialogueProfesseur2 = ["Hé, attends ! Ne pars pas",
                                    "C'est très dangereux ! Des pokémons sauvages infestent les hautes herbes !",
                                    "Il te faut un pokémon pour te protéger.. Je sais !",
                                    "Suis-moi !"]

        self.dialogueProfesseur3 = [f"{self.infoHero} ? Heu...",
                                   "Ah, c'est vrai ! Je t'ai dit de venir...",
                                   "Tiens, NT ",
                                   "Il y a trois pokémon ici !",
                                   "Ils sont dans ces poké balls",
                                   "Plus jeune, j'étais sacré DRESSEUR DE POKEMON ! Eh oui",
                                   "Mais à cause de mon âge, je n'en ai gardé que trois!",
                                   "Il y en a un pour toi. Allez ! Choisis-en un !"]

    '''Méthode permettant d'afficher la dialogueBox et l'image du professeur à l'écran'''
    def affichage(self):
        imgDialogue = pygame.image.load("Map/Images/dialogBox.png")
        self.imgProfesseur = pygame.image.load("Map/Images/pnj_professeur.png")
        self.carte.jeu.screen.blit(imgDialogue, (0, 0))

    '''Méthode de déclenchement de la cinématique 1'''
    def cine1(self):
        self.numCine = 1 #Définir le numéro de la cinématique
        self.numMaxDialogue = len(self.dialogueMaman) #Récupérer le nombre de ligne de dialogue
        self.affichage() #Afficher la box diaglogue

        self.carte.jeu.screen.blit(self.text.render(self.dialogueMaman[self.numDialogue], 1, (0, 0, 0)), (45, 500)) #Afficher le texte correspondant au dialogue

    '''Méthode de déclenchement de la cinématique 2'''
    def cine2(self):
        self.numCine = 2
        self.numMaxDialogue = len(self.dialogueProfesseur2)
        self.affichage()

        self.carte.jeu.screen.blit(self.text.render(self.dialogueProfesseur2[self.numDialogue], 1, (0, 0, 0)), (45, 500))

        if self.numDialogue >= 1: #Si nous sommes dans un endroit précis du dialogue afficher ces éléments en plus
            cropped = pygame.Surface((48, 60))
            image = pygame.transform.scale(self.imgProfesseur, (48, 240)) #Afficher image prof
            image.set_colorkey([36, 255, 0])
            cropped.blit(image, (0, 0), (0, 60, 48, 120))
            self.carte.jeu.screen.blit(pygame.transform.rotate(cropped, self.tournerProf), (239, 356))
            self.tournerProf += 5

    '''Méthode de décelenchement de la cinématique 3'''
    def cine3(self):
        self.infoHero = str(self.laBdd.chargerInfosHero()[1]) #Récupérer les infos du héro
        self.numCine = 3
        self.numMaxDialogue = len(self.dialogueProfesseur3)
        self.affichage()

        self.carte.jeu.screen.blit(self.text.render(self.dialogueProfesseur3[self.numDialogue], 1, (0, 0, 0)), (45, 500))

    '''Méthode pour déclenchement de la cinématique 4'''
    def cine4(self):
        self.numCine = 4

        if self.dansChoixPokemon: #Si nous sommes dans la zone choix Pokémon

            if self.carte.joueur.position > [144, 94] and self.carte.joueur.position < [156, 94]: #Si le jour est entre ces deux coordonnées lui proposer le pokémon bulbizarre
                self.pokemonChoisis = "bulbizarre"
                pygame.draw.rect(self.carte.jeu.screen, (255, 255, 255, 100), pygame.Rect(50, 400, 600, 150))
                pygame.draw.rect(self.carte.jeu.screen, (0, 0, 0), pygame.Rect(50, 400, 600, 150), 2)
                self.carte.jeu.screen.blit(self.text.render("Voulez vous choisir pokémon Bulbizarre ?", True, (0, 0, 0)), (60, 425))
                self.carte.jeu.screen.blit(pygame.image.load("Map/Images/bulbizarre.png"), (500, 350))
                if self.validationChoixPokemon: #Si nous attendons la validation du joueur, en fonction de sa réponse afficher oui ou non
                    self.carte.jeu.screen.blit(self.text.render("> Oui", True, (0, 0, 0)), (60, 450))
                    self.carte.jeu.screen.blit(self.text.render("Non", True, (0, 0, 0)), (60, 475))
                else:
                    self.carte.jeu.screen.blit(self.text.render("Oui", True, (0, 0, 0)), (60, 450))
                    self.carte.jeu.screen.blit(self.text.render("> Non", True, (0, 0, 0)), (60, 475))

            elif self.carte.joueur.position > [156, 94] and self.carte.joueur.position < [172, 94]: #Si le jour est entre ces deux coordonnées lui proposer le pokémon salamèche
                self.pokemonChoisis = "salameche"
                pygame.draw.rect(self.carte.jeu.screen, (255, 255, 255, 100), pygame.Rect(50, 400, 600, 150))
                pygame.draw.rect(self.carte.jeu.screen, (0, 0, 0), pygame.Rect(50, 400, 600, 150), 2)
                self.carte.jeu.screen.blit(self.text.render("Voulez vous choisir pokémon Salamèche ?", True, (0, 0, 0)), (60, 425))
                self.carte.jeu.screen.blit(pygame.image.load("Map/Images/salamèche.png"), (500, 350))
                if self.validationChoixPokemon: #Si nous attendons la validation du joueur, en fonction de sa réponse afficher oui ou non
                    self.carte.jeu.screen.blit(self.text.render("> Oui", True, (0, 0, 0)), (60, 450))
                    self.carte.jeu.screen.blit(self.text.render("Non", True, (0, 0, 0)), (60, 475))
                else:
                    self.carte.jeu.screen.blit(self.text.render("Oui", True, (0, 0, 0)), (60, 450))
                    self.carte.jeu.screen.blit(self.text.render("> Non", True, (0, 0, 0)), (60, 475))

            elif self.carte.joueur.position > [172, 94] and self.carte.joueur.position < [184, 94]: #Si le jour est entre ces deux coordonnées lui proposer le pokémon carapuce
                self.pokemonChoisis = "carapuce"
                pygame.draw.rect(self.carte.jeu.screen, (255, 255, 255, 100), pygame.Rect(50, 400, 600, 150))
                pygame.draw.rect(self.carte.jeu.screen, (0, 0, 0), pygame.Rect(50, 400, 600, 150), 2)
                self.carte.jeu.screen.blit(self.text.render("Voulez vous choisir pokémon Carapuce ?", True, (0, 0, 0)), (60, 425))
                self.carte.jeu.screen.blit(pygame.image.load("Map/Images/carapuce.png"), (500, 350))
                if self.validationChoixPokemon: #Si nous attendons la validation du joueur, en fonction de sa réponse afficher oui ou non
                    self.carte.jeu.screen.blit(self.text.render("> Oui", True, (0, 0, 0)), (60, 450))
                    self.carte.jeu.screen.blit(self.text.render("Non", True, (0, 0, 0)), (60, 475))
                else:
                    self.carte.jeu.screen.blit(self.text.render("Oui", True, (0, 0, 0)), (60, 450))
                    self.carte.jeu.screen.blit(self.text.render("> Non", True, (0, 0, 0)), (60, 475))

            if pygame.key.get_pressed()[pygame.K_RETURN] and self.validationChoixPokemon: #Si la touche entrée est appuyé et que le joueur est dans l'attente du choix
                if self.pokemonChoisis == "bulbizarre": #Si c'est bulbizarre le créer dans la BDD pour le joueur

                    infoPokemon = self.laBdd.searchPokemon("Bulbizarre")  # chercher dans la base de donnée le pokémon
                    lePokemon = Pokemon(self.carte.jeu, infoPokemon[0], "Bulbizarre", infoPokemon[1], infoPokemon[2],
                                        infoPokemon[3], infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7],
                                        infoPokemon[8], infoPokemon[9], infoPokemon[10],
                                        infoPokemon[11],infoPokemon[12])  # initialisation du pokémon
                    lePokemon.setLevelPokemon(5)
                    autre = self.laBdd.searchPokemon("Pikachu")
                    lautre = Pokemon(self.carte.jeu, autre[0], "Pikachu", autre[1], autre[2],
                                        autre[3], autre[4], autre[5], autre[6], autre[7],
                                        autre[8], autre[9], autre[10],
                                        autre[11], autre[12])  # initialisation du pokémon
                    lautre.setLevelPokemon(2)
                    self.carte.joueur.addPokemon(lePokemon,5)
                    self.carte.joueur.addPokemon(lautre,2)
                    self.laBdd.setCurrentCinematique(5)
                    self.laBdd.addObjSac(5, "pokeball", "image", "pokeball")
                    self.laBdd.addObjSac(2, "potion", "image", "potion")

                elif self.pokemonChoisis == "salameche": #Si c'est salamèche

                    infoPokemon = self.laBdd.searchPokemon("Salamèche")  # chercher dans la base de donnée le pokémon
                    lePokemon = Pokemon(self.carte.jeu, infoPokemon[0], "Salamèche", infoPokemon[1], infoPokemon[2],
                                        infoPokemon[3], infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7],
                                        infoPokemon[8], infoPokemon[9], infoPokemon[10],
                                        infoPokemon[11],infoPokemon[12])  # initialisation du pokémon
                    lePokemon.setLevelPokemon(5)

                    autre = self.laBdd.searchPokemon("Pikachu")
                    lautre = Pokemon(self.carte.jeu, autre[0], "Pikachu", autre[1], autre[2],
                                     autre[3], autre[4], autre[5], autre[6], autre[7],
                                     autre[8], autre[9], autre[10],
                                     autre[11], autre[12])  # initialisation du pokémon
                    lautre.setLevelPokemon(2)
                    self.carte.joueur.addPokemon(lePokemon,5)
                    self.carte.joueur.addPokemon(lautre, 2)
                    self.laBdd.setCurrentCinematique(5)
                    self.laBdd.addObjSac(5, "pokeball", "image", "pokeball")
                    self.laBdd.addObjSac(2, "potion", "image", "potion")

                elif self.pokemonChoisis == "carapuce": #Si c'est carapuce

                    infoPokemon = self.laBdd.searchPokemon("Carapuce")  # chercher dans la base de donnée le pokémon
                    lePokemon = Pokemon(self.carte.jeu, infoPokemon[0], "Carapuce", infoPokemon[1], infoPokemon[2],
                                        infoPokemon[3], infoPokemon[4], infoPokemon[5], infoPokemon[6], infoPokemon[7],
                                        infoPokemon[8], infoPokemon[9], infoPokemon[10],
                                        infoPokemon[11],infoPokemon[12])  # initialisation du pokémon
                    lePokemon.setLevelPokemon(5)

                    autre = self.laBdd.searchPokemon("Pikachu")
                    lautre = Pokemon(self.carte.jeu, autre[0], "Pikachu", autre[1], autre[2],
                                     autre[3], autre[4], autre[5], autre[6], autre[7],
                                     autre[8], autre[9], autre[10],
                                     autre[11], autre[12])  # initialisation du pokémon
                    lautre.setLevelPokemon(2)
                    self.carte.joueur.addPokemon(lePokemon,5)
                    self.carte.joueur.addPokemon(lautre, 2)
                    self.laBdd.setCurrentCinematique(5)
                    self.laBdd.addObjSac(5, "pokeball", "image", "pokeball")
                    self.laBdd.addObjSac(2, "potion", "image", "potion")

                #self.carte.jeu.ecran_affiche = "fightP"
                #self.carte.jeu.mettre_a_jour = True

        elif pygame.key.get_pressed()[pygame.K_SPACE]: #Sinon, si seulement le touche ESPACE est appuyé
            if self.carte.joueur.position > [144, 94] and self.carte.joueur.position < [145, 94]: #Si le joueur est entre ces coordonnées le passer en choix pokémon
                self.dansChoixPokemon = True
            elif self.carte.joueur.position > [156, 94] and self.carte.joueur.position < [157, 94]:  #Si le joueur est entre ces coordonnées le passer en choix pokémon
                self.dansChoixPokemon = True
            elif self.carte.joueur.position > [172, 94] and self.carte.joueur.position < [173, 94]:  #Si le joueur est entre ces coordonnées le passer en choix pokémon
                self.dansChoixPokemon = True
            else: #Sinon passer enCinématique à False
                self.carte.enCinematique = False
        else: #Si la touche ESPACE n'est pas enfoncé passer enCinématique à False
            self.carte.enCinematique = False

    '''Méthode pour gérer les touches de la cinématique'''
    def gestion_touches(self):

        if pygame.key.get_pressed()[pygame.K_SPACE] and self.numDialogue < self.numMaxDialogue - 1 and self.continuer: #ESPACE pour avancer le dialogue
            self.numDialogue += 1
            self.continuer = False
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.numDialogue == self.numMaxDialogue - 1 and self.numCine == 2 and self.continuer: #ESPACE pour avancer le dialogue si nous somme dans la cinématique 2
            self.carte.bdd.setCurrentCinematique(self.numCine + 1)
            self.carte.enCinematique = False
            self.numMaxDialogue = 0
            self.numDialogue = 0
            self.continuer = True
            self.carte.chargerCarte("laboratoire", "spawn_labo")
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.numDialogue == self.numMaxDialogue - 1 and self.continuer: #ESPACE à la fin du dialogue
            self.carte.bdd.setCurrentCinematique(self.numCine + 1)
            self.carte.enCinematique = False
            self.numMaxDialogue = 0
            self.numDialogue = 0
            self.continuer = True
        elif pygame.key.get_pressed()[pygame.K_UP] and self.numCine == 4: #Touche HAUT pour cinématique 4
            self.validationChoixPokemon = True
        elif pygame.key.get_pressed()[pygame.K_DOWN] and self.numCine == 4: #Touche BAS pour cinématique 4
            self.validationChoixPokemon = False
        elif pygame.key.get_pressed()[pygame.K_RETURN] and self.numCine == 4: #Touche ENTREE pour cinématique 4
            if self.validationChoixPokemon: #Si choix pokémon
                self.dansChoixPokemon = False
            else:
                self.dansChoixPokemon = False
        elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.continuer: #Sinon pour éviter spam touche attendre pour remttre à True
            self.continuer = True