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
            
            # Get current stock before update
            cursor.execute(
                """
                SELECT stock_quantity
                FROM products
                WHERE product_id = %s
                """,
                (product_id,)
            )

            previous_stock = cursor.fetchone()[0]

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

            # Calculate new stock
            new_stock = previous_stock + quantity

            # Save stock movement
            cursor.execute(
                """
                INSERT INTO stock_logs
                (
                    product_id,
                    change_type,
                    quantity_changed,
                    previous_stock,
                    new_stock,
                    reference_type,
                    reference_id
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    product_id,
                    "IN",
                    quantity,
                    previous_stock,
                    new_stock,
                    "Purchase",
                    purchase_id
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
    
    @staticmethod
    def update_purchase(
        purchase_id,
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
            
            cursor.execute(
                """
                SELECT
                    product_id,
                    quantity
                FROM purchase_items
                WHERE purchase_id=%s
                """,
                (purchase_id,)
            )

            old_product_id, old_quantity = cursor.fetchone()
            
            # Restore old stock
            cursor.execute(
                """
                UPDATE products
                SET stock_quantity = stock_quantity - %s
                WHERE product_id = %s
                """,
                (
                   old_quantity,
                   old_product_id
                )
            )
            # Update purchases table
            cursor.execute(
                """
                UPDATE purchases
                SET supplier_id=%s,
                    total_amount=%s,
                    payment_status=%s
                WHERE purchase_id=%s
                """,
                (
                   supplier_id,
                   total_amount,
                   payment_status,
                   purchase_id
                )
            )

            # Update purchase_items table
            cursor.execute(
                """
                UPDATE purchase_items
                SET product_id=%s,
                    quantity=%s,
                    purchase_price=%s,
                    total_price=%s
                WHERE purchase_id=%s
                """,
                (
                   product_id,
                   quantity,
                   purchase_price,
                   total_amount,
                   purchase_id
                )
            )
            # Apply new stock
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

        except Exception:
           conn.rollback()
           raise

        finally:
           cursor.close()
           conn.close()
           
    @staticmethod
    def delete_purchase(purchase_id):

        conn = get_connection()
        cursor = conn.cursor()

        try:

            # Get product and quantity
            cursor.execute(
                """
                SELECT product_id, quantity
                FROM purchase_items
                WHERE purchase_id=%s
                """,
                (purchase_id,)
            )

            product_id, quantity = cursor.fetchone()

            # Restore stock
            cursor.execute(
                """
                UPDATE products
                SET stock_quantity = stock_quantity - %s
                WHERE product_id=%s
                """,
                (
                    quantity,
                    product_id
                )
            )

            # Delete purchase items
            cursor.execute(
                """
                DELETE FROM purchase_items
                WHERE purchase_id=%s
                """,
                (purchase_id,)
            )

            # Delete purchase
            cursor.execute(
                """
                DELETE FROM purchases
                WHERE purchase_id=%s
                """,
                (purchase_id,)
            )

            conn.commit()

        except Exception:
           conn.rollback()
           raise

        finally:
           cursor.close()
           conn.close()
           
    @staticmethod
    def search_purchase(keyword):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
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
            WHERE
               s.supplier_name LIKE %s
               OR pr.product_name LIKE %s
            ORDER BY p.purchase_date DESC
            """,
            (
              f"%{keyword}%",
              f"%{keyword}%"
            )
        )

        purchases = cursor.fetchall()

        cursor.close()
        conn.close()

        return purchases
    
    