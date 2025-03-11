import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = " ",
    database = "LaPlateforme"
)

cursor = db.cursor()
cursor.execute("SELECT SUM(superficie) FROM etage;")

results = cursor.fetchone()[0]
print("La superficie de la Plateforme est de", results, "m2.")

cursor.close()
db.close()
