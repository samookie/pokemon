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
          dmg INTEGER,
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
          spAtt INTEGER,
          defense INTEGER,
          spDef INTEGER,
          image TEXT,
          d_image TEXT,
          f_image TEXT
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
        self.createTPA()
        self.createPokemon()

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

    def createTPA(self):
        self.c.execute("""INSERT INTO Type_Att ("libelle")  VALUES ("Normal"),("Feu"),("Eau"),("Plante"),("Electrik"),
        ("Glace"),("Combat"),("Poison"),("Sol"),("Vol"),("Psy"),("Insecte"),("Roche"),
        ("Spectre"),("Dragon"),("Tenebres"),("Acier")
        """)
        self.conn.commit()

    '''Méthode permettant de récupérer les objets du héro'''
    def getObjSac(self):
        return self.c.execute("SELECT description, image, nbr FROM Objet").fetchall()

    def getPokemonHero(self):
        return self.c.execute("SELECT nomPoke, niveau, hp, image FROM Pokemon P JOIN Liste_Pokemon L ON P.idPoke = L.idPoke AND idHero = 1").fetchall()


    def createPokemon(self):
        self.c.execute(""" INSERT INTO Pokemon ("nomPoke","nomEvo","niveau","hp","vitesse","attaque","speAtt","defense","speDef","image","d_image","f_image") VALUES 
            ("Bulbizarre","Herbizarre",1,45,45,49,65,49,65,"bulbizarre","d_bulbizarre","f_bulbizarre"),
            ("Herbizarre","Ivysaure",1,60,60,62,80,63,80,"herbizarre","d_herbizarre","f_herbizarre"),
            ("Salamèche","Reptincel",1,39,65,52,60,43,50,"salamèche","d_salamèche","f_salamèche"),
            ("Reptincel","Dracaufeu",1,58,80,64,80,58,65,"reptincel","d_reptincel","f_reptincel"),
            ("Carapuce","Carabaffe",1,44,43,48,50,65,64,"carapuce","d_carapuce","f_carapuce"),
            ("Carabaffe","Tortank",1,59,58,63,65,80,80,"carabaffe","d_carabaffe","f_carabaffe"),
            ("Chenipan","Chrysacier",1,45,45,30,20,35,20,"chenipan","d_chenipan","f_chenipan"),
            ("Chrysacier","Papilusion",1,50,30,20,25,55,25,"chrysacier","d_chrysacier","f_chrysacier"),
            ("Aspicot","Coconfort",1,40,50,35,20,30,20,"aspicot","d_aspicot","f_aspicot"),
            ("Coconfort","Dardargnan",1,45,35,25,25,50,25,"coconfort","d_coconfort","f_coconfort"),
            ("Roucool","Roucoups",1,40,56,45,35,40,35,"roucool","d_roucool","f_roucool"),
            ("Roucoups","",1,63,71,60,50,55,50,"roucoups","d_roucoups","f_roucoups"),
            ("Rattata","Rattatac",1,30,72,56,25,35,35,"rattata","d_rattata","f_rattata"),
            ("Rattatac","",1,55,97,81,50,60,70,"rattatac","d_rattatac","f_rattatac"),
            ("Pikachu","Raichu",1,35,90,55,90,40,50,"pikachu","d_pikachu","f_pikachu"),
            ("Raichu","",1,60,110,90,90,5,50,"raichu","d_raichu","f_raichu"),
            ("Sabelette","Sablaireau",1,50,40,75,20,85,30,"sabelette","d_sabelette","f_sabelette"),
            ("Racaillou","Gravalanch",1,40,20,80,30,100,30,"racaillou","d_racaillou","f_racaillou"),
            ("Onix","",1,35,70,45,30,160,40,"onix","d_onix","f_onix");
        """)
        self.conn.commit()

    def createAtt(self):
        """
        libelle TEXT,
          dmg INTEGER,
          idTPA INTEGER,
        :return:
        """
        self.c.execute(""" INSERT INTO Attaque ("libelle",
        """)






