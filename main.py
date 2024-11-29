import json

from src.conf import API_KEY, redis
from src.feature.gpt import GptAPI
from src.logger import logger


def change_post(post: str):
    prompt = """
    Ты один из лучших новостных редакторов, твоя задача не меняя суть поста улучшить текст и сделать его красивым для привлечения людей к твоему телеграмм каналу.
    Сообщения не должна быть огромными твоя аудиотория это люди из россии им от 18 до 30 лет. Весь текст должен быть не больше 1024 символа. Старайся делать посты короткие, и выделять в них самое главное.  
    
    Помни что текст отправляется в телеграмм канал, поэтому обязательно соблюдай правила форматирования HTML: 
    """
    client = GptAPI(API_KEY)
    return client.create(prompt=prompt, user_message=post)

def main():
    try:
        message = redis.receive_from_queue(queue_name="processing")
        if message and "content" in message and isinstance(message["content"], str):
            new_post = change_post(message["content"])
            json_news = {
                "channel": message["channel"],
                "content": new_post,
                "id_post": message["id_post"]
            }
            redis.send_to_queue(queue_name="ReadyNews", data=json.dumps(json_news))
    except Exception as error:
        logger.error(error)

if __name__ == '__main__':
    logger.info("Start work")
    while True:
        main()