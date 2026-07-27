from database.db_connection import get_connection


class ProductDB:

    @staticmethod
    def add_product(
        product_name,
        barcode,
        purchase_price,
        selling_price,
        gst_percent,
        stock_quantity,
        unit
    ):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO products
        (
            product_name,
            barcode,
            purchase_price,
            selling_price,
            gst_percent,
            stock_quantity,
            unit
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            query,
            (
                product_name,
                barcode,
                purchase_price,
                selling_price,
                gst_percent,
                stock_quantity,
                unit
            )
        )

        conn.commit()

        cursor.close()
        conn.close()
        
    @staticmethod
    def get_all_products():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
               product_id,
               product_name,
               purchase_price,
               selling_price,
               stock_quantity,
               gst_percent,
               barcode,
               unit
            FROM products
        """)

        products = cursor.fetchall()

        cursor.close()
        conn.close()
        return products
    
    @staticmethod
    def get_product_by_name(product_name):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                product_id,
                product_name,
                selling_price,
                gst_percent,
                stock_quantity
            FROM products
            WHERE product_name=%s
            """,
            (product_name,)
        )

        product = cursor.fetchone()

        cursor.close()
        conn.close()

        return product
    
    @staticmethod
    def update_product(
        product_id,
        product_name,
        barcode,
        purchase_price,
        selling_price,
        gst_percent,
        stock_quantity,
        unit
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
           """
           UPDATE products
           SET product_name=%s,
              barcode=%s,
              purchase_price=%s,
              selling_price=%s,
              gst_percent=%s,
              stock_quantity=%s,
              unit=%s
            WHERE product_id=%s
            """,
            (
              product_name,
              barcode,
              purchase_price,
              selling_price,
              gst_percent,
              stock_quantity,
              unit,
              product_id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()
        
    @staticmethod
    def delete_product(product_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
           """
           DELETE FROM products
           WHERE product_id=%s
           """,
           (product_id,)
        )

        conn.commit()

        cursor.close()
        conn.close()
        
    @staticmethod
    def get_product_names():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
           SELECT product_name
           FROM products
           ORDER BY product_name
        """)

        products = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return products
    
    @staticmethod
    def get_product_id_by_name(product_name):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT product_id
            FROM products
            WHERE product_name=%s
            """,
            (product_name,)
        )

        product = cursor.fetchone()

        cursor.close()
        conn.close()

        return product[0] if product else None
    
    @staticmethod
    def reduce_stock(product_id, quantity):

        conn = get_connection()
        cursor = conn.cursor()

        # Current stock
        cursor.execute(
            """
            SELECT stock_quantity
            FROM products
            WHERE product_id = %s
            """,
           (product_id,)
        )

        before = cursor.fetchone()[0]
        print("Stock Before:", before)

        # Reduce stock
        cursor.execute(
           """
           UPDATE products
           SET stock_quantity = stock_quantity - %s
           WHERE product_id = %s
           """,
           (quantity, product_id)
        )

        print("Rows Updated:", cursor.rowcount)

        # Check stock again
        cursor.execute(
            """
            SELECT stock_quantity
            FROM products
            WHERE product_id = %s
            """,
            (product_id,)
        )

        after = cursor.fetchone()[0]
        print("Stock After:", after)

        conn.commit()

        cursor.close()
        conn.close()
        
    @staticmethod
    def increase_stock(product_id, quantity):

        conn = get_connection()
        cursor = conn.cursor()

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
        cursor.close()
        conn.close()
        
    @staticmethod
    def get_all_stock():

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
               p.product_id,
               p.product_name,
               c.category_name,
               p.stock_quantity,
               p.selling_price
            FROM products p
            JOIN categories c
               ON p.category_id = c.category_id
            ORDER BY p.product_name
        """)

        stock = cursor.fetchall()

        cursor.close()
        conn.close()

        return stock

    
    @staticmethod
    def get_low_stock_products():

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.product_id,
                p.product_name,
                c.category_name,
                p.stock_quantity,
                p.selling_price
            FROM products p
            JOIN categories c
                ON p.category_id = c.category_id
            WHERE p.stock_quantity <= 5
            ORDER BY p.stock_quantity
        """)

        products = cursor.fetchall()

        cursor.close()
        conn.close()

        return products
    
    @staticmethod
    def search_stock(keyword):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
                SELECT
                   p.product_id,
                   p.product_name,
                   c.category_name,
                   p.stock_quantity,
                   p.selling_price
                FROM products p
                JOIN categories c
                   ON p.category_id = c.category_id
                WHERE
                   p.product_name LIKE %s
                ORDER BY p.product_name
            """,
            (f"%{keyword}%",)
        )

        stock = cursor.fetchall()

        cursor.close()
        conn.close()

        return stock

    @staticmethod
    def get_product_name(product_id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT product_name
            FROM products
            WHERE product_id = %s
            """,
            (product_id,)
        )

        product = cursor.fetchone()

        cursor.close()
        conn.close()

        return product