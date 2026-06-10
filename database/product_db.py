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