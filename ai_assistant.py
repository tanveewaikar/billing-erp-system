import customtkinter as ctk


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
            text="Ask questions about your sales, stock, customers, purchases and payments.",
            font=("Segoe UI", 15)
        )
        description.pack(pady=(0, 20))

        # Chat display area
        self.chat_box = ctk.CTkTextbox(
            parent,
            height=400,
            font=("Segoe UI", 15),
            wrap="word"
        )
        self.chat_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.chat_box.insert(
            "end",
            "🤖 AI Assistant\n\n"
            "Hello! I can help you analyze your business data.\n\n"
            "Try asking:\n"
            "• What are my total sales?\n"
            "• Which products have low stock?\n"
            "• What is my pending payment amount?\n"
        )

        self.chat_box.configure(
            state="disabled"
        )

        # Input section
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

        ask_button = ctk.CTkButton(
            input_frame,
            text="Ask AI",
            width=120,
            height=45,
            command=self.ask_ai
        )
        ask_button.pack(
            side="right",
            padx=(5, 10),
            pady=10
        )

    def ask_ai(self):

        question = self.question_entry.get().strip()

        if not question:
            return

        self.chat_box.configure(
            state="normal"
        )

        self.chat_box.insert(
            "end",
            f"\n\nYou: {question}\n"
        )

        self.chat_box.insert(
            "end",
            "\nAI: AI integration will be added next."
        )

        self.chat_box.configure(
            state="disabled"
        )

        self.chat_box.see("end")

        self.question_entry.delete(0, "end")