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