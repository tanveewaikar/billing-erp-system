import customtkinter as ctk
from tkinter import ttk
from database.dashboard_db import DashboardDB
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

# ==========================
# UI CONSTANTS
# ==========================

CARD_COLOR = "white"
CARD_RADIUS = 12

TITLE_FONT = ("Segoe UI", 15)
VALUE_FONT = ("Segoe UI", 24, "bold")
SECTION_FONT = ("Segoe UI", 20, "bold")

TEXT_PRIMARY = "#111827"
TEXT_SECONDARY = "#6B7280"

ACCENT_BLUE = "#2563EB"

def indian_currency(x, pos):
    return f"₹{x:,.0f}"

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
            width=220
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
            fg_color=CARD_COLOR,
            corner_radius=15
        )

        graph_frame.pack(
            fill="x",
            pady=(15,20)
        )

        graph_frame.pack_propagate(False)

        graph_title = ctk.CTkLabel(
            graph_frame,
            text="Monthly Sales Overview",
            font=("Segoe UI", 20, "bold")
        )

        graph_title.pack(pady=20)
        
        figure = Figure(
           figsize=(10, 5),
           dpi=100
        )

        ax = figure.add_subplot(111)
        sales_data = DashboardDB.get_monthly_sales()

        months = []
        totals = []

        for row in sales_data:
            months.append(row["month"])
            totals.append(float(row["total_sales"]))
        
        ax.bar(months, totals, width=0.5, color="#2563EB")
        bars = ax.bar(
            months,
            totals,
            width=0.5,
            color="#2563EB"
        )
        
        for bar in bars:

            height = bar.get_height()

            ax.annotate(
                f"₹{height:,.0f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),
                textcoords="offset points",
                ha="center",
                fontsize=9,
                fontweight="bold"
            )
            
        ax.set_ylabel("Sales (₹)")
        ax.yaxis.set_major_formatter(
            FuncFormatter(indian_currency)
        )
        
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        
        ax.grid(
           axis="y",
           linestyle="--",
           linewidth=0.6,
           alpha=0.3
        )
        
        figure.subplots_adjust(
           left=0.08,
           right=0.98,
           top=0.94,
           bottom=0.18
        )
        
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
        
    def create_card(self, parent, title, value, width=150):

        card = ctk.CTkFrame(
            parent,
            width=width,
            height=140,
            fg_color="white",
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color="#E5E7EB"
        )
        
        accent = ctk.CTkFrame(
            card,
            width=6,
            height=140,
            fg_color=ACCENT_BLUE,
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
            text_color=TEXT_SECONDARY
        )

        title_label.pack(
            anchor="w",
            padx = 20,
            pady=(25, 10)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=VALUE_FONT,
            text_color=TEXT_PRIMARY
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
            
    