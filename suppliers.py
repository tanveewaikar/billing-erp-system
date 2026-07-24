import customtkinter as ctk
from tkinter import ttk, messagebox
from database.suppliers_db import SupplierDB


class SuppliersPage:

    def __init__(self, parent):

        self.selected_supplier_id = None

        title = ctk.CTkLabel(
            parent,
            text="Supplier Management",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)

        # ==========================
        # Form
        # ==========================

        form = ctk.CTkFrame(parent)
        form.pack(fill="x", padx=20)

        self.supplier_name = ctk.CTkEntry(
            form,
            placeholder_text="Supplier Name"
        )
        self.supplier_name.grid(row=0, column=0, padx=10, pady=10)

        self.contact_person = ctk.CTkEntry(
            form,
            placeholder_text="Contact Person"
        )
        self.contact_person.grid(row=0, column=1, padx=10, pady=10)

        self.phone = ctk.CTkEntry(
            form,
            placeholder_text="Phone"
        )
        self.phone.grid(row=1, column=0, padx=10, pady=10)

        self.email = ctk.CTkEntry(
            form,
            placeholder_text="Email"
        )
        self.email.grid(row=1, column=1, padx=10, pady=10)

        self.address = ctk.CTkEntry(
            form,
            placeholder_text="Address"
        )
        self.address.grid(row=2, column=0, padx=10, pady=10)

        # ==========================
        # Buttons
        # ==========================

        btn_frame = ctk.CTkFrame(parent)
        btn_frame.pack(fill="x", padx=20, pady=10)

        self.add_btn = ctk.CTkButton(
            btn_frame,
            text="Add Supplier",
            command=self.add_supplier
        )
        self.add_btn.pack(side="left", padx=10)

        self.update_btn = ctk.CTkButton(
            btn_frame,
            text="Update Supplier"
        )
        self.update_btn.pack(side="left", padx=10)

        self.delete_btn = ctk.CTkButton(
            btn_frame,
            text="Delete Supplier"
        )
        self.delete_btn.pack(side="left", padx=10)

        # ==========================
        # Table
        # ==========================

        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        columns = (
            "ID",
            "Supplier",
            "Contact Person",
            "Phone",
            "Email",
            "Address"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)

        self.tree.pack(fill="both", expand=True)
        
    def add_supplier(self):

        supplier_name = self.supplier_name.get().strip()
        contact_person = self.contact_person.get().strip()
        phone = self.phone.get().strip()
        email = self.email.get().strip()
        address = self.address.get().strip()
        if not supplier_name:
           messagebox.showerror(
            "Error",
            "Supplier name is required."
           )
           return
        try:

           SupplierDB.add_supplier(
            supplier_name,
            contact_person,
            phone,
            email,
            address
           )
           
           messagebox.showinfo(
            "Success",
            "Supplier added successfully."
           )
           self.clear_fields()
        
        except Exception as e:

            messagebox.showerror(
             "Error",
             str(e)
            )   
            
    def clear_fields(self):

        self.supplier_name.delete(0, "end")
        self.contact_person.delete(0, "end")
        self.phone.delete(0, "end")
        self.email.delete(0, "end")
        self.address.delete(0, "end")