import customtkinter as ctk
from tkinter import ttk
from database.dashboard_db import DashboardDB

class DashboardPage:

    def __init__(self, parent):

        # ==========================
        # CARDS
        # ==========================

        

        cards_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        cards_frame.pack(fill="x")

        self.create_card(
            cards_frame,
            "Today's Sales",
            f"₹{DashboardDB.get_today_sales():,.2f}",
            width=270
        )

        self.create_card(
            cards_frame,
            "Customers",
            DashboardDB.get_total_customers()
        )

        self.create_card(
            cards_frame,
            "Products",
            DashboardDB.get_total_products()
        )

        self.create_card(
            cards_frame,
            "Suppliers",
            DashboardDB.get_total_suppliers()
        )

        self.create_card(
            cards_frame,
            "Low Stock",
            DashboardDB.get_low_stock_count()
        )

        # ==========================
        # GRAPH
        # ==========================

        graph_frame = ctk.CTkFrame(
            parent,
            height=300,
            fg_color="white",
            corner_radius=15
        )

        graph_frame.pack(
            fill="x",
            pady=20
        )

        graph_frame.pack_propagate(False)

        graph_title = ctk.CTkLabel(
            graph_frame,
            text="Sales Analytics",
            font=("Segoe UI", 20, "bold")
        )

        graph_title.pack(pady=20)

        graph_placeholder = ctk.CTkLabel(
            graph_frame,
            text="Sales Graph Here",
            font=("Segoe UI", 18)
        )

        graph_placeholder.pack(pady=80)

        # ==========================
        # TABLE
        # ==========================

        table_frame = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=15
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        table_title = ctk.CTkLabel(
            table_frame,
            text="Recent Invoices",
            font=("Segoe UI", 20, "bold")
        )

        table_title.pack(pady=20)

        columns = (
            "Invoice No",
            "Customer",
            "Amount",
            "Status",
            "Date"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:

            tree.heading(col, text=col)
            tree.column(col, width=150)

        tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        sample_data = [
            ("INV001", "Rahul", "₹5000", "Paid", "17-05-2026"),
            ("INV002", "Aman", "₹3200", "Pending", "17-05-2026"),
            ("INV003", "Priya", "₹9200", "Paid", "17-05-2026"),
        ]

        for row in sample_data:
            tree.insert("", "end", values=row)

    def create_card(self, parent, title, value, width=170):

        card = ctk.CTkFrame(
            parent,
            width=width,
            height=140,
            fg_color="white",
            corner_radius=15
        )

        card.pack(
            side="left",
            padx=10,
            pady=10
        )

        card.pack_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 16)
        )

        title_label.pack(
            pady=(25, 10)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 24, "bold")
        )

        value_label.pack(expand=True)