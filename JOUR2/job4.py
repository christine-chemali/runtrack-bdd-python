import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = " ",
    database = "LaPlateforme"
)

cursor = db.cursor()

cursor.execute("SELECT nom, capacite FROM salle;")

results = cursor.fetchall()
print(results)
cursor.close()