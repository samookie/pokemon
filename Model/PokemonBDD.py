import sqlite3

conn = sqlite3.connect('PokemonBDD.db')

c = conn.cursor()

#c.execute("""
#CREATE TABLE Dialogue(
#    idDial INTEGER PRIMARY KEY,
#    dialogue TEXT
#);
#"""")

#c.execute("""
#CREATE TABLE Game(
#  idGame INTEGER PRIMARY KEY,
#  sauvegarde_dh TEXT
#);
    
#""")

#c.execute("""
#CREATE TABLE Sac(
#  idSac INTEGER PRIMARY KEY,
#  taille INTEGER
#);

#""")

#c.execute("""
#CREATE TABLE Objet(
#  idObj INTEGER PRIMARY KEY,
#  description TEXT,
#  type TEXT,
#  image TEXT,
#  idSac INTEGER,
#  FOREIGN KEY (idSac) REFERENCES Sac(idSac)
#);

#""")

#c.execute("""
#CREATE TABLE Type_Pokemon(
#  idTP INTEGER PRIMARY KEY,
#  libelle TEXT
#);
#""")


#c.execute("""
#CREATE TABLE Attaque(
#  idAtt INTEGER PRIMARY KEY,
#  libelle TEXT
#);
#""")

#c.execute("""
#CREATE TABLE Hero(
#  idHero INTEGER PRIMARY KEY,
#  nom TEXT,
#  sexe TEXT,
#  argent INTEGER,
#  pos_x INTEGER,
#  pos_y INTEGER,
#  idSac INTEGER,
#  FOREIGN KEY (idSac) REFERENCES Sac(idSac)
#);
#""")

#c.execute("""
#CREATE TABLE Pokemon(
#  idPoke INTEGER PRIMARY KEY,
#  nomPoke TEXT,
#  nom TEXT,
#  niveau INTEGER,
#  hp INTEGER,
#  vitesse INTEGER,
#  attaque INTEGER,
#  defense INTEGER,
#  image INTEGER,
#  idTP INTEGER,
#  FOREIGN KEY (idTP) REFERENCES Type_Pokemon(idTP)
#);
#""")

#c.execute("""
#CREATE TABLE Liste_Pokemon(
# idHero INTEGER,
#  idPoke INTEGER,
#  PRIMARY KEY (idHero, idPoke),
#  FOREIGN KEY (idHero) REFERENCES Hero(idHero),
#  FOREIGN KEY (idPoke) REFERENCES Pokemon(idPoke)
#);
#""")

#c.execute("""
#CREATE TABLE Liste_Attaque(
#  idAtt INTEGER,
#  idPoke INTEGER,
#  PRIMARY KEY (idAtt, idPoke),
#  FOREIGN KEY (idAtt) REFERENCES Attaque(idAtt),
#  FOREIGN KEY (idPoke) REFERENCES Pokemon(idPoke)
#);
#""")

c.execute("INSERT Dialogue VALUES ('Je test') ")

conn.commit()

conn.close()