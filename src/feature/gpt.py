from openai import OpenAI

class GptAPI:
    def __init__(self, api_key: str):
        self.client = None
        self.api_key = api_key
        self.initialize_client()

    def initialize_client(self):
        self.client = OpenAI(api_key=self.api_key)

    def create(self, prompt: str, user_message: str, model: str = "gpt-4o") -> str:
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )
            return completion.choices[0].message.content
        except Exception as error:
            print(f"Ошибка при вызове API: {error}")
            return "Ошибка при получении ответа."