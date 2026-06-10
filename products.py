import customtkinter as ctk
from tkinter import ttk
from tkinter import ttk, messagebox
from database.product_db import ProductDB

class ProductsPage:

    def __init__(self, parent):
        
        self.selected_product_id = None
        title = ctk.CTkLabel(
            parent,
            text="Product Management",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)

        form = ctk.CTkFrame(parent)
        form.pack(fill="x", padx=20)

        self.product_name = ctk.CTkEntry(form, placeholder_text="Product Name")
        self.product_name.grid(row=0, column=0, padx=10, pady=10)

        self.price = ctk.CTkEntry(form, placeholder_text="Selling Price")
        self.price.grid(row=0, column=1, padx=10, pady=10)

        self.stock = ctk.CTkEntry(form, placeholder_text="Stock Quantity")
        self.stock.grid(row=1, column=0, padx=10, pady=10)

        self.gst = ctk.CTkEntry(form, placeholder_text="GST %")
        self.gst.grid(row=1, column=1, padx=10, pady=10)
        
        self.purchase_price = ctk.CTkEntry(form, placeholder_text="Purchase Price")
        self.purchase_price.grid(row=2, column=0, padx=10, pady=10)

        self.barcode = ctk.CTkEntry(form, placeholder_text="Barcode")
        self.barcode.grid(row=2, column=1, padx=10, pady=10)

        self.unit = ctk.CTkEntry(form, placeholder_text="Unit (pcs/kg/ltr)")
        self.unit.grid(row=3, column=0, padx=10, pady=10)

        btn_frame = ctk.CTkFrame(parent)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        self.save_btn = ctk.CTkButton( btn_frame, text="Add Product",command=self.add_product)
        self.save_btn.pack(side="left", padx=10)

        self.update_btn = ctk.CTkButton( btn_frame, text="Update Product",  command=self.update_product)
        self.update_btn.pack(side="left", padx=10)

        self.delete_btn = ctk.CTkButton( btn_frame, text="Delete Product")
        self.delete_btn.pack(side="left", padx=10)

        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        columns = (
            "ID",
            "Product",
            "Purchase Price"
            "Selling Price",
            "Stock",
            "GST",
            "Barcode",
            "Unit"
        )

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind(
           "<<TreeviewSelect>>",
           self.on_row_select
        )
        self.load_products()
        
    def add_product(self):

        product_name = self.product_name.get().strip()
        selling_price = self.price.get().strip()
        stock_quantity = self.stock.get().strip()
        gst_percent = self.gst.get().strip()

        if not product_name:
           messagebox.showerror(
             "Error",
             "Product name is required"
           )
           return
        
        if not self.barcode.get().strip():
            messagebox.showerror(
             "Error",
             "Barcode is required"
            )
            return

        try:

            ProductDB.add_product(
              product_name,
              self.barcode.get().strip(),
              float(self.purchase_price.get() or 0),
              float(selling_price),
              float(gst_percent),
              int(stock_quantity),
              self.unit.get().strip() or "pcs"
            )

            messagebox.showinfo(
                "Success",
                "Product added successfully"
            )

            self.clear_fields()
            self.load_products()

        except Exception as e:
            messagebox.showerror(
              "Error",
              str(e)
            )
        
    def clear_fields(self):

        self.product_name.delete(0, "end")
        self.price.delete(0, "end")
        self.stock.delete(0, "end")
        self.gst.delete(0, "end")
        self.purchase_price.delete(0, "end")
        self.barcode.delete(0, "end")
        self.unit.delete(0, "end")
        
    def load_products(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        products = ProductDB.get_all_products()

        for product in products:

            self.tree.insert(
              "",
              "end",
              values=product
            )
            
    def on_row_select(self, event):

       selected = self.tree.focus()

       if not selected:
        return

       values = self.tree.item(selected, "values")

       self.selected_product_id = values[0]

       self.product_name.delete(0, "end")
       self.product_name.insert(0, values[1])

       self.purchase_price.delete(0, "end")
       self.purchase_price.insert(0, values[2])

       self.price.delete(0, "end")
       self.price.insert(0, values[3])

       self.stock.delete(0, "end")
       self.stock.insert(0, values[4])

       self.gst.delete(0, "end")
       self.gst.insert(0, values[5])

       self.barcode.delete(0, "end")
       self.barcode.insert(0, values[6])

       self.unit.delete(0, "end")
       self.unit.insert(0, values[7])
    
    def update_product(self):

        if not self.selected_product_id:
            messagebox.showerror(
              "Error",
              "Please select a product"
            )
            return

        ProductDB.update_product(
            self.selected_product_id,
            self.product_name.get(),
            float(self.price.get()),
            int(self.stock.get()),
            float(self.gst.get())
        )

        messagebox.showinfo(
           "Success",
           "Product updated successfully"
        )

        self.clear_fields()
        self.load_products()

        self.selected_product_id = None