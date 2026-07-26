import customtkinter as ctk
from tkinter import ttk


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
        self.supplier_combo = ctk.CTkComboBox(
            form,
            values=[],
            width=220
        )
        self.supplier_combo.set("Select Supplier")
        self.supplier_combo.grid(row=0, column=0, padx=10, pady=10)

        # Product
        self.product_combo = ctk.CTkComboBox(
            form,
            values=[],
            width=220
        )
        self.product_combo.set("Select Product")
        self.product_combo.grid(row=0, column=1, padx=10, pady=10)

        # Purchase Price
        self.purchase_price = ctk.CTkEntry(
            form,
            placeholder_text="Purchase Price"
        )
        self.purchase_price.grid(row=1, column=0, padx=10, pady=10)

        # Quantity
        self.quantity = ctk.CTkEntry(
            form,
            placeholder_text="Quantity"
        )
        self.quantity.grid(row=1, column=1, padx=10, pady=10)

        # Payment Status
        self.payment_status = ctk.CTkComboBox(
            form,
            values=["Paid", "Pending"],
            width=220
        )
        self.payment_status.set("Pending")
        self.payment_status.grid(row=2, column=0, padx=10, pady=10)

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

        # ==========================
        # TABLE
        # ==========================

        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = (
            "Purchase ID",
            "Supplier",
            "Product",
            "Purchase Price",
            "Quantity",
            "Payment Status",
            "Date"
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
        
        