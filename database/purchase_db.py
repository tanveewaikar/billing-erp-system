from database.db_connection import get_connection


class PurchaseDB:

    @staticmethod
    def get_all_suppliers():

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT supplier_id, supplier_name
        FROM suppliers
        ORDER BY supplier_name
        """

        cursor.execute(query)

        suppliers = cursor.fetchall()

        cursor.close()
        connection.close()

        return suppliers


    @staticmethod
    def get_all_products():

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT product_id, product_name
        FROM products
        ORDER BY product_name
        """

        cursor.execute(query)

        products = cursor.fetchall()

        cursor.close()
        connection.close()

        return products
    
    @staticmethod
    def add_purchase(
        supplier_id,
        product_id,
        quantity,
        purchase_price,
        total_amount,
        payment_status
    ):

        conn = get_connection()
        cursor = conn.cursor()

        try:

            # Insert into purchases table
            cursor.execute(
                """
                INSERT INTO purchases
                (
                    supplier_id,
                    total_amount,
                    payment_status
                )
                VALUES (%s, %s, %s)
                """,
                (
                    supplier_id,
                    total_amount,
                    payment_status
                )
            )

            purchase_id = cursor.lastrowid

            # Insert into purchase_items table
            cursor.execute(
                """
                INSERT INTO purchase_items
                (
                    purchase_id,
                    product_id,
                    quantity,
                    purchase_price,
                    total_price
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    purchase_id,
                    product_id,
                    quantity,
                    purchase_price,
                    total_amount
                )
            )
            
            # Increase Product Stock
            cursor.execute(
                """
                UPDATE products
                SET stock_quantity = stock_quantity + %s
                WHERE product_id = %s
                """,
                (
                    quantity,
                    product_id
                )
            )

            conn.commit()

            return purchase_id

        except Exception:
            conn.rollback()
            raise

        finally:
            cursor.close()
            conn.close()
            
    @staticmethod
    def get_all_purchases():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.purchase_id,
                s.supplier_name,
                pr.product_name,
                pi.quantity,
                pi.purchase_price,
                pi.total_price,
                p.payment_status,
                p.purchase_date
            FROM purchases p
            JOIN suppliers s
                ON p.supplier_id = s.supplier_id
            JOIN purchase_items pi
                ON p.purchase_id = pi.purchase_id
            JOIN products pr
                ON pi.product_id = pr.product_id
            ORDER BY p.purchase_date DESC
        """)

        purchases = cursor.fetchall()

        conn.close()
        return purchases
    
    