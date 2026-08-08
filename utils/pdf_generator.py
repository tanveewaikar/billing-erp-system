from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from database.settings_db import SettingsDB
import os


def generate_pdf(
    invoice_number,
    customer_name,
    bill_items,
    subtotal,
    gst,
    grand_total
):

    # Project root folder
    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    # invoices folder
    invoices_folder = os.path.join(
        project_root,
        "invoices"
    )

    # Create invoices folder if it doesn't exist
    os.makedirs(invoices_folder, exist_ok=True)

    # Full PDF path
    pdf_path = os.path.join(
        invoices_folder,
        f"{invoice_number}.pdf"
    )

    print("PDF Path:", pdf_path)

    c = canvas.Canvas(pdf_path, pagesize=letter)

    width, height = letter
    
    settings = SettingsDB.get_settings()

    y = height - 50

   # Company Name
    c.setFont("Helvetica-Bold", 20)
    c.drawString(
      50,
      y,
      settings["company_name"]
    )

    # Invoice Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(
       430,
       y,
       "INVOICE"
    )

    y -= 30

    c.setFont("Helvetica", 11)

    c.drawString(
       50,
       y,
       f"Owner : {settings['owner_name']}"
    )

    y -= 18

    c.drawString(
       50,
       y,
       f"Phone : {settings['phone']}" 
    )

    y -= 18

    c.drawString(
       50,
       y,
       f"Email : {settings['email']}"
    )

    y -= 18

    c.drawString(
       50,
       y,
       f"GST : {settings['gst_number']}"
    )

    y -= 18

    address_lines = settings["address"].splitlines()
    for line in address_lines:

        c.drawString(
           50,
           y,
           line
        )

        y -= 15
    y -= 10
    
    c.setFont("Helvetica", 12)

    c.drawString(
        50,
        y,
        f"Invoice No : {invoice_number}"
    )

    y -= 20

    c.drawString(
        50,
        y,
        f"Customer : {customer_name}"
    )

    y -= 30

    c.line(50, y, 550, y)

    y -= 25

    # Table Header
    c.drawString(50, y, "Product")
    c.drawString(250, y, "Qty")
    c.drawString(320, y, "Price")
    c.drawString(420, y, "Total")

    y -= 15

    c.line(50, y, 550, y)

    y -= 25

    # Products
    for product_name, data in bill_items.items():

        qty = data["qty"]
        price = data["price"]
        gst_percent = data["gst"]

        item_subtotal = qty * price

        item_total = item_subtotal + (
            item_subtotal * gst_percent / 100
        )

        c.drawString(
            50,
            y,
            product_name
        )

        c.drawString(
            250,
            y,
            str(qty)
        )

        c.drawString(
            320,
            y,
            f"Rs.{price:.2f}"
        )

        c.drawString(
            420,
            y,
            f"Rs.{item_total:.2f}"
        )

        y -= 25

    y -= 20

    c.line(50, y, 550, y)

    y -= 30

    # Totals
    c.drawString(
        350,
        y,
        f"Subtotal : Rs.{subtotal:.2f}"
    )

    y -= 20

    c.drawString(
        350,
        y,
        f"GST : Rs.{gst:.2f}"
    )

    y -= 20

    c.drawString(
        350,
        y,
        f"Grand Total : Rs.{grand_total:.2f}"
    )

    y -= 40

    c.drawString(
        50,
        y,
        "Thank You For Your Purchase!"
    )

    # Save PDF
    c.save()

    print("Exists:", os.path.exists(pdf_path))

    # Auto-open PDF
    if os.path.exists(pdf_path):
        os.startfile(pdf_path)

    return pdf_path