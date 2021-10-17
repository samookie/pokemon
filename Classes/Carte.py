import pyscroll
import pytmx

class Carte:

    '''Méthode permettant de charger la map principale du jeu'''
    def carte_princiaple(self, taille):
        tmx_data = pytmx.util_pygame.load_pygame("Map/ville.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, taille)
        map_layer.zoom = 3

        return map_layer

    '''Méthode permettant de charger la map principale du jeu'''

    def carte_magasin(self, taille):
        tmx_data = pytmx.util_pygame.load_pygame("Map/magasin.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, taille)
        map_layer.zoom = 3

        return map_layer