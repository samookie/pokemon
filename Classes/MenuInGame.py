import pygame.draw


class MenuInGame():

    def __init__(self, leJeu):
        self.leJeu = leJeu
        self.text = pygame.font.Font("Map/Polices/Pokemon.ttf", 15)  # Initialiser la police pour le texte

        self.continuer = True
        self.menuAffiche = {
            "haut": False
        }

    def affichage(self):
        self.gestion_touches()
        if self.menuAffiche["haut"]:
            self.creationMenuHautDroite()


    def creationMenuHautDroite(self):
        pygame.draw.rect(self.leJeu.screen, (255, 255, 255, 100), pygame.Rect(490, 10, 200, 125))
        pygame.draw.rect(self.leJeu.screen, (0, 0, 0), pygame.Rect(490, 10, 200, 125), 2)
        self.leJeu.screen.blit(self.text.render("Pokémons", True, (0, 0, 0)), (500, 15))
        self.leJeu.screen.blit(self.text.render("Sac", True, (0, 0, 0)), (500, 35))
        self.leJeu.screen.blit(self.text.render("Joueur", True, (0, 0, 0)), (500, 55))
        self.leJeu.screen.blit(self.text.render("Sauvegarder", True, (0, 0, 0)), (500, 75))
        self.leJeu.screen.blit(self.text.render("Quitter", True, (0, 0, 0)), (500, 95))

    def gestion_touches(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE] and self.continuer:
            if self.menuAffiche["haut"]:
                self.menuAffiche["haut"] = False
            else:
                self.menuAffiche["haut"] = True
            self.continuer = False
        elif not pygame.key.get_pressed()[pygame.K_ESCAPE] and not self.continuer:
            self.continuer = True