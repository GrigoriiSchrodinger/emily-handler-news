import json
import redis

class RedisQueue:
    def __init__(self, queue_name, host='localhost', port=6379, db=0):
        """
        Инициализирует подключение к Redis и имя очереди.
        """
        self.queue_name = queue_name
        self.redis_conn = redis.Redis(host=host, port=port, db=db)

    def send_to_queue(self, queue_name, data):
        """
        Отправляет данные в очередь
        """
        self.redis_conn.rpush(queue_name, data)

    def receive_from_queue(self, queue_name, block=True, timeout=None):
        """
        Получает данные из очереди
        Если блокировка включена, будет ждать до появления данных.
        """
        if block:
            item = self.redis_conn.blpop(queue_name, timeout=timeout)
        else:
            item = self.redis_conn.lpop(queue_name)

        if item:
            return json.loads(item[1].decode('utf-8'))
        return None