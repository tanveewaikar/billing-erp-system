from database.customer_db import CustomerDB

customer_db = CustomerDB()

print("CustomerDB Connected Successfully")

customer_db.close_connection()