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