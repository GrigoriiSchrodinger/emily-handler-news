import os

from src.feature.RedisManager import RedisQueue

redis = RedisQueue(queue_name="processing", host="localhost", port=6379, db=0)
API_KEY = os.getenv('API_KEY')