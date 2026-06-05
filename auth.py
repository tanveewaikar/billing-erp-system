# auth.py

import mysql.connector
from database.db_connection import get_connection
from tkinter import messagebox


class AuthSystem:

    def __init__(self):

        self.connection = get_connection()

        self.cursor = self.connection.cursor()
        print("Connected to MySQL Successfully")

    # ==========================================
    # REGISTER USER
    # ==========================================

    def register_user(self, full_name, username, password, role="Admin"):

        try:

            query = """
            INSERT INTO users (
                full_name,
                username,
                password,
                role
            )
            VALUES (%s, %s, %s, %s)
            """

            values = (
                full_name,
                username,
                password,
                role
            )

            self.cursor.execute(query, values)
            self.connection.commit()

            messagebox.showinfo(
                "Success",
                "User registered successfully!"
            )

        except mysql.connector.Error as err:

            messagebox.showerror(
                "Database Error",
                str(err)
            )

    # ==========================================
    # LOGIN USER
    # ==========================================

    def login_user(self, username, password):

        try:

            query = """
            SELECT user_id, full_name, username, password, role
            FROM users
            WHERE username = %s
            """

            self.cursor.execute(query, (username,))
            user = self.cursor.fetchone()

            if user:

                stored_password = user[3]

                # Plain text password comparison
                if password == stored_password:

                    return {
                        "status": True,
                        "user_id": user[0],
                        "full_name": user[1],
                        "username": user[2],
                        "role": user[4]
                    }

                else:

                    return {
                        "status": False,
                        "message": "Incorrect password"
                    }

            else:

                return {
                    "status": False,
                    "message": "User not found"
                }

        except mysql.connector.Error as err:

            return {
                "status": False,
                "message": str(err)
            }

    # ==========================================
    # CLOSE CONNECTION
    # ==========================================

    def close_connection(self):

        self.cursor.close()
        self.connection.close()