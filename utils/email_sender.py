import smtplib
import os

from email.message import EmailMessage


def send_invoice_email(
    sender_email,
    sender_password,
    customer_email,
    customer_name,
    invoice_number,
    pdf_path
):

    message = EmailMessage()

    message["Subject"] = f"Invoice {invoice_number}"
    message["From"] = sender_email
    message["To"] = customer_email

    message.set_content(
        f"""Dear {customer_name},

Please find attached your invoice {invoice_number}.

Thank you for your purchase.

Regards,
Billing ERP
"""
    )

    # Attach PDF
    with open(pdf_path, "rb") as file:

        pdf_data = file.read()

    message.add_attachment(
        pdf_data,
        maintype="application",
        subtype="pdf",
        filename=f"{invoice_number}.pdf"
    )

    # Gmail SMTP
    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            sender_email,
            sender_password
        )

        smtp.send_message(message)