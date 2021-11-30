import pygame

class Pokemon():

    def __init__(self, leJeu, nomPoke, nom, nomEvo,niveau, hp, vitesse, attaque, speAtt, defense, speDef, image, d_image, f_image ):
        self.jeu = leJeu
        self.nomPokemon = nomPoke
        self.nom = nom
        self.nomEvo = nomEvo
        self.niveau = niveau
        self.hp = hp
        self.vitesse = vitesse
        self.attaque = attaque
        self.speAtt = speAtt
        self.defense = defense
        self.speDef = speDef
        self.image = image
        self.d_image = d_image
        self.f_image = f_image

    def levelUp(self):
        self.niveau += 1
        self.attaque += 3
        self.speAtt += 3
        self.defense += 3
        self.speDef += 3

    def getPokemon(self):
        listeCaractPokemon = [self.nomPokemon,
                               self.nom,
                               self.nomEvo,
                               self.niveau,
                               self.hp,
                               self.vitesse,
                               self.attaque,
                               self.speAtt,
                               self.defense,
                               self.speDef,
                               self.image,
                               self.d_image,
                               self.f_image]

        return listeCaractPokemon

    def setLevelPokemon (self, level):
        if level != self.niveau:
            self.niveau = level
            self.hp += level*3
            self.attaque += level*3
            self.speAtt += level*3
            self.defense += level*3
            self.speDef += level*3





