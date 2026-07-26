from database.db_connection import get_connection


class PurchaseDB:

    @staticmethod
    def get_all_suppliers():

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT supplier_id, supplier_name
        FROM suppliers
        ORDER BY supplier_name
        """

        cursor.execute(query)

        suppliers = cursor.fetchall()

        cursor.close()
        connection.close()

        return suppliers


    @staticmethod
    def get_all_products():

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT product_id, product_name
        FROM products
        ORDER BY product_name
        """

        cursor.execute(query)

        products = cursor.fetchall()

        cursor.close()
        connection.close()

        return products