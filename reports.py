import customtkinter as ctk
from tkinter import ttk
from database.invoice_db import InvoiceDB

style = ttk.Style()
style.theme_use("default")

style.configure(
    "Treeview",
    rowheight=28,
    font=("Segoe UI", 11)
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 11, "bold")
)

class ReportsPage:

    def __init__(self, parent):

        title = ctk.CTkLabel(
            parent,
            text="Reports & Analytics",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)

        filter_frame = ctk.CTkFrame(parent)
        filter_frame.pack(fill="x", padx=20)

        from_date = ctk.CTkEntry(
            filter_frame,
            placeholder_text="From Date"
        )
        from_date.pack(side="left", padx=10, pady=10)

        to_date = ctk.CTkEntry(
            filter_frame,
            placeholder_text="To Date"
        )
        to_date.pack(side="left", padx=10)

        generate = ctk.CTkButton(
            filter_frame,
            text="Generate Report"
        )
        generate.pack(side="left", padx=10)

        graph = ctk.CTkFrame(parent, height=300)
        graph.pack(fill="x", padx=20, pady=20)

        graph_label = ctk.CTkLabel(
            graph,
            text="Sales Graph Area"
        )
        graph_label.pack(pady=120)

        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = (
            "Invoice ID",
            "Invoice No",
            "Customer",
            "Date",
            "Total Amount"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.column("Invoice ID", width=80, anchor="center")
        self.tree.column("Invoice No", width=150, anchor="center")
        self.tree.column("Customer", width=180, anchor="center")
        self.tree.column("Date", width=150, anchor="center")
        self.tree.column("Total Amount", width=120, anchor="center")
            

        self.tree.pack(fill="both", expand=True, padx=20,pady=20)
        # new line added
        print("Tree children:", self.tree.get_children()) 
        
        self.load_invoices()
        # new line added 
        print("Tree children after loading:", self.tree.get_children())
        
    # def load_invoices(self):

    #     invoices = InvoiceDB.get_all_invoices()

    #     for invoice in invoices:
    #         self.tree.insert("", "end", values=invoice)
    
    def load_invoices(self):

        invoices = InvoiceDB.get_all_invoices()

        print("Total invoices:", len(invoices))

        for invoice in invoices:
           print("Inserting:", invoice)
           self.tree.insert("", "end", values=invoice)
           