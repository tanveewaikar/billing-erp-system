import customtkinter as ctk
from tkinter import ttk, messagebox
from database.customer_db import CustomerDB

class CustomersPage:

    def __init__(self, parent):
        
        self.customer_db = CustomerDB()
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
        self.email.grid(row=0, column=2, padx=10, pady=10)

        self.gst = ctk.CTkEntry(form, placeholder_text="GST Number")
        self.gst.grid(row=0, column=3, padx=10, pady=10)
        
        self.address = ctk.CTkEntry(form, placeholder_text = "Address")
        self.address.grid(row = 1, column = 0, padx=10, pady=10)
        
        self.city = ctk.CTkEntry(form, placeholder_text= "City")
        self.city.grid(row=1, column =1, padx=10, pady=10)
        
        self.state = ctk.CTkEntry(form, placeholder_text = "State")
        self.state.grid(row =1, column=2, padx=10, pady= 10)
        
        self.pincode = ctk.CTkEntry(form, placeholder_text ="Pincode")
        self.pincode.grid(row = 1, column = 3, padx = 10, pady = 10)

        add_btn = ctk.CTkButton(form, text="Add Customer", command =self.add_customer)
        add_btn.grid(row=2, column=0, pady=20)

        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = (
            "ID",
            "Name",
            "Phone",
            "Email",
            "GST",
            "Address",
            "City",
            "State",
            "Pincode"
        )

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True)
    
    # ==========================================
    # ADD CUSTOMER
    # ==========================================

    def add_customer(self):

        try:

            self.customer_db.add_customer(
                customer_name=self.name.get(),
                phone=self.phone.get(),
                email=self.email.get(),
                 gst_number=self.gst.get(),
                address= self.address.get(),
                city= self.city.get(),
                state= self.state.get(),
                pincode= self.pincode.get()
               
            )

            messagebox.showinfo(
                "Success",
                "Customer added successfully!"
            )

            self.name.delete(0, "end")
            self.phone.delete(0, "end")
            self.email.delete(0, "end")
            self.gst.delete(0, "end")
            self.address.delete(0, "end")
            self.city.delete(0, "end")
            self.state.delete(0, "end")
            self.pincode.delete(0, "end")

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )