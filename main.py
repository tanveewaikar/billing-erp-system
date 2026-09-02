import os
import sys
import customtkinter as ctk

from login import LoginPage


def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

icon_path = resource_path(
    os.path.join("assets", "BillingInvoiceSystem.ico")
)

app.iconbitmap(icon_path)

app.geometry("1400x850")
app.title("Billing & Invoice System")

LoginPage(app)

app.mainloop()