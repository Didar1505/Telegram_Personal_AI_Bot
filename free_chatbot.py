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
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                stream_options={"include_usage": True}
            )
            
            response_content = ""
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    response_content += chunk.choices[0].delta.content
            
            return response_content
        except Exception as e:
            return f"Error: {str(e)}"