import customtkinter as ctk
from tkinter import messagebox, filedialog
import shutil
import os
from database.settings_db import SettingsDB


class SettingsPage:

    def __init__(self, parent):

        self.logo_label= ctk.CTkLabel(
            parent,
            text="No Logo Selected",
            width = 150,
            height = 150
        )
        self.logo_label.pack(pady=(0,20))

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
        
        self.logo_btn = ctk.CTkButton(
            self.form,
            text="Choose Company Logo",
            width=220,
            command=self.choose_logo
        )
        self.logo_btn.pack(pady=10)
        
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
        
        self.logo_path = settings["logo_path"]

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
        self.load_logo()
        
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
            self.logo_path,
            invoice_prefix
        )

        messagebox.showinfo(
            "Success",
            "Settings updated successfully."
        )
        
    def choose_logo(self):

        file_path = filedialog.askopenfilename(
            title="Select Company Logo",
            filetypes=[
                 ("Image Files", "*.png *.jpg *.jpeg")
            ]
        )

        if not file_path:
             return

        os.makedirs("assets/logos", exist_ok=True)

        filename = os.path.basename(file_path)

        destination = os.path.join(
            "assets",
            "logos",
            filename
        )

        shutil.copy(file_path, destination)

        self.logo_path = destination
    
        messagebox.showinfo(
            "Success",
            "Company logo selected successfully."
        ) 