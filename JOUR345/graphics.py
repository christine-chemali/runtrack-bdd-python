import matplotlib.pyplot as plt
import mysql.connector
from database import Database

class Graphics:
    def __init__(self, db: Database):
        self.db = db

    def plot_quantity_by_category(self):
        query = """
        SELECT category.name, SUM(quantity)
        FROM product
        JOIN category ON product.id_category = category.id
        GROUP BY category.name;
        """
        return self.db.execute_query(query)

    def plot_distribution_of_products(self):
        query = """
        SELECT category.name, COUNT(product.id)
        FROM product
        JOIN category ON product.id_category = category.id
        GROUP BY category.name;
        """
        return self.db.execute_query(query)

    def plot_average_price_by_category(self):
        query = """
        SELECT category.name, AVG(product.price)
        FROM product
        JOIN category ON product.id_category = category.id
        GROUP BY category.name;
        """
        return self.db.execute_query(query)

    def plot_top_products_by_quantity(self):
        query = """
        SELECT product.name, product.quantity
        FROM product
        ORDER BY product.quantity DESC
        LIMIT 10;
        """
        return self.db.execute_query(query)

    def plot_total_stock_value_by_category(self):
        query = """
        SELECT category.name, SUM(product.price * product.quantity)
        FROM product
        JOIN category ON product.id_category = category.id
        GROUP BY category.name;
        """
        return self.db.execute_query(query)

    def execute_query(self, query):
        try:
            self.db.cursor.execute(query)
            data = self.db.cursor.fetchall()
            columns_names = [index[0] for index in self.db.cursor.description]
            return columns_names, data
        except mysql.connector.Error as error:
            raise Exception(f"Error while executing query: {error}")

    def plot_horizontal_bar_graph(self, ax, data, title):
        categories, values = zip(*data)
        ax.barh(categories, values)
        ax.set_title(title)
        ax.set_xlabel("TOTAL QUANTITY")
        ax.text(-0.1, 0.99, "CATEGORY", transform=ax.transAxes, rotation=0, ha='center', va='bottom', fontsize=10)


    def plot_donut_chart(self, ax, data, title):
        categories, values = zip(*data)
        wedges, texts, autotexts = ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=140, pctdistance=0.85)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = ax.figure
        fig.gca().add_artist(centre_circle)
        ax.set_title(title)
        ax.axis('equal')

    def plot_box_plot(self, ax, data, title):
        categories, values = zip(*data)
        ax.fill_betweenx(categories, 0, values, color='lightgreen', alpha=0.5)    
        ax.set_title(title)    
        ax.set_xlabel("VALUE")    
        ax.text(-0.1, 0.99, "CATEGORY", transform=ax.transAxes, rotation=0, ha='center', va='bottom', fontsize=10)

    def plot_dot_plot(self, ax, data, title):
        products, quantities = zip(*data)        
        ax.scatter(quantities, products, color='orange')    
        ax.set_title(title)    
        ax.set_xlabel("QUANTITY")    
        ax.text(-0.1, 0.99, "PRODUCT", transform=ax.transAxes, rotation=0, ha='center', va='bottom', fontsize=10)    
        for i, quantity in enumerate(quantities):        
            ax.text(quantity, products[i], str(quantity), fontsize=10, ha='left', va='center')

    def plot_tree_map(self, ax, data, title):
        categories, values = zip(*data)
        ax.barh(categories, values)
        ax.set_title(title)
        ax.set_xlabel("TOTAL STOCK VALUE")
        ax.text(-0.1, 0.99, "CATEGORY", transform=ax.transAxes, rotation=0, ha='center', va='bottom', fontsize=10)

        