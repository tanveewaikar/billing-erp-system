from database.db_connection import get_connection


class SettingsDB:

    @staticmethod
    def get_settings():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM company_settings LIMIT 1"
        cursor.execute(query)

        settings = cursor.fetchone()

        cursor.close()
        conn.close()

        return settings


    @staticmethod
    def update_settings(
        company_name,
        owner_name,
        phone,
        email,
        address,
        gst_number,
        invoice_prefix
    ):

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE company_settings
        SET
            company_name=%s,
            owner_name=%s,
            phone=%s,
            email=%s,
            address=%s,
            gst_number=%s,
            invoice_prefix=%s
        WHERE company_id=1
        """

        cursor.execute(
            query,
            (
                company_name,
                owner_name,
                phone,
                email,
                address,
                gst_number,
                invoice_prefix
            )
        )

        conn.commit()

        cursor.close()
        conn.close()