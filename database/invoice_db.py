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
        
    @staticmethod
    def get_all_invoices():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                i.invoice_id,
                i.invoice_number,
                c.customer_name,
                i.invoice_date,
                i.grand_total
            FROM invoices i
            LEFT JOIN customers c
                ON i.customer_id = c.customer_id
            ORDER BY i.invoice_id DESC
        """)

        invoices = cursor.fetchall()
        cursor.close()
        conn.close()

        return invoices
    
    @staticmethod
    def search_invoices(keyword):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                i.invoice_id,
                i.invoice_number,
                c.customer_name,
                i.invoice_date,
                i.grand_total
            FROM invoices i
            LEFT JOIN customers c
                ON i.customer_id = c.customer_id
            WHERE
                i.invoice_number LIKE %s
                OR c.customer_name LIKE %s
            ORDER BY i.invoice_id DESC
            """, (f"%{keyword}%", f"%{keyword}%"))

        invoices = cursor.fetchall()

        cursor.close()
        conn.close()

        return invoices

    @staticmethod
    def get_invoices_by_date(from_date, to_date):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
          SELECT
            i.invoice_id,
            i.invoice_number,
            c.customer_name,
            i.invoice_date,
            i.grand_total
          FROM invoices i
          LEFT JOIN customers c
            ON i.customer_id = c.customer_id
          WHERE DATE(i.invoice_date)
          BETWEEN %s AND %s
          ORDER BY i.invoice_id DESC
        """, (from_date, to_date))
        invoices = cursor.fetchall()

        cursor.close()
        conn.close()

        return invoices
    
    @staticmethod
    def get_invoice_items(invoice_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
               p.product_name,
               ii.quantity,
               ii.price,
               ii.gst_percent,
               ii.total_price
            FROM invoice_items ii
            JOIN products p
               ON ii.product_id = p.product_id
            WHERE ii.invoice_id = %s
        """, (invoice_id,))

        items = cursor.fetchall()

        cursor.close()
        conn.close()
        
    