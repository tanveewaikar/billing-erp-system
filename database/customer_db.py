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

        try:

            # Check whether customer has invoice history
            self.cursor.execute(
                """
                SELECT COUNT(*)
                FROM invoices
                WHERE customer_id = %s
                """,
                (customer_id,)
            )

            invoice_count = self.cursor.fetchone()[0]

            if invoice_count > 0:

                raise ValueError(
                    "This customer cannot be deleted because "
                    "purchase history exists."
                )

            # Delete customer only if no invoices exist
            self.cursor.execute(
                """
                DELETE FROM customers
                WHERE customer_id = %s
                """,
                (customer_id,)
            )

            self.connection.commit()

        except Exception:
            self.connection.rollback()
            raise
        
        
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
    
    # ==========================================
    # SEARCH CUSTOMERS
    # ==========================================

    def search_customers(self, keyword):

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
        WHERE
            customer_name LIKE %s
            OR phone LIKE %s
            OR email LIKE %s
        ORDER BY customer_id DESC
        """

        search_value = f"%{keyword}%"

        self.cursor.execute(
            query,
            (
                search_value,
                search_value,
                search_value
            )
        )
        return self.cursor.fetchall()
    
    
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
    
    