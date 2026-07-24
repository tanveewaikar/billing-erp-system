from database.db_connection import get_connection


class SupplierDB:

    @staticmethod
    def add_supplier(
        supplier_name,
        contact_person,
        phone,
        email,
        address
    ):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO suppliers
        (
            supplier_name,
            contact_person,
            phone,
            email,
            address
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                supplier_name,
                contact_person,
                phone,
                email,
                address
            )
        )

        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get_all_suppliers():

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM suppliers
            ORDER BY supplier_id DESC
            """
        )

        suppliers = cursor.fetchall()

        cursor.close()
        connection.close()

        return suppliers
    
    
    @staticmethod
    def update_supplier(
       supplier_id,
       supplier_name,
       contact_person,
       phone,
       email,
       address
    ):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        UPDATE suppliers
        SET
           supplier_name = %s,
           contact_person = %s,
           phone = %s,
           email = %s,
           address = %s
        WHERE supplier_id = %s
        """

        cursor.execute(
           query,
            (
              supplier_name,
              contact_person,
              phone,
              email,
              address,
              supplier_id
            )
        )

        connection.commit()

        cursor.close()
        connection.close()
        
    @staticmethod
    def delete_supplier(supplier_id):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        DELETE FROM suppliers
        WHERE supplier_id = %s
        """

        cursor.execute(query, (supplier_id,))

        connection.commit()

        cursor.close()
        connection.close()
        
    