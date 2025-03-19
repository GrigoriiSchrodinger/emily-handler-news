import json

from src.feature.request.RequestHandler import RequestDataBase
from src.logger import logger
from src.service import redis, gpt_handler


def main():
    try:
        request_db = RequestDataBase()
        message = redis.receive_from_queue(queue_name="text_conversion")
        if message and "content" in message and isinstance(message["content"], str):
            new_post = gpt_handler.upgrade_news(text=message["content"], links=message["outlinks"])["text"]
            json_news = {
                "seed": message["seed"]
            }
            request_db.create_modified_news(channel=message["channel"], id_post=message["id_post"], text=new_post)
            redis.send_to_queue(queue_name="ForModer", data=json.dumps(json_news))
    except Exception as error:
        logger.error(error)

if __name__ == '__main__':
    logger.info("Start work")
    while True:
        main()