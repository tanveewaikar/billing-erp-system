import os

from dotenv import load_dotenv
from google import genai

from database.ai_db import AIDB


load_dotenv()


class AIService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env"
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.chat = self.client.chats.create(
            model="gemini-3.5-flash-lite",
            config={
                "system_instruction": """
You are the AI Business Assistant for a Billing ERP system.

Important rules:

1. All monetary values from this ERP are in Indian Rupees (INR).
2. Always display monetary amounts using the ₹ symbol.
3. Never use $, USD, €, or any other currency symbol.
4. Answer questions using the available ERP tools whenever business data is required.
5. Do not invent business data.
6. Give clear, concise and useful business insights.
7. If the user asks a question unrelated to the ERP/business,
   politely explain that you are designed to help with this Billing ERP.
""",
                "tools": [
                    AIDB.get_total_sales,
                    AIDB.get_low_stock_products,
                    AIDB.get_pending_payment,
                    AIDB.get_customer_count,
                    AIDB.get_product_count,
                    AIDB.get_supplier_count,
                    AIDB.get_highest_spending_customer
                ]
            }
        )

    def ask(self, question):

        response = self.chat.send_message(
            question
        )

        return response.text