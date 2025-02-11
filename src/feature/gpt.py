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
            logger.debug(
                f"Запрос GPT - model = {self.model} | prompt = {prompt[:50]}... | user_message = {user_message[:100]}...",
                extra={'tags': {'service': 'gpt', 'action': 'request'}}
            )
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
            
            logger.info(
                "Ответ GPT получен",
                extra={
                    'tags': {
                        'service': 'gpt',
                        'action': 'response',
                        'model': completion.model,
                        'completion_id': completion.id,
                        'token_usage': completion.usage.total_tokens
                    }
                }
            )
            return completion.choices[0].message.content
            
        except Exception as error:
            logger.exception(
                f"GPT API Error: {str(error)}",
                extra={'tags': {
                    'service': 'gpt',
                    'error_type': error.__class__.__name__,
                    'status_code': getattr(error, 'status_code', None)
                }}
            )
            raise