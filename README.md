# Billing & Invoice Management System

A desktop-based Billing & Invoice Management System built using Python, CustomTkinter, and MySQL.

The application helps businesses manage customers, products, suppliers, purchases, billing, invoices, payments, inventory, reports, and business insights from a single desktop application.

It also includes a real AI-powered Business Assistant using Google Gemini to analyze business data and answer natural-language questions.

---

## Features

### Authentication
- User login system
- Secure configuration using environment variables
- Protected access to the application

### Customer Management
- Add customers
- Update customer information
- Delete customers
- Search customers
- View customer records
- GST and contact information
- Complete customer address management

### Product Management
- Add products
- Update product information
- Delete products
- Search products
- Purchase price and selling price
- GST percentage
- Barcode and unit management
- Stock quantity tracking
- Stock validation
- Protection against deleting products with transaction history

### Supplier Management
- Add suppliers
- Update supplier information
- Delete suppliers
- Search suppliers
- Supplier contact information
- Supplier address management
- Protection against deleting suppliers with purchase history

### Purchase Management
- Record purchases from suppliers
- Add multiple products to purchases
- Automatically increase product stock
- Maintain purchase records
- Track stock movements

### Billing & Invoicing
- Create customer invoices
- Add multiple products to invoices
- Automatic subtotal calculation
- GST calculation
- Grand total calculation
- Stock availability validation
- Automatically reduce stock after billing
- Partial payment support
- Full payment support
- Automatic invoice number generation

### PDF Invoice Generation
- Generate professional PDF invoices
- Company logo support
- Customer information
- Product details
- GST calculation
- Payment status
- Total amount
- Pending balance
- Automatically open generated invoice

### Email Invoice
- Send invoices through email
- Gmail SMTP integration
- PDF invoice attachment
- Environment-variable based email configuration

### Inventory & Stock Management
- View current stock
- Track stock IN and OUT movements
- View stock history
- Low-stock monitoring
- Purchases automatically increase stock
- Billing automatically decreases stock
- Stock movement logging

### Reports
- View invoice history
- Search invoices
- Search by customer
- Filter invoices by date
- View invoice details
- View invoice items

### Dashboard
- Today's sales
- Customer count
- Product count
- Supplier count
- Low-stock products
- Monthly sales analytics
- Recent invoices

### Settings
- Company information
- Invoice prefix
- Company logo
- Invoice configuration

### AI Business Assistant

The application includes a real AI-powered Business Assistant using Google Gemini.

Users can ask natural-language questions about their business data, for example:

- What are my total sales?
- Which products have low stock?
- What is my pending payment?
- How many customers do I have?
- Who is my highest-spending customer?
- What is my best-selling product?
- What is my total profit?
- What were my monthly sales?
- Give me a business overview.
- Give me some business recommendations.

The AI assistant retrieves actual ERP data from the MySQL database instead of relying on hard-coded responses.

---

## Technologies Used

### Programming Language
- Python

### GUI
- CustomTkinter
- Tkinter
- Matplotlib

### Database
- MySQL
- MySQL Connector/Python

### AI
- Google Gemini API
- Google GenAI Python SDK

### PDF & Email
- ReportLab
- SMTP
- Gmail

### Development & Deployment
- Git
- GitHub
- PyInstaller
- python-dotenv

---

## Project Architecture

```text
Billing & Invoice Management System
│
├── assets/
│   └── BillingInvoiceSystem.ico
│
├── database/
│   ├── ai_db.py
│   ├── ai_service.py
│   ├── customer_db.py
│   ├── dashboard_db.py
│   ├── db_connection.py
│   ├── invoice_db.py
│   ├── payment_db.py
│   ├── product_db.py
│   ├── purchase_db.py
│   ├── settings_db.py
│   ├── stock_log_db.py
│   └── suppliers_db.py
│
├── utils/
│   ├── email_sender.py
│   └── pdf_generator.py
│
├── invoices/
│
├── ai_assistant.py
├── auth.py
├── billing.py
├── customers.py
├── dashboard_page.py
├── main.py
├── products.py
├── purchases.py
├── reports.py
├── settings.py
├── stock.py
├── suppliers.py
├── .env
├── .gitignore
└── requirements.txt

## Key Development Highlights

- Built a complete desktop ERP-style application using Python and CustomTkinter
- Integrated MySQL for persistent business data
- Designed separate database classes for different application modules
- Implemented CRUD operations for customers, products, and suppliers
- Developed purchase, billing, invoice, payment, and inventory workflows
- Implemented automatic stock updates and stock movement logging
- Added GST calculation and payment tracking
- Generated professional PDF invoices using ReportLab
- Integrated email invoice delivery using SMTP
- Integrated Google Gemini for AI-powered business analysis
- Implemented background threading for AI requests
- Added error handling and environment-based configuration
- Packaged the application as a Windows executable using PyInstaller
- Used Git and GitHub for version control

---

## Author

### Tanvee Waikar

BE Information Technology

GitHub:  
https://github.com/tanveewaikar

Portfolio:  
https://portfolio-gamma-beige-45.vercel.app/

---

## License

This project was developed for learning, portfolio, and demonstration purposes.