from database.db_connection import get_connection


class PaymentDB:

    @staticmethod
    def add_payment(
        invoice_id,
        amount_paid,
        payment_method,
        transaction_id=None
    ):

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO payments
        (
            invoice_id,
            amount_paid,
            payment_method,
            transaction_id
        )
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                invoice_id,
                amount_paid,
                payment_method,
                transaction_id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()