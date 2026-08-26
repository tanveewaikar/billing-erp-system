from database.db_connection import get_connection


class InvoiceDB:
    pass

    @staticmethod
    def create_invoice(
        invoice_number,
        customer_id,
        subtotal,
        grand_total
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO invoices
            (
                invoice_number,
                customer_id,
                subtotal,
                grand_total
            )
            VALUES (%s,%s,%s,%s)
            """,
            (
                invoice_number,
                customer_id,
                subtotal,
                grand_total
            )
        )

        conn.commit()

        invoice_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return invoice_id
    
    @staticmethod
    def create_complete_invoice(
        invoice_number,
        customer_id,
        subtotal,
        grand_total,
        bill_items
    ):

        conn = get_connection()
        cursor = conn.cursor()

        try:

            # =====================================
            # CREATE INVOICE
            # =====================================

            cursor.execute(
                """
                INSERT INTO invoices
                (
                    invoice_number,
                    customer_id,
                    subtotal,
                    grand_total
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    invoice_number,
                    customer_id,
                    subtotal,
                    grand_total
                )
            )

            invoice_id = cursor.lastrowid


            # =====================================
            # PROCESS ALL BILL ITEMS
            # =====================================

            for product_name, data in bill_items.items():

                # Get product details
                cursor.execute(
                    """
                    SELECT
                        product_id,
                        stock_quantity
                    FROM products
                    WHERE product_name = %s
                    """,
                    (product_name,)
                )

                product = cursor.fetchone()

                if not product:
                    raise ValueError(
                        f"Product '{product_name}' not found."
                    )

                product_id, previous_stock = product

                quantity = data["qty"]
                price = data["price"]
                gst_percent = data["gst"]


                # =====================================
                # VALIDATE STOCK
                # =====================================

                if quantity > previous_stock:

                    raise ValueError(
                        f"Insufficient stock for '{product_name}'. "
                        f"Available: {previous_stock}"
                    )


                # =====================================
                # CALCULATE ITEM TOTAL
                # =====================================

                item_subtotal = price * quantity

                total_price = (
                    item_subtotal
                    + (item_subtotal * gst_percent / 100)
                )


                # =====================================
                # ADD INVOICE ITEM
                # =====================================

                cursor.execute(
                    """
                    INSERT INTO invoice_items
                    (
                        invoice_id,
                        product_id,
                        quantity,
                        price,
                        gst_percent,
                        total_price
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        invoice_id,
                        product_id,
                        quantity,
                        price,
                        gst_percent,
                        total_price
                    )
                )


                # =====================================
                # REDUCE STOCK
                # =====================================

                new_stock = previous_stock - quantity

                cursor.execute(
                    """
                    UPDATE products
                    SET stock_quantity = %s
                    WHERE product_id = %s
                    """,
                    (
                        new_stock,
                        product_id
                    )
                )


                # =====================================
                # ADD STOCK LOG
                # =====================================

                cursor.execute(
                    """
                    INSERT INTO stock_logs
                    (
                        product_id,
                        change_type,
                        quantity_changed,
                        previous_stock,
                        new_stock,
                        reference_type,
                        reference_id
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        product_id,
                        "OUT",
                        quantity,
                        previous_stock,
                        new_stock,
                        "Invoice",
                        invoice_id
                    )
                )


            # =====================================
            # COMMIT COMPLETE INVOICE
            # =====================================

            conn.commit()

            return invoice_id


        except Exception:

            conn.rollback()
            raise


        finally:

            cursor.close()
            conn.close()
    
    
    @staticmethod
    def add_invoice_item(
        invoice_id,
        product_id,
        quantity,
        price,
        gst_percent,
        total_price
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
           """
           INSERT INTO invoice_items
           (
               invoice_id,
               product_id,
               quantity,
               price,
               gst_percent,
               total_price
           )
           VALUES (%s,%s,%s,%s,%s,%s)
           """,
           ( 
              invoice_id,
              product_id,
              quantity,
              price,
              gst_percent,
              total_price
            )
        )

        conn.commit()

        cursor.close()
        conn.close()
        
    @staticmethod
    def get_all_invoices():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                i.invoice_id,
                i.invoice_number,
                c.customer_name,
                i.invoice_date,
                i.grand_total
            FROM invoices i
            LEFT JOIN customers c
                ON i.customer_id = c.customer_id
            ORDER BY i.invoice_id DESC
        """)

        invoices = cursor.fetchall()
        cursor.close()
        conn.close()

        return invoices
    
    @staticmethod
    def search_invoices(keyword):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                i.invoice_id,
                i.invoice_number,
                c.customer_name,
                i.invoice_date,
                i.grand_total
            FROM invoices i
            LEFT JOIN customers c
                ON i.customer_id = c.customer_id
            WHERE
                i.invoice_number LIKE %s
                OR c.customer_name LIKE %s
            ORDER BY i.invoice_id DESC
            """, (f"%{keyword}%", f"%{keyword}%"))

        invoices = cursor.fetchall()

        cursor.close()
        conn.close()

        return invoices

    @staticmethod
    def get_invoices_by_date(from_date, to_date):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
          SELECT
            i.invoice_id,
            i.invoice_number,
            c.customer_name,
            i.invoice_date,
            i.grand_total
          FROM invoices i
          LEFT JOIN customers c
            ON i.customer_id = c.customer_id
          WHERE DATE(i.invoice_date)
          BETWEEN %s AND %s
          ORDER BY i.invoice_id DESC
        """, (from_date, to_date))
        invoices = cursor.fetchall()

        cursor.close()
        conn.close()

        return invoices
    
    @staticmethod
    def get_invoice_items(invoice_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
               p.product_name,
               ii.quantity,
               ii.price,
               ii.gst_percent,
               ii.total_price
            FROM invoice_items ii
            JOIN products p
               ON ii.product_id = p.product_id
            WHERE ii.invoice_id = %s
        """, (invoice_id,))

        items = cursor.fetchall()

        cursor.close()
        conn.close()
        return items
    