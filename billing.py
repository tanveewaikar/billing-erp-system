import customtkinter as ctk
from tkinter import ttk
from database.customer_db import CustomerDB
from database.product_db import ProductDB
from tkinter import ttk, messagebox

class BillingPage:

    def __init__(self, parent):
        
        self.bill_items = []
        
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

        product_name = self.product_combo.get()

        try:
            qty = int(self.qty.get())
        except ValueError:
            print("Invalid quantity")
            return

        product = ProductDB.get_product_by_name(product_name)

        if not product:
            return

        product_id, name, price, gst_percent, stock = product
        if qty > stock:
            messagebox.showerror(
                "Insufficient Stock",
                f"Only {stock} items available in stock"
                )
            return

        subtotal = float(price) * qty
        gst_amount = subtotal * (float(gst_percent) / 100)
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
        self.qty.delete(0, "end")