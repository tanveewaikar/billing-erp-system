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
    
    