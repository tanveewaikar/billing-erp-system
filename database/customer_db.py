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
        
    # ==========================================
    # GET ALL CUSTOMERS
    # ==========================================

    def get_all_customers(self):

        query = """
        SELECT
            customer_id,
            customer_name,
            phone,
            email,
            gst_number,
            address,
            city,
            state,
            pincode
        FROM customers
        ORDER BY customer_id DESC
        """

        self.cursor.execute(query)

        return self.cursor.fetchall()

    def close_connection(self):

        self.cursor.close()
        self.connection.close()