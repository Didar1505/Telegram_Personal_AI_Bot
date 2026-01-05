from openai import OpenAI

class OpenRouterChatbot:
    def __init__(self, api_key:str, model_name: str = "@preset/personal"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = model_name

    def generate_response(self, message: str, chat_history: list = None):
        """Sends a message to OpenRouter and returns the text content."""
        if chat_history is None:
            chat_history = []

        messages = chat_history + [
            {
                "role": "user",
                "content": message
            }
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                extra_body={"reasoning": {"enabled": False}}
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"