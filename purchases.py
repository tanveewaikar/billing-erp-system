import customtkinter as ctk
from tkinter import ttk
from database.purchase_db import PurchaseDB


class PurchasesPage:

    def __init__(self, parent):

        self.selected_purchase_id = None

        # ==========================
        # TITLE
        # ==========================

        title = ctk.CTkLabel(
            parent,
            text="Purchase Management",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)

        # ==========================
        # FORM
        # ==========================

        form = ctk.CTkFrame(parent)
        form.pack(fill="x", padx=20)

        # Supplier
        ctk.CTkLabel(
           form,
           text="Supplier"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.supplier_combo = ctk.CTkComboBox(
            form,
            values=[],
            width=220
        )
        self.supplier_combo.grid(row=0, column=1, padx=10, pady=10)

        # Product
        ctk.CTkLabel(
            form,
            text="Product"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.product_combo = ctk.CTkComboBox(
            form,
            values=[],
            width=220
        )
        self.product_combo.grid(row=0, column=1, padx=10, pady=10)

        # Purchase Price
        ctk.CTkLabel(
            form,
            text="Purchase"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
               
        self.purchase_combo = ctk.CTkComboBox(
            form,
            values=[],
            width=220
        )
        self.purchase_combo.grid(row=0, column=1, padx=10, pady=10)
        
        self.purchase_price.bind(
            "<KeyRelease>",
            self.calculate_total
        )
        
        # Quantity
        ctk.CTkLabel(
            form,
            text="Quantity"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
                
        self.quantity_combo = ctk.CTkComboBox(
            form,
            values=[],
            width=220
        )
        self.quantity_combo.grid(row=0, column=1, padx=10, pady=10)
        
        self.quantity.bind(
            "<KeyRelease>",
            self.calculate_total
        )
        
        #Total Amount
        ctk.CTkLabel(
            form,
            text="Total Amount"
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.total_amount = ctk.CTkEntry(
            form,
            width=220,
            state="readonly"
        )
        self.total_amount.grid(row=2, column=1, padx=10, pady=10)
        
        # Payment Status
        ctk.CTkLabel(
            form,
            text="Payment"
        ).grid(row=2, column=2, padx=10, pady=10, sticky="w")
                
        self.payment_combo = ctk.CTkComboBox(
            form,
            values=[],
            width=220
        )
        self.payment_combo.grid(row=0, column=1, padx=10, pady=10)

        # ==========================
        # BUTTONS
        # ==========================

        btn_frame = ctk.CTkFrame(parent)
        btn_frame.pack(fill="x", padx=20, pady=10)

        self.add_btn = ctk.CTkButton(
            btn_frame,
            text="Add Purchase"
        )
        self.add_btn.pack(side="left", padx=10)

        self.update_btn = ctk.CTkButton(
            btn_frame,
            text="Update Purchase"
        )
        self.update_btn.pack(side="left", padx=10)

        self.delete_btn = ctk.CTkButton(
            btn_frame,
            text="Delete Purchase"
        )
        self.delete_btn.pack(side="left", padx=10)
        
        self.clear_btn = ctk.CTkButton(
            btn_frame,
            text="Clear"
        )
        self.clear_btn.pack(side="left", padx=10)
        
        # ==========================
        # SEARCH 
        # ==========================
        search_frame = ctk.CTkFrame(parent)
        search_frame.pack(fill="x", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search Purchase...",
            width=300
        )
        self.search_entry.pack(side="left", padx=10)

        self.search_btn = ctk.CTkButton(
            search_frame,
            text="Search"
        )
        self.search_btn.pack(side="left", padx=10)

        self.show_all_btn = ctk.CTkButton(
            search_frame,
            text="Show All"
        )
        self.show_all_btn.pack(side="left", padx=10)

        # ==========================
        # TABLE
        # ==========================

        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = (
            "Purchase ID",
            "Supplier",
            "Product",
            "Quantity",
            "Purchase Price",
            "Total Amount",
            "Payment Status",
            "Purchase Date"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )
        
        self.load_suppliers()
        self.load_products()
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True)
        
        
    def load_suppliers(self):

        suppliers = PurchaseDB.get_all_suppliers()

        self.supplier_dict = {}

        supplier_names = []

        for supplier_id, supplier_name in suppliers:

           supplier_names.append(supplier_name)
           self.supplier_dict[supplier_name] = supplier_id

        self.supplier_combo.configure(values=supplier_names)

        if supplier_names:
           self.supplier_combo.set(supplier_names[0])
           
    def load_products(self):

        products = PurchaseDB.get_all_products()

        self.product_dict = {}

        product_names = []

        for product_id, product_name in products:

           product_names.append(product_name)
           self.product_dict[product_name] = product_id

        self.product_combo.configure(values=product_names)

        if product_names:
           self.product_combo.set(product_names[0])
           
           
    def calculate_total(self, event=None):

        try:

            price = float(self.purchase_price.get() or 0)
            quantity = int(self.quantity.get() or 0)

            total = price * quantity

            self.total_amount.configure(state="normal")
            self.total_amount.delete(0, "end")
            self.total_amount.insert(0, f"{total:.2f}")
            self.total_amount.configure(state="readonly")

        except ValueError:

            self.total_amount.configure(state="normal")
            self.total_amount.delete(0, "end")
            self.total_amount.insert(0, "0.00")
            self.total_amount.configure(state="readonly")
            
    