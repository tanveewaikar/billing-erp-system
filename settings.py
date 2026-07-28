import customtkinter as ctk
from database.settings_db import SettingsDB
from tkinter import messagebox

class SettingsPage:

    def __init__(self, parent):

        title = ctk.CTkLabel(
            parent,
            text="Settings",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)

        self.form = ctk.CTkFrame(parent)
        self.form.pack(fill="x", padx=20, pady=20)

        self.company_entry = ctk.CTkEntry(
           self.form,
           placeholder_text="Company Name",
           width=450
        )
        self.company_entry.pack(pady=8)

        self.owner_entry = ctk.CTkEntry(
            self.form,
            placeholder_text="Owner Name",
            width=450
        )
        self.owner_entry.pack(pady=8)

        self.phone_entry = ctk.CTkEntry(
            self.form,
            placeholder_text="Phone Number",
            width=450
        )
        self.phone_entry.pack(pady=8)

        self.email_entry = ctk.CTkEntry(
            self.form,
            placeholder_text="Business Email",
            width=450
        )
        self.email_entry.pack(pady=8)

        self.address_entry = ctk.CTkTextbox(
            self.form,
            width=450,
            height=80
        )
        self.address_entry.pack(pady=8)

        self.gst_entry = ctk.CTkEntry(
            self.form,
            placeholder_text="GST Number",
            width=450
        )
        self.gst_entry.pack(pady=8)

        self.prefix_entry = ctk.CTkEntry(
            self.form,
            placeholder_text="Invoice Prefix (Example: INV)",
            width=450
        )
        self.prefix_entry.pack(pady=8)

        self.footer_entry = ctk.CTkTextbox(
            self.form,
            width=450,
            height=60
        )
        self.footer_entry.pack(pady=8)
        
        self.save_btn = ctk.CTkButton(
            self.form,
            text="Save Settings",
            width=200,
            command=self.save_settings
        )
        self.save_btn.pack(pady=20)
        self.load_settings()
        
    def load_settings(self):

        settings = SettingsDB.get_settings()

        if not settings:
           return

        self.company_entry.insert(0, settings["company_name"])
        self.owner_entry.insert(0, settings["owner_name"])
        self.phone_entry.insert(0, settings["phone"])
        self.email_entry.insert(0, settings["email"])

        self.address_entry.insert(
            "1.0",
            settings["address"]
        )

        self.gst_entry.insert(
            0,
            settings["gst_number"]
        )

        self.prefix_entry.insert(
            0,
            settings["invoice_prefix"]
        )

        self.footer_entry.insert(
            "1.0",
            settings["invoice_footer"] or ""
        )
        
    def save_settings(self):

        company_name = self.company_entry.get()
        owner_name = self.owner_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get("1.0", "end").strip()
        gst_number = self.gst_entry.get()
        invoice_prefix = self.prefix_entry.get()

        SettingsDB.update_settings(
            company_name,
            owner_name,
            phone,
            email,
            address,
            gst_number,
            invoice_prefix
        )

        messagebox.showinfo(
            "Success",
            "Settings updated successfully."
        )
        