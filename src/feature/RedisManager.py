import json

import redis

from src.logger import logger


class RedisQueue:
    def __init__(self, queue_name, host='redis', port=6379, db=0):
        """
        Инициализирует подключение к Redis и имя очереди.
        """
        self.queue_name = queue_name
        self.redis_conn = redis.Redis(host=host, port=port, db=db)

    def send_to_queue(self, queue_name, data):
        """
        Отправляет данные в очередь
        """
        try:
            logger.debug(
                f"Отправляем в очередь - {queue_name} | {json.loads(data)}",
                extra={'tags': {
                    'service': 'redis',
                    'action': 'send',
                    'queue': queue_name,
                    'data_length': len(data)
                }}
            )
            self.redis_conn.rpush(queue_name, data)
        except Exception as error:
            logger.exception(
                "Ошибка отправки в очередь",
                extra={'tags': {
                    'service': 'redis',
                    'error_type': error.__class__.__name__,
                    'queue': queue_name
                }}
            )

    def receive_from_queue(self, queue_name, block=True, timeout=None):
        """
        Получает данные из очереди
        Если блокировка включена, будет ждать до появления данных.
        """
        try:
            if block:
                logger.debug(
                    f"Ждем ответа очереди - {queue_name}",
                    extra={'tags': {
                        'service': 'redis',
                        'action': 'receive_blocking',
                        'queue': queue_name,
                        'timeout': timeout
                    }}
                )
                item = self.redis_conn.blpop(queue_name, timeout=timeout)
            else:
                logger.debug(
                    f"Неблокирующее чтение очереди - {queue_name}",
                    extra={'tags': {
                        'service': 'redis',
                        'action': 'receive_non_blocking',
                        'queue': queue_name
                    }}
                )
                item = self.redis_conn.lpop(queue_name)

            if item:
                decoded_data = item[1].decode('utf-8')
                logger.info(
                    "Успешно получены данные из очереди",
                    extra={'tags': {
                        'service': 'redis',
                        'action': 'received',
                        'queue': queue_name,
                        'data_length': len(decoded_data)
                    }}
                )
                return json.loads(decoded_data)
            return None
        except Exception as error:
            logger.exception(
                "Ошибка получения из очереди",
                extra={'tags': {
                    'service': 'redis',
                    'error_type': error.__class__.__name__,
                    'queue': queue_name
                }}
            )

    def clear_queue(self, queue_name):
        """
        Очищает очередь, удаляя все элементы.
        """
        try:
            deleted_count = self.redis_conn.delete(queue_name)
            logger.warning(
                "Очередь очищена",
                extra={'tags': {
                    'service': 'redis',
                    'action': 'clear',
                    'queue': queue_name,
                    'deleted_items': deleted_count
                }}
            )
        except Exception as error:
            logger.exception(
                "Ошибка очистки очереди",
                extra={'tags': {
                    'service': 'redis',
                    'error_type': error.__class__.__name__,
                    'queue': queue_name
                }}
            )

