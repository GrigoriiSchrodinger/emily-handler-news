from openai import OpenAI

from src.logger import logger


class GptAPI:
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = None
        self.api_key = api_key
        self.model = model
        self.initialize_client()

    def initialize_client(self):
        try:
            self.client = OpenAI(api_key=self.api_key)
        except Exception as error:
            logger.error(error)

    def create(self, prompt: str, user_message: str) -> str:
        try:
            logger.debug(f"Запрос GPT - model = {self.model} | prompt = {prompt} | user_message = {user_message}")
            completion = self.client.chat.completions.create(
                model=self.model,
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
            logger.info(f"Ответ GPT - {completion}")
            return completion.choices[0].message.content
        except Exception as error:
            logger.error(error)