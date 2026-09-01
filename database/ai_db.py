from database.db_connection import get_connection


class AIDB:

    @staticmethod
    def get_total_sales():
        """Returns the total sales amount from all invoices."""

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
        """Returns products whose stock quantity is 10 or less."""

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

        return [
            {
                "product": product[0],
                "stock": product[1]
            }
            for product in products
        ]


    @staticmethod
    def get_pending_payment():
        """Returns the total amount still pending from customers."""

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(grand_total), 0)
            FROM invoices
        """)

        total_invoice_amount = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(amount_paid), 0)
            FROM payments
        """)

        total_paid = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return float(total_invoice_amount) - float(total_paid)


    @staticmethod
    def get_customer_count():
        """Returns the total number of customers."""

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM customers
        """)

        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count


    @staticmethod
    def get_product_count():
        """Returns the total number of products."""

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM products
        """)

        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count


    @staticmethod
    def get_supplier_count():
        """Returns the total number of suppliers."""

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM suppliers
        """)

        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count
    
    @staticmethod
    def get_highest_spending_customer():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.customer_name,
                COALESCE(SUM(i.grand_total), 0) AS total_spending
            FROM customers c
            JOIN invoices i
                ON c.customer_id = i.customer_id
            GROUP BY
                c.customer_id,
                c.customer_name
            ORDER BY total_spending DESC
            LIMIT 1
        """)

        customer = cursor.fetchone()

        cursor.close()
        conn.close()

        if customer:
            return (
                customer[0],
                float(customer[1])
            )

        return None
    
    @staticmethod
    def get_best_selling_product():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.product_name,
                SUM(ii.quantity) AS total_quantity
            FROM invoice_items ii
            JOIN products p
                ON ii.product_id = p.product_id
            GROUP BY
                p.product_id,
                p.product_name
            ORDER BY total_quantity DESC
            LIMIT 1
        """)

        product = cursor.fetchone()

        cursor.close()
        conn.close()

        if product:
            return {
                "product": product[0],
                "quantity_sold": int(product[1])
            }

        return None
    
    @staticmethod
    def get_total_profit():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COALESCE(
                    SUM(
                        (ii.price - p.purchase_price) * ii.quantity
                    ),
                    0
                )
                FROM invoice_items ii
                JOIN products p
                    ON ii.product_id = p.product_id
            """)

        total_profit = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return float(total_profit)
    
    @staticmethod
    def get_monthly_sales():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                DATE_FORMAT(invoice_date, '%Y-%m') AS month,
                COALESCE(SUM(grand_total), 0) AS total_sales
            FROM invoices
            GROUP BY DATE_FORMAT(invoice_date, '%Y-%m')
            ORDER BY month
        """)

        sales = cursor.fetchall()

        cursor.close()
        conn.close()

        return [
            {
                "month": row[0],
                "sales": float(row[1])
            }
            for row in sales
        ]
        