import customtkinter as ctk
from tkinter import ttk
from database.invoice_db import InvoiceDB


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

        self.search_entry = ctk.CTkEntry(
           filter_frame,
           placeholder_text="Search by Invoice No or Customer"
        )
        self.search_entry.pack(side="left", padx=10, pady=10)
        
        to_date = ctk.CTkEntry(
            filter_frame,
            placeholder_text="To Date"
        )
        to_date.pack(side="left", padx=10)

        search_btn = ctk.CTkButton(
           filter_frame,
           text="Search",
           command=self.search_invoice
        )
        search_btn.pack(side="left", padx=10)
        
        show_all_btn = ctk.CTkButton(
            filter_frame,
            text="Show All",
            command=self.show_all_invoices
        )
        show_all_btn.pack(side="left", padx=10)
        
        # graph = ctk.CTkFrame(parent, height=300)
        # graph.pack(fill="x", padx=20, pady=20)

        # graph_label = ctk.CTkLabel(
        #     graph,
        #     text="Sales Graph Area"
        # )
        # graph_label.pack(pady=120)

        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
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
            show="headings",
            height = 12
        )

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.column("Invoice ID", width=80, anchor="center")
        self.tree.column("Invoice No", width=150, anchor="center")
        self.tree.column("Customer", width=180, anchor="center")
        self.tree.column("Date", width=150, anchor="center")
        self.tree.column("Total Amount", width=120, anchor="center")
            

        self.tree.pack(fill="both", expand=True, padx=20,pady=20)
       
        self.load_invoices()
        
    # def load_invoices(self):

    #     invoices = InvoiceDB.get_all_invoices()

    #     for invoice in invoices:
    #         self.tree.insert("", "end", values=invoice)
    
    def load_invoices(self):

        invoices = InvoiceDB.get_all_invoices()

        for invoice in invoices:
           self.tree.insert("", "end", values=invoice)
    
    def search_invoice(self):

        keyword = self.search_entry.get().strip()

        # Clear old data
        for item in self.tree.get_children():
            self.tree.delete(item)

        invoices = InvoiceDB.search_invoices(keyword)

        for invoice in invoices:
            self.tree.insert("", "end", values=invoice)
            
    def show_all_invoices(self):

        self.search_entry.delete(0, "end")

        # Clear table
        for item in self.tree.get_children():
           self.tree.delete(item)

        # Load all invoices
        self.load_invoices()