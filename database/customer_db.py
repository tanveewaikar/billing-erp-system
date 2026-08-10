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
    
    # ==========================================
    # UPDATE CUSTOMER
    # ==========================================

    def update_customer(
        self,
        customer_id,
        customer_name,
        phone,
        email,
        gst_number,
        address,
        city,
        state,
        pincode
    ):

        query = """
        UPDATE customers
        SET
           customer_name=%s,
           phone=%s,
           email=%s,
           gst_number=%s,
           address=%s,
           city=%s,
           state=%s,
           pincode=%s
        WHERE customer_id=%s
        """

        values = (
           customer_name,
           phone,
           email,
           gst_number,
           address,
           city,
           state,
           pincode,
           customer_id
        )

        self.cursor.execute(query, values)
        self.connection.commit()
    
    # ==========================================
    # DELETE CUSTOMER
    # ==========================================

    def delete_customer(self, customer_id):

        query = """
        DELETE FROM customers
        WHERE customer_id = %s
        """

        self.cursor.execute(query, (customer_id,))
        self.connection.commit()
        
    @staticmethod
    def get_customer_names():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
           SELECT customer_name
           FROM customers
           ORDER BY customer_name
        """)

        customers = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return customers
    
    @staticmethod
    def get_customer_by_name(customer_name):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
               customer_id,
               customer_name,
               phone,
               email,
               address,
               city,
               state,
               pincode,
               gst_number
            FROM customers
            WHERE customer_name=%s
            """,
            (customer_name,)
        )

        customer = cursor.fetchone()

        cursor.close()
        conn.close()

        return customer
    
    