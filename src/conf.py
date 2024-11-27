import os
from dotenv import load_dotenv

from src.feature.RedisManager import RedisQueue

load_dotenv()
redis = RedisQueue(queue_name="processing", host="localhost", port=6379, db=0)
API_KEY = os.getenv('API_KEY')