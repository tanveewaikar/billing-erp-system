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
                "tools": [
                    AIDB.get_total_sales,
                    AIDB.get_low_stock_products,
                    AIDB.get_pending_payment,
                    AIDB.get_customer_count,
                    AIDB.get_product_count,
                    AIDB.get_supplier_count
                ]
            }
        )

    def ask(self, question):

        response = self.chat.send_message(
            question
        )

        return response.text