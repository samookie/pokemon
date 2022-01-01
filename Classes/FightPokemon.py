import pygame

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
        self.att_allier = self.bdd.liste_attaque_pokemon("Pikachu") # Tableau contenant le nom de l'attaque, l'attaque, et le type de l'attaque du pokémon allié
        self.att_ennemy = self.bdd.liste_attaque_pokemon(self.lePokemon) # Tableau contenant le nom de l'attaque, l'attaque, et le type de l'attaque du pokémon allié
        self.dialogueBleu = pygame.image.load("Map/Images/fightDia.png")
        self.attaqueOne = True # passer à true quand on attaque


    '''Méthode permettant d'afficher l'écran d'accueil et d'appliquer les modifications dessus'''
    def affichage(self):
        pygame.draw.rect(self.leJeu.screen, (0, 0, 0),pygame.Rect(0, 0, 700, 600))  # Créer un fond noir sur tout l'écran

        self.fight_img = pygame.image.load("Map/Images/fight.png")
        self.leJeu.screen.blit(self.fight_img, (0, 0)) #Dessiner l'image de fond

        self.afficher_Pokemon_haut(self.lePokemon)
        self.afficher_Pokemon_bas("pikachu")

        self.afficher_stat_haut()
        self.afficher_stat_bas()

        self.afficher_bar_vie_haut()
        self.afficher_bar_vie_bas()

        if self.actuellement == "txtIntro":
            self.leJeu.screen.blit(self.dialogueBleu, (0, 0))  # Dessiner l'image du dialogue bleu
            if self.txtNum == 0:
                self.leJeu.screen.blit(self.text.render(f"Un {self.lePokemon[1]} sauvage apparaît!", True, (255,255,255)), (27, 495))
            elif self.txtNum == 1:
                self.leJeu.screen.blit(self.text.render('PIKACHOUM! GO!', True, (255, 255, 255)), (27, 495))
            elif self.txtNum == 2:
                self.actuellement = "choixMenu"
        elif self.actuellement == "choixMenu":
            self.afficher_choix_menu()
        elif self.actuellement == "choixAttaque":
            self.choix_attaque()
        elif self.actuellement == "attaqueEnCours":
            self.leJeu.screen.blit(self.dialogueBleu, (0, 0))  # Dessiner l'image du dialogue bleu
            self.attaque()



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
            if pygame.key.get_pressed()[pygame.K_SPACE] and self.passer:
                self.actuellement = "choixMenu"
                self.passer = False
            elif not pygame.key.get_pressed()[pygame.K_SPACE] and not self.passer:
                self.passer = True




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
        calcule = (self.lePokemon[13] * 100) / self.lePokemon[4]
        total = calcule * 118 / 100
        pygame.draw.rect(self.leJeu.screen,(0,255,0),pygame.Rect((526,407),(total,8)))

    def afficher_bar_vie_haut(self):
        calcule = (self.lePokemon[13] * 100) / self.lePokemon[4]
        total = calcule * 120 / 100
        pygame.draw.rect(self.leJeu.screen,(0,255,0),pygame.Rect((135 ,251),(total,8)))


    def calculeVie(self, attaque):
        if self.attaqueOne:
            self.lePokemon[13] = self.lePokemon[13] - attaque
            print(self.lePokemon[13])
            self.attaqueOne = False

    def afficher_stat_bas(self):
        statPB = pygame.image.load("Map/Images/statPokemonAlly.png")
        self.leJeu.screen.blit(statPB, (0, 0))  # Dessiner l'image des stats du pokémon du bas
        self.leJeu.screen.blit(self.text.render("Pikachoum", 1, (0, 0, 0)), (445, 374))
        self.leJeu.screen.blit(self.text.render("5", 1, (0, 0, 0)), (642, 374))

    def afficher_stat_haut(self):
        statPH = pygame.image.load("Map/Images/statPokemonEnnemy.png")
        self.leJeu.screen.blit(statPH, (0, 0))  # Dessiner l'image des stats du pokémon du haut
        self.leJeu.screen.blit(self.text.render(str(self.lePokemon[1]), 1, (0, 0, 0)), (58 , 218))
        self.leJeu.screen.blit(self.text.render(str(self.lePokemon[3]), 1, (0, 0, 0)), (246 ,218))

    def afficher_choix_menu(self):
        self.menu_choix()
        self.leJeu.screen.blit(self.text.render("Que dois faire ", True,(255, 255, 255)), (29, 495))
        self.leJeu.screen.blit(self.text.render("Pikachoum ?", True, (255, 255, 255)), (29, 520))

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
            self.choixAtt = "att3"

        elif self.a[0][1] == 1 and pygame.key.get_pressed()[pygame.K_DOWN]:  # l'attaque2 pour passer à l'attaque4
            self.a[0][1] = 0
            self.a[1][1] = 1
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
            self.choixAtt = "att3"

        elif self.a[1][0] == 1 and pygame.key.get_pressed()[pygame.K_UP]:  # attaque3 pour passer à l'attaque1
            self.a[1][0] = 0
            self.a[0][0] = 1
            self.choixAtt = "att1"

        elif self.a[1][0] == 1 and pygame.key.get_pressed()[pygame.K_RIGHT]:  # attaque3 pour passer à l'attaque4
            self.a[1][0] = 0
            self.a[1][1] = 1
            self.choixAtt = "att4"

        elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.txtNum = 2


    def choix_attaque(self):
        menuChoixAtt = pygame.image.load("Map/Images/boxCombat.png")
        self.leJeu.screen.blit(menuChoixAtt, (0, 0))
        if self.choixAtt == "att1":
            self.leJeu.screen.blit(self.text.render(f">{self.att_allier[0][0]}", True, (0, 0, 0)), (32, 490))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[1][0]}", True, (0, 0, 0)), (262, 490))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[2][0]}", True, (0, 0, 0)), (32, 541))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[3][0]}", True, (0, 0, 0)), (262, 541))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[0][1]}", True, (0, 0, 0)), (562, 496))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[0][2]}", True, (0, 0, 0)), (573, 543))
        elif self.choixAtt == "att2":
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[0][0]}", True, (0, 0, 0)), (32, 490))
            self.leJeu.screen.blit(self.text.render(f">{self.att_allier[1][0]}", True, (0, 0, 0)), (262, 490))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[2][0]}", True, (0, 0, 0)), (32, 541))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[3][0]}", True, (0, 0, 0)), (262, 541))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[1][1]}", True, (0, 0, 0)), (562, 496))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[1][2]}", True, (0, 0, 0)), (573, 543))
        elif self.choixAtt == "att3":
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[0][0]}", True, (0, 0, 0)), (32, 490))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[1][0]}", True, (0, 0, 0)), (262, 490))
            self.leJeu.screen.blit(self.text.render(f">{self.att_allier[2][0]}", True, (0, 0, 0)), (32, 541))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[3][0]}", True, (0, 0, 0)), (262, 541))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[2][1]}", True, (0, 0, 0)), (562, 496))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[2][2]}", True, (0, 0, 0)), (573, 543))
        elif self.choixAtt == "att4":
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[0][0]}", True, (0, 0, 0)), (32, 490))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[1][0]}", True, (0, 0, 0)), (262, 490))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[2][0]}", True, (0, 0, 0)), (32, 541))
            self.leJeu.screen.blit(self.text.render(f">{self.att_allier[3][0]}", True, (0, 0, 0)), (262, 541))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[3][1]}", True, (0, 0, 0)), (562, 496))
            self.leJeu.screen.blit(self.text.render(f"{self.att_allier[3][2]}", True, (0, 0, 0)), (573, 543))

    def attaque(self):
        if self.choixAtt == "att1" :

            self.leJeu.screen.blit(self.text.render(f"PIKACHOUM utilise {self.att_allier[0][0]}", True, (255, 255, 255)), (29, 495))
            self.calculeVie(self.att_allier[0][1])

        elif self.choixAtt == "att2":

            self.leJeu.screen.blit(self.text.render(f"PIKACHOUM utilise {self.att_allier[1][0]}", True, (255, 255, 255)), (29, 495))
            self.calculeVie(self.att_allier[1][1])

        elif self.choixAtt == "att3":

            self.leJeu.screen.blit(self.text.render(f"PIKACHOUM utilise {self.att_allier[2][0]}", True, (255, 255, 255)), (29, 495))
            self.calculeVie(self.att_allier[2][1])

        elif self.choixAtt == "att4":

            self.leJeu.screen.blit(self.text.render(f"PIKACHOUM utilise {self.att_allier[3][0]}", True, (255, 255, 255)), (29, 495))
            self.calculeVie(self.att_allier[3][1])


    def attaquePremier(self):

        pass

    def attaqueEnnemi(lepokemon):
        attaque = random.randint(0, 3)
        if attaque == 0:
            listeAllie[lePokemon].hpActu -= attEnnemi[0][1]
            print("Votre pokémon ", listeAllie[lePokemon].nom, " a ", listeAllie[lePokemon].hpActu, "hp sur ",
                  listeAllie[lePokemon].hp)
        elif attaque == 1:
            print(roucool.nom, " vous frappe avec l'attaque 2 donc vous perdez ", attEnnemi[1][1])
            listeAllie[lePokemon].hpActu -= attEnnemi[1][1]
            print("Votre pokémon ", listeAllie[lePokemon].nom, " a ", listeAllie[lePokemon].hpActu, "hp sur ",
                  listeAllie[lePokemon].hp)
        elif attaque == 2:
            print(roucool.nom, " vous frappe avec l'attaque 3 donc vous perdez ", attEnnemi[2][1])
            listeAllie[lePokemon].hpActu -= attEnnemi[2][1]
            print("Votre pokémon ", listeAllie[lePokemon].nom, " a ", listeAllie[lePokemon].hpActu, "hp sur ",
                  listeAllie[lePokemon].hp)
        elif attaque == 3:
            print(roucool.nom, " vous frappe avec l'attaque 4 donc vous perdez ", attEnnemi[3][1])
            listeAllie[lePokemon].hpActu -= attEnnemi[3][1]
            print("Votre pokémon ", listeAllie[lePokemon].nom, " a ", listeAllie[lePokemon].hpActu, "hp sur ",
                  listeAllie[lePokemon].hp)

    def attaque(att, defence, puissance, niv):
        calcule = (((niv + att + puissance) * 0.2) / defence * 50)
        calcule = round(calcule)
        return calcule

    def double(att, defence, puissance, niv):

        calcule = (((niv + att + puissance) * 0.2) / defence * 50)
        total = calcule * 2
        total = round(total)
        return total

    def faiblesse(att, defence, puissance, niv):
        calcule = (((niv + att + puissance) * 0.2) / defence * 50)
        total = calcule / 2
        total = round(total)
        return total