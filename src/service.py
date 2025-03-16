from src.feature.RedisManager import RedisQueue

redis = RedisQueue(queue_name="text_conversion", port=6379, db=0)
