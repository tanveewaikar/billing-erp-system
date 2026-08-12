import customtkinter as ctk
from tkinter import ttk
from database.payment_db import PaymentDB


class PaymentHistoryPage:

    def __init__(self, parent):
        
        table_frame = ctk.CTkFrame(parent)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
        
        search_frame = ctk.CTkFrame(parent)

        search_frame.pack(
            fill="x",
            padx=20,
            pady=(20, 0)
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Search Invoice / Method / Transaction ID"
        )

        self.search_entry.pack(
            side="left",
            padx=10,
            pady=10
        )


        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_payments
        )

        search_btn.pack(
            side="left",
            padx=10,
            pady=10
        )

        show_all_btn = ctk.CTkButton(
            search_frame,
            text="Show All",
            command=self.load_payments
        )

        show_all_btn.pack(
            side="left",
            padx=10,
            pady=10
        )

        columns = (
            "Payment ID",
            "Invoice No",
            "Date",
            "Amount",
            "Method",
            "Transaction ID"
        )


        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )


        for col in columns:

            self.tree.heading(
                col,
                text=col
            )

            self.tree.column(
                col,
                width=160
            )


        self.tree.pack(
            fill="both",
            expand=True
        )


        self.load_payments()


    def load_payments(self):

        for item in self.tree.get_children():

            self.tree.delete(item)


        payments = PaymentDB.get_all_payments()


        for payment in payments:

            self.tree.insert(
                "",
                "end",
                values=(
                    payment["payment_id"],
                    payment["invoice_number"],
                    payment["payment_date"],
                    f"₹{payment['amount_paid']:.2f}",
                    payment["payment_method"],
                    payment["transaction_id"] or "-"
                )
            )
            
    def search_payments(self):

        search_text = self.search_entry.get().strip()

        if not search_text:
            self.load_payments()
            return

        payments = PaymentDB.search_payments(search_text)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for payment in payments:

            self.tree.insert(
                "",
                "end",
                values=(
                    payment["payment_id"],
                    payment["invoice_number"],
                    payment["payment_date"],
                    f"₹{payment['amount_paid']:.2f}",
                    payment["payment_method"],
                    payment["transaction_id"] or "-"
                )
            )