import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from ttkthemes import ThemedTk
from exportcsv import Exportcsv
from database import Database
from graphics import Graphics
from product import Product 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import csv

class Application(ThemedTk):
    def __init__(self, db: Database):
        super().__init__()
        self.set_theme("radiance")
        self.db = db
        self.export = Exportcsv(self.db)
        self.graphics = Graphics(self.db)
        self.product_manager = Product(self.db)
        self.title("Inventory Management")
        self.state('zoomed')
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.create_main_areas()

    def create_main_areas(self):
        # Top frame (contains Area 1 and Area 2)
        top_frame = ttk.Frame(self.scrollable_frame)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Bottom frame (contains Area 3 and Area 4)
        bottom_frame = ttk.Frame(self.scrollable_frame)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Four areas
        self.area1 = ttk.LabelFrame(top_frame, text=" Product List - Export and Delete ")
        self.area2 = ttk.LabelFrame(top_frame, text=" Graphics ")
        self.area3 = ttk.LabelFrame(bottom_frame, text=" Modify Product ")
        self.area4 = ttk.LabelFrame(bottom_frame, text=" Create New Product ")

        # Grid
        self.area1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.area2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.area3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.area4.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Content
        self.create_area1_content()
        self.create_area2_content()
        self.create_area3_content()
        self.create_area4_content()

        self.refresh_product_list()

    def create_area1_content(self):
        # Product List
        ttk.Label(self.area1).pack(anchor=tk.W, padx=5, pady=5)

        listbox_frame = ttk.Frame(self.area1)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.product_list = tk.Listbox(listbox_frame, height=10)
        self.product_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar_v = ttk.Scrollbar(listbox_frame, command=self.product_list.yview)
        scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_list.config(yscrollcommand=scrollbar_v.set)

        scrollbar_h = ttk.Scrollbar(listbox_frame, command=self.product_list.xview, orient=tk.HORIZONTAL)
        scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)
        self.product_list.config(xscrollcommand=scrollbar_h.set)

        # Export section
        ttk.Label(self.area1, text="Export").pack(anchor=tk.W, padx=5, pady=5)
        ttk.Button(self.area1, text="Export All Products", command=self.export_all).pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(self.area1, text="Category ID:").pack(anchor=tk.W, padx=5, pady=5)
        self.entry_id_category = ttk.Entry(self.area1)
        self.entry_id_category.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.area1, text="Export by Category", command=self.export_by_category).pack(fill=tk.X, padx=5, pady=2)

        # Delete section
        ttk.Label(self.area1, text="Delete").pack(anchor=tk.W, padx=5, pady=5)
        ttk.Label(self.area1, text="Product ID:").pack(anchor=tk.W, padx=5, pady=5)
        self.entry_delete = ttk.Entry(self.area1)
        self.entry_delete.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.area1, text="Delete", command=self.delete_product_from_entry).pack(fill=tk.X, padx=5, pady=2)

    def delete_product_from_entry(self):
        """Handle deleting a product using the ID from the entry field."""
        product_id = self.entry_delete.get()
        try:
            self.product_manager.delete_product(product_id)
            messagebox.showinfo("Success", "Product deleted successfully.")
            self.refresh_product_list()
            self.entry_delete.delete(0, tk.END)
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def create_area2_content(self):
        # Graphs section
        ttk.Label(self.area2).pack(anchor=tk.W, padx=5, pady=5)
        
        self.graph_display_frame = ttk.LabelFrame(self.area2, text=" Graphic Zone ")
        self.graph_display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        buttons_frame = ttk.Frame(self.area2)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        graph_methods = [
            ("Quantities by Category", self.graphics.plot_quantity_by_category),
            ("Distribution of Products", self.graphics.plot_distribution_of_products),
            ("Average Price by Category", self.graphics.plot_average_price_by_category),
            ("Top Products by Quantity", self.graphics.plot_top_products_by_quantity),
            ("Total Stock Value by Category", self.graphics.plot_total_stock_value_by_category)
        ]

        for title, method in graph_methods:
            ttk.Button(buttons_frame, text=title, command=lambda m=method: self.update_graph(m)).pack(fill=tk.X, padx=5, pady=2)

        self.current_graph_method = self.graphics.plot_quantity_by_category
        self.display_graph(self.current_graph_method)

    def create_area3_content(self):
        # Modify section
        ttk.Label(self.area3).pack(anchor=tk.W, padx=5, pady=5)
        
        ttk.Label(self.area3, text="Product ID:").pack(anchor=tk.W, padx=5, pady=5)
        self.entry_insert_product_id = ttk.Entry(self.area3)
        self.entry_insert_product_id.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(self.area3, text="New Name:").pack(anchor=tk.W, padx=5, pady=5)
        self.entry_modify_product_name = ttk.Entry(self.area3)
        self.entry_modify_product_name.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.area3, text="Modify Name", command=self.modify_product_name).pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(self.area3, text="New Category ID:").pack(anchor=tk.W, padx=5, pady=5)
        self.entry_modify_product_category_id = ttk.Entry(self.area3)
        self.entry_modify_product_category_id.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.area3, text="Modify Category", command=self.modify_product_category_id).pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(self.area3, text="New Description:").pack(anchor=tk.W, padx=5, pady=5)
        self.modify_text_description = scrolledtext.ScrolledText(self.area3, height=4)
        self.modify_text_description.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.area3, text="Modify Description", command=self.modify_product_text_description).pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(self.area3, text="New Price:").pack(anchor=tk.W, padx=5, pady=5)
        self.entry_modify_product_price = ttk.Entry(self.area3)
        self.entry_modify_product_price.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.area3, text="Modify Price", command=self.modify_product_price).pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(self.area3, text="New Quantity:").pack(anchor=tk.W, padx=5, pady=5)
        self.entry_modify_product_quantity = ttk.Entry(self.area3)
        self.entry_modify_product_quantity.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.area3, text="Modify Quantity", command=self.modify_product_quantity).pack(fill=tk.X, padx=5, pady=2)

    def create_area4_content(self):
        # Create section
        ttk.Label(self.area4).pack(anchor=tk.W, padx=5, pady=5)
        
        ttk.Label(self.area4, text="Product Name:").pack(anchor=tk.W, padx=5, pady=5)
        self.entry_product_name = ttk.Entry(self.area4)
        self.entry_product_name.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(self.area4, text="Category ID:").pack(anchor=tk.W, padx=5, pady=5)
        self.entry_category_id = ttk.Entry(self.area4)
        self.entry_category_id.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(self.area4, text="Description:").pack(anchor=tk.W, padx=5, pady=5)
        self.text_description = scrolledtext.ScrolledText(self.area4, height=4)
        self.text_description.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(self.area4, text="Price:").pack(anchor=tk.W, padx=5, pady=5)
        self.entry_product_price = ttk.Entry(self.area4)
        self.entry_product_price.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(self.area4, text="Quantity:").pack(anchor=tk.W, padx=5, pady=5)
        self.entry_product_quantity = ttk.Entry(self.area4)
        self.entry_product_quantity.pack(fill=tk.X, padx=5, pady=2)

        ttk.Button(self.area4, text="Create Product", command=self.create_product).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.area4, text="Quit", command=self.on_closing).pack(fill=tk.X, padx=5, pady=90)

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
            messagebox.showerror("Error", str(error))

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
                messagebox.showinfo("Success", f"Data registered in '{file_path}'.")

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
            
            self.entry_product_name.delete(0, tk.END)
            self.text_description.delete("1.0", tk.END)
            self.entry_product_price.delete(0, tk.END)
            self.entry_category_id.delete(0, tk.END)
            self.entry_product_quantity.delete(0, tk.END)
            self.entry_product_name.focus_set()
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def delete_product(self, product_id):
        """Handle deleting a product."""
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
            self.entry_modify_product_name.delete(0, tk.END)
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
            self.modify_product_text_description.delete(0, tk.END)
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
            self.entry_modify_product_price.delete(0, tk.END)  
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
            self.entry_modify_product_category_id.delete(0, tk.END) 
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
            self.entry_modify_product_quantity.delete(0, tk.END)
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

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

