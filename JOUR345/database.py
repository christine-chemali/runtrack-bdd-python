import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()
passw = os.getenv("PASSWORD")

class Database:
    def __init__(self):
        """To use the database"""
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=passw,
                database="store"
            )
            print("Database connection is done.")
        except mysql.connector.Error as databaseerror:
            print(f"An error occurred while connecting to the database: {databaseerror}")
            self.db = None
            
    def close(self):
        """To close the database connection"""
        if self.db and self.db.is_connected():
            self.db.close()
            print("The database connection is closed.")

    def get_cursor(self):
        """Get a new cursor from the connection"""
        if self.db is not None and self.db.is_connected():
            return self.db.cursor()
        else:
            raise Exception("Database connection is not established.")

    def execute_query(self, query):
        """Execute a SQL query and return the results."""
        try:
            cursor = self.get_cursor()  
            cursor.execute(query)
            data = cursor.fetchall()
            columns_names = [desc[0] for desc in cursor.description]
            return columns_names, data
        except mysql.connector.Error as error:
            raise Exception(f"Error while executing query: {error}")
        finally:
            cursor.close() 