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
          FOREIGN KEY (idSac) REFERENCES Sac(idSac)
        );

        """)

        self.c.execute("""
        CREATE TABLE Type_Pokemon(
          idTP INTEGER PRIMARY KEY,
          libelle TEXT
        );
        """)

        self.c.execute("""
        CREATE TABLE Attaque(
          idAtt INTEGER PRIMARY KEY,
          libelle TEXT
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
          niveau INTEGER,
          hp INTEGER,
          vitesse INTEGER,
          attaque INTEGER,
          defense INTEGER,
          image INTEGER,
          idTP INTEGER,
          FOREIGN KEY (idTP) REFERENCES Type_Pokemon(idTP)
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


    '''Méthode permettant de reset la BDD'''
    def resetBDD(self):
        self.c.execute("DROP TABLE Dialogue")
        self.c.execute("DROP TABLE Game")
        self.c.execute("DROP TABLE Sac")
        self.c.execute("DROP TABLE Objet")
        self.c.execute("DROP TABLE Type_Pokemon")
        self.c.execute("DROP TABLE Attaque")
        self.c.execute("DROP TABLE Hero")
        self.c.execute("DROP TABLE Pokemon")
        self.c.execute("DROP TABLE Liste_Pokemon")
        self.c.execute("DROP TABLE Liste_Attaque")
        self.createBDD()

    '''Méthode permettant de créer le Héro'''
    def creationPersonnage(self, nomJoueur, sexe):
        self.c.execute("INSERT INTO Sac VALUES (null, 10)")
        self.c.execute("INSERT INTO Hero VALUES (null, ?, ?, 0, 0, 0, 1)", [nomJoueur, sexe])
        self.conn.commit()

    '''Méthode permettant de récupérer le sexe du Héro'''
    def getSexePersonnage(self):
        return self.c.execute("SELECT sexe FROM Hero").fetchone()

    '''Méthode permettant de vérifier si une sauvegarde existe'''
    def getSavExist(self):
        return self.c.execute("SELECT COUNT(*) FROM Game").fetchone()