import customtkinter as ctk
from tkinter import ttk, messagebox
from database.invoice_db import InvoiceDB


class ReportsPage:

    def __init__(self, parent):
        self.parent = parent 
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
        
        self.from_date_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="YYYY-MM-DD",
            width=140
        )
        self.from_date_entry.pack(side="left", padx=10, pady=10)

        self.to_date_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="YYYY-MM-DD",
            width=140
        )
        self.to_date_entry.pack(side="left", padx=10)
        
        filter_btn = ctk.CTkButton(
            filter_frame,
            text="Filter Date",
            command=self.filter_by_date
        )

        filter_btn.pack(side="left", padx=10)

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
        
        self.tree.bind("<Double-1>", self.open_invoice)
       
        self.load_invoices()
    
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
           
         # Clear date fields
        self.from_date_entry.delete(0, "end")
        self.to_date_entry.delete(0, "end")

        # Load all invoices
        self.load_invoices()
        
    def filter_by_date(self):

        from_date = self.from_date_entry.get().strip()
        to_date = self.to_date_entry.get().strip()

        # Check empty fields
        if not from_date or not to_date:
            messagebox.showwarning(
                "Validation Error",
                "Please enter both From Date and To Date."
            )
            return

        # Validate date format
        try:
            from datetime import datetime

            from_date_obj = datetime.strptime(
                from_date,
                "%Y-%m-%d"
            )

            to_date_obj = datetime.strptime(
                to_date,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Date",
                "Please enter dates in YYYY-MM-DD format."
            )
            return

        # Check date range
        if from_date_obj > to_date_obj:

            messagebox.showwarning(
                "Invalid Date Range",
                "From Date cannot be greater than To Date."
            )
            return

        # Clear old rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get filtered invoices
        invoices = InvoiceDB.get_invoices_by_date(
            from_date,
            to_date
        )

        # Display results
        for invoice in invoices:

            self.tree.insert(
                "",
                "end",
                values=invoice
            )  
            
    def open_invoice(self, event):

        selected = self.tree.focus()

        if not selected:
           return

        values = self.tree.item(selected, "values")

        invoice_id = values[0]

        items = InvoiceDB.get_invoice_items(invoice_id)

        details_window = ctk.CTkToplevel(self.parent)

        details_window.title("Invoice Details")
        details_window.geometry("700x500")

        title = ctk.CTkLabel(
            details_window,
            text="Invoice Details",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=15)
        invoice_no = ctk.CTkLabel(
            details_window,
            text=f"Invoice No : {values[1]}",
            font=("Arial", 16)
        )
        invoice_no.pack(anchor="w", padx=20, pady=5)

        customer = ctk.CTkLabel(
            details_window,
            text=f"Customer : {values[2]}",
            font=("Arial", 16)
        )
        customer.pack(anchor="w", padx=20, pady=5)

        date = ctk.CTkLabel(
            details_window,
            text=f"Date : {values[3]}",
            font=("Arial", 16)
        )
        date.pack(anchor="w", padx=20, pady=5)

        grand_total = ctk.CTkLabel(
            details_window,
            text=f"Grand Total : ₹{values[4]}",
            font=("Arial", 16, "bold")
        )
        grand_total.pack(anchor="w", padx=20, pady=5)
        
        product_frame = ctk.CTkFrame(details_window)
        product_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        columns = (
            "Product",
            "Quantity",
            "Price",
            "GST %",
             "Total"
        )
        
        scrollbar = ttk.Scrollbar(
            product_frame,
            orient="vertical"
        )
        
        product_tree = ttk.Treeview(
        product_frame,
        columns=columns,
        show="headings",
        height=8,
        yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=product_tree.yview)
        
        for col in columns:
            product_tree.heading(col, text=col)

        product_tree.column("Product", width=220)
        product_tree.column("Quantity", width=80, anchor="center")
        product_tree.column("Price", width=100, anchor="center")
        product_tree.column("GST %", width=80, anchor="center")
        product_tree.column("Total", width=120, anchor="center")
        
        scrollbar.pack(side="right", fill="y")
        product_tree.pack(side="left", fill="both", expand=True)
        
        for item in items:
            product_tree.insert("", "end", values=item)