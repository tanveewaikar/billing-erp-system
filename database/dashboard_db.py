from database.db_connection import get_connection


class DashboardDB:

    @staticmethod
    def get_total_customers():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM customers"
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total

    @staticmethod
    def get_total_products():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM products"
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total
    
    
    @staticmethod
    def get_total_suppliers():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM suppliers"
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total
    
    @staticmethod
    def get_today_sales():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT IFNULL(SUM(grand_total), 0)
            FROM invoices
            WHERE DATE(invoice_date) = CURDATE()
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total
    
    @staticmethod
    def get_low_stock_count():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM products
            WHERE stock_quantity <= 10
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total
    
    @staticmethod
    def get_recent_invoices():

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                i.invoice_number,
                c.customer_name,
                i.grand_total,
                i.payment_status,
                i.invoice_date
            FROM invoices i
            LEFT JOIN customers c
                ON i.customer_id = c.customer_id
            ORDER BY i.invoice_date DESC
            LIMIT 5
        """

        cursor.execute(query)

        invoices = cursor.fetchall()

        conn.close()

        return invoices
    
    