import customtkinter as ctk
from tkinter import messagebox
import threading

from database.ai_service import AIService


class AIAssistantPage:

    def __init__(self, parent):

        title = ctk.CTkLabel(
            parent,
            text="AI Business Assistant",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)

        description = ctk.CTkLabel(
            parent,
            text="Ask questions about your business data using AI.",
            font=("Segoe UI", 15)
        )
        description.pack(pady=(0, 20))

        # ==============================
        # CHAT DISPLAY
        # ==============================

        self.chat_box = ctk.CTkTextbox(
            parent,
            height=350,
            font=("Segoe UI", 15),
            wrap="word"
        )

        self.chat_box.pack(
            fill="both",
            padx=20,
            pady=10
        )

        self.chat_box.insert(
            "end",
            "🤖 AI Assistant\n\n"
            "Hello! I can analyze your business data.\n\n"
            "You can ask questions such as:\n"
            "• What are my total sales?\n"
            "• Which products have low stock?\n"
            "• What is my pending payment?\n"
            "• How many customers do I have?\n"
            "• Give me a business overview.\n"
        )

        self.chat_box.configure(
            state="disabled"
        )

        # ==============================
        # INPUT SECTION
        # ==============================

        input_frame = ctk.CTkFrame(parent)

        input_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.question_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ask a question about your business...",
            height=45,
            font=("Segoe UI", 15)
        )

        self.question_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(10, 5),
            pady=10
        )

        self.ask_button = ctk.CTkButton(
            input_frame,
            text="Ask AI",
            width=120,
            height=45,
            command=self.ask_ai
        )

        self.ask_button.pack(
            side="right",
            padx=(5, 10),
            pady=10
        )

        # Allow Enter key to ask
        self.question_entry.bind(
            "<Return>",
            lambda event: self.ask_ai()
        )

        # ==============================
        # GEMINI SERVICE
        # ==============================

        try:

            self.ai_service = AIService()

        except Exception as e:

            self.ai_service = None

            messagebox.showerror(
                "AI Setup Error",
                str(e)
            )

    # ==========================================
    # ASK AI
    # ==========================================

    def ask_ai(self):

        question = self.question_entry.get().strip()

        if not question:
            return

        # Display user question
        self.chat_box.configure(
            state="normal"
        )

        self.chat_box.insert(
            "end",
            f"\n\nYou: {question}\n"
        )

        self.chat_box.configure(
            state="disabled"
        )

        self.chat_box.see("end")

        # Check AI service
        if self.ai_service is None:

            self.show_ai_response(
                "AI service is not available."
            )

            return

        # Disable input while AI is working
        self.ask_button.configure(
            text="Thinking...",
            state="disabled"
        )

        self.question_entry.configure(
            state="disabled"
        )

        # Clear input
        self.question_entry.delete(
            0,
            "end"
        )

        # Start AI request in background
        thread = threading.Thread(
            target=self.get_ai_response,
            args=(question,),
            daemon=True
        )

        thread.start()

    # ==========================================
    # GET AI RESPONSE
    # ==========================================

    def get_ai_response(self, question):

        try:

            response = self.ai_service.ask(
                question
            )

        except Exception:

            response = (
                "Sorry, I could not process your request.\n"
                "The AI service is temporarily unavailable. "
                "Please check your internet connection and try again."
            )

        # Update UI safely through Tkinter main thread
        self.parent_after(
            response
        )

    # ==========================================
    # UPDATE UI
    # ==========================================

    def parent_after(self, response):

        # Schedule UI update on main thread
        self.chat_box.after(
            0,
            lambda: self.show_ai_response(response)
        )

    # ==========================================
    # SHOW AI RESPONSE
    # ==========================================

    def show_ai_response(self, response):

        self.chat_box.configure(
            state="normal"
        )

        self.chat_box.insert(
            "end",
            f"\nAI: {response}"
        )

        self.chat_box.configure(
            state="disabled"
        )

        self.chat_box.see("end")

        # Enable input again
        self.question_entry.configure(
            state="normal"
        )

        # Clear question field
        self.question_entry.delete(
            0,
            "end"
        )

        # Enable Ask AI button
        self.ask_button.configure(
            text="Ask AI",
            state="normal"
        )

        self.question_entry.focus()