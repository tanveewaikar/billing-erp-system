# dashboard.py

import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
from customers import CustomersPage
from products import ProductsPage
from billing import BillingPage
from reports import ReportsPage
from suppliers import SuppliersPage
from purchases import PurchasesPage
from dashboard_page import DashboardPage
from settings import SettingsPage
from payment_history import PaymentHistoryPage
from stock import StockPage
from ai_assistant import AIAssistantPage

class Dashboard:

    def __init__(self, root):

        self.root = root

        # ==============================
        # MAIN LAYOUT
        # ==============================

        self.sidebar = ctk.CTkScrollableFrame(
            root,
            width=250,
            fg_color="#0F172A",
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = ctk.CTkFrame(
            root,
            fg_color="#F4F6F9"
        )
        self.main_frame.pack(side="right", fill="both", expand=True)
        
        # ==============================
        # SIDEBAR
        # ==============================

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="Billing ERP",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        )
        self.logo.pack(pady=30)

        self.create_sidebar_button(
            "🏠 Dashboard",
            self.show_dashboard
        )

        self.create_sidebar_button(
            "👤 Customers",
            self.show_customers
        )

        self.create_sidebar_button(
            "📦 Products",
            self.show_products
        )
        
        self.create_sidebar_button(
            "🚚 Suppliers",
            self.show_suppliers
        )
        
        self.create_sidebar_button(
            "🛒 Purchases",
            self.show_purchases
        )
        
        self.create_sidebar_button(
            "📦 Stock Management",
            self.show_stock
        )
        
        self.create_sidebar_button(
            "🧾 Billing",
            self.show_billing
        )

        self.create_sidebar_button(
            "📊 Reports",
            self.show_reports
        )
        
        self.create_sidebar_button(
            "🤖 AI Assistant",
            self.show_ai_assistant
        )
        
        self.create_sidebar_button(
            "💰 Payment History",
            self.show_payment_history
        )
        
        self.create_sidebar_button(
            "⚙️ Settings",
            self.show_settings
        )
         
        # ==============================
        # HEADER
        # ==============================

        self.header = ctk.CTkFrame(
            self.main_frame,
            height=80,
            fg_color="white"
        )
        self.header.pack(fill="x", padx=20, pady=20)

        self.header.pack_propagate(False)

        self.title = ctk.CTkLabel(
            self.header,
            text="Dashboard",
            font=("Segoe UI", 28, "bold"),
            text_color="#111827"
        )
        self.title.pack(side="left", padx=20)

        self.clock = ctk.CTkLabel(
            self.header,
            text="",
            font=("Segoe UI", 16),
            text_color="#6B7280"
        )
        self.clock.pack(side="right", padx=20)

        self.update_clock()

        # ==============================
        # CONTENT FRAME
        # ==============================

        self.content_frame = ctk.CTkFrame(
        self.main_frame,
        fg_color="transparent"
        )

        self.content_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
        )
       
        self.show_dashboard()
        
    # ======================================
    # SIDEBAR BUTTON
    # ======================================

    def create_sidebar_button(self, text, command):

      btn = ctk.CTkButton(
        self.sidebar,
        text=text,
        command=command,
        width=220,
        height=45,
        fg_color="transparent",
        hover_color="#1E293B",
        anchor="w",
        font=("Segoe UI", 16)
      )

      btn.pack(pady=5)


    # ======================================
    # PAGE NAVIGATION
    # ======================================

    def clear_content(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def set_page_title(self, title):

        self.title.configure(text=title)
    
    def show_dashboard(self):

        self.clear_content()
        
        self.set_page_title("Dashboard")

        page = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
        )
        page.pack(fill="both", expand=True)

        DashboardPage(page)

    def show_customers(self):

        self.clear_content()
        
        self.set_page_title("Customers")

        page = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
        )
        page.pack(fill="both", expand=True)

        CustomersPage(page)

    def show_products(self):

        self.clear_content()
        
        self.set_page_title("Products")

        page = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
        )
        page.pack(fill="both", expand=True)

        ProductsPage(page)
        
    def show_suppliers(self):

        self.clear_content()
        
        self.set_page_title("Suppliers")
        
        page = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
        )
        page.pack(fill="both", expand=True)

        SuppliersPage(page)
    
    def show_purchases(self):

        self.clear_content()
        
        self.set_page_title("Purchases")

        page = ctk.CTkScrollableFrame(
           self.content_frame,
           fg_color="transparent"
        )
        page.pack(fill="both", expand=True)

        PurchasesPage(page)
        
    def show_stock(self):

        self.clear_content()

        self.set_page_title("Stock Management")

        page = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
        )

        page.pack(
            fill="both",
            expand=True
        )

        stock_page = StockPage(page)

        stock_page.pack(fill="both",expand=True)
    
    def show_billing(self):

        self.clear_content()
        
        self.set_page_title("Billing")

        page = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
        )
        page.pack(fill="both", expand=True)

        BillingPage(page)

    def show_reports(self):

        self.clear_content()
        
        self.set_page_title("Reports")

        page = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
        )
        page.pack(fill="both", expand=True)

        ReportsPage(page)
        
    def show_ai_assistant(self):

        self.clear_content()

        self.set_page_title("AI Business Assistant")

        page = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
        )

        page.pack(fill="both", expand=True )

        AIAssistantPage(page)
        
    def show_payment_history(self):

        self.clear_content()

        self.set_page_title("Payment History")

        page = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
        )

        page.pack(
           fill="both",
           expand=True
        )

        PaymentHistoryPage(page)
    
    def show_settings(self):

        self.clear_content()
        
        self.set_page_title("Settings")
        
        page = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
        )
        page.pack(fill="both", expand=True)

        SettingsPage(page)
        
    # ======================================
    # CARD CREATOR
    # ======================================

    def create_card(self, parent, title, value):

        card = ctk.CTkFrame(
            parent,
            width=250,
            height=140,
            fg_color="white",
            corner_radius=15
        )

        card.pack(side="left", padx=10, pady=10)
        card.pack_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 16),
            text_color="#6B7280"
        )

        title_label.pack(pady=(25, 10))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 28, "bold"),
            text_color="#111827"
        )

        value_label.pack()

    # ======================================
    # LIVE CLOCK
    # ======================================

    def update_clock(self):

        current_time = datetime.now().strftime(
            "%d-%m-%Y  %H:%M:%S"
        )

        self.clock.configure(text=current_time)

        self.root.after(1000, self.update_clock)