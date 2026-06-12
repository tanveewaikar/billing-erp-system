from database.db_connection import get_connection

class InvoiceDB:
    pass

    @staticmethod
    def create_invoice(
        invoice_number,
        customer_id,
        subtotal,
        grand_total
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO invoices
            (
                invoice_number,
                customer_id,
                subtotal,
                grand_total
            )
            VALUES (%s,%s,%s,%s)
            """,
            (
                invoice_number,
                customer_id,
                subtotal,
                grand_total
            )
        )

        conn.commit()

        invoice_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return invoice_id
    
    @staticmethod
    def add_invoice_item(
        invoice_id,
        product_id,
        quantity,
        price,
        gst_percent,
        total_price
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
           """
           INSERT INTO invoice_items
           (
               invoice_id,
               product_id,
               quantity,
               price,
               gst_percent,
               total_price
           )
           VALUES (%s,%s,%s,%s,%s,%s)
           """,
           ( 
              invoice_id,
              product_id,
              quantity,
              price,
              gst_percent,
              total_price
            )
        )

        conn.commit()

        cursor.close()
        conn.close()