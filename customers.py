import customtkinter as ctk
from tkinter import ttk

class CustomersPage:

    def __init__(self, parent):

        title = ctk.CTkLabel(
            parent,
            text="Customer Management",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)

        form = ctk.CTkFrame(parent)
        form.pack(fill="x", padx=20)

        self.name = ctk.CTkEntry(form, placeholder_text="Customer Name")
        self.name.grid(row=0, column=0, padx=10, pady=10)

        self.phone = ctk.CTkEntry(form, placeholder_text="Phone")
        self.phone.grid(row=0, column=1, padx=10, pady=10)

        self.email = ctk.CTkEntry(form, placeholder_text="Email")
        self.email.grid(row=1, column=0, padx=10, pady=10)

        self.gst = ctk.CTkEntry(form, placeholder_text="GST Number")
        self.gst.grid(row=1, column=1, padx=10, pady=10)

        add_btn = ctk.CTkButton(form, text="Add Customer")
        add_btn.grid(row=2, column=0, pady=20)

        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = (
            "ID",
            "Name",
            "Phone",
            "Email",
            "GST"
        )

        tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        tree.pack(fill="both", expand=True)