from database import Database
import mysql.connector

class Product:
    def __init__(self, db: Database):
        self.db = db

    def get_all_products(self):
        """Retrieve all products with their categories."""
        cursor = None
        try:
            cursor = self.db.get_cursor()  
            cursor.execute("SELECT product.id, product.name, product.description, product.price, product.quantity, product.id_category, category.name AS category_name FROM product LEFT JOIN category ON product.id_category = category.id;")
            rows = cursor.fetchall()
            return rows  
        except mysql.connector.Error as error:
            raise Exception(f"Error retrieving products: {error}")
        finally:
            if cursor:
                cursor.close()

    def add_product(self, name, description, price, id_category, quantity):
        """Add a new product to the database."""
        if not (name.replace(" ", "").isalpha() and description.replace(" ", "").isalpha()):
            raise ValueError("Name and description must contain only letters.")
        if not price.isdigit() or not id_category.isdigit() or not quantity.isdigit():
            raise ValueError("Price, Category ID, and Quantity must be integers.")
        if not name or not description or price == "" or id_category == "" or quantity == "":
            raise ValueError("All fields must be filled out.")

        cursor = None
        try:
            cursor = self.db.get_cursor()  
            cursor.execute("INSERT INTO product (name, description, price, id_category, quantity) VALUES (%s, %s, %s, %s, %s)",
                           (name, description, float(price), int(id_category), int(quantity)))
            self.db.db.commit()
        except mysql.connector.Error as error:
            raise Exception(f"Error adding product: {error}")
        finally:
            if cursor:
                cursor.close() 

    def delete_product(self, product_id):
        """Delete a product from the database."""
        if not product_id.isdigit():
            raise ValueError("Product ID must be an integer.")
        
        cursor = None
        try:
            cursor = self.db.get_cursor()  
            cursor.execute("DELETE FROM product WHERE id = %s", (int(product_id),))
            self.db.db.commit()  
        except mysql.connector.Error as error:
            raise Exception(f"Error deleting product: {error}")
        finally:
            if cursor:
                cursor.close()  

    def update_product_name(self, product_id, new_name):
        """Update product name."""
        if not new_name.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters.")
        if not product_id.isdigit():
            raise ValueError("Product ID must be an integer.")

        cursor = None
        try:
            cursor = self.db.get_cursor()  
            cursor.execute("UPDATE product SET name = %s WHERE id = %s;", (new_name, int(product_id)))
            self.db.db.commit() 
        except mysql.connector.Error as error:
            raise Exception(f"Error updating product name: {error}")
        finally:
            if cursor:
                cursor.close() 

    def update_product_description(self, product_id, new_description):
        """Update product description."""
        if not new_description.replace(" ", "").isalpha():
            raise ValueError("Description must contain only letters.")
        if not product_id.isdigit():
            raise ValueError("Product ID must be an integer.")
        
        cursor = None
        try:
            cursor = self.db.get_cursor() 
            cursor.execute("UPDATE product SET description = %s WHERE id = %s;", (new_description, int(product_id)))
            self.db.db.commit()
        except mysql.connector.Error as error:
            raise Exception(f"Error updating product description: {error}")
        finally:
            if cursor:
                cursor.close()  

    def update_product_price(self, product_id, new_price):
        """Update product price."""
        if not new_price.isdigit():
            raise ValueError("Price must be an integer.")
        if not product_id.isdigit():
            raise ValueError("Product ID must be an integer.")
        
        cursor = None
        try:
            cursor = self.db.get_cursor() 
            cursor.execute("UPDATE product SET price = %s WHERE id = %s;", (float(new_price), int(product_id)))
            self.db.db.commit() 
        except mysql.connector.Error as error:
            raise Exception(f"Error updating product price: {error}")
        finally:
            if cursor:
                cursor.close() 

    def update_product_category(self, product_id, new_category_id):
        """Update product category."""
        if not new_category_id.isdigit():
            raise ValueError("Category ID must be an integer.")
        if not product_id.isdigit():
            raise ValueError("Product ID must be an integer.")
        
        cursor = None
        try:
            cursor = self.db.get_cursor()  
            cursor.execute("UPDATE product SET id_category = %s WHERE id = %s;", (int(new_category_id), int(product_id)))
            self.db.db.commit() 
        except mysql.connector.Error as error:
            raise Exception(f"Error updating product category: {error}")
        finally:
            if cursor:
                cursor.close()

    def update_product_quantity(self, product_id, new_quantity):
        """Update product quantity."""
        if not new_quantity.isdigit():
            raise ValueError("Quantity must be an integer.")
        if not product_id.isdigit():
            raise ValueError("Product ID must be an integer.")
        
        cursor = None
        try:
            cursor = self.db.get_cursor()  
            cursor.execute("UPDATE product SET quantity = %s WHERE id = %s;", (int(new_quantity), int(product_id)))
            self.db.db.commit() 
        except mysql.connector.Error as error:
            raise Exception(f"Error updating product quantity: {error}")
        finally:
            if cursor:
                cursor.close()  