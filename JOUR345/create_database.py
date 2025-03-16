import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()
passw = os.getenv("PASSWORD")

def create_database_and_tables():
    """To create the database and tables"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=passw
        )
        
        cursor = connection.cursor() 

        cursor.execute("CREATE DATABASE IF NOT EXISTS store")
        print("Database 'store' created successfully.")

        cursor.execute("USE store")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS product(
            id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            price INT NOT NULL,
            id_category INT NOT NULL,
            quantity INT NOT NULL,)
        ''')
        print("Table 'product' created successfully.")

        cursor.execute('''  # Fixed typo here
            CREATE TABLE IF NOT EXISTS category (
                id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL )
        ''')

        print("Table 'category' created successfully.")

    except Error as error:
        print(f"An error occurred: {error}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():  
            connection.close()
        print("Database connection is closed.")

if __name__ == "__main__":
    create_database_and_tables()