import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = " ",
    database = "societe"
)

cursor = db.cursor()
cursor.execute("SELECT * FROM employe WHERE salaire > 3000;")
results = cursor.fetchall()

print (results)
print("------------------------------")

cursor.execute("SELECT employe.prenom, service.nom FROM employe INNER JOIN service ON employe.id_service = service.id;")
results = cursor.fetchall()

print(results)
print("---------------------------------------")

cursor.close()
db.close()

class Employe:
    def __init__(self):
        self.db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = " ",
            database = "societe"
            )
        self.cursor = self.db.cursor()

    def create_employe(self):
        self.cursor.execute("INSERT INTO employe (nom, prenom, salaire, id_service) VALUES ('HotDog', 'Arielle', 1980, 1);")
        self.db.commit()
        print("Employé créé.")

    def read_employe(self):
        self.cursor.execute("SELECT * FROM employe WHERE salaire < 3000;")
        results = self.cursor.fetchall()
        print( "Employés dont le salaire est infèrieur à 3000 :", results)
    
    def update_employe(self):
        self.cursor.execute("UPDATE employe SET salaire = 4500 WHERE id = 1;")
        self.db.commit()
        print("Employé mis à jour.")
    
    def delete_employe(self):
        self.cursor.execute("DELETE FROM employe WHERE id=7;")
        self.db.commit()
        print("Employé supprimé.")

    def show_all_employe(self):
        self.cursor.execute("SELECT * FROM employe;")
        results = self.cursor.fetchall()
        print(results)
    
    def close(self):
        self.cursor.close()
        self.db.close()

employe_crud = Employe()
employe_crud.create_employe()
employe_crud.read_employe()
employe_crud.update_employe()
employe_crud.delete_employe()
employe_crud.show_all_employe()
employe_crud.close()