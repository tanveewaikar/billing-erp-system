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
        
    @staticmethod
    def get_total_paid(invoice_id):

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT COALESCE(SUM(amount_paid), 0)
        FROM payments
        WHERE invoice_id = %s
        """

        cursor.execute(
           query,
           (invoice_id,)
        )

        total_paid = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return float(total_paid)
    
    @staticmethod
    def get_payment_status(invoice_id, invoice_total):

        total_paid = PaymentDB.get_total_paid(invoice_id)

        if total_paid <= 0:
           return "UNPAID"

        if total_paid >= float(invoice_total):
            return "PAID"

        return "PARTIALLY PAID"
    
    