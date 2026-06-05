from database.db_connection import get_connection


class CustomerDB:

    def __init__(self):

        self.connection = get_connection()
        self.cursor = self.connection.cursor()

    # ==========================================
    # ADD CUSTOMER
    # ==========================================

    def add_customer(
        self,
        customer_name,
        phone,
        email,
        address,
        city,
        state,
        pincode,
        gst_number
    ):

        query = """
        INSERT INTO customers (
            customer_name,
            phone,
            email,
            address,
            city,
            state,
            pincode,
            gst_number
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            customer_name,
            phone,
            email,
            address,
            city,
            state,
            pincode,
            gst_number
        )

        self.cursor.execute(query, values)
        self.connection.commit()

    def close_connection(self):

        self.cursor.close()
        self.connection.close()