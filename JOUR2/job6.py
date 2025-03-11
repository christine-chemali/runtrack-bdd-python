import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = " ",
    database = "LaPlateforme"
)

cursor = db.cursor()
cursor.execute("SELECT SUM(capacite) FROM salle;")

results = cursor.fetchone()[0]
print("La capacité de toutes les salles est de :", results)

cursor.close()
db.close()