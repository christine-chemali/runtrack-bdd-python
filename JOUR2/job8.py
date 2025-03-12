import mysql.connector

"""
For this exercice the database was created in mysql here the snipset
CREATE DATABASE zoo;

USE zoo;

CREATE TABLE animal
(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
nom VARCHAR (255) NOT NULL,
race VARCHAR (255) NOT NULL,
cage_id INT NOT NULL,
date_naissance DATE NOT NULL,
pays_origine VARCHAR (255) NOT NULL
);

CREATE TABLE cage
(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
superficie INT NOT NULL,
capacite INT
);

Also a lot of things can be improved like:
give the choice to change a specific field in choice 5 and 6 
for that update_animal, and update_cage has to be improved
errors handling (here 0 error handling... 
what if we put an animal in a cage that is already full ?)
add an .env (for the password)
and create the database and the table in python

"""

class Zoo :
    def __init__(self):
        self.db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = " ",
            database = "zoo"
        )
        self.cursor = self.db.cursor()

    def create_animal(self, nom, race, cage_id, date_naissance, pays_origine):
        self.cursor.execute ("INSERT INTO animal (nom, race, cage_id, date_naissance, pays_origine) VALUES (%s, %s, %s, %s, %s);", (nom, race, cage_id, date_naissance, pays_origine))
        self.db.commit()
        print("L'animal à été ajouté.")
    
    def create_cage(self, superficie, capacite):
        self.cursor.execute("INSERT INTO cage (superficie, capacite) VALUES (%s, %s);", (superficie, capacite))
        self.db.commit()
        print("La cage a été ajoutée.")

    def read_animal_in_cage(self):
        self.cursor.execute("SELECT cage.id, animal.nom FROM cage LEFT JOIN animal ON cage.id = animal.cage_id;")
        cages = self.cursor.fetchall()
        for cage in cages:
            print(f"Cage ID : {cage[0]}, Animal : {cage[1] if cage[1] else "Aucun animal"}")
    
    def read_animal (self):
        self.cursor.execute("SELECT * FROM animal;")
        animals = self.cursor.fetchall()
        for animal in animals:
            print(animal)
    
    def update_animal(self, id, nom, race, cage_id, date_naissance, pays_origine):
        self.cursor.execute("UPDATE animal SET nom = %s, race = %s, cage_id = %s, date_naissance = %s, pays_origine = %s WHERE id = %s;", (nom, race, cage_id, date_naissance, pays_origine, id))
        self.db.commit()
        print("L'animal a été modifié avec succès.")
    
    def update_cage(self, superficie, capacite, id):
        self.cursor.execute("UPDATE cage SET superficie = %s, capacite = %s WHERE id = %s;", (superficie, capacite, id))
        self.db.commit()
        print("La cage a été modifiée.")
    
    def delete_animal(self, id):
        self.cursor.execute("DELETE FROM animal WHERE id = %s;", (id,))
        self.db.commit()
        print("L'animal a été supprimé.")
    
    def delete_cage(self, id):
        self.cursor.execute("DELETE FROM cage WHERE id = %s;", (id,))
        self.db.commit()
        print("La cage a été supprimée.")
    
    def total_cage_area(self):
        self.cursor.execute("SELECT SUM(superficie) FROM cage;")
        total_area = self.cursor.fetchone()[0]
        print("Superficie totale des cages :", total_area)
    
    def close(self):
       self.cursor.close()
       self.db.close()

def main():
    zoo = Zoo()
    while True:
        print("\nmenu:")
        print("1. Ajouter un animal")
        print("2. Ajouter une cage")
        print("3. Afficher tous les animaux.")
        print("4. Afficher les animaux par cage")
        print("5. Modifier un animal")
        print("6. Modifier une cage")
        print("7. Supprimer un animal")
        print("8. Supprimer une cage")
        print("9. Calculer la superficie totale des cages")
        print("10. Quitter")
    
        choice = input("Choisissez une option : ")
        if choice == '1':
            nom = input("Entrez le nom de l'animal : ")
            race = input("Entrez la race de l'animal : ")
            cage_id = int(input("Entrez l'ID de la cage (ou 0 si sans cage) : "))
            date_naissance = input("Entrez la date de naissance (YYYY-MM-DD) : ")
            pays_origine = input("Entrez le pays d'origine : ")
            zoo.create_animal(nom, race, cage_id, date_naissance, pays_origine)
        
        elif choice == '2':
            superficie = float(input("Entrez la superficie de la cage : "))
            capacite = int(input("Entez la capacité de la cage : "))
            zoo.create_cage(superficie, capacite)

        elif choice == '3':
            print("Liste de tous les animaux : ")
            zoo.read_animal()
        
        elif choice == '4':
            print("Animaux par cage : ")
            zoo.read_animal_in_cage()
        
        elif choice == '5':
            id = int(input("Entrez l'ID de l'animal à modifier : "))
            nom = input("Entrez le nouveau nom de l'animal : ")
            race = input("Entrez la nouvelle race de l'animal : ")
            cage_id = int(input("Entrez le nouvel ID de la cage (ou 0 si sans cage) : "))
            date_naissance = input("Entrez la nouvelle date de naissance (YYYY-MM-DD) : ")
            pays_origine = input("Entrez le nouveau pays d'origine : ")
            zoo.update_animal(id, nom, race, cage_id, date_naissance, pays_origine)
        
        elif choice == '6':
            id = int(input("Entrez L'ID de la cage à modifier : "))
            superficie = int(input("Entrez la nouvelle superficie de la cage : "))
            capacite = int(input("Entrez la nouvelle capacité de la cage : "))
            zoo.update_cage(id, superficie, capacite)
        
        elif choice == '7':
            id = int(input("Entrez l'ID de l'animal à supprimer : "))
            zoo.delete_animal(id)
        
        elif choice == '8':
            id = int(input("Entrez l'ID de la cage à supprimer : "))
            zoo.delete_cage(id)
        
        elif choice == '9':
            zoo.total_cage_area()

        elif choice == '10':
            zoo.close()
            break
        else:
            print("Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()

