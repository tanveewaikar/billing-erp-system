import customtkinter as ctk
from tkinter import ttk, messagebox
from database.payment_db import PaymentDB


class PaymentHistoryPage:

    def __init__(self, parent):

        # ==============================
        # SEARCH SECTION
        # ==============================

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

        clear_btn = ctk.CTkButton(
            search_frame,
            text="Clear",
            command=self.clear_search
        )

        clear_btn.pack(
            side="left",
            padx=10,
            pady=10
        )


        # ==============================
        # DATE FILTER
        # ==============================

        date_frame = ctk.CTkFrame(parent)

        date_frame.pack(
            fill="x",
            padx=20,
            pady=(10, 0)
        )

        self.from_date_entry = ctk.CTkEntry(
            date_frame,
            width=150,
            placeholder_text="From Date"
        )

        self.from_date_entry.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.to_date_entry = ctk.CTkEntry(
            date_frame,
            width=150,
            placeholder_text="To Date"
        )

        self.to_date_entry.pack(
            side="left",
            padx=10,
            pady=10
        )

        filter_btn = ctk.CTkButton(
            date_frame,
            text="Filter",
            command=self.filter_by_date
        )

        filter_btn.pack(
            side="left",
            padx=10,
            pady=10
        )


        # ==============================
        # PAYMENT SUMMARY
        # ==============================

        summary_frame = ctk.CTkFrame(parent)

        summary_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.total_payment_label = ctk.CTkLabel(
            summary_frame,
            text="Total Payments : ₹0.00",
            font=("Segoe UI", 16, "bold")
        )

        self.total_payment_label.pack(
            side="left",
            padx=20,
            pady=10
        )

        self.cash_label = ctk.CTkLabel(
            summary_frame,
            text="Cash : ₹0.00"
        )

        self.cash_label.pack(
            side="left",
            padx=20,
            pady=10
        )

        self.upi_label = ctk.CTkLabel(
            summary_frame,
            text="UPI : ₹0.00"
        )

        self.upi_label.pack(
            side="left",
            padx=20,
            pady=10
        )

        self.card_label = ctk.CTkLabel(
            summary_frame,
            text="Card : ₹0.00"
        )

        self.card_label.pack(
            side="left",
            padx=20,
            pady=10
        )


        self.bank_transfer_label = ctk.CTkLabel(
            summary_frame,
            text="Bank Transfer : ₹0.00"
        )

        self.bank_transfer_label.pack(
            side="left",
            padx=20,
            pady=10
        )
        
        # ==============================
        # PAYMENT TABLE
        # ==============================

        table_frame = ctk.CTkFrame(parent)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
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


        # ==============================
        # LOAD DATA
        # ==============================

        self.load_payments()


    # ==========================================
    # LOAD ALL PAYMENTS
    # ==========================================

    def load_payments(self):

        for item in self.tree.get_children():

            self.tree.delete(item)


        payments = PaymentDB.get_all_payments()


        self.update_payment_summary(
            payments
        )


        for payment in payments:

            self.tree.insert(
                "",
                "end",
                values=(
                    payment["payment_id"],
                    payment["invoice_number"],
                    self.format_payment_date(
                        payment["payment_date"]
                    ),
                    f"₹{payment['amount_paid']:.2f}",
                    payment["payment_method"],
                    payment["transaction_id"] or "-"
                )
            )


    # ==========================================
    # SEARCH PAYMENTS
    # ==========================================

    def search_payments(self):

        search_text = self.search_entry.get().strip()

        if not search_text:

            self.load_payments()

            return


        payments = PaymentDB.search_payments(
            search_text
        )


        self.update_payment_summary(
            payments
        )


        for item in self.tree.get_children():

            self.tree.delete(item)


        for payment in payments:

            self.tree.insert(
                "",
                "end",
                values=(
                    payment["payment_id"],
                    payment["invoice_number"],
                    self.format_payment_date(
                        payment["payment_date"]
                    ),
                    f"₹{payment['amount_paid']:.2f}",
                    payment["payment_method"],
                    payment["transaction_id"] or "-"
                )
            )


    # ==========================================
    # CLEAR SEARCH / FILTER
    # ==========================================

    def clear_search(self):

        self.search_entry.delete(
            0,
            "end"
        )

        self.from_date_entry.delete(
            0,
            "end"
        )

        self.to_date_entry.delete(
            0,
            "end"
        )

        self.load_payments()


    # ==========================================
    # FILTER PAYMENTS BY DATE
    # ==========================================

    def filter_by_date(self):

        from_date = self.from_date_entry.get().strip()

        to_date = self.to_date_entry.get().strip()


        if not from_date or not to_date:

            messagebox.showerror(
                "Date Filter",
                "Please enter both From Date and To Date."
            )

            return


        try:

            from datetime import datetime

            datetime.strptime(
                from_date,
                "%Y-%m-%d"
            )

            datetime.strptime(
                to_date,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showerror(
                "Date Filter",
                "Please use date format YYYY-MM-DD."
            )

            return


        if from_date > to_date:

            messagebox.showerror(
                "Date Filter",
                "From Date cannot be greater than To Date."
            )

            return


        payments = PaymentDB.filter_payments_by_date(
            from_date,
            to_date
        )


        self.update_payment_summary(
            payments
        )


        for item in self.tree.get_children():

            self.tree.delete(item)


        for payment in payments:

            self.tree.insert(
                "",
                "end",
                values=(
                    payment["payment_id"],
                    payment["invoice_number"],
                    self.format_payment_date(
                        payment["payment_date"]
                    ),
                    f"₹{payment['amount_paid']:.2f}",
                    payment["payment_method"],
                    payment["transaction_id"] or "-"
                )
            )


    # ==========================================
    # UPDATE PAYMENT SUMMARY
    # ==========================================

    def update_payment_summary(self, payments):

        total_amount = 0
        cash_amount = 0
        upi_amount = 0
        card_amount = 0
        bank_transfer_amount = 0

        for payment in payments:

            amount = float(
                payment["amount_paid"]
            )

            total_amount += amount


            if payment["payment_method"] == "Cash":

                cash_amount += amount


            elif payment["payment_method"] == "UPI":

                upi_amount += amount
                
            elif payment["payment_method"] == "Card":

                card_amount += amount


            elif payment["payment_method"] == "Bank Transfer":

                bank_transfer_amount += amount


        self.total_payment_label.configure(
            text=f"Total Payments : ₹{total_amount:.2f}"
        )

        self.cash_label.configure(
            text=f"Cash : ₹{cash_amount:.2f}"
        )

        self.upi_label.configure(
            text=f"UPI : ₹{upi_amount:.2f}"
        )
        
        self.card_label.configure(
            text=f"Card : ₹{card_amount:.2f}"
        )


        self.bank_transfer_label.configure(
            text=f"Bank Transfer : ₹{bank_transfer_amount:.2f}"
        )
        
    # ==========================================
    # FORMAT PAYMENT DATE
    # ==========================================

    def format_payment_date(self, payment_date):

        if not payment_date:
            return "-"

        return payment_date.strftime(
            "%d-%m-%Y %H:%M"
        )