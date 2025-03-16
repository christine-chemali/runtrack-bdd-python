from database import Database
import mysql.connector

class Exportcsv:
    def __init__(self, db: Database):
        self.db = db
    
    def export_all_products(self):
        """Export all products csv file"""
        try :
            cursor = self.db.get_cursor()
            cursor.execute("SELECT * FROM product")
            rows = cursor.fetchall()
            columns_names = [index[0] for index in cursor.description]
            return columns_names, rows
        
        except mysql.connector.Error as error:
            raise Exception (f"Error while connecting to the database: {error}.")

        finally:
            if cursor:
                cursor.close() 
    
    def export_products_by_category(self, id_category):
        """Export products based on category csv file"""
        if not id_category.isdigit():
            raise ValueError ("Please, enter a valid category ID.")
        
        try :
            cursor = self.db.get_cursor()
            cursor.execute("SELECT COUNT(*) FROM category WHERE id = %s", (id_category,))
            exists = cursor.fetchone()[0] > 0

            if not exists:
                raise ValueError ("This ID does not exist in the database.")
            
            cursor.execute("SELECT * FROM product WHERE id_category = %s", (id_category,))
            rows = cursor.fetchall()
            columns_names = [index[0] for index in cursor.description]
            return rows, columns_names

        except mysql.connector.Error as error:
            raise Exception (f"Error while connecting to the database: {error}.")
        
        finally:
            if cursor:
                cursor.close()
    