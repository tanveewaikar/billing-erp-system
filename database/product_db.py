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
        
        print(
            f"BEFORE UPDATE -> Product ID={product_id}, Qty={quantity}"
        )
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE products
            SET stock_quantity = stock_quantity - %s
            WHERE product_id = %s
            AND stock_quantity >= %s
            """,
            (
                quantity,
                product_id,
                quantity
            )
        )
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
        
    def get_all_stock(self):
        query = """
            SELECT
                product_id,
                product_name,
                category,
                stock_quantity,
                selling_price
            FROM products
            ORDER BY product_name
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()


    def get_low_stock_products(self):
        query = """
            SELECT
                product_id,
                product_name,
                stock_quantity
            FROM low_stock_products
            ORDER BY stock_quantity
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def search_stock(self, keyword):
        query = """
            SELECT
                product_id,
                product_name,
                category,
                stock_quantity,
                selling_price
            FROM products
            WHERE product_name LIKE %s
            ORDER BY product_name
        """

        self.cursor.execute(query, (f"%{keyword}%",))
        return self.cursor.fetchall()
    
    def get_stock_history(self, product_id):
        query = """
            SELECT
               change_type,
               quantity_changed,
               previous_stock,
               new_stock,
               reference_type,
               reference_id,
               created_at
            FROM stock_logs
            WHERE product_id = %s
            ORDER BY created_at DESC
        """

        self.cursor.execute(query, (product_id,))
        return self.cursor.fetchall()


    def get_product_name(self, product_id):
        query = """
           SELECT product_name
           FROM products
           WHERE product_id = %s
        """

        self.cursor.execute(query, (product_id,))
        return self.cursor.fetchone()
    
    