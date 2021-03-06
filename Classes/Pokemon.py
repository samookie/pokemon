import pygame

class Pokemon():

    def __init__(self, leJeu, nomPoke, nom, nomEvo, niveau, hp, vitesse, attaque, speAtt, defense, speDef, image, d_image, f_image,typePoke ):
        self.jeu = leJeu
        self.nomPokemon = nomPoke #nom personnalisé du pokémon
        self.nom = nom #nom de base du pokémon
        self.nomEvo = nomEvo
        self.niveau = niveau
        self.hp = hp
        self.hpActu = self.hp
        self.vitesse = vitesse
        self.attaque = attaque
        self.speAtt = speAtt
        self.defense = defense
        self.speDef = speDef
        self.image = image # petite image du pokémon
        self.d_image = d_image # image de dos du pokémon
        self.f_image = f_image # image de face du pokémon
        self.xp = 0
        self.xp_max = 15
        self.typeP = typePoke
        self.lvlExp = [[1,15,6],[2,37,15],[3,70,25],[4,115,50],[5,169,60],
                       [6,231,75],[7,305,98],[8,384,117],[9,474,147],[10,569,205],
                       [11,672,222],[12,781,263],[13,897,361],[14,1.018,366],[15,1.144,500],
                       [16,1.274,584],[17,1.409,689],[18,1.547,794],[19,1.689,914],[20,1.832,1.042],[21,2.001,1.100],[22,2.101,1.120],[23,2.221,1.190],[24,2.301,1.200],[25,2.401,1.300],[26,2.501,1.400]] # tableau comprenant le level, le max d'xp et l'exp donnée par un combat avec le niveau

    def levelUp(self):
        self.niveau += 1
        self.attaque += 3
        self.speAtt += 3
        self.defense += 3
        self.speDef += 3
        self.xp = 0

        xpNiv = self.niveau
        if xpNiv == 1 :
            xpNiv = 0
        else:
            xpNiv = self.niveau - 1

        self.xp_max = self.lvlExp[xpNiv][1]

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
                               self.f_image,
                               self.hpActu,
                               self.xp,
                               self.xp_max,
                               self.typeP]
        return listeCaractPokemon

    def setLevelPokemon (self, level):
        if level != self.niveau:
            self.niveau = level
            self.hp += level*3
            self.attaque += level*3
            self.speAtt += level*3
            self.defense += level*3
            self.speDef += level*3
            self.hpActu += level*3

            xpNiv = level
            if xpNiv == 1:
                xpNiv = 0
            else:
                xpNiv = level - 1

            self.xp_max = self.lvlExp[xpNiv][1]

    def xp_up(self, xp):
        self.xp += xp
        if self.xp >= self.xp_max:
           self.levelUp()

    def soignerPokemon(self):
        self.hpActu = self.hp

    def soigner(self, hp):
        if (hp + self.hpActu) >= self.hp:
            self.hpActu = self.hp
        else:
            self.hpActu += hp

    def infoXP(self, niveauEnnemi):
        xp = 0
        if niveauEnnemi == 1:
            xp = 4
        else :
            print("xp actuelle :", self.xp , "sur xp max :" , self.xp_max)
            xp = self.lvlExp[niveauEnnemi-1][2]

        self.xp_up(xp)




