from database.db_connection import get_connection


class StockLogDB:

    @staticmethod
    def add_stock_log(
        product_id,
        change_type,
        quantity_changed,
        previous_stock,
        new_stock,
        reference_type,
        reference_id
    ):

        conn = get_connection()
        cursor = conn.cursor()

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
            VALUES
            (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                product_id,
                change_type,
                quantity_changed,
                previous_stock,
                new_stock,
                reference_type,
                reference_id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()


    @staticmethod
    def get_stock_history(product_id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
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
            """,
            (product_id,)
        )

        history = cursor.fetchall()

        cursor.close()
        conn.close()

        return history