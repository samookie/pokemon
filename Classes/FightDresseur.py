import pygame
import random

from Classes.Joueur import Joueur
from Model.PokemonBDD import PokemonBDD


class FightDresseur:

    def __init__(self, leJeu, liste_ennemie = [], liste_pokemon = []):
        '''
        Constructeur permettant d'initialisier la clasee FightPokemon qui est seulement utilisé contre les pokémons rencontré dans les hautes herbes
        :param leJeu: la variable qui continent le jeu
        :param nomPokemon: le nom du pokémon ennemi
        :param liste_pokemon: la liste pokémon du héro
        '''
        self.nomEnnemie = ""
        self.leJeu = leJeu #cLasse jeu
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 15) #Initialiser la police pour le texte
        self.bdd = PokemonBDD() #variable de la bdd
        self.liste_ennemie = liste_ennemie # le pokémon ennemie
        self.liste_pokemon = liste_pokemon # la liste des pokémons de l'allié
        self.alliePokemon = 0 # le compteur des pokémons de l'allié
        self.ennemiePokemon = 0 # Le compteur des pokémons de l'ennemie
        self.txtNum = 0 # le numéro d'orde des dialogues
        self.passer = True # varier pour savoir si on peut passer les dialogues
        self.suivant = True # variable pour savoir si on peut apsser les dialogues
        self.choix = "Attaque" #gestion des choix
        self.a = [[1, 0], [0, 0]] #tableau pour la gestion des choix du combat
        self.choixAtt = "att1" # variable permettant de savoir quel attaque on a choisi
        self.actuellement = "txtIntro" # variable permettant de savoir dans quel situaltion on se trouve dans l'algorithme
        self.dialogueBleu = pygame.image.load("Map/Images/fightDia.png") # image du dialogue bleue
        self.attaqueOne = True # passer à true quand on attaque
        self.attaqueUneFois = True # attaque permmetant d'attaquer qu'une fois
        self.attaque1 = True # attaque permettant de faire la première attaque
        self.attaque2 = False # variable permettatn de faire la seconde attaque
        self.attA = 0 # variable permettant d'afficher le nombre auquel appartient le dialogue de l'attaque allié
        self.attE = 0 # variable permettant d'afficher le nombre auquel appartient le dialogue de l'attaque ennemi


    '''Méthode permettant d'afficher l'écran d'accueil et d'appliquer les modifications dessus'''
    def affichage(self):
        '''
        Fonction permettant d'afficher les contenus dans la fenêtre
        :return:
        '''
        self.att_ennemy = self.bdd.liste_attaque_pokemon(self.liste_ennemie[self.ennemiePokemon].nomPokemon) #initialise le tableau de l'attaque de l'ennemi
        self.att_allier = self.bdd.liste_attaque_pokemon(self.liste_pokemon[self.alliePokemon].nomPokemon)  # Tableau contenant le nom de l'attaque, l'attaque, et le type de l'attaque du pokémon allié
        pygame.draw.rect(self.leJeu.screen, (0, 0, 0),pygame.Rect(0, 0, 700, 600))  # Créer un fond noir sur tout l'écran

        self.fight_img = pygame.image.load("Map/Images/fight.png") #image du fond de fight
        self.leJeu.screen.blit(self.fight_img, (0, 0)) #Dessiner l'image de fond

        self.afficher_Pokemon_haut(self.liste_ennemie[self.ennemiePokemon].image) #fonction qui permet d'afficher le pokémon ennemi
        self.afficher_Pokemon_bas(self.liste_pokemon[self.alliePokemon].nomPokemon) # fonction qui permet d'afficher le pokémon allié

        self.afficher_stat_haut() # fonction permettanant d'afficher les stats du pokémon ennemi
        self.afficher_stat_bas() # fonction permettant d'affficher les stats de la statup

        self.afficher_bar_vie_haut() # fonction permettanant d'afficher la barre de vie du pokémon ennemi
        self.afficher_bar_vie_bas() # fonction permettanant d'afficher la barre de vie du pokémon allié
        self.bdd.getPokemonHero() # permettant d'avoir les pokémon de l'allié
        if self.actuellement == "txtIntro": # si on se trouve actuellement dans l'intro
            self.leJeu.screen.blit(self.dialogueBleu, (0, 0))  # Dessiner l'image du dialogue bleu
            if self.txtNum == 0: # dialogue 1
                self.leJeu.screen.blit(self.text.render(f"Un {self.liste_ennemie[self.ennemiePokemon].nomPokemon} sauvage apparaît!", True, (255,255,255)), (27, 495))
            elif self.txtNum == 1: # dialogue 2
                self.leJeu.screen.blit(self.text.render(f"{self.liste_pokemon[self.alliePokemon].nomPokemon}! GO!", True, (255, 255, 255)), (27, 495))
            elif self.txtNum == 2: # dialogue 3
                self.actuellement = "choixMenu" #basuler en choixMenu permet de savoir quand passe directement dans le choixMenu
        elif self.actuellement == "choixMenu": # Si on se retrouve dans le choix menu alors on affiche le menu
            self.afficher_choix_menu()
        elif self.actuellement == "choixAttaque": # Si l'on se retrouve dans le choix attaque alors on affiche les attaques
            self.choix_attaque()
        elif self.actuellement == "attaqueEnCours": # Si l'on se retouve dans l'attaque en cours alors on active la fonction attaque
            self.leJeu.screen.blit(self.dialogueBleu, (0, 0))  # Dessiner l'image du dialogue bleu
            self.attaque() # Fonction attaque permettant de faire les 2 attaques (allié, ennemi)
        elif self.actuellement == "ennemieMort": # Si l'on se retrouve avec l'ennemi mort alors on affiche le message de mortet on quitte le combat on donne aussi les récompenses
            self.leJeu.screen.blit(self.dialogueBleu, (0, 0)) # Dessiner l'image du dialogue bleu
            self.ennemieMort() # Fonction ou l'ennemi meurt
            print(len(self.liste_ennemie), self.ennemiePokemon)
            # Faire la fonction qui xp le pokémon
        elif self.actuellement == "allieMort": # Si l'on se retouve avec l'allié mort alors on affiche le message et on quitte
            self.leJeu.screen.blit(self.dialogueBleu, (0, 0)) # Dessiner l'image du dialogue bleu
            self.allieMort() # Fonction ou l'allié meurt
        elif self.actuellement == "tousMort":
            self.leJeu.screen.blit(self.dialogueBleu, (0,0))
            self.tousMort()

        if self.leJeu.mettre_a_jour: # Si le jeu est à jour
            self.actuellement = "txtIntro" # Donc revenir à l'intro
            self.choix = "Attaque" # remettre le choix à attaque
            self.choixAtt = "att1" # remettre l'attaque à l'attaque 1
            pygame.mixer.init()  # Initialiser le mixeur musique
            self.musique = pygame.mixer.Sound("Map/Musiques/07-Wild Pokemon Battle.wav")  # Lancer la musique de fond
            self.musique.play(-1)
            self.leJeu.mettre_a_jour = False
        pygame.display.flip()  # MAJ de l'affichage

    def gestion_touches(self):
        '''Méthode permettant de vérifier la frappe des touches sur cette classe'''

        if self.actuellement == "txtIntro": # Si l'on se retrouve aux texte d'intro avant le menu :
            if pygame.key.get_pressed()[pygame.K_SPACE] and self.passer and self.suivant: #Si la touche est espace, que l'on peut encore naviguer dans le dialogue et que la variable passer est à True
                self.txtNum = self.txtNum + 1 # on passe au dialogue suivant
                self.passer = False
            elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.passer:
                self.passer = True
        elif self.actuellement == "choixMenu": # Si l'on se retrouve dans le menu
            self.algorithm_choix() # Alors activer algorithm_choix() qui  permet de se déplacer dans les choix
            self.gestion_touches_choix() # Alors activer gestion_touches_choix() qui  permet de se déplacer dans les choix
        elif self.actuellement == "choixAttaque": # Si l'on est sur les choix de l'attaque
            self.algorithm_attaque() # Alors activer la fonction qui permet de savoir ou on se trouve dans les choix
            self.gestion_touches_choix_attaque() # Alors activer la fonction qui permet de se déplacer
        elif self.actuellement == "attaqueEnCours": # Si l'on est en plein dans le combats après avoir choisi l'attaque
            self.gestion_touches_en_attaque() # gestion de l'ordre de l'attaque
        elif self.actuellement == "ennemieMort":
            self.gestion_touche_mort()
        elif self.actuellement == "allieMort":
            self.gestion_touche_mort()
        elif self.actuellement == "tousMort":
            self.gestion_touche_mort()


    def gestion_touches_choix(self):
        '''Fonction permettant de naviguer dans le menu et par rapport à ton choix faire une action'''
        if self.choix == "Attaque" and pygame.key.get_pressed()[pygame.K_SPACE] and self.passer: #Si il choisi l'option attaque il se retrouve dans l'attaque
            self.actuellement = "choixAttaque" # actuellement se change en choixAttaque ce qui permet de changer la vue
            self.passer = False

        elif self.choix == "Sac" and pygame.key.get_pressed()[pygame.K_SPACE] and self.passer: #Si il choisi Sac il se retrouve dans la vue du sac
            self.leJeu.ecran_affiche = "sac" # Le jeu affiche la classe du Sac et donc la vue du sac
            self.leJeu.mettre_a_jour = True # Pour mettre à jour la vue de la fenêtre complète
            self.musique.fadeout(2000)
            self.txtNum = 2 #Si il reviens il reviendra dans la vue avec le dialogue 2
            self.leJeu.sac.carte = "fightD" #Faire comprendre que l'on se trouve toujours dans le combat
            self.passer = False

        elif self.choix == "Pokemon" and pygame.key.get_pressed()[pygame.K_SPACE] and self.passer: # Si il choisi Pokemon il se retrouve dans la vue du choix de pokemon
            self.leJeu.ecran_affiche = "pokemons" # le jeu affiche la classe PokemonView
            self.leJeu.mettre_a_jour = True # Pour mettre à jour la vue de la fênetre complète
            self.musique.fadeout(2000)
            self.txtNum = 2 # Si il revient il reviendra dans la vue avec le dialogue 2
            self.leJeu.pokemon_ecran.carte = "fightD" #Faire comprendre que l'on se trouve toujours dans le combat
            self.passer = False

        elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.passer:
            self.passer = True

    def gestion_touches_choix_attaque(self):
        '''Fonction qui permet de passer de l'attaque à attaque en cours'''
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.passer:
            self.actuellement = "attaqueEnCours"
            self.passer = False
            self.attaqueOne = True
        elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.passer:
            self.passer = True

    def gestion_touche_mort(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.passer and self.actuellement == "ennemieMort":
            self.interdireZone()
            for poke in self.liste_ennemie:
                self.xpPokemon() # faire gagner de l'xp au pokemon
                self.bdd.gagnerArgent(25) # gagner de l'argent
            self.passer = False
            self.leJeu.ecran_affiche = "jeu"  # le jeu affiche la classe Carte
            self.leJeu.mettre_a_jour = True  # Pour mettre à jour la vue de la fênetre complète
            self.musique.fadeout(2000)
            self.txtNum = 0  # Si il revient il reviendra dans la première partie du dialogue
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.passer and self.actuellement == "allieMort":
            self.interdireZone()
            self.passer = False
            self.leJeu.ecran_affiche = "jeu"  # le jeu affiche la classe Carte
            self.leJeu.mettre_a_jour = True  # Pour mettre à jour la vue de la fênetre complète
            self.musique.fadeout(2000)
            self.txtNum = 0  # Si il revient il reviendra dans la première partie du dialogue
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.passer and self.actuellement == "tousMort":
            self.interdireZone()
            self.passer = False
            self.leJeu.ecran_affiche = "jeu"  # le jeu affiche la classe Carte
            self.leJeu.mettre_a_jour = True  # Pour mettre à jour la vue de la fênetre complète
            self.musique.fadeout(2000)
            self.txtNum = 0  # Si il revient il reviendra dans la première partie du dialogue
        elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.passer:
            self.passer = True

    def gestion_touches_en_attaque(self):
        '''Fonction permettant de gérer la partie attaque et combat (lequel attaque en premier)'''
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.passer and self.attaque1: #Si l'attaque1 est faite

            self.passer = False
            self.attaque1 = False
            self.attaque2 = True
            self.attaqueUneFois = True
            self.attaqueOne = True
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.passer and not self.attaque1 and self.attaque2 and not self.attaqueUneFois:# Si l'attaque1 et L'attaque2 viennent de se terminer

            self.passer = False
            self.attaque2 = False
            self.attaqueUneFois = False
            self.attaqueOne = True
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.passer and not self.attaque1 and not self.attaque2 and not self.attaqueUneFois: #Si l'attaque1 et l'attaque 2 sont passées

            self.actuellement = "choixMenu"
            self.passer = False
            self.attaque1 = True
            self.attaque2 = True
            self.attaqueUneFois = True
            self.attaqueOne = True
        elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.passer:
            self.passer = True

################################## Affichage ###################################

    def afficher_Pokemon_bas(self, pokemon):
        '''
        Fonction qui permet d'afficher le pokémon d'en bas
        :param pokemon: nom du pokémon
        '''
        pokemonBas = pygame.image.load(f'Map/Images/d_{pokemon}.png')
        pokemonBasScale = pygame.transform.scale(pokemonBas, (200, 200))  # Redimensionner l'image du professeur
        self.leJeu.screen.blit(pokemonBasScale, (100, 310))  # Dessiner l'image du pokémon d'en bas

    def afficher_Pokemon_haut(self, pokemon):
        '''
        Fonction qui permet d'afficher le pokémon d'en bas
        :param pokemon: le nom du pokémon
        '''
        pokemonHaut = pygame.image.load(f'Map/Images/f_{pokemon}.png')  # Dessiner l'image du pokémon d'en haut
        pokemonHautScale = pygame.transform.scale(pokemonHaut, (200, 200))  # Redimensionner l'image du professeur
        self.leJeu.screen.blit(pokemonHautScale, (409, 190))

    def changerPokemon(self, liste_ennemie, liste_pokemon):
        '''
        Fonction qui permet de changer le pokémon ennemie et la liste pokémon du héro
        :param pokemon: le pokémon ennemie en mode objet
        :param liste_pokemon: la liste du héro
        '''
        self.liste_ennemie = liste_ennemie
        self.liste_pokemon = liste_pokemon

    def afficher_bar_vie_bas(self):
        '''Fonction qui permet d'afficher la barre de vie du pokémon d'en bas (allié)'''
        calcule = (self.liste_pokemon[self.alliePokemon].hpActu * 100) / self.liste_pokemon[self.alliePokemon].hp #Fait le calcule de la vie un produit en crois permettant de s'adapter au dessin de la barre de vie
        total = calcule * 128 / 100
        pygame.draw.rect(self.leJeu.screen,(0,255,0),pygame.Rect((526,407),(total,8)))

    def afficher_bar_vie_haut(self):
        '''Fonction qui permet d'afficher la barre de vie du pokémon d'en haut (ennemie)'''
        calcule = (self.liste_ennemie[self.ennemiePokemon].hpActu * 100) / self.liste_ennemie[self.ennemiePokemon].hp #Fait le calcule de la vie un produit en crois permettant de s'adapter au dessin de la barre de vie
        total = calcule * 120 / 100
        pygame.draw.rect(self.leJeu.screen,(0,255,0),pygame.Rect((135 ,251),(total,8)))


    def calculeVie(self, attaque, pokemon):
        if self.attaqueOne:
            if pokemon == self.liste_ennemie[self.ennemiePokemon].nomPokemon:

                self.liste_pokemon[self.alliePokemon].hpActu = self.liste_pokemon[self.alliePokemon].hpActu - attaque
                self.attaqueOne = False
            else:
                self.liste_ennemie[self.ennemiePokemon].hpActu = self.liste_ennemie[self.ennemiePokemon].hpActu - attaque
                self.attaqueOne = False

    def afficher_stat_bas(self):
        statPB = pygame.image.load("Map/Images/statPokemonAlly.png")
        self.leJeu.screen.blit(statPB, (0, 0))  # Dessiner l'image des stats du pokémon du bas
        self.leJeu.screen.blit(self.text.render(self.liste_pokemon[self.alliePokemon].nomPokemon, 1, (0, 0, 0)), (445, 374))
        self.leJeu.screen.blit(self.text.render(f"{self.liste_pokemon[self.alliePokemon].niveau}", 1, (0, 0, 0)), (642, 374))

    def afficher_stat_haut(self):
        statPH = pygame.image.load("Map/Images/statPokemonEnnemy.png")
        self.leJeu.screen.blit(statPH, (0, 0))  # Dessiner l'image des stats du pokémon du haut
        self.leJeu.screen.blit(self.text.render(self.liste_ennemie[self.ennemiePokemon].nomPokemon, 1, (0, 0, 0)), (58 , 218))
        self.leJeu.screen.blit(self.text.render(f"{self.liste_ennemie[self.ennemiePokemon].niveau}", 1, (0, 0, 0)), (246 ,218))

    def afficher_choix_menu(self):
        self.menu_choix()
        self.leJeu.screen.blit(self.text.render("Que dois faire ", True,(255, 255, 255)), (29, 495))
        self.leJeu.screen.blit(self.text.render(f"{self.liste_pokemon[self.alliePokemon].nomPokemon} ?", True, (255, 255, 255)), (29, 520))

    def menu_choix(self):
        menuChoix = pygame.image.load("Map/Images/choixFight.png")
        self.leJeu.screen.blit(menuChoix, (0, 0))
        if self.choix == "Attaque":
            self.leJeu.screen.blit(self.text.render(">ATTAQUE ", True, (0, 0, 0)), (380, 494))
            self.leJeu.screen.blit(self.text.render("SAC", True, (0, 0, 0)), (585, 494))
            self.leJeu.screen.blit(self.text.render("POKEMON", True, (0, 0, 0)), (380, 545))

        elif self.choix == "Sac":
            self.leJeu.screen.blit(self.text.render("ATTAQUE ", True, (0, 0, 0)), (380, 494))
            self.leJeu.screen.blit(self.text.render(">SAC", True, (0, 0, 0)), (585, 494))
            self.leJeu.screen.blit(self.text.render("POKEMON", True, (0, 0, 0)), (380, 545))

        elif self.choix == "Pokemon":
            self.leJeu.screen.blit(self.text.render("ATTAQUE ", True, (0, 0, 0)), (380, 494))
            self.leJeu.screen.blit(self.text.render("SAC", True, (0, 0, 0)), (585, 494))
            self.leJeu.screen.blit(self.text.render(">POKEMON", True, (0, 0, 0)), (380, 545))

        elif self.choix == "Fuite":
            self.leJeu.screen.blit(self.text.render("ATTAQUE ", True, (0, 0, 0)), (380, 494))
            self.leJeu.screen.blit(self.text.render("SAC", True, (0, 0, 0)), (585, 494))
            self.leJeu.screen.blit(self.text.render("POKEMON", True, (0, 0, 0)), (380, 545))


    def algorithm_choix(self):
        if self.a[0][0] == 1 and pygame.key.get_pressed()[pygame.K_RIGHT]:  # attaque pour passer à sac
            self.a[0][0] = 0
            self.a[0][1] = 1
            self.choix ="Sac"

        elif self.a[0][0] == 1 and pygame.key.get_pressed()[pygame.K_DOWN]:  # attaque pour passer à pokemon
            self.a[0][0] = 0
            self.a[1][0] = 1
            self.choix = "Pokemon"

        elif self.a[0][1] == 1 and pygame.key.get_pressed()[pygame.K_LEFT]:  # sac pour passer à attaque
            self.a[0][1] = 0
            self.a[0][0] = 1
            self.choix = "Attaque"

        elif self.a[1][1] == 1 and pygame.key.get_pressed()[pygame.K_UP]:  # fuite pour passer à sac
            self.a[1][1] = 0
            self.a[0][1] = 1
            self.choix = "Sac"

        elif self.a[1][1] == 1 and pygame.key.get_pressed()[pygame.K_LEFT]:  # fuite pour passer à pokemon
            self.a[1][1] = 0
            self.a[1][0] = 1
            self.choix = "Pokemon"

        elif self.a[1][0] == 1 and pygame.key.get_pressed()[pygame.K_UP]:  # pokemon pour passer à attaque
            self.a[1][0] = 0
            self.a[0][0] = 1
            self.choix = "Attaque"


    def algorithm_attaque(self):
        if self.a[0][0] == 1 and pygame.key.get_pressed()[pygame.K_RIGHT]:  # attaque 1 pour passer à l'attaque 2
            self.a[0][0] = 0
            self.a[0][1] = 1
            self.choixAtt ="att2"

        elif self.a[0][0] == 1 and pygame.key.get_pressed()[pygame.K_DOWN]:  # attaque1 pour passer à l'attaque3
            self.a[0][0] = 0
            self.a[1][0] = 1
            if self.liste_pokemon[self.alliePokemon].niveau >= 7:
                self.choixAtt = "att3"

        elif self.a[0][1] == 1 and pygame.key.get_pressed()[pygame.K_DOWN]:  # l'attaque2 pour passer à l'attaque4
            self.a[0][1] = 0
            self.a[1][1] = 1
            if self.liste_pokemon[self.alliePokemon].niveau >= 14:
                self.choixAtt = "att4"

        elif self.a[0][1] == 1 and pygame.key.get_pressed()[pygame.K_LEFT]:  # l'attaque2 pour passer à l'attaque1
            self.a[0][1] = 0
            self.a[0][0] = 1
            self.choixAtt = "att1"

        elif self.a[1][1] == 1 and pygame.key.get_pressed()[pygame.K_UP]:  # l'attaque4 pour passer à l'attaque2
            self.a[1][1] = 0
            self.a[0][1] = 1
            self.choixAtt = "att2"

        elif self.a[1][1] == 1 and pygame.key.get_pressed()[pygame.K_LEFT]:  # l'attaque4 pour passer à l'attaque3
            self.a[1][1] = 0
            self.a[1][0] = 1
            if self.liste_pokemon[self.alliePokemon].niveau >= 7:
                self.choixAtt = "att3"

        elif self.a[1][0] == 1 and pygame.key.get_pressed()[pygame.K_UP]:  # attaque3 pour passer à l'attaque1
            self.a[1][0] = 0
            self.a[0][0] = 1
            self.choixAtt = "att1"

        elif self.a[1][0] == 1 and pygame.key.get_pressed()[pygame.K_RIGHT]:  # attaque3 pour passer à l'attaque4
            self.a[1][0] = 0
            self.a[1][1] = 1
            if self.liste_pokemon[self.alliePokemon].niveau >= 14:
                self.choixAtt = "att4"

        elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.txtNum = 2


    def choix_attaque(self):
        menuChoixAtt = pygame.image.load("Map/Images/boxCombat.png")
        self.leJeu.screen.blit(menuChoixAtt, (0, 0))
        if self.choixAtt == "att1":
            self.leJeu.screen.blit(self.text.render(f">{self.att_allier[0][0]}", True, (0, 0, 0)), (32, 490))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[1][0]}", True, (0, 0, 0)), (262, 490))
            if self.liste_pokemon[self.alliePokemon].niveau >= 7:
                self.leJeu.screen.blit(self.text.render(f"{self.att_allier[2][0]}", True, (0, 0, 0)), (32, 541))
            else:
                self.leJeu.screen.blit(self.text.render(f" ---", True, (0, 0, 0)), (32, 541))
            if self.liste_pokemon[self.alliePokemon].niveau >= 14:
                self.leJeu.screen.blit(self.text.render(f"{self.att_allier[3][0]}", True, (0, 0, 0)), (262, 541))
            else:
                self.leJeu.screen.blit(self.text.render(f" ---", True, (0, 0, 0)), (262, 541))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[0][1]}", True, (0, 0, 0)), (562, 496))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[0][2]}", True, (0, 0, 0)), (573, 543))
        elif self.choixAtt == "att2":
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[0][0]}", True, (0, 0, 0)), (32, 490))
            self.leJeu.screen.blit(self.text.render(f">{self.att_allier[1][0]}", True, (0, 0, 0)), (262, 490))
            if self.liste_pokemon[self.alliePokemon].niveau >= 7:
                self.leJeu.screen.blit(self.text.render(f"{self.att_allier[2][0]}", True, (0, 0, 0)), (32, 541))
            else:
                self.leJeu.screen.blit(self.text.render(f" ---", True, (0, 0, 0)), (32, 541))
            if self.liste_pokemon[self.alliePokemon].niveau >= 14:
                self.leJeu.screen.blit(self.text.render(f"{self.att_allier[3][0]}", True, (0, 0, 0)), (262, 541))
            else:
                self.leJeu.screen.blit(self.text.render(f" ---", True, (0, 0, 0)), (262, 541))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[1][1]}", True, (0, 0, 0)), (562, 496))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[1][2]}", True, (0, 0, 0)), (573, 543))
        elif self.choixAtt == "att3":
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[0][0]}", True, (0, 0, 0)), (32, 490))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[1][0]}", True, (0, 0, 0)), (262, 490))
            if self.liste_pokemon[self.alliePokemon].niveau >= 7:
                self.leJeu.screen.blit(self.text.render(f">{self.att_allier[2][0]}", True, (0, 0, 0)), (32, 541))
                self.leJeu.screen.blit(self.text.render(f"{self.att_allier[2][1]}", True, (0, 0, 0)), (562, 496))
                self.leJeu.screen.blit(self.text.render(f"{self.att_allier[2][2]}", True, (0, 0, 0)), (573, 543))
            else:
                self.leJeu.screen.blit(self.text.render(f"> ---", True, (0, 0, 0)), (32, 541))
                self.leJeu.screen.blit(self.text.render(f" ?", True, (0, 0, 0)), (562, 496))
                self.leJeu.screen.blit(self.text.render(f" inconnu", True, (0, 0, 0)), (573, 543))

            if self.liste_pokemon[self.alliePokemon].niveau >= 14:
                self.leJeu.screen.blit(self.text.render(f"{self.att_allier[3][0]}", True, (0, 0, 0)), (262, 541))
            else:
                self.leJeu.screen.blit(self.text.render(f" ---", True, (0, 0, 0)), (262, 541))
        elif self.choixAtt == "att4":
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[0][0]}", True, (0, 0, 0)), (32, 490))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[1][0]}", True, (0, 0, 0)), (262, 490))
            if self.liste_pokemon[self.alliePokemon].niveau >= 7:
                self.leJeu.screen.blit(self.text.render(f"{self.att_allier[2][0]}", True, (0, 0, 0)), (32, 541))
            else:
                self.leJeu.screen.blit(self.text.render(f" ---", True, (0, 0, 0)), (32, 541))
            if self.liste_pokemon[self.alliePokemon].niveau >= 14:
                self.leJeu.screen.blit(self.text.render(f">{self.att_allier[3][0]}", True, (0, 0, 0)), (262, 541))
                self.leJeu.screen.blit(self.text.render(f"{self.att_allier[3][1]}", True, (0, 0, 0)), (562, 496))
                self.leJeu.screen.blit(self.text.render(f"{self.att_allier[3][2]}", True, (0, 0, 0)), (573, 543))
            else:
                self.leJeu.screen.blit(self.text.render(f"> ---", True, (0, 0, 0)), (262, 541))
                self.leJeu.screen.blit(self.text.render(f" ?", True, (0, 0, 0)), (562, 496))
                self.leJeu.screen.blit(self.text.render(f" inconnu", True, (0, 0, 0)), (573, 543))

    def attaque(self):
        if self.liste_ennemie[self.ennemiePokemon].hpActu <= 0 and len(self.liste_ennemie) == self.ennemiePokemon + 1:
            self.actuellement = "ennemieMort"
        elif self.liste_pokemon[self.alliePokemon].hpActu <= 0 and len(self.liste_pokemon) == self.alliePokemon + 1:
            self.actuellement = "allieMort"
        elif len(self.liste_pokemon) > self.alliePokemon and self.liste_pokemon[self.alliePokemon].hpActu <= 0 :
            self.alliePokemon += 1
        elif len(self.liste_ennemie) > self.ennemiePokemon and self.liste_ennemie[self.ennemiePokemon].hpActu <= 0 and not len(self.liste_ennemie) == self.ennemiePokemon + 1 :
            self.ennemiePokemon += 1
        if self.liste_pokemon[self.alliePokemon].vitesse > self.liste_ennemie[self.ennemiePokemon].vitesse:
            if self.attaque1:
                print("attaque1", self.attaque1, self.attaque2)
                self.affAllieAtt(self.attA)
                if self.attaqueUneFois:
                    print("allié attaque")
                    self.attaqueUneFois = False
                    self.attaqueAllie()
            else:
                print("attaque2", self.attaque2, self.attaque1)
                self.affEnnemyAtt(self.attE)
                if self.attaqueUneFois:
                    print("ennemie attaque")
                    self.attaqueUneFois = False
                    self.attaqueEnnemi()
        else:
            if self.attaque1:
                print("attaque 1", self.attaque1, self.attaque2)
                self.affEnnemyAtt(self.attE)
                if self.attaqueUneFois:
                    print("ennemie attaque")
                    self.attaqueUneFois = False
                    self.attaqueEnnemi()
            else:
                print("attaque2", self.attaque2, self.attaque1)
                self.affAllieAtt(self.attA)
                if self.attaqueUneFois:
                    print("allié attaque")
                    self.attaqueUneFois = False
                    self.attaqueAllie()

    def attaqueAllie(self):
        if self.choixAtt == "att1":
            self.attE = 0

            if self.information(self.att_allier[0][2],self.liste_ennemie[self.ennemiePokemon].typeP) == []:
                self.calculeVie(self.attaqueNormal(self.att_allier[0][1],self.liste_ennemie[self.ennemiePokemon].defense, self.liste_pokemon[self.alliePokemon].speAtt, self.liste_pokemon[self.alliePokemon].niveau), self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[0][2],self.liste_ennemie[self.ennemiePokemon].typeP) == [1, 0, 0]:
                print(f"{self.att_allier[0][2]} est la faiblesse de : {self.liste_ennemie[self.ennemiePokemon].typeP}")
                self.calculeVie(self.double(self.att_allier[0][1], self.liste_ennemie[self.ennemiePokemon].defense,self.liste_pokemon[self.alliePokemon].speAtt,self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[0][2],self.liste_ennemie[self.ennemiePokemon].typeP) == [0, 1, 0]:
                print(f"{self.att_allier[0][2]} est faible contre les :{self.liste_ennemie[self.ennemiePokemon].typeP}")
                self.calculeVie(self.faiblesse(self.att_allier[0][1], self.liste_ennemie[self.ennemiePokemon].defense,self.liste_pokemon[self.alliePokemon].speAtt,self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[0][2],self.liste_ennemie[self.ennemiePokemon].typeP) == [0, 0, 1]:
                print(f"{self.att_allier[0][2]} font zero dégats contre les {self.liste_ennemie[self.ennemiePokemon].typeP}")


        elif self.choixAtt == "att2":
            self.attA = 1

            if self.information(self.att_allier[1][2],self.liste_ennemie[self.ennemiePokemon].typeP) == []:
                print("aucun effet")
                self.calculeVie(self.attaqueNormal(self.att_allier[1][1],self.liste_ennemie[self.ennemiePokemon].defense,self.liste_pokemon[self.alliePokemon].speAtt,
                                                   self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[1][2],self.liste_ennemie[self.ennemiePokemon].typeP) == [1, 0, 0]:
                print(f"{self.att_allier[1][2]} est la faiblesse de : {self.liste_ennemie[self.ennemiePokemon].typeP}")
                self.calculeVie(self.double(self.att_allier[1][1],self.liste_ennemie[self.ennemiePokemon].defense,self.liste_pokemon[self.alliePokemon].speAtt,self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[1][2],self.liste_ennemie[self.ennemiePokemon].typeP) == [0, 1, 0]:
                print(f"{self.att_allier[1][2]} est faible contre les :{self.liste_ennemie[self.ennemiePokemon].typeP}")
                self.calculeVie(self.faiblesse(self.att_allier[1][1],self.liste_ennemie[self.ennemiePokemon].defense, self.liste_pokemon[self.alliePokemon].speAtt,self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[1][2],self.liste_ennemie[self.ennemiePokemon].typeP) == [0, 0, 1]:
                print(f"{self.att_allier[1][2]} font zero dégats contre les {self.liste_ennemie[self.ennemiePokemon].typeP}")

        elif self.choixAtt == "att3":
            self.attA = 2

            if self.information(self.att_allier[2][2],self.liste_ennemie[self.ennemiePokemon].typeP) == []:
                print("aucun effet")
                self.calculeVie(self.attaqueNormal(self.att_allier[2][1], self.liste_ennemie[self.ennemiePokemon].defense,self.liste_pokemon[self.alliePokemon].speAtt,
                                                   self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[2][2],self.liste_ennemie[self.ennemiePokemon].typeP) == [1, 0, 0]:
                print(f"{self.att_allier[2][2]} est la faiblesse de : {self.liste_ennemie[self.ennemiePokemon].typeP}")
                self.calculeVie(self.double(self.att_allier[2][1], self.liste_ennemie[self.ennemiePokemon].defense,self.liste_pokemon[self.alliePokemon].speAtt,self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[2][2],self.liste_ennemie[self.ennemiePokemon].typeP) == [0, 1, 0]:
                print(f"{self.att_allier[2][2]} est faible contre les :{self.liste_ennemie[self.ennemiePokemon].typeP}")
                self.calculeVie(self.faiblesse(self.att_allier[2][1], self.liste_ennemie[self.ennemiePokemon].defense, self.liste_pokemon[self.alliePokemon].speAtt,self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[2][2],self.liste_ennemie[self.ennemiePokemon].typeP) == [0, 0, 1]:
                print(f"{self.att_allier[2][2]} font zero dégats contre les {self.liste_ennemie[self.ennemiePokemon].typeP}")

        elif self.choixAtt == "att4":
            self.attA = 3
            if self.information(self.att_allier[3][2],self.liste_ennemie[self.ennemiePokemon].typeP) == []:
                print("aucun effet")
                self.calculeVie(self.attaqueNormal(self.att_allier[3][1], self.liste_ennemie[self.ennemiePokemon].defense,
                                                   self.liste_pokemon[self.alliePokemon].speAtt,
                                                   self.liste_pokemon[self.alliePokemon].niveau),
                                self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[3][2],self.liste_ennemie[self.ennemiePokemon].typeP) == [1, 0, 0]:
                print(f"{self.att_allier[3][2]} est la faiblesse de : {self.liste_ennemie[self.ennemiePokemon].typeP}")
                self.calculeVie(
                    self.double(self.att_allier[3][1],self.liste_ennemie[self.ennemiePokemon].defense, self.liste_pokemon[self.alliePokemon].speAtt,
                                self.liste_pokemon[self.alliePokemon].niveau),
                    self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[3][2], self.liste_ennemie[self.ennemiePokemon].typeP) == [0, 1, 0]:
                print(f"{self.att_allier[3][2]} est faible contre les :{self.liste_ennemie[self.ennemiePokemon].typeP}")
                self.calculeVie(self.faiblesse(self.att_allier[3][1], self.liste_ennemie[self.ennemiePokemon].defense,
                                               self.liste_pokemon[self.alliePokemon].speAtt,
                                               self.liste_pokemon[self.alliePokemon].niveau),
                                self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[3][2],self.liste_ennemie[self.ennemiePokemon].typeP) == [0, 0, 1]:
                print(f"{self.att_allier[3][2]} font zero dégats contre les {self.liste_ennemie[self.ennemiePokemon].typeP}")

    def attaqueEnnemi(self):
        att = random.randint(0, 3)

        if att == 0:
            self.attE = 0

            if self.information(self.att_ennemy[0][2],self.liste_pokemon[self.alliePokemon].typeP) == []:

                self.calculeVie(self.attaqueNormal(self.att_ennemy[0][1], self.liste_pokemon[self.alliePokemon].defense, self.liste_ennemie[self.ennemiePokemon].speAtt,
                                                   self.liste_ennemie[self.ennemiePokemon].niveau), self.liste_ennemie[self.ennemiePokemon].nomPokemon)

            elif self.information(self.att_ennemy[0][2],self.liste_pokemon[self.alliePokemon].typeP) == [1, 0, 0]:

                print(f"{self.att_ennemy[0][2]} est la faiblesse de : {self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(self.double(self.att_ennemy[0][1], self.liste_pokemon[self.alliePokemon].defense,self.liste_ennemie[self.ennemiePokemon].speAtt,
                                            self.liste_ennemie[self.ennemiePokemon].niveau),self.liste_ennemie[self.ennemiePokemon].nomPokemon)

            elif self.information(self.att_ennemy[0][2],self.liste_pokemon[self.alliePokemon].typeP) == [0, 1, 0]:

                print(f"{self.att_ennemy[0][2]} est faible contre les :{self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(self.faiblesse(self.att_ennemy[0][1], self.liste_pokemon[self.alliePokemon].defense,self.liste_ennemie[self.ennemiePokemon].speAtt,
                                               self.liste_ennemie[self.ennemiePokemon].niveau),self.liste_ennemie[self.ennemiePokemon].nomPokemon)

            elif self.information(self.att_ennemy[0][2],self.liste_pokemon[self.alliePokemon].typeP) == [0, 0, 1]:
                print(f"{self.att_ennemy[0][2]} font zero dégats contre les {self.liste_pokemon[self.alliePokemon].typeP}")
        elif att == 1:
            self.attE = 1

            if self.information(self.att_ennemy[1][2],self.liste_pokemon[self.alliePokemon].typeP) == []:

                self.calculeVie(self.attaqueNormal(self.att_ennemy[1][1], self.liste_pokemon[self.alliePokemon].defense,self.liste_ennemie[self.ennemiePokemon].speAtt,
                                                   self.liste_ennemie[self.ennemiePokemon].niveau), self.liste_ennemie[self.ennemiePokemon].nomPokemon)

            elif self.information(self.att_ennemy[1][2],self.liste_pokemon[self.alliePokemon].typeP) == [1, 0, 0]:

                print(f"{self.att_ennemy[1][2]} est la faiblesse de : {self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(self.double(self.att_ennemy[1][1], self.liste_pokemon[self.alliePokemon].defense,self.liste_ennemie[self.ennemiePokemon].speAtt,
                                            self.liste_ennemie[self.ennemiePokemon].niveau),self.liste_ennemie[self.ennemiePokemon].nomPokemon)

            elif self.information(self.att_ennemy[1][2],self.liste_pokemon[self.alliePokemon].typeP) == [0, 1, 0]:

                print(f"{self.att_ennemy[1][2]} est faible contre les :{self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(self.faiblesse(self.att_ennemy[1][1], self.liste_pokemon[self.alliePokemon].defense,self.liste_ennemie[self.ennemiePokemon].speAtt,
                                               self.liste_ennemie[self.ennemiePokemon].niveau),self.liste_ennemie[self.ennemiePokemon].nomPokemon)

            elif self.information(self.att_ennemy[1][2],self.liste_pokemon[self.alliePokemon].typeP) == [0, 0, 1]:
                print(f"{self.att_ennemy[1][2]} font zero dégats contre les {self.liste_pokemon[self.alliePokemon].typeP}")

        elif att == 2:
            self.attE = 2
            if self.information(self.att_ennemy[2][2], self.liste_pokemon[self.alliePokemon].typeP) == []:

                self.calculeVie(self.attaqueNormal(self.att_ennemy[2][1], self.liste_pokemon[self.alliePokemon].defense,
                                                   self.liste_ennemie[self.ennemiePokemon].speAtt,
                                                   self.liste_ennemie[self.ennemiePokemon].niveau), self.liste_ennemie[self.ennemiePokemon].nomPokemon)

            elif self.information(self.att_ennemy[2][2], self.liste_pokemon[self.alliePokemon].typeP) == [1, 0, 0]:

                print(f"{self.att_ennemy[2][2]} est la faiblesse de : {self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(
                    self.double(self.att_ennemy[2][1], self.liste_pokemon[self.alliePokemon].defense,self.liste_ennemie[self.ennemiePokemon].speAtt,
                                self.liste_ennemie[self.ennemiePokemon].niveau), self.liste_ennemie[self.ennemiePokemon].nomPokemon)

            elif self.information(self.att_ennemy[2][2], self.liste_pokemon[self.alliePokemon].typeP) == [0, 1, 0]:

                print(f"{self.att_ennemy[2][2]} est faible contre les :{self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(self.faiblesse(self.att_ennemy[2][1], self.liste_pokemon[self.alliePokemon].defense,
                                               self.liste_ennemie[self.ennemiePokemon].speAtt,
                                               self.liste_ennemie[self.ennemiePokemon].niveau),self.liste_ennemie[self.ennemiePokemon].nomPokemon)

            elif self.information(self.att_ennemy[2][2], self.liste_pokemon[self.alliePokemon].typeP) == [0, 0, 1]:
                print(f"{self.att_ennemy[2][2]} font zero dégats contre les {self.liste_pokemon[self.alliePokemon].typeP}")
        elif att == 3:
            self.attE = 3
            if self.information(self.att_ennemy[3][2], self.liste_pokemon[self.alliePokemon].typeP) == []:

                self.calculeVie(self.attaqueNormal(self.att_ennemy[3][1], self.liste_pokemon[self.alliePokemon].defense,
                                                   self.liste_ennemie[self.ennemiePokemon].speAtt,
                                                   self.liste_ennemie[self.ennemiePokemon].niveau),self.liste_ennemie[self.ennemiePokemon].nomPokemon)

            elif self.information(self.att_ennemy[3][2], self.liste_pokemon[self.alliePokemon].typeP) == [1, 0, 0]:

                print(f"{self.att_ennemy[3][2]} est la faiblesse de : {self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(
                    self.double(self.att_ennemy[3][1], self.liste_pokemon[self.alliePokemon].defense, self.liste_ennemie[self.ennemiePokemon].speAtt,
                                self.liste_ennemie[self.ennemiePokemon].niveau), self.liste_ennemie[self.ennemiePokemon].nomPokemon)

            elif self.information(self.att_ennemy[3][2], self.liste_pokemon[self.alliePokemon].typeP) == [0, 1, 0]:

                print(f"{self.att_ennemy[3][2]} est faible contre les :{self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(self.faiblesse(self.att_ennemy[3][1], self.liste_pokemon[self.alliePokemon].defense,
                                               self.liste_ennemie[self.ennemiePokemon].speAtt,
                                               self.liste_ennemie[self.ennemiePokemon].niveau), self.liste_ennemie[self.ennemiePokemon].nomPokemon)

            elif self.information(self.att_ennemy[3][2], self.liste_pokemon[self.alliePokemon].typeP) == [0, 0, 1]:
                print(
                    f"{self.att_ennemy[3][2]} font zero dégats contre les {self.liste_pokemon[self.alliePokemon].typeP}")


    def attaqueNormal(self,att, defence, puissance, niv):
        calcule = (((niv + att + puissance) * 0.2) / defence * 50)
        calcule = round(calcule)
        return calcule

    def double(self,att, defence, puissance, niv):

        calcule = (((niv + att + puissance) * 0.2) / defence * 50)
        total = calcule * 2
        total = round(total)
        return total

    def faiblesse(self,att, defence, puissance, niv):
        calcule = (((niv + att + puissance) * 0.2) / defence * 50)
        total = calcule / 2
        total = round(total)
        return total

    def information(self,typeAllie, typeEnnemie):
        listeDouble = [["Feu", "Plante", "Glace", "Insect", "Acier"],
                       ["Eau", "Feu", "Sol", "Roche"],
                       ["Plante", "Eau", "Sol", "Roche"],
                       ["Electrik", "Eau", "Vol"],
                       ["Glace", "Plante", "Sol", "Vol", "Dragon"],
                       ["Combat", "Normal", "Glace", "Roche", "Tenebres", "Acier"],
                       ["Poison", "Plante"],
                       ["Sol", "Feu", "Electrik", "Poison", "Roche", "Acier"],
                       ["Vol", "Plante", "Combat", "Insecte"],
                       ["Psy", "Combat", "Poison"],
                       ["Insecte", "Plante", "Psy", "Tenebres"],
                       ["Roche", "Feu", "Glace", "Vol", "Insecte"],
                       ["Spectre", "Psy", "Spectre"],
                       ["Dragon", "Dragon"],
                       ["Tenebres", "Psy", "Spectre"],
                       ["Acier", "Glace", "Roche"]
                       ]
        listeFaiblesse = [["Normal", "Roche", "Acier"],
                          ["Feu", "Feu", "Eau", "Roche", "Dragon"],
                          ["Eau", "Eau", "Plante", "Dragon"],
                          ["Plante", "Feu", "Plante", "Poison", "Vol", "Insecte", "Dragon", "Acier"],
                          ["Electrik", "Plante", "Electrik"],
                          ["Glace", "Feu", "Eau", "Glace", "Acier"],
                          ["Combat", "Poison", "Vol", "Psy", "Insecte"],
                          ["Poison", "Poison", "Sol", "Roche", "Spectre"],
                          ["Sol", "Plante", "Insecte"],
                          ["Vol", "Electrik", "Roche"],
                          ["Psy", "Psy", "Acier"],
                          ["Insecte", "Feu", "Combat", "Poison", "Vol", "Spectre", "Acier"],
                          ["Roche", "Combat", "Sol", "Acier"],
                          ["Spectre", "Tenebres"],
                          ["Dragon", "Dragon"],
                          ["Tenebres", "Combat", "Tenebres"],
                          ["Acier", "Feu", "Eau", "Electrik", "Acier"]
                          ]
        listeAucun = [["Normal", "Spectre"],
                      ["Electrik", "Sol"],
                      ["Combat", "Spectre"],
                      ["Poison", "Acier"],
                      ["Sol", "Vol"],
                      ["Psy", "Tenebres"],
                      ["Spectre", "Normal"]
                      ]
        listeRep = []
        count = 0
        for double in range(len(listeDouble)):
            if listeDouble[double][0] == typeAllie:
                count = double
                for j in range(len(listeDouble[count])):
                    if listeDouble[count][j] == typeEnnemie and j != 0:
                        listeRep = [1, 0, 0]
        count = 0
        for double in range(len(listeFaiblesse)):
            if listeFaiblesse[double][0] == typeAllie:
                count = double
                for j in range(len(listeFaiblesse[count])):
                    if listeFaiblesse[count][j] == typeEnnemie and j != 0:
                        listeRep = [0, 1, 0]

        for double in range(len(listeAucun)):
            if listeAucun[double][0] == typeAllie and listeAucun[double][1] == typeEnnemie:
                listeRep = [0, 0, 1]

        return listeRep

    def ennemieMort(self):
        self.leJeu.screen.blit(self.text.render(f"Vous avez battu {self.liste_ennemie[self.ennemiePokemon].nomPokemon}!", True, (255, 255, 255)),(27, 495))

    def xpPokemon(self):
        self.liste_pokemon[self.alliePokemon].infoXP(self.liste_ennemie[self.ennemiePokemon].niveau)
    def allieMort(self):
        self.leJeu.screen.blit(self.text.render(f"{self.liste_pokemon[self.alliePokemon].nomPokemon} à été battu !", True, (255, 255, 255)),(27, 495))
    def tousMort(self):
        self.leJeu.screen.blit(
            self.text.render(f"Tous vos pokémons n'ont plus de vie, quittez et soignez les au centre pokémon!", True,(255, 255, 255)), (27, 495))
    def affEnnemyAtt(self, attaque):
        self.leJeu.screen.blit(self.text.render(f"{self.liste_ennemie[self.ennemiePokemon].nomPokemon} ennemie attaque {self.att_ennemy[attaque][0]}!", True, (255, 255, 255)),(27, 495))
    def affAllieAtt(self, attaque):
        self.leJeu.screen.blit(self.text.render(f"{self.liste_pokemon[self.alliePokemon].nomPokemon} attaque avec {self.att_allier[attaque][0]}!", True, (255, 255, 255)),(27, 495))

    def initDresseur(self,nom):
        self.nomEnnemie = nom

    def interdireZone(self):

        if self.nomEnnemie == "omar":
            self.leJeu.carte.omar = False
        elif self.nomEnnemie == "alfred":
            self.leJeu.carte.alfred = False
        elif self.nomEnnemie == "anthony":
            self.leJeu.carte.anthony = False
        elif self.nomEnnemie == "charles":
            self.leJeu.carte.charles = False
        elif self.nomEnnemie == "sammy":
            self.leJeu.carte.sammy = False
        elif self.nomEnnemie == "elvin":
            self.leJeu.carte.elvin = False
        elif self.nomEnnemie == "pierre":
            self.leJeu.carte.pierre = False