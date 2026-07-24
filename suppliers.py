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
            text="Update Supplier",
            command=self.update_supplier
        )
        self.update_btn.pack(side="left", padx=10)

        self.delete_btn = ctk.CTkButton(
            btn_frame,
            text="Delete Supplier",
            command=self.delete_supplier
        )
        self.delete_btn.pack(side="left", padx=10)
        
        # ==========================
            # Search bar
        # ==========================
        
        search_frame = ctk.CTkFrame(parent)
        search_frame.pack(fill="x", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search Supplier...",
            width=300
        )
        self.search_entry.pack(side="left", padx=10)

        self.search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_supplier
        )
        self.search_btn.pack(side="left", padx=10)

        self.show_all_btn = ctk.CTkButton(
            search_frame,
            text="Show All",
            command=self.load_suppliers
        )
        self.show_all_btn.pack(side="left", padx=10)
        
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
        self.tree.bind(
          "<<TreeviewSelect>>",
          self.on_row_select
        )

        self.load_suppliers()
        
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
           self.load_suppliers();
           
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
        
    def load_suppliers(self):

        for item in self.tree.get_children():
           self.tree.delete(item)

        suppliers = SupplierDB.get_all_suppliers()

        for supplier in suppliers:

           self.tree.insert(
              "",
              "end",
              values=supplier
            )
           
    def on_row_select(self, event):
        selected = self.tree.focus()
        if not selected:
           return
        values = self.tree.item(selected, "values")

        self.selected_supplier_id = values[0]

        self.supplier_name.delete(0, "end")
        self.supplier_name.insert(0, values[1])

        self.contact_person.delete(0, "end")
        self.contact_person.insert(0, values[2])

        self.phone.delete(0, "end")
        self.phone.insert(0, values[3])

        self.email.delete(0, "end")
        self.email.insert(0, values[4])

        self.address.delete(0, "end")
        self.address.insert(0, values[5])
        
    def update_supplier(self):

        if not self.selected_supplier_id:
            messagebox.showerror(
               "Error",
               "Please select a supplier."
            )
            return

        try:

            SupplierDB.update_supplier(
                self.selected_supplier_id,
                self.supplier_name.get().strip(),
                self.contact_person.get().strip(),
                self.phone.get().strip(),
                self.email.get().strip(),
                self.address.get().strip()
            )

            messagebox.showinfo(
                "Success",
                "Supplier updated successfully."
            )

            self.clear_fields()
            self.load_suppliers()
  
            self.selected_supplier_id = None

        except Exception as e:

            messagebox.showerror(
               "Error",
               str(e)
            )
            
            
    def delete_supplier(self):

        if not self.selected_supplier_id:
            messagebox.showerror(
                "Error",
                "Please select a supplier."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this supplier?"
        )

        if not confirm:
            return

        try:

            SupplierDB.delete_supplier(
                self.selected_supplier_id
            )

            messagebox.showinfo(
               "Success",
               "Supplier deleted successfully."
            )

            self.clear_fields()
            self.load_suppliers()

            self.selected_supplier_id = None

        except Exception as e:

            messagebox.showerror(
               "Error",
                str(e)
            )
            
    
    def search_supplier(self):

        keyword = self.search_entry.get().strip()

        for item in self.tree.get_children():
            self.tree.delete(item)

        suppliers = SupplierDB.search_supplier(keyword)

        for supplier in suppliers:

            self.tree.insert(
                "",
                "end",
                values=supplier
            )
            
    