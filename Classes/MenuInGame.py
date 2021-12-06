import pygame.draw

from Model.PokemonBDD import PokemonBDD


class MenuInGame():

    def __init__(self, leJeu):
        self.leJeu = leJeu
        self.laBdd = PokemonBDD()
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 15)  # Initialiser la police pour le texte

        self.continuer = True
        self.menuAffiche = {
            "haut": False,
            "ci": False
        }
        self.menuSelec = 1

    def affichage(self):
        self.gestion_touches()
        if self.menuAffiche["haut"]:
            self.creationMenuHautDroite()
            self.leJeu.dansMenu = False
        elif self.menuAffiche["ci"]:
            self.creationCIChasseur()
            self.leJeu.dansMenu = False
        else:
            self.leJeu.dansMenu = True


    def creationMenuHautDroite(self):
        pygame.draw.rect(self.leJeu.screen, (255, 255, 255, 100), pygame.Rect(490, 10, 200, 125))
        pygame.draw.rect(self.leJeu.screen, (0, 0, 0), pygame.Rect(490, 10, 200, 125), 2)
        if self.menuSelec == 1:
            self.leJeu.screen.blit(self.text.render("> Pokémons", True, (0, 0, 0)), (500, 15))
        else:
            self.leJeu.screen.blit(self.text.render("Pokémons", True, (0, 0, 0)), (500, 15))
        if self.menuSelec == 2:
            self.leJeu.screen.blit(self.text.render("> Sac", True, (0, 0, 0)), (500, 35))
        else:
            self.leJeu.screen.blit(self.text.render("Sac", True, (0, 0, 0)), (500, 35))
        if self.menuSelec == 3:
            self.leJeu.screen.blit(self.text.render("> Joueur", True, (0, 0, 0)), (500, 55))
        else:
            self.leJeu.screen.blit(self.text.render("Joueur", True, (0, 0, 0)), (500, 55))
        if self.menuSelec == 4:
            self.leJeu.screen.blit(self.text.render("> Sauvegarder", True, (0, 0, 0)), (500, 75))
        else:
            self.leJeu.screen.blit(self.text.render("Sauvegarder", True, (0, 0, 0)), (500, 75))
        if self.menuSelec == 5:
            self.leJeu.screen.blit(self.text.render("> Quitter", True, (0, 0, 0)), (500, 95))
        else:
            self.leJeu.screen.blit(self.text.render("Quitter", True, (0, 0, 0)), (500, 95))

    def creationCIChasseur(self):
        donnesHero = self.laBdd.chargerInfosHero()

        ciChasseur = pygame.image.load("Map/Images/ci.png")
        self.leJeu.screen.blit(ciChasseur, (0, 0))

        self.leJeu.screen.blit(self.text.render(str(donnesHero[0]), True, (0, 0, 0)), (376, 205))
        self.leJeu.screen.blit(self.text.render("Nom : " + donnesHero[1], True, (0, 0, 0)), (209, 232))
        self.leJeu.screen.blit(self.text.render("Argent : " + str(donnesHero[3]), True, (0, 0, 0)), (209, 300))

        if donnesHero[2] == "g":
            self.leJeu.screen.blit(self.text.render("Genre : Garçon", True, (0, 0, 0)), (209, 275))
        else:
            self.leJeu.screen.blit(self.text.render("Genre : Fille", True, (0, 0, 0)), (209, 275))

    def razAffMenu(self):
        for menu in self.menuAffiche:
            self.menuAffiche[menu] = False

    def gestion_touches(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE] and self.continuer:
            if self.menuAffiche["haut"]:
                self.menuAffiche["haut"] = False
            else:
                self.razAffMenu()
                self.menuAffiche["haut"] = True
            self.continuer = False

        elif pygame.key.get_pressed()[pygame.K_DOWN] and self.continuer:
            if self.menuSelec < 5:
                self.menuSelec += 1
            self.continuer = False

        elif pygame.key.get_pressed()[pygame.K_UP] and self.continuer:
            if self.menuSelec > 1:
                self.menuSelec -= 1
            self.continuer = False

        elif pygame.key.get_pressed()[pygame.K_RETURN] and not self.leJeu.dansMenu and self.continuer:
            if self.menuSelec == 1:
                self.leJeu.ecran_affiche = "pokemons"
                self.leJeu.mettre_a_jour = True
            elif self.menuSelec == 2:
                self.leJeu.ecran_affiche = "sac"
                self.leJeu.mettre_a_jour = True
            elif self.menuSelec == 3:
                if self.menuAffiche["ci"]:
                    self.menuAffiche["ci"] = False
                else:
                    self.razAffMenu()
                    self.menuAffiche["ci"] = True
            elif self.menuSelec == 4:
                self.laBdd.savPartie(self.leJeu.carte.nom_carte, self.leJeu.carte.joueur.position[0], self.leJeu.carte.joueur.position[1])
                self.menuAffiche["haut"] = False
            elif self.menuSelec == 5:
                pygame.quit()
            self.continuer = False

        elif not pygame.key.get_pressed()[pygame.K_ESCAPE] and not pygame.key.get_pressed()[pygame.K_DOWN] and not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[pygame.K_RETURN] and not self.continuer:
            self.continuer = True