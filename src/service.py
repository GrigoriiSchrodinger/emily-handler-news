from src.feature.RedisManager import RedisQueue
from src.feature.request.RequestHandler import RequestGptHandler

redis = RedisQueue(queue_name="text_conversion", port=6379, db=0)
gpt_handler = RequestGptHandler()