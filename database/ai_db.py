from database.db_connection import get_connection


class AIDB:

    @staticmethod
    def get_total_sales():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(grand_total), 0)
            FROM invoices
        """)

        total_sales = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return float(total_sales)


    @staticmethod
    def get_low_stock_products():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                product_name,
                stock_quantity
            FROM products
            WHERE stock_quantity <= 10
            ORDER BY stock_quantity ASC
        """)

        products = cursor.fetchall()

        cursor.close()
        conn.close()

        return products


    @staticmethod
    def get_pending_payment():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COALESCE(SUM(i.grand_total), 0)
            FROM invoices i
        """)

        total_invoice_amount = cursor.fetchone()[0]

        cursor.execute("""
            SELECT
                COALESCE(SUM(amount_paid), 0)
            FROM payments
        """)

        total_paid = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        pending_amount = (
            float(total_invoice_amount)
            - float(total_paid)
        )

        return pending_amount
    
    