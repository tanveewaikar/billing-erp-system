import customtkinter as ctk
from tkinter import ttk
from database.customer_db import CustomerDB
from database.product_db import ProductDB
from tkinter import ttk, messagebox
from database.invoice_db import InvoiceDB
from utils.pdf_generator import generate_pdf
from database.settings_db import SettingsDB
from database.stock_log_db import StockLogDB
from database.payment_db import PaymentDB


class BillingPage:

    def __init__(self, parent):
        
        self.bill_items = {}
        
        self.subtotal_amount = 0
        self.gst_amount = 0
        self.grand_total = 0

        title = ctk.CTkLabel(
            parent,
            text="Create Invoice",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)

        top_frame = ctk.CTkFrame(parent)
        top_frame.pack(fill="x", padx=20)

        self.customer = ctk.CTkComboBox(
            top_frame,
            values=CustomerDB.get_customer_names()
        )
        self.customer.pack(side="left", padx=10, pady=10)
        
        self.product_combo = ctk.CTkComboBox(
        top_frame,
        values=ProductDB.get_product_names(),
        width=200
        )
        self.product_combo.pack( side="left",padx=10,pady=10)
        
        self.qty = ctk.CTkEntry(top_frame,width=80,placeholder_text="Qty")
        self.qty.pack(side="left",padx=10)
        
        add_btn = ctk.CTkButton(top_frame, text="Add Product",command=self.add_product_to_bill)
        add_btn.pack(side="left", padx=10)
        
        remove_btn = ctk.CTkButton(top_frame,text="Remove Product", command=self.remove_product)
        remove_btn.pack(side="left", padx=10)

        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        columns = (
            "Product",
            "Qty",
            "Price",
            "GST",
            "Total"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True)

        summary = ctk.CTkFrame(parent)
        summary.pack(fill="x", padx=20)

        self.subtotal_label = ctk.CTkLabel(summary,text="Subtotal : ₹0.00")
        self.subtotal_label.pack(anchor="e", padx=20, pady=5)

        self.gst_label = ctk.CTkLabel( summary,text="GST : ₹0.00")
        self.gst_label.pack(anchor="e", padx=20, pady=5)

        self.total_label = ctk.CTkLabel(summary,text="Grand Total : ₹0.00",font=("Segoe UI", 18, "bold"))
        self.total_label.pack(anchor="e", padx=20, pady=10)
        
        # ==============================
        # PAYMENT SECTION
        # ==============================

        payment_frame = ctk.CTkFrame(parent)
        payment_frame.pack(fill="x", padx=20, pady=10)

        payment_title = ctk.CTkLabel(
           payment_frame,
           text="Payment Details",
           font=("Segoe UI", 18, "bold")
        )
        payment_title.pack(anchor="w", padx=15, pady=(10, 5))


        self.payment_method = ctk.CTkComboBox(
            payment_frame,
            values=[
               "Cash",
               "Card",
               "UPI",
               "Bank Transfer"
            ],
            width=200
        )
        self.payment_method.set("Cash")
        self.payment_method.pack(
            side="left",
            padx=10,
            pady=10
        )


        self.amount_paid = ctk.CTkEntry(
            payment_frame,
            width=150,
            placeholder_text="Amount Paid"
        )
        self.amount_paid.pack(
            side="left",
            padx=10,
            pady=10
        )


        self.transaction_id = ctk.CTkEntry(
            payment_frame,
            width=200,
            placeholder_text="Transaction ID (Optional)"
        )
        self.transaction_id.pack(
           side="left",
           padx=10,
           pady=10
        )
        
        self.save_payment_btn = ctk.CTkButton(
            payment_frame,
            text="Save Payment",
            width=150,
            command=self.save_payment
        )

        self.save_payment_btn.pack(
            side="left",
            padx=10,
            pady=10
        )
        
        btn_frame = ctk.CTkFrame(parent)
        btn_frame.pack(fill="x", padx=20, pady=20)

        generate_btn = ctk.CTkButton(btn_frame, text="Generate Invoice", command=self.generate_invoice)
        generate_btn.pack(side="left", padx=10)

        print_btn = ctk.CTkButton(btn_frame, text="Print")
        print_btn.pack(side="left", padx=10)

        email_btn = ctk.CTkButton(btn_frame, text="Email Invoice")
        email_btn.pack(side="left", padx=10)
        
    def add_product_to_bill(self):

        print("Add Product Clicked")

        product_name = self.product_combo.get()
        print("Product:", product_name)

        try:
            qty = int(self.qty.get())
        except ValueError:
            print("Invalid quantity")
            return

        product = ProductDB.get_product_by_name(product_name)

        print("Product from DB:", product)

        if not product:
            print("No product found")
            return

        product_id, name, price, gst_percent, stock = product

        print("Before:", self.bill_items)

        if name in self.bill_items:

            print("Existing product")

            new_qty = self.bill_items[name]["qty"] + qty

            if new_qty > stock:
                print("Stock exceeded")
                return

            self.bill_items[name]["qty"] = new_qty

        else:
            if qty > stock:
                messagebox.showerror(
                    "Stock Error",
                    f"Only {stock} item(s) available in stock."
                )
                return
            
            print("New product")

            self.bill_items[name] = {
               "qty": qty,
               "price": float(price),
               "gst": float(gst_percent)
            }

        print("After:", self.bill_items)

        self.refresh_bill_table()

        self.qty.delete(0, "end")
        
                
    def refresh_bill_table(self):
        
        print("refresh_bill_table called")
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.subtotal_amount = 0
        self.gst_amount = 0
        self.grand_total = 0

        for name, data in self.bill_items.items():

            qty = data["qty"]
            price = data["price"]
            gst_percent = data["gst"]

            subtotal = price * qty
            gst_amount = subtotal * gst_percent / 100
            total = subtotal + gst_amount
    
            self.tree.insert(
               "",
               "end",
               values=(
                    name,
                    qty,
                    f"{price:.2f}",
                    f"{gst_amount:.2f}",
                    f"{total:.2f}"
                )
            )

            self.subtotal_amount += subtotal
            self.gst_amount += gst_amount
            self.grand_total += total

        self.subtotal_label.configure(
            text=f"Subtotal : ₹{self.subtotal_amount:.2f}"
        )

        self.gst_label.configure(
            text=f"GST : ₹{self.gst_amount:.2f}"
        )

        self.total_label.configure(
            text=f"Grand Total : ₹{self.grand_total:.2f}"
        )
        
    def generate_invoice(self):
        
        
        if not self.bill_items:
          messagebox.showerror(
            "Error",
            "Please add products to the invoice"
          )
          return

        from datetime import datetime

        settings = SettingsDB.get_settings()

        invoice_prefix = "INV"

        if settings and settings["invoice_prefix"]:
            invoice_prefix = settings["invoice_prefix"]

        invoice_number = (
            invoice_prefix +
            "-" +
            datetime.now().strftime("%Y%m%d%H%M%S")
        )

        print(invoice_number)

        customer_name = self.customer.get()
  
        customer = CustomerDB.get_customer_by_name(
        customer_name
        )

        print(customer)

        if not customer:
           print("Customer not found")
           return

        customer_id = customer[0]
        customer_details = {
            "name": customer[1],
            "phone": customer[2],
            "email": customer[3],
            "address": customer[4],
            "city": customer[5],
            "state": customer[6],
            "pincode": customer[7],
            "gst_number": customer[8]
        }

        invoice_id = InvoiceDB.create_invoice(
           invoice_number,
           customer_id,
           self.subtotal_amount,
           self.grand_total
       )
       
        for product_name, data in self.bill_items.items():

            product_id = ProductDB.get_product_id_by_name(
                product_name
            )

            qty = data["qty"]
            price = data["price"]
            gst_percent = data["gst"]

            subtotal = price * qty

            total_price = subtotal + (
                subtotal * gst_percent / 100
            )
 
            print(product_name)

            InvoiceDB.add_invoice_item(
                invoice_id,
                product_id,
                qty,
                price,
                gst_percent,
                total_price
            )
            
            previous_stock, new_stock = ProductDB.reduce_stock(
                product_id,
                qty
            )
            
            StockLogDB.add_stock_log(
                product_id=product_id,
                change_type="OUT",
                quantity_changed=qty,
                previous_stock=previous_stock,
                new_stock=new_stock,
                reference_type="Invoice",
                reference_id=invoice_id
            )
            
        print("Invoice ID:", invoice_id)  
        
        generate_pdf(
            invoice_number,
            customer_name,
            customer_details,
            self.bill_items,
            self.subtotal_amount,
            self.gst_amount,
            self.grand_total
        )
            
        self.bill_items.clear()

        self.refresh_bill_table()

        messagebox.showinfo(
            "Success",
            f"Invoice {invoice_number} generated successfully"
        )
    
    def save_payment(self):

        if not self.bill_items:
            messagebox.showerror(
                "Error",
                "Please generate an invoice first."
            )
            return

        print("Save Payment clicked")
    
    def remove_product(self):

        selected = self.tree.focus()

        if not selected:
            messagebox.showerror(
               "Error",
               "Please select a product"
            )
            return

        values = self.tree.item(selected, "values")

        product_name = values[0]

        if product_name in self.bill_items:
            del self.bill_items[product_name]
 
        self.refresh_bill_table()