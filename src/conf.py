import os
from src.feature.RedisManager import RedisQueue

redis = RedisQueue(queue_name="text_conversion", host="redis", port=6379, db=0)
API_KEY = os.getenv('API_KEY')
