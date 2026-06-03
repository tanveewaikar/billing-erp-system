import customtkinter as ctk
from login import LoginPage

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1400x850")
app.title("Billing & Invoice System")

LoginPage(app)

app.mainloop()