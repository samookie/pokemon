import pygame
import random

from Classes.Joueur import Joueur
from Model.PokemonBDD import PokemonBDD
from Classes.TypePokemon import TypePokemon


class FightPokemon:

    def __init__(self, leJeu, nomPokemon = "", liste_pokemon = []):
        self.leJeu = leJeu #cLasse jeu
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 15) #Initialiser la police pour le texte
        self.bdd = PokemonBDD()
        self.lePokemon = nomPokemon
        self.liste_pokemon = liste_pokemon
        self.alliePokemon = 0
        self.txtNum = 0 # le numéro d'orde des dialogues
        self.passer = True
        self.suivant = True
        self.choix = "Attaque" #gestion des choix
        self.a = [[1, 0], [0, 0]] #tableau pour la gestion des choix du combat
        self.choixAtt = "att1"
        self.actuellement = "txtIntro"
        self.att_ennemy = self.bdd.liste_attaque_pokemon(self.lePokemon) # Tableau contenant le nom de l'attaque, l'attaque, et le type de l'attaque du pokémon allié
        self.dialogueBleu = pygame.image.load("Map/Images/fightDia.png")
        self.attaqueOne = True # passer à true quand on attaque
        self.attaqueUneFois = True
        self.attaque1 = True
        self.attaque2 = True
        self.attA = 0
        self.attE = 0


    '''Méthode permettant d'afficher l'écran d'accueil et d'appliquer les modifications dessus'''
    def affichage(self):
        self.att_ennemy = self.bdd.liste_attaque_pokemon(self.lePokemon[0])
        self.att_allier = self.bdd.liste_attaque_pokemon(self.liste_pokemon[self.alliePokemon].nomPokemon)  # Tableau contenant le nom de l'attaque, l'attaque, et le type de l'attaque du pokémon allié
        pygame.draw.rect(self.leJeu.screen, (0, 0, 0),pygame.Rect(0, 0, 700, 600))  # Créer un fond noir sur tout l'écran

        self.fight_img = pygame.image.load("Map/Images/fight.png")
        self.leJeu.screen.blit(self.fight_img, (0, 0)) #Dessiner l'image de fond

        self.afficher_Pokemon_haut(self.lePokemon)
        self.afficher_Pokemon_bas(self.liste_pokemon[self.alliePokemon].nomPokemon)

        self.afficher_stat_haut()
        self.afficher_stat_bas()

        self.afficher_bar_vie_haut()
        self.afficher_bar_vie_bas()
        self.bdd.getPokemonHero()
        if self.actuellement == "txtIntro":
            self.leJeu.screen.blit(self.dialogueBleu, (0, 0))  # Dessiner l'image du dialogue bleu
            if self.txtNum == 0:
                self.leJeu.screen.blit(self.text.render(f"Un {self.lePokemon[1]} sauvage apparaît!", True, (255,255,255)), (27, 495))
            elif self.txtNum == 1:
                self.leJeu.screen.blit(self.text.render(f"{self.liste_pokemon[self.alliePokemon].nomPokemon}! GO!", True, (255, 255, 255)), (27, 495))
            elif self.txtNum == 2:
                self.actuellement = "choixMenu"
        elif self.actuellement == "choixMenu":
            self.afficher_choix_menu()
        elif self.actuellement == "choixAttaque":
            self.choix_attaque()
        elif self.actuellement == "attaqueEnCours":
            self.leJeu.screen.blit(self.dialogueBleu, (0, 0))  # Dessiner l'image du dialogue bleu
            self.attaque()
        elif self.actuellement == "ennemieMort":
            self.leJeu.screen.blit(self.dialogueBleu, (0, 0))
            self.ennemieMort()
        elif self.actuellement == "allieMort":
            self.leJeu.screen.blit(self.dialogueBleu, (0, 0))
            self.allieMort()

        if self.leJeu.mettre_a_jour:
            self.actuellement = "txtIntro"
            self.choix = "Attaque"
            self.choixAtt = "att1"
            self.leJeu.mettre_a_jour = False
        pygame.display.flip()  # MAJ de l'affichage

    '''Méthode permettant de vérifier la frappe des touches sur cette classe'''
    def gestion_touches(self):

        if self.actuellement == "txtIntro":
            if pygame.key.get_pressed()[pygame.K_SPACE] and self.passer and self.suivant: #Si la touche est espace, que l'on peut encore naviguer dans le dialogue et que la variable passer est à True
                self.txtNum = self.txtNum + 1
                self.passer = False
            elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.passer:
                self.passer = True
        elif self.actuellement == "choixMenu":
            self.algorithm_choix()
            self.gestion_touches_choix()
        elif self.actuellement == "choixAttaque":
            self.algorithm_attaque()
            self.gestion_touches_choix_attaque()
        elif self.actuellement == "attaqueEnCours":
            self.gestion_touches_en_attaque()


    def gestion_touches_choix(self):
        if self.choix == "Attaque" and pygame.key.get_pressed()[pygame.K_SPACE] and self.passer:
            self.actuellement = "choixAttaque"
            self.passer = False

        elif self.choix == "Sac" and pygame.key.get_pressed()[pygame.K_SPACE] and self.passer:
            self.leJeu.ecran_affiche = "sac"
            self.leJeu.mettre_a_jour = True
            self.txtNum = 2
            self.leJeu.sac.carte = "fight"
            self.passer = False

        elif self.choix == "Pokemon" and pygame.key.get_pressed()[pygame.K_SPACE] and self.passer:
            self.leJeu.ecran_affiche = "pokemons"
            self.leJeu.mettre_a_jour = True
            self.txtNum = 2
            self.leJeu.pokemon_ecran.carte = "fight"
            self.passer = False

        elif self.choix == "Fuite" and pygame.key.get_pressed()[pygame.K_SPACE] and self.passer:
            self.leJeu.ecran_affiche = "jeu"
            self.leJeu.mettre_a_jour = True
            self.txtNum = 0
            self.passer = False

        elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.passer:
            self.passer = True

    def gestion_touches_choix_attaque(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.passer:
            self.actuellement = "attaqueEnCours"
            self.passer = False
            self.attaqueOne = True
        elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.passer:
            self.passer = True

    def gestion_touches_en_attaque(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.passer and self.attaque1:
            self.passer = False
            self.attaque1 = False
            self.attaqueUneFois = True
            self.attaqueOne = True
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.passer and not self.attaque1 and self.attaque2:
            self.passer = False
            self.attaque2 = False
            self.attaqueUneFois = True
            self.attaqueOne = True
        elif pygame.key.get_pressed()[pygame.K_SPACE] and self.passer and not self.attaque1 and not self.attaque2 and not self.attaqueUneFois:
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
        pokemonHaut = pygame.image.load(f'Map/Images/{pokemon[12]}.png')  # Dessiner l'image du pokémon d'en haut
        pokemonHautScale = pygame.transform.scale(pokemonHaut, (200, 200))  # Redimensionner l'image du professeur
        self.leJeu.screen.blit(pokemonHautScale, (409, 190))

    def changerPokemon(self, pokemon, liste_pokemon):
        self.lePokemon = pokemon
        self.liste_pokemon = liste_pokemon

    def afficher_bar_vie_bas(self):
        calcule = (self.liste_pokemon[self.alliePokemon].hpActu * 100) / self.liste_pokemon[self.alliePokemon].hp
        total = calcule * 128 / 100
        pygame.draw.rect(self.leJeu.screen,(0,255,0),pygame.Rect((526,407),(total,8)))

    def afficher_bar_vie_haut(self):
        calcule = (self.lePokemon[13] * 100) / self.lePokemon[4]
        total = calcule * 120 / 100
        pygame.draw.rect(self.leJeu.screen,(0,255,0),pygame.Rect((135 ,251),(total,8)))


    def calculeVie(self, attaque, pokemon):
        print("STATUT ATTAQUEONE", self.attaqueOne)
        if self.attaqueOne:
            if pokemon == self.lePokemon[0]:
                print("AVANT ATTAQUE",self.attaqueOne)
                self.liste_pokemon[self.alliePokemon].hpActu = self.liste_pokemon[self.alliePokemon].hpActu - attaque
                self.attaqueOne = False
                print("APRES ATTAQUE",self.attaqueOne)
            else:
                print("AVANT ATTAQUE", self.attaqueOne)
                self.lePokemon[13] = self.lePokemon[13] - attaque
                print(self.lePokemon[13])
                self.attaqueOne = False
                print("APRES ATTAQUE", self.attaqueOne)

    def afficher_stat_bas(self):
        statPB = pygame.image.load("Map/Images/statPokemonAlly.png")
        self.leJeu.screen.blit(statPB, (0, 0))  # Dessiner l'image des stats du pokémon du bas
        self.leJeu.screen.blit(self.text.render(self.liste_pokemon[self.alliePokemon].nomPokemon, 1, (0, 0, 0)), (445, 374))
        self.leJeu.screen.blit(self.text.render(f"{self.liste_pokemon[self.alliePokemon].niveau}", 1, (0, 0, 0)), (642, 374))

    def afficher_stat_haut(self):
        statPH = pygame.image.load("Map/Images/statPokemonEnnemy.png")
        self.leJeu.screen.blit(statPH, (0, 0))  # Dessiner l'image des stats du pokémon du haut
        self.leJeu.screen.blit(self.text.render(str(self.lePokemon[1]), 1, (0, 0, 0)), (58 , 218))
        self.leJeu.screen.blit(self.text.render(str(self.lePokemon[3]), 1, (0, 0, 0)), (246 ,218))

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
            self.leJeu.screen.blit(self.text.render("FUITE", True, (0, 0, 0)), (585, 545))
        elif self.choix == "Sac":
            self.leJeu.screen.blit(self.text.render("ATTAQUE ", True, (0, 0, 0)), (380, 494))
            self.leJeu.screen.blit(self.text.render(">SAC", True, (0, 0, 0)), (585, 494))
            self.leJeu.screen.blit(self.text.render("POKEMON", True, (0, 0, 0)), (380, 545))
            self.leJeu.screen.blit(self.text.render("FUITE", True, (0, 0, 0)), (585, 545))
        elif self.choix == "Pokemon":
            self.leJeu.screen.blit(self.text.render("ATTAQUE ", True, (0, 0, 0)), (380, 494))
            self.leJeu.screen.blit(self.text.render("SAC", True, (0, 0, 0)), (585, 494))
            self.leJeu.screen.blit(self.text.render(">POKEMON", True, (0, 0, 0)), (380, 545))
            self.leJeu.screen.blit(self.text.render("FUITE", True, (0, 0, 0)), (585, 545))
        elif self.choix == "Fuite":
            self.leJeu.screen.blit(self.text.render("ATTAQUE ", True, (0, 0, 0)), (380, 494))
            self.leJeu.screen.blit(self.text.render("SAC", True, (0, 0, 0)), (585, 494))
            self.leJeu.screen.blit(self.text.render("POKEMON", True, (0, 0, 0)), (380, 545))
            self.leJeu.screen.blit(self.text.render(">FUITE", True, (0, 0, 0)), (585, 545))

    def algorithm_choix(self):
        if self.a[0][0] == 1 and pygame.key.get_pressed()[pygame.K_RIGHT]:  # attaque pour passer à sac
            self.a[0][0] = 0
            self.a[0][1] = 1
            self.choix ="Sac"

        elif self.a[0][0] == 1 and pygame.key.get_pressed()[pygame.K_DOWN]:  # attaque pour passer à pokemon
            self.a[0][0] = 0
            self.a[1][0] = 1
            self.choix = "Pokemon"

        elif self.a[0][1] == 1 and pygame.key.get_pressed()[pygame.K_DOWN]:  # sac pour passer à fuite
            self.a[0][1] = 0
            self.a[1][1] = 1
            self.choix = "Fuite"

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

        elif self.a[1][0] == 1 and pygame.key.get_pressed()[pygame.K_RIGHT]:  # pokemon pour passer à fuite
            self.a[1][0] = 0
            self.a[1][1] = 1
            self.choix = "Fuite"

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
                self.leJeu.screen.blit(self.text.render(f"{self.att_allier[2][0]}", True, (0, 0, 0)), (32, 541))
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
                self.leJeu.screen.blit(self.text.render(f"{self.att_allier[3][0]}", True, (0, 0, 0)), (262, 541))
                self.leJeu.screen.blit(self.text.render(f"{self.att_allier[3][1]}", True, (0, 0, 0)), (562, 496))
                self.leJeu.screen.blit(self.text.render(f"{self.att_allier[3][2]}", True, (0, 0, 0)), (573, 543))
            else:
                self.leJeu.screen.blit(self.text.render(f"> ---", True, (0, 0, 0)), (262, 541))
                self.leJeu.screen.blit(self.text.render(f" ?", True, (0, 0, 0)), (562, 496))
                self.leJeu.screen.blit(self.text.render(f" inconnu", True, (0, 0, 0)), (573, 543))

    def attaque(self):
        if self.lePokemon[13] <= 0 :
            self.actuellement = "ennemieMort"
        elif self.liste_pokemon[self.alliePokemon].hpActu <= 0:
            self.actuellement = "allieMort"

        if self.liste_pokemon[self.alliePokemon].vitesse > self.lePokemon[5]:
            if self.attaque1:
                print("attaque1")
                if self.attaqueUneFois:
                    print("allié attaque")
                    self.attaqueAllie()
                    self.attaqueUneFois = False
                    self.affAllieAtt(self.attA)
            else:
                print("attaque2")
                if self.attaqueUneFois:
                    print("ennemie attaque")
                    self.attaqueEnnemi()
                    self.attaqueUneFois = False
                    self.affEnnemyAtt(self.attE)
        else:
            if self.attaque1:
                print("attaque 1")
                if self.attaqueUneFois:
                    print("ennemie attaque")
                    self.attaqueEnnemi()
                    self.attaqueUneFois = False
                    self.affEnnemyAtt(self.attE)
            else:
                print("attaque2")
                if self.attaqueUneFois:
                    print("allié attaque")
                    self.attaqueAllie()
                    self.attaqueUneFois = False
                    self.affAllieAtt(self.attA)

    def attaqueAllie(self):
        print("ATTAQUE ALLIE")
        if self.choixAtt == "att1":
            self.attE = 0
            print("ATTAQUE 1")

            if self.information(self.att_allier[0][2],self.lePokemon[16]) == []:
                self.calculeVie(self.attaqueNormal(self.att_allier[0][1], self.lePokemon[8], self.liste_pokemon[self.alliePokemon].speAtt, self.liste_pokemon[self.alliePokemon].niveau), self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[0][2],self.lePokemon[16]) == [1, 0, 0]:
                print(f"{self.att_allier[0][2]} est la faiblesse de : {self.lePokemon[16]}")
                self.calculeVie(self.double(self.att_allier[0][1], self.lePokemon[8],self.liste_pokemon[self.alliePokemon].speAtt,self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[0][2],self.lePokemon[16]) == [0, 1, 0]:
                print(f"{self.att_allier[0][2]} est faible contre les :{self.lePokemon[16]}")
                self.calculeVie(self.faiblesse(self.att_allier[0][1], self.lePokemon[8],self.liste_pokemon[self.alliePokemon].speAtt,self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[0][2],self.lePokemon[16]) == [0, 0, 1]:
                print(f"{self.att_allier[0][2]} font zero dégats contre les {self.lePokemon[16]}")


        elif self.choixAtt == "att2":
            self.attA = 1
            print("ATTAQUE 2")

            if self.information(self.att_allier[1][2],self.lePokemon[16]) == []:
                print("aucun effet")
                self.calculeVie(self.attaqueNormal(self.att_allier[1][1], self.lePokemon[8],self.liste_pokemon[self.alliePokemon].speAtt,
                                                   self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[1][2],self.lePokemon[16]) == [1, 0, 0]:
                print(f"{self.att_allier[1][2]} est la faiblesse de : {self.lePokemon[16]}")
                self.calculeVie(self.double(self.att_allier[1][1], self.lePokemon[8],self.liste_pokemon[self.alliePokemon].speAtt,self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[1][2],self.lePokemon[16]) == [0, 1, 0]:
                print(f"{self.att_allier[1][2]} est faible contre les :{self.lePokemon[16]}")
                self.calculeVie(self.faiblesse(self.att_allier[1][1], self.lePokemon[8], self.liste_pokemon[self.alliePokemon].speAtt,self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[1][2],self.lePokemon[16]) == [0, 0, 1]:
                print(f"{self.att_allier[1][2]} font zero dégats contre les {self.lePokemon[16]}")

        elif self.choixAtt == "att3":
            self.attA = 2
            print("ATTAQUE 3")

            if self.information(self.att_allier[2][2],self.lePokemon[16]) == []:
                print("aucun effet")
                self.calculeVie(self.attaqueNormal(self.att_allier[2][1], self.lePokemon[8],self.liste_pokemon[self.alliePokemon].speAtt,
                                                   self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[2][2],self.lePokemon[16]) == [1, 0, 0]:
                print(f"{self.att_allier[2][2]} est la faiblesse de : {self.lePokemon[16]}")
                self.calculeVie(self.double(self.att_allier[2][1], self.lePokemon[8],self.liste_pokemon[self.alliePokemon].speAtt,self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[2][2],self.lePokemon[16]) == [0, 1, 0]:
                print(f"{self.att_allier[2][2]} est faible contre les :{self.lePokemon[16]}")
                self.calculeVie(self.faiblesse(self.att_allier[2][1], self.lePokemon[8], self.liste_pokemon[self.alliePokemon].speAtt,self.liste_pokemon[self.alliePokemon].niveau),self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[2][2],self.lePokemon[16]) == [0, 0, 1]:
                print(f"{self.att_allier[2][2]} font zero dégats contre les {self.lePokemon[16]}")

        elif self.choixAtt == "att4":
            print("ATTAQUE 4")
            self.attA = 3
            if self.information(self.att_allier[3][2], self.lePokemon[16]) == []:
                print("aucun effet")
                self.calculeVie(self.attaqueNormal(self.att_allier[3][1], self.lePokemon[8],
                                                   self.liste_pokemon[self.alliePokemon].speAtt,
                                                   self.liste_pokemon[self.alliePokemon].niveau),
                                self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[3][2], self.lePokemon[16]) == [1, 0, 0]:
                print(f"{self.att_allier[3][2]} est la faiblesse de : {self.lePokemon[16]}")
                self.calculeVie(
                    self.double(self.att_allier[3][1], self.lePokemon[8], self.liste_pokemon[self.alliePokemon].speAtt,
                                self.liste_pokemon[self.alliePokemon].niveau),
                    self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[3][2], self.lePokemon[16]) == [0, 1, 0]:
                print(f"{self.att_allier[3][2]} est faible contre les :{self.lePokemon[16]}")
                self.calculeVie(self.faiblesse(self.att_allier[3][1], self.lePokemon[8],
                                               self.liste_pokemon[self.alliePokemon].speAtt,
                                               self.liste_pokemon[self.alliePokemon].niveau),
                                self.liste_pokemon[self.alliePokemon].nomPokemon)
            elif self.information(self.att_allier[3][2], self.lePokemon[16]) == [0, 0, 1]:
                print(f"{self.att_allier[3][2]} font zero dégats contre les {self.lePokemon[16]}")

    def attaqueEnnemi(self):
        print("ATTAQUE ENNEMIE")
        att = random.randint(0, 3)

        if att == 0:
            self.attE = 0
            print("ATTAQUE 1")

            if self.information(self.att_ennemy[0][2],self.liste_pokemon[self.alliePokemon].typeP) == []:

                self.calculeVie(self.attaqueNormal(self.att_ennemy[0][1], self.liste_pokemon[self.alliePokemon].defense, self.lePokemon[7],
                                                   self.lePokemon[3]), self.lePokemon[0])

            elif self.information(self.att_ennemy[0][2],self.liste_pokemon[self.alliePokemon].typeP) == [1, 0, 0]:

                print(f"{self.att_ennemy[0][2]} est la faiblesse de : {self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(self.double(self.att_ennemy[0][1], self.liste_pokemon[self.alliePokemon].defense,self.lePokemon[7],
                                            self.lePokemon[3]),self.lePokemon[0])

            elif self.information(self.att_ennemy[0][2],self.liste_pokemon[self.alliePokemon].typeP) == [0, 1, 0]:

                print(f"{self.att_ennemy[0][2]} est faible contre les :{self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(self.faiblesse(self.att_ennemy[0][1], self.liste_pokemon[self.alliePokemon].defense,self.lePokemon[7],
                                               self.lePokemon[3]),self.lePokemon[0])

            elif self.information(self.att_ennemy[0][2],self.liste_pokemon[self.alliePokemon].typeP) == [0, 0, 1]:
                print(f"{self.att_ennemy[0][2]} font zero dégats contre les {self.liste_pokemon[self.alliePokemon].typeP}")
        elif att == 1:
            self.attE = 1
            print("ATTAQUE 2")

            if self.information(self.att_ennemy[1][2],self.liste_pokemon[self.alliePokemon].typeP) == []:

                self.calculeVie(self.attaqueNormal(self.att_ennemy[1][1], self.liste_pokemon[self.alliePokemon].defense, self.lePokemon[7],
                                                   self.lePokemon[3]), self.lePokemon[0])

            elif self.information(self.att_ennemy[1][2],self.liste_pokemon[self.alliePokemon].typeP) == [1, 0, 0]:

                print(f"{self.att_ennemy[1][2]} est la faiblesse de : {self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(self.double(self.att_ennemy[1][1], self.liste_pokemon[self.alliePokemon].defense,self.lePokemon[7],
                                            self.lePokemon[3]),self.lePokemon[0])

            elif self.information(self.att_ennemy[1][2],self.liste_pokemon[self.alliePokemon].typeP) == [0, 1, 0]:

                print(f"{self.att_ennemy[1][2]} est faible contre les :{self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(self.faiblesse(self.att_ennemy[1][1], self.liste_pokemon[self.alliePokemon].defense,self.lePokemon[7],
                                               self.lePokemon[3]),self.lePokemon[0])

            elif self.information(self.att_ennemy[1][2],self.liste_pokemon[self.alliePokemon].typeP) == [0, 0, 1]:
                print(f"{self.att_ennemy[1][2]} font zero dégats contre les {self.liste_pokemon[self.alliePokemon].typeP}")

        elif att == 2:
            print("ATTAQUE 3")
            self.attE = 2
            if self.information(self.att_ennemy[2][2], self.liste_pokemon[self.alliePokemon].typeP) == []:

                self.calculeVie(self.attaqueNormal(self.att_ennemy[2][1], self.liste_pokemon[self.alliePokemon].defense,
                                                   self.lePokemon[7],
                                                   self.lePokemon[3]), self.lePokemon[0])

            elif self.information(self.att_ennemy[2][2], self.liste_pokemon[self.alliePokemon].typeP) == [1, 0, 0]:

                print(f"{self.att_ennemy[2][2]} est la faiblesse de : {self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(
                    self.double(self.att_ennemy[2][1], self.liste_pokemon[self.alliePokemon].defense, self.lePokemon[7],
                                self.lePokemon[3]), self.lePokemon[0])

            elif self.information(self.att_ennemy[2][2], self.liste_pokemon[self.alliePokemon].typeP) == [0, 1, 0]:

                print(f"{self.att_ennemy[2][2]} est faible contre les :{self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(self.faiblesse(self.att_ennemy[2][1], self.liste_pokemon[self.alliePokemon].defense,
                                               self.lePokemon[7],
                                               self.lePokemon[3]),self.lePokemon[0])

            elif self.information(self.att_ennemy[2][2], self.liste_pokemon[self.alliePokemon].typeP) == [0, 0, 1]:
                print(f"{self.att_ennemy[2][2]} font zero dégats contre les {self.liste_pokemon[self.alliePokemon].typeP}")
        elif att == 3:
            print("ATTAQUE 4")
            self.attE = 3
            if self.information(self.att_ennemy[3][2], self.liste_pokemon[self.alliePokemon].typeP) == []:

                self.calculeVie(self.attaqueNormal(self.att_ennemy[3][1], self.liste_pokemon[self.alliePokemon].defense,
                                                   self.lePokemon[7],
                                                   self.lePokemon[3]), self.lePokemon[0])

            elif self.information(self.att_ennemy[3][2], self.liste_pokemon[self.alliePokemon].typeP) == [1, 0, 0]:

                print(f"{self.att_ennemy[3][2]} est la faiblesse de : {self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(
                    self.double(self.att_ennemy[3][1], self.liste_pokemon[self.alliePokemon].defense, self.lePokemon[7],
                                self.lePokemon[3]), self.lePokemon[0])

            elif self.information(self.att_ennemy[3][2], self.liste_pokemon[self.alliePokemon].typeP) == [0, 1, 0]:

                print(f"{self.att_ennemy[3][2]} est faible contre les :{self.liste_pokemon[self.alliePokemon].typeP}")
                self.calculeVie(self.faiblesse(self.att_ennemy[3][1], self.liste_pokemon[self.alliePokemon].defense,
                                               self.lePokemon[7],
                                               self.lePokemon[3]), self.lePokemon[0])

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
        self.leJeu.screen.blit(self.text.render(f"Vous avez battu {self.lePokemon[0]}!", True, (255, 255, 255)),(27, 495))

    def allieMort(self):
        self.leJeu.screen.blit(self.text.render(f"{self.liste_pokemon[self.alliePokemon].nomPokemon} à été battu !", True, (255, 255, 255)),(27, 495))

    def affEnnemyAtt(self, attaque):
        self.leJeu.screen.blit(self.text.render(f"{self.lePokemon[0]} ennemie attaque {self.att_ennemy[attaque][0]}!", True, (255, 255, 255)),(27, 495))
    def affAllieAtt(self, attaque):
        self.leJeu.screen.blit(self.text.render(f"{self.liste_pokemon[self.alliePokemon].nomPokemon} attaque avec {self.att_allier[attaque][0]}!", True, (255, 255, 255)),(27, 495))