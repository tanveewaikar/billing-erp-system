import customtkinter as ctk
from tkinter import ttk
from database.dashboard_db import DashboardDB
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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
            height=220,
            fg_color="white",
            corner_radius=15
        )

        graph_frame.pack(
            fill="x",
            pady=(15,20)
        )

        graph_frame.pack_propagate(False)

        graph_title = ctk.CTkLabel(
            graph_frame,
            text="Sales Analytics",
            font=("Segoe UI", 20, "bold")
        )

        graph_title.pack(pady=20)
        
        figure = Figure(
           figsize=(8, 3),
           dpi=100
        )

        ax = figure.add_subplot(111)
        sales_data = DashboardDB.get_monthly_sales()

        months = []
        totals = []

        for row in sales_data:
            months.append(row["month"])
            totals.append(float(row["total_sales"]))
        
        ax.bar(months, totals, width=0.5)
        ax.set_title("Monthly Sales Analytics", fontsize= 14, fontwight = "bold")
        ax.set_xlabel("Month")
        ax.set_ylabel("Sales (₹)")
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        
        figure.tight_layout()
        
        canvas = FigureCanvasTkAgg(
            figure,
            master=graph_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

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
        
        style = ttk.Style()

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 11, "bold")
        )

        style.configure(
            "Treeview",
            rowheight=30,
            font=("Segoe UI", 10)
        )
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )

        for col in columns:

            self.tree.heading(col, text=col)
            if col == "Invoice No":
                self.tree.column(col, width=140, anchor="center")

            elif col == "Customer":
                self.tree.column(col, width=220)

            elif col == "Amount":
                self.tree.column(col, width=140, anchor="e")

            elif col == "Status":
                self.tree.column(col, width=120, anchor="center")

            elif col == "Date":
                self.tree.column(col, width=150, anchor="center")

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
        self.load_recent_invoices()
        
    def create_card(self, parent, title, value, width=170):

        card = ctk.CTkFrame(
            parent,
            width=width,
            height=140,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E5E7EB"
        )
        
        accent = ctk.CTkFrame(
            card,
            width=6,
            height=140,
            fg_color="#2563EB",
            corner_radius=0
        )
        accent.place(x=0, y=0)

        card.pack(
            side="left",
            padx=10,
            pady=10
        )

        card.pack_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 15),
            text_color="#6B7280"
        )

        title_label.pack(
            anchor="w",
            padx = 20,
            pady=(25, 10)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 24, "bold"),
            text_color="#111827"
        )

        value_label.pack(
            # expand=True,
            anchor="w",
            padx = 20,
        )
        
    def load_recent_invoices(self):

        self.tree.delete(*self.tree.get_children())

        invoices = DashboardDB.get_recent_invoices()

        for invoice in invoices:

            self.tree.insert(
                "",
                "end",
                values=(
                    invoice["invoice_number"],
                    invoice["customer_name"],
                    f"₹{invoice['grand_total']:.2f}",
                    invoice["payment_status"],
                    invoice["invoice_date"].strftime("%d-%m-%Y")
                )
            )
            
    