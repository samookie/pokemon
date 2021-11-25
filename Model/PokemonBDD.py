import datetime
import sqlite3

class PokemonBDD():

    '''Modèle pour la BDD'''
    def __init__(self):
        self.conn = sqlite3.connect('Model/PokemonBDD.db')
        self.c = self.conn.cursor()

    '''Méthode permettant de créer la BDD'''
    def createBDD(self):
        self.c.execute("""
        CREATE TABLE Dialogue(
            idDial INTEGER PRIMARY KEY,
            dialogue TEXT
        );
        """)

        self.c.execute("""
        CREATE TABLE Sac(
          idSac INTEGER PRIMARY KEY,
          taille INTEGER
        );

        """)

        self.c.execute("""
        CREATE TABLE Objet(
          idObj INTEGER PRIMARY KEY,
          description TEXT,
          type TEXT,
          image TEXT,
          idSac INTEGER,
          nbr INTEGER,
          FOREIGN KEY (idSac) REFERENCES Sac(idSac)
        );

        """)

        self.c.execute("""
        CREATE TABLE Type_Att(
          idTPA INTEGER PRIMARY KEY,
          libelle TEXT
        );
        """)

        self.c.execute("""
        CREATE TABLE Attaque(
          idAtt INTEGER PRIMARY KEY,
          libelle TEXT,
          idTPA INTEGER,
          FOREIGN KEY (idTPA) REFERENCES Type_Att(idTPA)
        );
        """)

        self.c.execute("""
        CREATE TABLE Hero(
          idHero INTEGER PRIMARY KEY,
          nom TEXT,
          sexe TEXT,
          argent INTEGER,
          pos_x INTEGER,
          pos_y INTEGER,
          idSac INTEGER,
          FOREIGN KEY (idSac) REFERENCES Sac(idSac)
        );
        """)

        self.c.execute("""
        CREATE TABLE Game(
          idGame INTEGER PRIMARY KEY,
          sauvegarde_dh TEXT,
          monde TEXT,
          idHero INTEGER,
          FOREIGN KEY (idHero) REFERENCES Hero(idHero)
        );
        """)

        self.c.execute("""
        CREATE TABLE Pokemon(
          idPoke INTEGER PRIMARY KEY,
          nomPoke TEXT,
          nom TEXT,
          nomEvo TEXT,
          niveau INTEGER,
          hp INTEGER,
          vitesse INTEGER,
          attaque INTEGER,
          defense INTEGER,
          image INTEGER
        );
        """)

        self.c.execute("""
        CREATE TABLE Liste_Pokemon(
         idHero INTEGER,
          idPoke INTEGER,
          PRIMARY KEY (idHero, idPoke),
          FOREIGN KEY (idHero) REFERENCES Hero(idHero),
          FOREIGN KEY (idPoke) REFERENCES Pokemon(idPoke)
        );
        """)

        self.c.execute("""
        CREATE TABLE Liste_Attaque(
          idAtt INTEGER,
          idPoke INTEGER,
          PRIMARY KEY (idAtt, idPoke),
          FOREIGN KEY (idAtt) REFERENCES Attaque(idAtt),
          FOREIGN KEY (idPoke) REFERENCES Pokemon(idPoke)
        );
        """)

        self.createTPokemon()


    '''Méthode permettant de reset la BDD'''
    def resetBDD(self):
        self.c.execute("DROP TABLE IF EXISTS Dialogue")
        self.c.execute("DROP TABLE IF EXISTS Game")
        self.c.execute("DROP TABLE IF EXISTS Sac")
        self.c.execute("DROP TABLE IF EXISTS Objet")
        self.c.execute("DROP TABLE IF EXISTS Type_Att")
        self.c.execute("DROP TABLE IF EXISTS Attaque")
        self.c.execute("DROP TABLE IF EXISTS Hero")
        self.c.execute("DROP TABLE IF EXISTS Pokemon")
        self.c.execute("DROP TABLE IF EXISTS Liste_Pokemon")
        self.c.execute("DROP TABLE IF EXISTS Liste_Attaque")
        self.createBDD()
        self.createTPokemon()

    '''Méthode permettant de créer le Héro'''
    def creationPersonnage(self, nomJoueur, sexe):
        self.c.execute("INSERT INTO Sac VALUES (1, 10)")
        self.c.execute("INSERT INTO Hero VALUES (1, ?, ?, 0, 0, 0, 1)", [nomJoueur, sexe])
        self.conn.commit()

    '''Méthode permettant de récupérer le sexe du Héro'''
    def getSexePersonnage(self):
        return self.c.execute("SELECT sexe FROM Hero").fetchone()

    '''Méthode permettant de vérifier si une sauvegarde existe'''
    def getSavExist(self):
        return self.c.execute("SELECT COUNT(*) FROM Game").fetchone()

    '''Méthode pour sauvegarder la partie'''
    def savPartie(self, carte, x, y):
        self.c.execute("DELETE FROM Game")
        self.c.execute("UPDATE Hero SET pos_x = ?, pos_y = ?", [x, y])
        self.c.execute("INSERT INTO Game VALUES (1, ?, ?, 1)", [datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), carte])
        self.conn.commit()

    '''Méthode pour récupérer les infos de sauvegarde de la partie'''
    def getInfosChargerSav(self):
        hero = self.c.execute("SELECT sexe, pos_x, pos_y FROM Hero").fetchone()
        game = self.c.execute("SELECT monde FROM Game").fetchone()
        return hero[0], hero[1], hero[2], game[0]

    '''Méthode pour récupérer les infos du Héro'''
    def chargerInfosHero(self):
        return self.c.execute("SELECT idHero, nom, sexe, argent FROM Hero").fetchone()

    def createTPokemon(self):
        self.c.execute("""INSERT INTO Type_Att ("libelle")  VALUES ("Normal"),("Fire"),("Water"),("Grass"),("Electric"),
        ("Ice"),("Fighting"),("Poison"),("Ground"),("Flying"),("Psychic"),("Bug"),("Rock"),
        ("Ghost"),("Dragon"),("Dark"),("Steel")
        """)
        self.conn.commit()

    '''Méthode permettant de récupérer les objets du héro'''
    def getObjSac(self):
        return self.c.execute("SELECT description, image, nbr FROM Objet").fetchall()

    def getPokemonHero(self):
        return self.c.execute("SELECT nomPoke, niveau, hp, image FROM Pokemon P JOIN Liste_Pokemon L ON P.idPoke = L.idPoke AND idHero = 1").fetchall()





