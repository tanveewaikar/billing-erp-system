import customtkinter as ctk


class StockPage:

    def __init__(self, parent):

        title = ctk.CTkLabel(
            parent,
            text="Stock Management",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)