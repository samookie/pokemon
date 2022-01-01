import pygame

from Classes.Animation import Animation


class TypePokemon():

    def __init__(self):
        self.listeDouble = [["Feu", "Plante", "Glace", "Insect", "Acier"],
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
        self.listeFaiblesse = [["Normal", "Roche", "Acier"],
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
        self.listeAucun = [["Normal", "Spectre"],
                      ["Electrik", "Sol"],
                      ["Combat", "Spectre"],
                      ["Poison", "Acier"],
                      ["Sol", "Vol"],
                      ["Psy", "Tenebres"],
                      ["Spectre", "Normal"]
                      ]

    def information(self,typeAllie, typeEnnemie):
        listeRep = []
        count = 0
        for double in range(len(self.listeDouble )):
            if self.listeDouble[double][0] == typeAllie:
                count = double
                for j in range(len(self.listeDouble[count])):
                    if self.listeDouble[count][j] == typeEnnemie:
                        listeRep = [1, 0, 0]
        count = 0
        for double in range(len(self.listeFaiblesse)):
            if self.listeFaiblesse[double][0] == typeAllie:
                count = double
                for j in range(len(self.listeFaiblesse[count])):
                    if self.listeFaiblesse[count][j] == typeEnnemie:
                        listeRep = [0, 1, 0]

        count = 0
        for double in range(len(self.listeAucun)):
            if self.listeAucun[double][0] == typeAllie:
                count = double
                for j in range(len(self.listeAucun[count])):
                    if self.listeAucun[count][j] == typeEnnemie:
                        listeRep = [0, 0, 1]

        return listeRep