import pygame

class Home_Screen:

    def __init__(self, leJeu):
        home_screen_img = pygame.image.load("Map/Images/testHome.png")

        leJeu.screen.blit(home_screen_img, (0, 0))
        pygame.display.flip()

        if(pygame.key.get_pressed() == pygame.K_f):
            leJeu.ecran_affiche = "jeu"
            leJeu.mettre_a_jour = True

        if(leJeu.mettre_a_jour == True):
            pygame.mixer.init()
            musique = pygame.mixer.Sound("Map/Musiques/pokemon_main-theme.wav")
            musique.play()
            leJeu.mettre_a_jour = False
