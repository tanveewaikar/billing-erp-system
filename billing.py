import customtkinter as ctk
from tkinter import ttk
from database.customer_db import CustomerDB
from database.product_db import ProductDB
from tkinter import ttk, messagebox

class BillingPage:

    def __init__(self, parent):
        
        self.bill_items = {}
        
        self.subtotal_amount = 0
        self.gst_amount = 0
        self.grand_total = 0

        title = ctk.CTkLabel(
            parent,
            text="Create Invoice",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)

        top_frame = ctk.CTkFrame(parent)
        top_frame.pack(fill="x", padx=20)

        self.customer = ctk.CTkComboBox(
            top_frame,
            values=CustomerDB.get_customer_names()
        )
        self.customer.pack(side="left", padx=10, pady=10)
        
        self.product_combo = ctk.CTkComboBox(
        top_frame,
        values=ProductDB.get_product_names(),
        width=200
        )
        self.product_combo.pack( side="left",padx=10,pady=10)
        
        self.qty = ctk.CTkEntry(top_frame,width=80,placeholder_text="Qty")
        self.qty.pack(side="left",padx=10)
        
        add_btn = ctk.CTkButton(top_frame, text="Add Product",command=self.add_product_to_bill)
        add_btn.pack(side="left", padx=10)
        
        remove_btn = ctk.CTkButton(top_frame,text="Remove Product", command=self.remove_product)
        remove_btn.pack(side="left", padx=10)

        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        columns = (
            "Product",
            "Qty",
            "Price",
            "GST",
            "Total"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True)

        summary = ctk.CTkFrame(parent)
        summary.pack(fill="x", padx=20)

        self.subtotal_label = ctk.CTkLabel(summary,text="Subtotal : ₹0.00")
        self.subtotal_label.pack(anchor="e", padx=20, pady=5)

        self.gst_label = ctk.CTkLabel( summary,text="GST : ₹0.00")
        self.gst_label.pack(anchor="e", padx=20, pady=5)

        self.total_label = ctk.CTkLabel(summary,text="Grand Total : ₹0.00",font=("Segoe UI", 18, "bold"))
        self.total_label.pack(anchor="e", padx=20, pady=10)
        
        btn_frame = ctk.CTkFrame(parent)
        btn_frame.pack(fill="x", padx=20, pady=20)

        generate_btn = ctk.CTkButton(btn_frame, text="Generate Invoice")
        generate_btn.pack(side="left", padx=10)

        print_btn = ctk.CTkButton(btn_frame, text="Print")
        print_btn.pack(side="left", padx=10)

        email_btn = ctk.CTkButton(btn_frame, text="Email Invoice")
        email_btn.pack(side="left", padx=10)
        
    def add_product_to_bill(self):

        print("Add Product Clicked")

        product_name = self.product_combo.get()
        print("Product:", product_name)

        try:
            qty = int(self.qty.get())
        except ValueError:
            print("Invalid quantity")
            return

        product = ProductDB.get_product_by_name(product_name)

        print("Product from DB:", product)

        if not product:
            print("No product found")
            return

        product_id, name, price, gst_percent, stock = product

        print("Before:", self.bill_items)

        if name in self.bill_items:

            print("Existing product")

            new_qty = self.bill_items[name]["qty"] + qty

            if new_qty > stock:
                print("Stock exceeded")
                return

            self.bill_items[name]["qty"] = new_qty

        else:

            print("New product")

            self.bill_items[name] = {
               "qty": qty,
               "price": float(price),
               "gst": float(gst_percent)
            }

        print("After:", self.bill_items)

        self.refresh_bill_table()

        self.qty.delete(0, "end")
        
                
    def refresh_bill_table(self):
        
        print("refresh_bill_table called")
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.subtotal_amount = 0
        self.gst_amount = 0
        self.grand_total = 0

        for name, data in self.bill_items.items():

            qty = data["qty"]
            price = data["price"]
            gst_percent = data["gst"]

            subtotal = price * qty
            gst_amount = subtotal * gst_percent / 100
            total = subtotal + gst_amount
    
            self.tree.insert(
               "",
               "end",
               values=(
                    name,
                    qty,
                    f"{price:.2f}",
                    f"{gst_amount:.2f}",
                    f"{total:.2f}"
                )
            )

            self.subtotal_amount += subtotal
            self.gst_amount += gst_amount
            self.grand_total += total

        self.subtotal_label.configure(
            text=f"Subtotal : ₹{self.subtotal_amount:.2f}"
        )

        self.gst_label.configure(
            text=f"GST : ₹{self.gst_amount:.2f}"
        )

        self.total_label.configure(
            text=f"Grand Total : ₹{self.grand_total:.2f}"
        )

    def remove_product(self):

        selected = self.tree.focus()

        if not selected:
            messagebox.showerror(
               "Error",
               "Please select a product"
            )
            return

        values = self.tree.item(selected, "values")

        product_name = values[0]

        if product_name in self.bill_items:
            del self.bill_items[product_name]
 
        self.refresh_bill_table()