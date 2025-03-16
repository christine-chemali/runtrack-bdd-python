import tkinter as tk
from tkinter import filedialog, messagebox 
from exportcsv import Exportcsv
from database import Database
from graphics import Graphics
from product import Product 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import csv

class Application(tk.Tk):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.export = Exportcsv(self.db)
        self.graphics = Graphics(self.db)
        self.product_manager = Product(self.db)
        self.title("Inventory Management")
        self.geometry("1000x900")  

        self.setup_ui()
        self.refresh_product_list()

    def setup_ui(self):
        """Setup the main UI components"""

        # Create a canvas and a scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.setup_main_frame()

    def setup_main_frame(self):
        """Setup the main UI components in the scrollable frame"""

        button_font = ('Arial', 10)
        # Top frame for graph display
        self.top_frame = tk.Frame(self.scrollable_frame)
        self.top_frame.pack(fill=tk.BOTH, expand=True)

        # Left side for graph display
        self.left_top_frame = tk.Frame(self.top_frame)
        self.left_top_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right side for graph buttons
        self.right_top_frame = tk.Frame(self.top_frame)
        self.right_top_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=50, pady=15)

        # Display area for the graph
        self.graph_display_frame = tk.Frame(self.left_top_frame)
        self.graph_display_frame.pack(fill=tk.BOTH, expand=True)

        # Create buttons for different graphs
        for title, graph_method in ([
            ("Quantities by Category", self.graphics.plot_quantity_by_category),
            ("Distribution of Products", self.graphics.plot_distribution_of_products),
            ("Average Price by Category", self.graphics.plot_average_price_by_category),
            ("Top Products by Quantity", self.graphics.plot_top_products_by_quantity), 
            ("Total Stock Value by Category", self.graphics.plot_total_stock_value_by_category)
        ]):
            btn_show_graph = tk.Button(self.right_top_frame, text=title, command=lambda method=graph_method: self.update_graph(method), width=25, font=button_font)
            btn_show_graph.pack(pady=15)

        # Initially display the first graph
        self.current_graph_method = self.graphics.plot_quantity_by_category
        self.display_graph(self.current_graph_method)

        # Frame for product list and export buttons
        self.left_frame = tk.Frame(self.scrollable_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Listbox for product list
        self.product_list = tk.Listbox(self.left_frame)
        self.product_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_product = tk.Scrollbar(self.left_frame, orient=tk.VERTICAL, command=self.product_list.yview)    
        self.scrollbar_product.pack(side=tk.RIGHT, fill=tk.Y)    
        self.product_list.config(yscrollcommand=self.scrollbar_product.set)

        # Button to export all products
        btn_export_all = tk.Button(self.left_frame, text="Export all products", command=self.export_all, width=20, font=button_font)
        btn_export_all.pack(padx=15, pady=15)

        # Label and entry for category ID
        label_id_category = tk.Label(self.left_frame, text="Category ID: ")
        label_id_category.pack(pady=15)
        self.entry_id_category = tk.Entry(self.left_frame)
        self.entry_id_category.pack(pady=15)

        # Button to export products by category
        btn_export_category = tk.Button(self.left_frame, text="Export by category", command=self.export_by_category, width=20, font=button_font)
        btn_export_category.pack(padx=15, pady=15)

        # Right side for product creation, deletion, and modification
        self.right_frame = tk.Frame(self.scrollable_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Section for creating a new product
        self.create_product_frame = tk.LabelFrame(self.right_frame, text="Create new product")
        self.create_product_frame.pack(padx=15, pady=15)

        tk.Label(self.create_product_frame, text="Product Name:").grid(row=0, column=0, sticky=tk.W)
        self.entry_product_name = tk.Entry(self.create_product_frame)
        self.entry_product_name.grid(row=0, column=1)

        tk.Label(self.create_product_frame, text="Category ID:").grid(row=0, column=2, sticky=tk.W)
        self.entry_category_id = tk.Entry(self.create_product_frame)
        self.entry_category_id.grid(row=0, column=3)

        tk.Label(self.create_product_frame, text="Description: ").grid(row=1, column=0, sticky=tk.W, columnspan=2)
        description_frame = tk.Frame(self.create_product_frame)
        description_frame.grid(row=1, column=2, columnspan=2)

        self.text_description = tk.Text(description_frame, height=5, width=50)
        self.text_description.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(description_frame, command=self.text_description.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_description.config(yscrollcommand=self.scrollbar.set)

        tk.Label(self.create_product_frame, text="Price:").grid(row=2, column=0, sticky=tk.W)
        self.entry_product_price = tk.Entry(self.create_product_frame)
        self.entry_product_price.grid(row=2, column=1)

        tk.Label(self.create_product_frame, text="Quantity:").grid(row=2, column=2, sticky=tk.W)
        self.entry_product_quantity = tk.Entry(self.create_product_frame)
        self.entry_product_quantity.grid(row=2, column=3)

        btn_create_product = tk.Button(self.create_product_frame, text="Create", command=self.create_product)
        btn_create_product.grid(row=3, columnspan=4, pady=10)

        # Section for deleting a product
        self.delete_product_frame = tk.LabelFrame(self.right_frame, text="Delete product")
        self.delete_product_frame.pack(padx=15, pady=15)

        tk.Label(self.delete_product_frame, text="Product ID: ").grid(row=0, column=0, sticky=tk.W)
        self.entry_delete_product_id = tk.Entry(self.delete_product_frame)
        self.entry_delete_product_id.grid(row=0, column=1)

        btn_delete_product = tk.Button(self.delete_product_frame, text="Delete", command=self.delete_product)
        btn_delete_product.grid(row=1, columnspan=2, pady=10)

        # Section to modify a product 
        self.modify_product_frame = tk.LabelFrame(self.right_frame, text="Modify Product")
        self.modify_product_frame.pack(padx=15, pady=15)

        tk.Label(self.modify_product_frame, text="Product ID:").grid(row=0, column=0, sticky=tk.W)
        self.entry_insert_product_id = tk.Entry(self.modify_product_frame)
        self.entry_insert_product_id.grid(row=0, column=1)

        tk.Label(self.modify_product_frame, text="New Name:").grid(row=1, column=0, sticky=tk.W)
        self.entry_modify_product_name = tk.Entry(self.modify_product_frame)
        self.entry_modify_product_name.grid(row=1, column=1)

        btn_modify_product_name = tk.Button(self.modify_product_frame, text="Modify", command=self.modify_product_name)
        btn_modify_product_name.grid(row=1, column=3, pady=10)

        tk.Label(self.modify_product_frame, text="New Category ID").grid(row=2, column=0, sticky=tk.W)
        self.entry_modify_product_category_id = tk.Entry(self.modify_product_frame)
        self.entry_modify_product_category_id.grid(row=2, column=1)

        btn_modify_product_category_id = tk.Button(self.modify_product_frame, text="Modify", command=self.modify_product_category_id)
        btn_modify_product_category_id.grid(row=2, column=2)

        tk.Label(self.modify_product_frame, text="New Description: ").grid(row=3, column=0, sticky=tk.W, columnspan=2)
        modify_description_frame = tk.Frame(self.modify_product_frame)
        modify_description_frame.grid(row=4, column=2, columnspan=2)

        self.modify_text_description = tk.Text(modify_description_frame, height=5, width=50)
        self.modify_text_description.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.scrollbar_modify = tk.Scrollbar(modify_description_frame, command=self.modify_text_description.yview)
        self.scrollbar_modify.pack(side=tk.RIGHT, fill=tk.Y)

        self.modify_text_description.config(yscrollcommand=self.scrollbar_modify.set)

        btn_modify_product_text_description = tk.Button(self.modify_product_frame, text="Modify", command=self.modify_product_text_description)
        btn_modify_product_text_description.grid(row=5, column=2)

        tk.Label(self.modify_product_frame, text="New Price").grid(row=6, column=0, sticky=tk.W)
        self.entry_modify_product_price = tk.Entry(self.modify_product_frame)
        self.entry_modify_product_price.grid(row=6, column=1)

        btn_modify_product_price = tk.Button(self.modify_product_frame, text="Modify", command=self.modify_product_price)
        btn_modify_product_price.grid(row=6, column=2)

        tk.Label(self.modify_product_frame, text="New Quantity").grid(row=7, column=0, sticky=tk.W)
        self.entry_modify_product_quantity = tk.Entry(self.modify_product_frame)
        self.entry_modify_product_quantity.grid(row=7, column=1)

        btn_modify_product_quantity = tk.Button(self.modify_product_frame, text="Modify", command=self.modify_product_quantity)        
        btn_modify_product_quantity.grid(row=7, column=2)

    def display_graph(self, method):
        """Clear existing and generate graph using the appropriate method."""
        for widget in self.graph_display_frame.winfo_children():
            widget.destroy() 

        try:
            columns_names, data = method() 
            
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)

            if method == self.graphics.plot_quantity_by_category:
                self.graphics.plot_horizontal_bar_graph(ax, data, "QUANTITIES BY CATEGORY")
            elif method == self.graphics.plot_distribution_of_products:
                self.graphics.plot_donut_chart(ax, data, "DISTRIBUTION OF PRODUCTS")
            elif method == self.graphics.plot_average_price_by_category:
                self.graphics.plot_box_plot(ax, data, "AVERAGE PRICE BY CATEGORY")
            elif method == self.graphics.plot_top_products_by_quantity:
                self.graphics.plot_dot_plot(ax, data, "TOP PRODUCTS BY QUANTITY")
            elif method == self.graphics.plot_total_stock_value_by_category:
                self.graphics.plot_tree_map(ax, data, "TOTAL STOCK VALUE BY CATEGORY")

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.graph_display_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True) 

        except Exception as error:
            messagebox.showerror("Error", f"An error occurred while generating the graph: {str(error)}")
            
    def update_graph(self, method):
        """Update method"""
        self.current_graph_method = method
        self.display_graph(method)

    def export_all(self):
        """Handle exporting all products"""
        try:
            columns_names, rows = self.export.export_all_products()
            self.save_to_csv(columns_names, rows)
        except Exception as error:
            messagebox.showerror("Error",str(error))

    def export_by_category(self):
        """Handle exporting products by the specified category"""
        id_category = self.entry_id_category.get()
        try:
            columns_names, rows = self.export.export_products_by_category(id_category)
            self.save_to_csv(columns_names, rows)
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def save_to_csv(self, columns_names, rows):
        """Save the provided data to a csv file"""
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")], title="Download the csv file")
        if file_path:
            with open(file_path, mode="w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(columns_names)
                writer.writerows(rows)
                messagebox.showinfo("Sucess", f"Data registered in '{file_path}'.")

    def create_product(self):
        """Handle adding a new product."""
        name = self.entry_product_name.get()
        description = self.text_description.get("1.0", tk.END).strip()
        price = self.entry_product_price.get()
        id_category = self.entry_category_id.get()
        quantity = self.entry_product_quantity.get()

        try:
            self.product_manager.add_product(name, description, price, id_category, quantity)
            messagebox.showinfo("Success", "Product added successfully.")
            self.refresh_product_list()  
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def delete_product(self):
        """Handle deleting a product."""
        product_id = self.entry_delete_product_id.get()

        try:
            self.product_manager.delete_product(product_id)
            messagebox.showinfo("Success", "Product deleted successfully.")
            self.refresh_product_list() 
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def modify_product_name(self):
        """Handle updating the product name."""
        product_id = self.entry_insert_product_id.get()
        new_name = self.entry_modify_product_name.get()

        try:
            self.product_manager.update_product_name(product_id, new_name)
            messagebox.showinfo("Success", "Product name updated successfully.")
            self.refresh_product_list() 
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def modify_product_text_description(self):
        """Handle updating the product description."""
        product_id = self.entry_insert_product_id.get()
        new_description = self.modify_text_description.get("1.0", tk.END).strip()

        try:
            self.product_manager.update_product_description(product_id, new_description)
            messagebox.showinfo("Success", "Product description updated successfully.")
            self.refresh_product_list() 
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def modify_product_price(self):
        """Handle updating the product price."""
        product_id = self.entry_insert_product_id.get()
        new_price = self.entry_modify_product_price.get()

        try:
            self.product_manager.update_product_price(product_id, new_price)
            messagebox.showinfo("Success", "Product price updated successfully.")
            self.refresh_product_list()  
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def modify_product_category_id(self):
        """Handle updating the product category ID."""
        product_id = self.entry_insert_product_id.get()
        new_category_id = self.entry_modify_product_category_id.get()

        try:
            self.product_manager.update_product_category(product_id, new_category_id)
            messagebox.showinfo("Success", "Product category ID updated successfully.")
            self.refresh_product_list()  
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def modify_product_quantity(self):
        """Handle updating the product quantity."""
        product_id = self.entry_insert_product_id.get()
        new_quantity = self.entry_modify_product_quantity.get()

        try:
            self.product_manager.update_product_quantity(product_id, new_quantity)
            messagebox.showinfo("Success", "Product quantity updated successfully.")
            self.refresh_product_list() 
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def refresh_product_list(self):
        """Refresh the list of products displayed in the Listbox."""
        self.product_list.delete(0, tk.END)  
        try:
            products = self.product_manager.get_all_products() 
            for product in products:

                self.product_list.insert(tk.END, f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Price: {product[3]}, Quantity: {product[4]}, Category ID: {product[5]}, Category Name: {product[6]}")
        except Exception as error:
            messagebox.showerror("Error", str(error))