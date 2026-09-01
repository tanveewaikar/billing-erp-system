import customtkinter as ctk
from tkinter import ttk, messagebox
from database.customer_db import CustomerDB


class CustomersPage:

    def __init__(self, parent):
        
        self.customer_db = CustomerDB()
        self.selected_customer_id = None
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
        
        update_btn = ctk.CTkButton(form,text="Update Customer",command=self.update_customer)
        update_btn.grid(row=2, column=1, pady=20)
        
        delete_btn = ctk.CTkButton(form,text="Delete Customer", fg_color="red",hover_color="darkred",command=self.delete_customer)
        delete_btn.grid(row=2, column=2, pady=20)
        
        clear_btn = ctk.CTkButton( form,text="Clear",command=self.clear_fields)
        clear_btn.grid(row=2, column=3, pady=20)
        
        # ==========================================
        # SEARCH
        # ==========================================

        search_frame = ctk.CTkFrame(parent)
        search_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Search Name / Phone / Email"
        )
        self.search_entry.pack(
            side="left",
            padx=10,
            pady=10
        )

        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_customers
        )
        search_btn.pack(
            side="left",
            padx=10,
            pady=10
        )

        show_all_btn = ctk.CTkButton(
            search_frame,
            text="Show All",
            command=self.load_customers
        )
        show_all_btn.pack(
            side="left",
            padx=10,
            pady=10
        )
        

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
        
        scrollbar_x = ttk.Scrollbar(table_frame,orient="horizontal", command=self.tree.xview)
        self.tree.configure( xscrollcommand=scrollbar_x.set)

        for col in columns:

            self.tree.heading(col, text=col)

            if col == "ID":
                self.tree.column(col, width=60, anchor="center")

            elif col == "Name":
                self.tree.column(col, width=160)

            elif col == "Phone":
                self.tree.column(col, width=130)

            elif col == "Email":
                self.tree.column(col, width=250)

            elif col == "GST":
                self.tree.column(col, width=180)

            elif col == "Address":
                self.tree.column(col, width=250)

            elif col == "City":
                self.tree.column(col, width=120)

            elif col == "State":
                self.tree.column(col, width=150)

            elif col == "Pincode":
                self.tree.column(col, width=100, anchor="center")

        self.tree.pack( fill="both", expand=True, padx=20, pady=(20, 0))
        scrollbar_x.pack( fill="x", padx=20, pady=(0, 20))
        
        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_customer
        )
        self.load_customers()
    
    # ==========================================
    # VALIDATE CUSTOMER
    # ==========================================

    def validate_customer(self):

        name = self.name.get().strip()
        phone = self.phone.get().strip()
        email = self.email.get().strip()
        address = self.address.get().strip()
        city = self.city.get().strip()
        state = self.state.get().strip()
        pincode = self.pincode.get().strip()

        # Customer Name
        if not name:
            messagebox.showwarning(
                "Validation Error",
                "Customer name is required."
            )
            return False

        if not all(char.isalpha() or char.isspace() for char in name):
            messagebox.showwarning(
                "Validation Error",
                "Customer name should contain only letters."
            )
            return False

        # Phone
        if not phone:
            messagebox.showwarning(
                "Validation Error",
                "Phone number is required."
            )
            return False

        if not phone.isdigit() or len(phone) != 10:
            messagebox.showwarning(
                "Validation Error",
                "Phone number must contain exactly 10 digits."
            )
            return False

        # Email
        if not email:
            messagebox.showwarning(
                "Validation Error",
                "Email is required."
            )
            return False

        if "@" not in email or "." not in email.split("@")[-1]:
            messagebox.showwarning(
                "Validation Error",
                "Please enter a valid email address."
            )
            return False

        # Address
        if not address:
            messagebox.showwarning(
                "Validation Error",
                "Address is required."
            )
            return False
        
        if not any(char.isalpha() for char in address):
            messagebox.showwarning(
                "Validation Error",
                 "Address must contain valid text."
            )
            return False

        # City
        if not city:
            messagebox.showwarning(
                "Validation Error",
                "City is required."
            )
            return False
        
        if not all(char.isalpha() or char.isspace() for char in city):
            messagebox.showwarning(
                "Validation Error",
                "City should contain only letters."
            )
            return False

        # State
        if not state:
            messagebox.showwarning(
                "Validation Error",
                "State is required."
            )
            return False
        
        if not all(char.isalpha() or char.isspace() for char in state):
            messagebox.showwarning(
                "Validation Error",
                "State should contain only letters."
            )
            return False

        # Pincode
        if not pincode:
            messagebox.showwarning(
                "Validation Error",
                "Pincode is required."
            )
            return False

        if not pincode.isdigit() or len(pincode) != 6:
            messagebox.showwarning(
                "Validation Error",
                "Pincode must contain exactly 6 digits."
            )
            return False

        return True
    
    # ==========================================
    # ADD CUSTOMER
    # ==========================================

    def add_customer(self):
        
        if not self.validate_customer():
            return

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
            
            self.load_customers()

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
            

    # ==========================================
    # LOAD CUSTOMERS
    # ==========================================

    def load_customers(self):

        # Clear search field
        self.search_entry.delete(0, "end")

        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch customers
        customers = self.customer_db.get_all_customers()

        # Insert customers
        for customer in customers:

            self.tree.insert(
               "",
               "end",
               values=customer
            )
            
    # ==========================================
    # SEARCH CUSTOMERS
    # ==========================================

    def search_customers(self):

        keyword = self.search_entry.get().strip()

        if not keyword:
            self.load_customers()
            return

        customers = self.customer_db.search_customers(
            keyword
        )

        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Display search results
        for customer in customers:

            self.tree.insert(
                "",
                "end",
                values=customer
            )
            
    # ==========================================
    # SELECT CUSTOMER
    # ==========================================

    def select_customer(self, event):

       selected = self.tree.focus()

       if not selected:
         return

       values = self.tree.item(selected, "values")

       self.selected_customer_id = values[0]

       self.name.delete(0, "end")
       self.name.insert(0, values[1])

       self.phone.delete(0, "end")
       self.phone.insert(0, values[2])

       self.email.delete(0, "end")
       self.email.insert(0, values[3])

       self.gst.delete(0, "end")
       self.gst.insert(0, values[4])

       self.address.delete(0, "end")
       self.address.insert(0, values[5])

       self.city.delete(0, "end")
       self.city.insert(0, values[6])

       self.state.delete(0, "end")
       self.state.insert(0, values[7])

       self.pincode.delete(0, "end")
       self.pincode.insert(0, values[8])
       
    # ==========================================
    # UPDATE CUSTOMER
    # ==========================================

    def update_customer(self):

        try:

            if not self.selected_customer_id:

                messagebox.showwarning(
                "Warning",
                "Please select a customer first."
                )
                return
            
            if not self.validate_customer():
                return
            
            self.customer_db.update_customer(
                customer_id=self.selected_customer_id,
                customer_name=self.name.get(),
                phone=self.phone.get(),
                email=self.email.get(),
                gst_number=self.gst.get(),
                address=self.address.get(),
                city=self.city.get(),
                state=self.state.get(),
                pincode=self.pincode.get()
            )

            messagebox.showinfo(
            "Success",
            "Customer updated successfully!"
            )

            self.load_customers()

        except Exception as e:

            messagebox.showerror(
            "Error",
            str(e)
            )
            
    # ==========================================
    # DELETE CUSTOMER
    # ==========================================

    def delete_customer(self):

        try:

            if not self.selected_customer_id:

                messagebox.showwarning(
                   "Warning",
                   "Please select a customer first."
                )
                return

            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this customer?"
            )

            if not confirm:
               return

            self.customer_db.delete_customer(
               self.selected_customer_id
            )

            messagebox.showinfo(
               "Success",
               "Customer deleted successfully!"
            )

            self.load_customers()
            self.selected_customer_id = None

        except Exception as e:

            messagebox.showerror(
               "Error",
               str(e)
            )
            
    # ==========================================
    # CLEAR FIELDS
    # ==========================================

    def clear_fields(self):

        self.name.delete(0, "end")
        self.phone.delete(0, "end")
        self.email.delete(0, "end")
        self.gst.delete(0, "end")
        self.address.delete(0, "end")
        self.city.delete(0, "end")
        self.state.delete(0, "end")
        self.pincode.delete(0, "end")

        self.selected_customer_id = None