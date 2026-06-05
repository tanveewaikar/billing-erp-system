from database.customer_db import CustomerDB

customer_db = CustomerDB()

customer_db.add_customer(
    customer_name="Rahul Sharma",
    phone="9876543210",
    email="rahul@gmail.com",
    address="Mumbai",
    city="Mumbai",
    state="Maharashtra",
    pincode="400001",
    gst_number="27ABCDE1234F1Z5"
)

print("Customer Added Successfully")

customer_db.close_connection()