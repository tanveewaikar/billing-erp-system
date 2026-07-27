import customtkinter as ctk
from tkinter import ttk
from database.product_db import ProductDB


class StockPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.product_db = ProductDB()

        # =========================
        # Title
        # =========================
        title = ctk.CTkLabel(
            self,
            text="Stock Management",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)

        # =========================
        # Search Frame
        # =========================
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=250,
            placeholder_text="Search Product"
        )
        self.search_entry.pack(side="left", padx=10, pady=10)

        self.search_btn = ctk.CTkButton(
            search_frame,
            text="Search"
        )
        self.search_btn.pack(side="left", padx=5)

        self.low_stock_btn = ctk.CTkButton(
            search_frame,
            text="Low Stock"
        )
        self.low_stock_btn.pack(side="left", padx=5)

        self.show_all_btn = ctk.CTkButton(
            search_frame,
            text="Show All"
        )
        self.show_all_btn.pack(side="left", padx=5)

        # =========================
        # Table Frame
        # =========================
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = (
            "Product ID",
            "Product Name",
            "Category",
            "Stock",
            "Selling Price"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical"
        )

        self.stock_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15,
            yscrollcommand=scrollbar.set
        )

        scrollbar.config(command=self.stock_tree.yview)

        for col in columns:
            self.stock_tree.heading(col, text=col)
            self.stock_tree.column(col, anchor="center", width=150)

        scrollbar.pack(side="right", fill="y")
        self.stock_tree.pack(fill="both", expand=True)