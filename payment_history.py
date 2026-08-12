import customtkinter as ctk
from tkinter import ttk
from database.payment_db import PaymentDB


class PaymentHistoryPage:

    def __init__(self, parent):

        title = ctk.CTkLabel(
            parent,
            text="Payment History",
            font=("Segoe UI", 26, "bold")
        )

        title.pack(
            pady=20
        )


        table_frame = ctk.CTkFrame(parent)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
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