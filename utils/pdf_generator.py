from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
from database.settings_db import SettingsDB
from database.payment_db import PaymentDB
from textwrap import wrap
import os


def generate_pdf(
    invoice_number,
    customer_name,
    customer_details,
    bill_items,
    subtotal,
    gst,
    grand_total,
    invoice_id
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
    
    total_paid = PaymentDB.get_total_paid(
       invoice_id
    )

    balance = grand_total - total_paid

    payment_status = PaymentDB.get_payment_status(
        invoice_id,
        grand_total
    )

    y = height - 50

    # Company Logo
    logo_path = settings["logo_path"]

    if logo_path:

        project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        full_logo_path = os.path.join(
           project_root,
           logo_path
        )

        if os.path.exists(full_logo_path):

            logo = ImageReader(full_logo_path)

            c.drawImage(
               logo,
               50,
               y - 65,
               width=60,
               height=60,
               preserveAspectRatio=True,
               mask="auto"
            )


    # Company Name
    c.setFont("Helvetica-Bold", 20)

    c.drawString(
        130,
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


    # Company Details
    c.setFont("Helvetica", 11)

    c.drawString(
       130,
       y,
       f"Owner : {settings['owner_name']}"
    )

    y -= 18

    c.drawString(
       130,
       y,
       f"Phone : {settings['phone']}"
    )

    y -= 18

    c.drawString(
       130,
       y,
       f"Email : {settings['email']}"
    )

    y -= 18

    c.drawString(
       130,
       y,
       f"GST : {settings['gst_number']}"
    )

    y -= 18

    # Address
    address_lines = settings["address"].splitlines()

    for line in address_lines:

        c.drawString(
            130,
            y,
            line
        )

        y -= 15

    y -= 10
    
    # Invoice Details
    invoice_date = datetime.now().strftime("%d-%m-%Y")

    c.setFont("Helvetica", 11)

    c.drawString(
        350,
        y + 5,
        f"Invoice No : {invoice_number}"
    )

    c.drawString(
        350,
        y - 15,
        f"Invoice Date : {invoice_date}"
    )

    c.drawString(
       350,
       y - 35,
       f"Customer : {customer_details['name']}"
    )

    c.drawString(
       350,
       y - 55,
       f"Phone : {customer_details['phone']}"
    )

    c.drawString(
       350,
       y - 75,
       f"Email : {customer_details['email']}"
    )
    
    customer_address = ", ".join(
        filter(
            None,
            [
                customer_details["address"],
                customer_details["city"],
                customer_details["state"],
                customer_details["pincode"]
            ]
        )
    )

    # Customer Address
    address_text = f"Address : {customer_address}"

    address_lines = wrap(
        address_text,
        width=42
    )

    address_y = y - 95

    for line in address_lines:

        c.drawString(
            350,
            address_y,
            line
        )

        address_y -= 15


    # Customer GST
    c.drawString(
        350,
        address_y,
        f"GST : {customer_details['gst_number'] or 'N/A'}"
    )

    y -= 145

    # Table Header
    c.line(50, y, 550, y)

    y -= 25

    c.drawString(
       50,
       y,
       "Product"
    )

    c.drawString(
       280,
       y,
       "Qty"
    )

    c.drawString(
       340,
       y,
       "Price"
    )
    
    c.drawString(
       420,
       y,
       "GST"
    )
    
    c.drawString(
       485,
       y,
       "Total"
    )

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

        display_name = product_name

        if len(display_name) > 32:
           display_name = display_name[:29] + "..."

        c.drawString(
            50,
            y,
            display_name
        )
        
        c.drawString(
            280,
            y,
            str(qty)
        )

        c.drawString(
            340,
            y,
            f"Rs.{price:.2f}"
        )
        
        c.drawString(
            420,
            y,
            f"{gst_percent:.0f}%"
        )
        
        c.drawString(
            485,
            y,
            f"Rs.{item_total:.2f}"
        )

        y -= 25

    y -= 20

    c.line(50, y, 550, y)

    y -= 30

    # Totals

    c.setFont(
       "Helvetica",
       12
    )

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

    # Grand Total
    c.setFont(
        "Helvetica-Bold",
        14
    )

    c.drawString(
        350,
        y,
        f"Grand Total : Rs.{grand_total:.2f}"
    )

    y -= 25

    # Payment Details
    c.setFont(
       "Helvetica",
       11
    )

    c.drawString(
       350,
       y,
       f"Paid Amount : Rs.{total_paid:.2f}"
    )

    y -= 20

    c.drawString(
        350,
        y,
        f"Balance : Rs.{balance:.2f}"
    )

    y -= 20

    c.drawString(
        350,
        y,
        f"Status : {payment_status}"
    )

    y -= 40

    c.setFont(
        "Helvetica",
        12
    )
    
    # Invoice Footer

    c.line(
       50,
       y + 15,
       550,
       y + 15
    )

    c.setFont(
       "Helvetica-Bold",
       11
    )

    c.drawCentredString(
       width / 2,
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